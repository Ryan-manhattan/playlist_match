import { withAuth } from "next-auth/middleware";
import { NextResponse } from "next/server";

export default withAuth(
  function middleware(req) {
    console.log("미들웨어 실행: ", req.nextUrl.pathname);
    return NextResponse.next();
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token,
    },
    pages: {
      signIn: "/login",
    },
  }
);

// 보호할 라우트 설정
export const config = {
  matcher: [
    "/profile",
    "/playlists/:path*",
    "/chart",
  ],
}; 