import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <>
      <main id="landingPage">
        <section className="gradient-bg text-white flex items-center justify-center hero-section relative overflow-hidden">
          <svg className="motion-graphic-svg absolute bottom-0 left-1/2 transform -translate-x-1/2 w-full max-w-3xl h-auto z-5 pointer-events-none" viewBox="0 0 800 200" preserveAspectRatio="xMidYMax meet">
            <defs>
              <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="rgba(255,255,255,0.1)" />
                <stop offset="50%" stopColor="rgba(255,255,255,0.3)" />
                <stop offset="100%" stopColor="rgba(255,255,255,0.1)" />
              </linearGradient>
            </defs>
            {[0,1,2,3].map(i => (
              <circle key={i} cx="400" cy="150" r="5" fill="none" stroke="url(#waveGradient)" strokeWidth="2">
                <animate attributeName="r" from="5" to="300" dur="4s" repeatCount="indefinite" begin={`${i}s`} />
                <animate attributeName="opacity" from="1" to="0" dur="4s" repeatCount="indefinite" begin={`${i}s`} />
              </circle>
            ))}
          </svg>
          <div className="text-center px-6 py-16 relative z-10">
            <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">당신의 플레이리스트,<br className="md:hidden" /> 새로운 인연의 시작</h1>
            <p className="text-lg md:text-xl mb-8 font-light text-indigo-100">좋아하는 음악으로 당신과 꼭 맞는 사람을 찾아보세요.</p>
            <Link href="/chart">
              <button className="bg-white hover:bg-gray-100 text-indigo-600 font-bold py-3 px-8 rounded-full text-lg transition duration-150 ease-in-out shadow-md">
                음악 차트 둘러보기
              </button>
            </Link>
          </div>
        </section>
        <section className="py-16 md:py-24 bg-white">
          <div className="container mx-auto px-6 text-center">
            <h2 className="text-3xl font-bold mb-4 text-gray-800">음악 취향, 어떻게 인연이 되나요?</h2>
            <p className="text-gray-600 mb-12 max-w-2xl mx-auto">Playlist Match는 당신의 음악 스트리밍 서비스 플레이리스트를 분석하여<br />가장 잘 맞는 음악적 감성의 상대를 찾아줍니다.</p>
            <div className="grid md:grid-cols-3 gap-8 text-left">
              <div className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition duration-150 ease-in-out">
                <div className="text-indigo-500 mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">플레이리스트 연동</h3>
                <p className="text-gray-600 text-sm">Spotify, YouTube Music 등 즐겨 사용하는 서비스의 플레이리스트를 간편하게 연결하세요.</p>
              </div>
              <div className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition duration-150 ease-in-out">
                <div className="text-indigo-500 mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">'음악 궁합' 분석</h3>
                <p className="text-gray-600 text-sm">좋아하는 장르, 아티스트, 곡 분위기를 분석하여 당신과 음악적 케미가 높은 상대를 찾아냅니다.</p>
              </div>
              <div className="bg-gray-50 p-6 rounded-lg shadow-sm hover:shadow-md transition duration-150 ease-in-out">
                <div className="text-indigo-500 mb-3">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold mb-2">의미있는 대화 시작</h3>
                <p className="text-gray-600 text-sm">음악이라는 공통 관심사로 자연스럽게 대화를 시작하고 서로를 알아가세요.</p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  );
}
