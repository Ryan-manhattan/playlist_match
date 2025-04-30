import { Playlist, Track, User } from '@prisma/client'

// thumbnail 필드를 명시적으로 포함한 타입
export type PlaylistWithThumbnail = Playlist & { thumbnail: string | null }

export interface PlaylistWithDetails extends Omit<Playlist, 'thumbnail'> {
  tracks: TrackWithDetails[]
  user: {
    name: string | null
    image: string | null
  }
  imageUrl: string | null // thumbnail 필드를 imageUrl로 매핑
}

export interface TrackWithDetails extends Track {
  title: string // name을 title로 매핑
  albumCover: string | null // imageUrl을 albumCover로 매핑
  duration: number // 추가 필드 (Spotify API에서 가져올 예정)
}

export function mapTrackToDetails(track: Track): TrackWithDetails {
  return {
    ...track,
    title: track.name,
    albumCover: track.imageUrl,
    duration: 0, // 기본값, Spotify API에서 가져올 예정
  }
}

export function mapPlaylistWithTracks(
  playlist: PlaylistWithThumbnail & {
    tracks: Track[]
    user: Pick<User, 'name' | 'image'>
  }
): PlaylistWithDetails {
  return {
    ...playlist,
    imageUrl: playlist.thumbnail,
    tracks: playlist.tracks.map(mapTrackToDetails),
  }
} 