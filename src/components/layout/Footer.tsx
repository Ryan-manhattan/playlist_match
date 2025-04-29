'use client';

import React from 'react';
import Link from 'next/link';

export default function Footer(): React.JSX.Element {
  console.log('Rendering Footer component');
  
  return (
    <footer className="bg-gray-800 text-gray-400 py-8">
      <div className="container mx-auto px-6 text-center text-sm">
        © {new Date().getFullYear()} Playlist Match. All rights reserved.
        <div className="mt-2">
          <Link href="/terms" className="hover:text-gray-300 mx-2">
            이용약관
          </Link>
          {' | '}
          <Link href="/privacy" className="hover:text-gray-300 mx-2">
            개인정보처리방침
          </Link>
        </div>
      </div>
    </footer>
  );
} 