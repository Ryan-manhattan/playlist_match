'use client';

import React, { useEffect, useState } from 'react';
import { getTopTracks } from '@/lib/spotify';

interface Track {
  id: string;
  name: string;
  artist: string;
  albumCover: string;
  previewUrl: string;
}

export default function ChartSection(): React.JSX.Element {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('ChartSection mounted - Fetching tracks...');
    
    const fetchTracks = async () => {
      try {
        setIsLoading(true);
        const spotifyTracks = await getTopTracks(50);
        console.log('Tracks fetched successfully:', spotifyTracks.length);
        setTracks(spotifyTracks);
      } catch (err) {
        console.error('Error fetching tracks:', err);
        setError('Failed to load tracks. Please try again later.');
      } finally {
        setIsLoading(false);
      }
    };

    fetchTracks();
  }, []);

  if (error) {
    console.log('Rendering error state');
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  if (isLoading) {
    console.log('Rendering loading state');
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  console.log('Rendering tracks:', tracks);
  return (
    <section className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8">Music Chart</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {tracks.map((track) => (
          <div
            key={track.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
          >
            <img
              src={track.albumCover}
              alt={`${track.name} album cover`}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h2 className="text-xl font-semibold mb-2">{track.name}</h2>
              <p className="text-gray-600">{track.artist}</p>
              {track.previewUrl && (
                <audio
                  controls
                  className="mt-4 w-full"
                  onPlay={() => console.log(`Playing track: ${track.name}`)}
                >
                  <source src={track.previewUrl} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              )}
            </div>
          </div>
        ))}
      </div>
    </section>
  );
} 