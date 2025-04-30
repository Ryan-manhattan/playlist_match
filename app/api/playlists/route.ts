import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "../auth/[...nextauth]/route";
import { PrismaClient } from "@prisma/client";
import * as fs from "fs/promises";
import path from "path";

const prisma = new PrismaClient();
const UPLOAD_DIR = path.join(process.cwd(), "public", "uploads");

// GET: 내 플레이리스트 목록 조회
export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session || !session.user?.email) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const user = await prisma.user.findUnique({
    where: { email: session.user.email },
    select: { id: true },
  });
  if (!user) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }
  const playlists = await prisma.playlist.findMany({
    where: { userId: user.id },
    orderBy: { createdAt: "desc" },
    select: {
      id: true,
      name: true,
      description: true,
      thumbnail: true,
      createdAt: true,
      tracks: true,
    },
  });
  // 트랙 수 계산
  const result = playlists.map(pl => ({
    ...pl,
    trackCount: pl.tracks.length,
  }));
  return NextResponse.json(result);
}

// POST: 플레이리스트 생성
export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session || !session.user?.email) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  const user = await prisma.user.findUnique({
    where: { email: session.user.email },
    select: { id: true },
  });
  if (!user) {
    return NextResponse.json({ error: "User not found" }, { status: 404 });
  }

  const formData = await req.formData();
  const name = formData.get("name") as string;
  const description = formData.get("description") as string;
  const thumbFile = formData.get("thumbnail") as File | null;
  let thumbnailPath: string | undefined = undefined;

  if (thumbFile && thumbFile.size > 0) {
    const ext = thumbFile.name.split(".").pop();
    const fileName = `playlist-${Date.now()}.${ext}`;
    const filePath = path.join(UPLOAD_DIR, fileName);
    const arrayBuffer = await thumbFile.arrayBuffer();
    await fs.writeFile(filePath, Buffer.from(arrayBuffer));
    thumbnailPath = `/uploads/${fileName}`;
  }

  const playlist = await prisma.playlist.create({
    data: {
      name,
      description,
      userId: user.id,
      thumbnail: thumbnailPath,
    },
    select: {
      id: true,
      name: true,
      description: true,
      thumbnail: true,
      createdAt: true,
    },
  });

  return NextResponse.json(playlist);
}
