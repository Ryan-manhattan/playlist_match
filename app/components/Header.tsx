'use client';

import Link from "next/link";
import { useSession, signOut } from "next-auth/react";
import Image from "next/image";
import { useState } from "react";

export default function Header() {
  const { data: session, status } = useSession();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const handleSignOut = async () => {
    await signOut({ callbackUrl: '/' });
  };

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <nav className="container mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-indigo-600">
          Playlist Match
        </Link>
        <div className="flex items-center">
          <Link href="/chart" className="text-gray-600 hover:text-indigo-600 mr-4">
            음악 차트
          </Link>
          {status === 'loading' ? (
            <div className="w-8 h-8 rounded-full bg-gray-200 animate-pulse"></div>
          ) : session?.user ? (
            <div className="relative">
              <button
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center space-x-2 focus:outline-none"
              >
                <div className="w-8 h-8 rounded-full overflow-hidden">
                  {session.user.image ? (
                    <Image
                      src={session.user.image}
                      alt="Profile"
                      width={32}
                      height={32}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-indigo-200 flex items-center justify-center text-indigo-600">
                      {session.user.name?.[0] || session.user.email?.[0] || '?'}
                    </div>
                  )}
                </div>
                <span className="text-gray-700">{session.user.name || session.user.email?.split('@')[0]}</span>
              </button>

              {isDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 z-50">
                  <Link
                    href="/profile"
                    className="block px-4 py-2 text-gray-700 hover:bg-indigo-50"
                    onClick={() => setIsDropdownOpen(false)}
                  >
                    프로필
                  </Link>
                  <Link
                    href="/playlists"
                    className="block px-4 py-2 text-gray-700 hover:bg-indigo-50"
                    onClick={() => setIsDropdownOpen(false)}
                  >
                    내 플레이리스트
                  </Link>
                  <button
                    onClick={handleSignOut}
                    className="w-full text-left px-4 py-2 text-gray-700 hover:bg-indigo-50"
                  >
                    로그아웃
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link href="/login" className="text-gray-600 hover:text-indigo-600 mr-4">
                로그인
              </Link>
              <Link
                href="/signup"
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition duration-150 ease-in-out"
              >
                회원가입
              </Link>
            </>
          )}
        </div>
      </nav>
    </header>
  );
} 