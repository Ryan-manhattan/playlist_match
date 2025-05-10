import './globals.css';

export const metadata = {
  title: 'Playlist Match',
  description: '음악으로 찾는 인연, Playlist Match',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body className="text-gray-800 bg-gray-50 min-h-screen flex flex-col">
        <main className="flex-1">{children}</main>
      </body>
    </html>
  );
} 