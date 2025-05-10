import Image from 'next/image'
import { PlaylistWithDetails } from '../../../types/playlist'
import TrackList from './TrackList'

interface PlaylistDetailProps {
  playlist: PlaylistWithDetails
}

export default function PlaylistDetail({ playlist }: PlaylistDetailProps) {
  console.log('Rendering PlaylistDetail:', playlist.name)
  
  return (
    <div className="space-y-8">
      {/* 플레이리스트 헤더 */}
      <div className="flex items-start gap-6">
        <div className="relative w-48 h-48">
          <Image
            src={playlist.imageUrl || '/default-playlist.svg'}
            alt={playlist.name}
            fill
            className="object-cover rounded-lg"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        </div>
        <div className="flex-1">
          <h1 className="text-3xl font-bold mb-2">{playlist.name}</h1>
          {playlist.description && (
            <p className="text-gray-600 mb-4">{playlist.description}</p>
          )}
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <Image
              src={playlist.user.image || '/default-avatar.svg'}
              alt={playlist.user.name || 'User'}
              width={24}
              height={24}
              className="rounded-full"
            />
            <span>Created by {playlist.user.name || 'Anonymous'}</span>
          </div>
        </div>
      </div>

      {/* 트랙 목록 */}
      <TrackList tracks={playlist.tracks} />
    </div>
  )
} 