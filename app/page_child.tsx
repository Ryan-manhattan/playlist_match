import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <section className="gradient-bg text-white flex items-center justify-center hero-section relative overflow-hidden">
      <div className="text-center px-6 py-16 relative z-10">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">당신의 플레이리스트,<br className="md:hidden" /> 새로운 인연의 시작</h1>
        <p className="text-lg md:text-xl mb-8 font-light text-indigo-100">좋아하는 음악으로 당신과 꼭 맞는 사람을 찾아보세요.</p>
        <Link href="/chart">
          <button className="bg-white hover:bg-gray-100 text-indigo-600 font-bold py-3 px-8 rounded-full text-lg transition duration-150 ease-in-out shadow-md">
            음악 차트 둘러보기
          </button>
        </Link>
      </div>
      {/* SVG 애니메이션 생략 가능, 추후 추가 */}
    </section>
  );
} 