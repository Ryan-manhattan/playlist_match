"use client";

import React, { useEffect, useState } from "react";
import Link from 'next/link';
import Header from "../components/Header";

interface Track {
  name: string;
  artist: { name: string };
  image: { "#text": string }[];
  listeners: string;
  url: string;
}

interface ApiResponse {
  tracks?: {
    track?: Track[];
    "@attr"?: {
      page?: string;
      perPage?: string;
      total?: string;
      totalPages?: string;
    };
  };
  error?: number;
  message?: string;
}

interface TrackModalInfo {
  title: string;
  artist: string;
  analysis?: {
    genre?: string;
    mood?: string;
    tempo?: string;
    lyricKeywords?: string[];
    artistBackground?: string[];
    lyrics?: string;
  };
}

export default function ChartPage() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modalInfo, setModalInfo] = useState<TrackModalInfo | null>(null);

  useEffect(() => {
    const fetchChart = async () => {
      try {
        console.log("차트 데이터 로딩 시작...");
        const apiKey = "5b4e51be0851f5698aebeab0b3b1ab91";
        const url = `https://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=${apiKey}&format=json`;
        
        console.log("API 요청 URL:", url);
        const res = await fetch(url);
        
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }

        const data: ApiResponse = await res.json();
        console.log("API 응답 데이터:", data);

        // API 에러 응답 체크
        if (data.error) {
          throw new Error(`Last.fm API 에러: ${data.message || '알 수 없는 에러'}`);
        }

        // 데이터 구조 검증
        if (!data.tracks?.track) {
          throw new Error('유효하지 않은 응답 데이터 구조');
        }

        setTracks(data.tracks.track);
        setError(null);
        console.log("차트 데이터 로딩 완료:", data.tracks.track.length, "개의 트랙");

      } catch (e) {
        console.error("차트 데이터 로딩 오류:", e);
        setError(e instanceof Error ? e.message : '알 수 없는 오류가 발생했습니다.');
        setTracks([]);
      } finally {
        setLoading(false);
      }
    };

    fetchChart();
  }, []);

  const showTrackInfo = (track: Track) => {
    // 실제 구현에서는 API를 통해 상세 정보를 가져올 수 있습니다
    setModalInfo({
      title: track.name,
      artist: track.artist.name,
      analysis: {
        genre: "Pop/Rock",
        mood: "Energetic",
        tempo: "Medium",
        lyricKeywords: ["love", "life", "dance"],
        artistBackground: ["Award-winning artist", "Multiple hit singles"],
        lyrics: "Sample lyrics would go here..."
      }
    });
  };

  const closeModal = () => {
    setModalInfo(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600 mb-4"></div>
          <p className="text-gray-600">차트 데이터를 불러오는 중입니다...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-100">
        <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
          <div className="text-red-500 text-xl mb-4">⚠️ 오류 발생</div>
          <p className="text-gray-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition-colors"
          >
            다시 시도
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">주간 인기 음악 차트</h1>
          <div className="max-w-4xl mx-auto">
            {tracks.map((track, index) => (
              <div 
                key={index}
                className="bg-white rounded-lg shadow-md mb-4 hover:shadow-lg transition-shadow duration-200 overflow-hidden"
                style={{
                  animation: `fadeIn 0.5s ease-out ${index * 0.1}s both`
                }}
              >
                <div className="flex items-center p-4">
                  <div className={`
                    w-12 h-12 flex items-center justify-center rounded-lg mr-4 font-bold text-lg
                    ${index === 0 ? 'bg-yellow-400 text-yellow-900' : 
                      index === 1 ? 'bg-gray-300 text-gray-700' :
                      index === 2 ? 'bg-orange-400 text-orange-900' :
                      'bg-gray-100 text-gray-600'}
                  `}>
                    {index + 1}
                  </div>
                  <div className="flex-grow">
                    <h2 
                      className="text-lg font-semibold text-gray-800 hover:text-indigo-600 cursor-pointer"
                      onClick={() => showTrackInfo(track)}
                    >
                      {track.name}
                    </h2>
                    <p 
                      className="text-gray-600 hover:text-indigo-500 cursor-pointer"
                      onClick={() => showTrackInfo(track)}
                    >
                      {track.artist.name}
                    </p>
                  </div>
                  <a
                    href={`https://www.youtube.com/results?search_query=${encodeURIComponent(`${track.artist.name} ${track.name}`)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-red-600 text-white px-4 py-2 rounded-full hover:bg-red-700 transition-colors flex items-center space-x-2"
                  >
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19.615 3.184c-3.604-.246-11.631-.245-15.23 0-3.897.266-4.356 2.62-4.385 8.816.029 6.185.484 8.549 4.385 8.816 3.6.245 11.626.246 15.23 0 3.897-.266 4.356-2.62 4.385-8.816-.029-6.185-.484-8.549-4.385-8.816zm-10.615 12.816v-8l8 3.993-8 4.007z"/>
                    </svg>
                    <span>Play</span>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {modalInfo && (
        <div 
          className="fixed inset-0 flex items-stretch justify-end z-50"
          onClick={(e) => {
            if (e.target === e.currentTarget) closeModal();
          }}
        >
          <div className="w-1/2 bg-transparent" onClick={closeModal}></div>
          <div 
            className="bg-white w-1/2 shadow-2xl transform transition-transform duration-500 ease-out animate-slide-in overflow-y-auto"
          >
            <div className="p-6 relative">
              <button 
                onClick={closeModal}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
              >
                ✕
              </button>
              <h3 className="text-2xl font-bold mb-4 text-gray-800">{modalInfo.title}</h3>
              <p className="text-lg text-gray-600 mb-6">{modalInfo.artist}</p>
              
              {modalInfo.analysis && (
                <div className="space-y-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="mb-2"><strong>장르:</strong> {modalInfo.analysis.genre}</p>
                    <p className="mb-2"><strong>분위기:</strong> {modalInfo.analysis.mood}</p>
                    <p className="mb-2"><strong>템포:</strong> {modalInfo.analysis.tempo}</p>
                  </div>

                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="mb-2"><strong>키워드</strong></p>
                    <div className="flex flex-wrap gap-2">
                      {modalInfo.analysis.lyricKeywords?.map((keyword, idx) => (
                        <span key={idx} className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="mb-2"><strong>아티스트 정보</strong></p>
                    <ul className="list-disc list-inside space-y-1 text-gray-600">
                      {modalInfo.analysis.artistBackground?.map((info, idx) => (
                        <li key={idx}>{info}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <details className="p-4 bg-gray-50 rounded-lg">
                    <summary className="cursor-pointer text-indigo-600 hover:text-indigo-700 font-medium">
                      가사 보기
                    </summary>
                    <p className="mt-3 text-gray-600 whitespace-pre-line">
                      {modalInfo.analysis.lyrics}
                    </p>
                  </details>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slideIn {
          from {
            transform: translateX(100%);
          }
          to {
            transform: translateX(0);
          }
        }

        .animate-slide-in {
          animation: slideIn 0.5s ease-out forwards;
        }

        .bg-black.bg-opacity-30 {
          backdrop-filter: blur(2px);
        }
      `}</style>
    </>
  );
} 