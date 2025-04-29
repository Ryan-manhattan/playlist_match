'use client';

import React from 'react';

const features = [
  {
    id: 'playlist-sync',
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
      />
    ),
    title: '플레이리스트 연동',
    description: 'Spotify, YouTube Music 등 즐겨 사용하는 서비스의 플레이리스트를 간편하게 연결하세요.',
  },
  {
    id: 'music-analysis',
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    ),
    title: "'음악 궁합' 분석",
    description: '좋아하는 장르, 아티스트, 곡 분위기를 분석하여 당신과 음악적 케미가 높은 상대를 찾아냅니다.',
  },
  {
    id: 'chat',
    icon: (
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z"
      />
    ),
    title: '의미있는 대화 시작',
    description: '음악이라는 공통 관심사로 자연스럽게 대화를 시작하고 서로를 알아가세요.',
  },
];

export default function FeaturesSection(): React.JSX.Element {
  console.log('Rendering FeaturesSection component');

  return (
    <section className="py-16 md:py-24 bg-white">
      <div className="container mx-auto px-6 text-center">
        <h2 className="text-3xl font-bold mb-4 text-gray-800">
          음악 취향, 어떻게 인연이 되나요?
        </h2>
        <p className="text-gray-600 mb-12 max-w-2xl mx-auto">
          Playlist Match는 당신의 음악 스트리밍 서비스 플레이리스트를 분석하여
          <br />
          가장 잘 맞는 음악적 감성의 상대를 찾아줍니다.
        </p>
        <div className="grid md:grid-cols-3 gap-8 text-left">
          {features.map((feature) => (
            <div
              key={feature.id}
              className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition duration-150 ease-in-out"
              onClick={() => console.log(`Clicked feature: ${feature.title}`)}
            >
              <div className="text-indigo-500 mb-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-10 w-10 inline-block"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  {feature.icon}
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600 text-sm">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
} 