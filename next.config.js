const path = require('path');

const nextConfig = {
  images: {
    domains: [
      'i.scdn.co', // Spotify 이미지 도메인 허용
      'lh3.googleusercontent.com', // Google 프로필 이미지 도메인 허용
    ],
  },
  env: {
    NEXT_PUBLIC_SPOTIFY_CLIENT_ID: process.env.NEXT_PUBLIC_SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET: process.env.SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REFRESH_TOKEN: process.env.SPOTIFY_REFRESH_TOKEN,
  },
  webpack: (config) => {
    // alias 제거: 상대경로만 허용
    return config;
  },
};

module.exports = nextConfig;
