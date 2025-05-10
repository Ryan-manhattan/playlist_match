import { prisma } from '../lib/prisma'
import { mapPlaylistWithTracks } from '../../types/playlist'
import { getServerSession } from 'next-auth'
import authOptions from '../lib/authOptions'

export async function getPlaylistById(id: string) {
  console.log('Fetching playlist by ID:', id)
  
  try {
    const session = await getServerSession(authOptions)
    if (!session?.user) {
      console.log('Unauthorized access attempt')
      return null
    }

    const playlist = await prisma.playlist.findUnique({
      where: {
        id,
      },
      include: {
        tracks: {
          orderBy: {
            createdAt: 'asc',
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
      console.log('Playlist not found:', id)
      return null
    }

    // Check if the user has access to this playlist
    if (playlist.userId !== session.user.id) {
      console.log(
        'Access denied to playlist:',
        id,
        'playlist.userId:',
        playlist.userId,
        'session.user.id:',
        session.user.id
      )
      return null
    }

    console.log('Successfully fetched playlist:', playlist.name)
    return mapPlaylistWithTracks(playlist)
  } catch (error) {
    console.error('Error fetching playlist:', error)
    return null
  }
} 