import { Metadata } from 'next'
import { notFound } from 'next/navigation'
import PlaylistDetail from '@/app/components/playlist/PlaylistDetail'
import { getPlaylistById } from '@/app/actions/playlist'

interface PlaylistPageProps {
  params: {
    id: string
  }
}

export async function generateMetadata({ params }: PlaylistPageProps): Promise<Metadata> {
  const playlist = await getPlaylistById(params.id)
  
  if (!playlist) {
    return {
      title: 'Playlist Not Found',
    }
  }

  return {
    title: `${playlist.title} - Playlist Match`,
    description: playlist.description || 'A playlist on Playlist Match',
  }
}

export default async function PlaylistPage({ params }: PlaylistPageProps) {
  console.log('Rendering PlaylistPage for ID:', params.id)
  
  const playlist = await getPlaylistById(params.id)
  
  if (!playlist) {
    console.log('Playlist not found:', params.id)
    notFound()
  }

  return (
    <main className="container mx-auto px-4 py-8">
      <PlaylistDetail playlist={playlist} />
    </main>
  )
} 