'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header(): React.JSX.Element {
  const pathname = usePathname();
  console.log('Current pathname:', pathname);

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-indigo-600">
          Playlist Match
        </Link>
        <div>
          <Link href="/chart" className="text-gray-600 hover:text-indigo-600 mr-4">
            음악 차트
          </Link>
          <Link href="/login" className="text-gray-600 hover:text-indigo-600 mr-4">
            로그인
          </Link>
          <Link 
            href="/signup" 
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition duration-150 ease-in-out"
          >
            회원가입
          </Link>
        </div>
      </nav>
    </header>
  );
} 