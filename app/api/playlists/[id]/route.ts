import { NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { prisma } from '../../../lib/prisma'
import authOptions from '../../../lib/authOptions'

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  try {
    console.log('GET /api/playlists/[id] - Fetching playlist:', params.id)
    
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      console.log('Unauthorized access attempt')
      return new NextResponse('Unauthorized', { status: 401 })
    }

    const playlist = await prisma.playlist.findUnique({
      where: {
        id: params.id,
      },
      include: {
        tracks: {
          orderBy: {
            order: 'asc',
          },
        },
        user: {
          select: {
            name: true,
            image: true,
          },
        },
      },
    })

    if (!playlist) {
      console.log('Playlist not found:', params.id)
      return new NextResponse('Not Found', { status: 404 })
    }

    // Check if the user has access to this playlist
    if (playlist.userId !== session.user.id) {
      console.log('Access denied to playlist:', params.id)
      return new NextResponse('Forbidden', { status: 403 })
    }

    console.log('Successfully fetched playlist:', playlist.title)
    return NextResponse.json(playlist)
  } catch (error) {
    console.error('Error fetching playlist:', error)
    return new NextResponse('Internal Server Error', { status: 500 })
  }
} 