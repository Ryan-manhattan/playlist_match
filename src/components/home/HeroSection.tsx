'use client';

import React from 'react';
import Link from 'next/link';

export default function HeroSection(): React.JSX.Element {
  console.log('Rendering HeroSection component');

  return (
    <section className="gradient-bg text-white flex items-center justify-center hero-section">
      <svg className="motion-graphic-svg" viewBox="0 0 800 200" preserveAspectRatio="xMidYMax meet">
        <defs>
          <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style={{ stopColor: 'rgba(255,255,255,0.1)' }} />
            <stop offset="50%" style={{ stopColor: 'rgba(255,255,255,0.3)' }} />
            <stop offset="100%" style={{ stopColor: 'rgba(255,255,255,0.1)' }} />
          </linearGradient>
        </defs>
        {[0, 1, 2, 3].map((i) => (
          <circle
            key={i}
            cx="400"
            cy="150"
            r="5"
            fill="none"
            stroke="url(#waveGradient)"
            strokeWidth="2"
          >
            <animate
              attributeName="r"
              from="5"
              to="300"
              dur="4s"
              repeatCount="indefinite"
              begin={`${i}s`}
            />
            <animate
              attributeName="opacity"
              from="1"
              to="0"
              dur="4s"
              repeatCount="indefinite"
              begin={`${i}s`}
            />
          </circle>
        ))}
      </svg>
      <div className="text-center px-6 py-16 relative z-10">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
          당신의 플레이리스트, <br className="md:hidden" /> 새로운 인연의 시작
        </h1>
        <p className="text-lg md:text-xl mb-8 font-light text-indigo-100">
          좋아하는 음악으로 당신과 꼭 맞는 사람을 찾아보세요.
        </p>
        <Link
          href="/chart"
          className="bg-white hover:bg-gray-100 text-indigo-600 font-bold py-3 px-8 rounded-full text-lg transition duration-150 ease-in-out shadow-md inline-block"
          onClick={() => console.log('Clicked: 음악 차트 둘러보기')}
        >
          음악 차트 둘러보기
        </Link>
      </div>
    </section>
  );
} 