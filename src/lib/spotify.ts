import SpotifyWebApi from 'spotify-web-api-node';

const CLIENT_ID = process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID;
const CLIENT_SECRET = process.env.SPOTIFY_CLIENT_SECRET;
const REFRESH_TOKEN = process.env.SPOTIFY_REFRESH_TOKEN;

interface SpotifyToken {
  access_token: string;
  token_type: string;
  expires_in: number;
}

interface SpotifyTrack {
  id: string;
  name: string;
  artist: string;
  albumCover: string;
  previewUrl: string | null;
}

interface SpotifyResponse {
  items: Array<{
    track: {
      id: string;
      name: string;
      artists: Array<{ name: string }>;
      album: {
        images: Array<{ url: string }>;
      };
      preview_url: string | null;
    };
  }>;
}

async function getAccessToken(): Promise<string> {
  console.log('Getting Spotify access token...');
  
  try {
    const basic = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64');
    const response = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        Authorization: `Basic ${basic}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: REFRESH_TOKEN!,
      }),
    });

    const data = await response.json() as SpotifyToken;
    console.log('Successfully obtained access token');
    return data.access_token;
  } catch (error) {
    console.error('Error getting access token:', error);
    throw new Error('Failed to get Spotify access token');
  }
}

export async function getTopTracks(limit: number = 50): Promise<SpotifyTrack[]> {
  console.log(`Fetching top ${limit} tracks from Spotify...`);
  
  try {
    const accessToken = await getAccessToken();
    const response = await fetch(
      `https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks?limit=${limit}`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json() as SpotifyResponse;
    console.log('Successfully fetched tracks from Spotify');
    
    return data.items.map((item) => ({
      id: item.track.id,
      name: item.track.name,
      artist: item.track.artists.map(artist => artist.name).join(', '),
      albumCover: item.track.album.images[0]?.url || '',
      previewUrl: item.track.preview_url,
    }));
  } catch (error) {
    console.error('Error fetching top tracks:', error);
    throw error;
  }
} 