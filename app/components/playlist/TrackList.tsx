import Image from 'next/image'
import { TrackWithDetails } from '../../../types/playlist'

interface TrackListProps {
  tracks: TrackWithDetails[]
}

export default function TrackList({ tracks }: TrackListProps) {
  console.log('Rendering TrackList with', tracks.length, 'tracks')
  
  if (tracks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        No tracks in this playlist yet
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tracks.map((track, index) => (
        <div
          key={track.id}
          className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
        >
          <div className="relative w-12 h-12">
            <Image
              src={track.albumCover || '/default-album.svg'}
              alt={track.title}
              fill
              className="object-cover rounded"
            />
          </div>
          <div className="flex-1 min-w-0">
            <h3 className="font-medium truncate">{track.title}</h3>
            <p className="text-sm text-gray-500 truncate">
              {track.artist}
            </p>
          </div>
          <div className="text-sm text-gray-500">
            {formatDuration(track.duration)}
          </div>
        </div>
      ))}
    </div>
  )
}

function formatDuration(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
} 