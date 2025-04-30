"use client";
import React, { useState, useEffect } from "react";

const PlaylistsPage = () => {
  const [playlists, setPlaylists] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newThumb, setNewThumb] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  // 플레이리스트 목록 불러오기
  useEffect(() => {
    const fetchPlaylists = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch("/api/playlists");
        if (!res.ok) throw new Error("플레이리스트를 불러오지 못했습니다.");
        const data = await res.json();
        setPlaylists(data);
        console.log("[Playlists] 플레이리스트 목록 불러오기:", data);
      } catch (err) {
        setError((err as Error).message);
        console.error("[Playlists] 목록 불러오기 에러:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchPlaylists();
  }, []);

  // 모달 열기
  const handleOpenModal = () => {
    setShowModal(true);
    console.log("[Playlists] 플레이리스트 생성 모달 열기");
  };
  // 모달 닫기
  const handleCloseModal = () => {
    setShowModal(false);
    setNewTitle("");
    setNewDesc("");
    setNewThumb(null);
    setPreview(null);
    console.log("[Playlists] 플레이리스트 생성 모달 닫기");
  };
  // 썸네일 파일 선택
  const handleThumbChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setNewThumb(file);
      const reader = new FileReader();
      reader.onloadend = () => setPreview(reader.result as string);
      reader.readAsDataURL(file);
      console.log("[Playlists] 썸네일 파일 선택:", file.name);
    }
  };
  // 플레이리스트 생성
  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("name", newTitle);
      formData.append("description", newDesc);
      if (newThumb) formData.append("thumbnail", newThumb);
      const res = await fetch("/api/playlists", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("플레이리스트 생성 실패");
      const data = await res.json();
      setPlaylists([data, ...playlists]);
      handleCloseModal();
      console.log("[Playlists] 플레이리스트 생성 성공:", data);
    } catch (err) {
      setError((err as Error).message);
      console.error("[Playlists] 플레이리스트 생성 에러:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto mt-10 p-4">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">내 플레이리스트</h2>
        <button
          className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
          onClick={handleOpenModal}
        >
          + 플레이리스트 생성
        </button>
      </div>
      {error && <div className="mb-4 text-red-500">{error}</div>}
      {loading ? (
        <div className="text-center py-10 text-gray-400">로딩 중...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {playlists.map((pl) => (
            <div key={pl.id} className="bg-white rounded shadow p-4 flex flex-col items-center">
              <img
                src={pl.thumbnail || "/default-playlist.png"}
                alt="썸네일"
                className="w-24 h-24 object-cover rounded mb-2 border"
              />
              <div className="font-semibold text-lg mb-1">{pl.name}</div>
              <div className="text-gray-500 text-sm mb-1">{pl.description}</div>
              <div className="text-gray-400 text-xs mb-2">{pl.createdAt?.slice(0, 10)} · {pl.trackCount ?? 0}곡</div>
              <div className="flex gap-2 mt-auto">
                <button className="text-blue-500 hover:underline text-sm" onClick={() => console.log("[Playlists] 수정 클릭:", pl.id)}>수정</button>
                <button className="text-red-500 hover:underline text-sm" onClick={() => console.log("[Playlists] 삭제 클릭:", pl.id)}>삭제</button>
              </div>
            </div>
          ))}
        </div>
      )}
      {/* 생성 모달 */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-lg relative">
            <button
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
              onClick={handleCloseModal}
            >
              ×
            </button>
            <h3 className="text-xl font-bold mb-4">플레이리스트 생성</h3>
            <form onSubmit={handleCreate}>
              <div className="mb-3">
                <label className="block mb-1 font-medium">제목</label>
                <input
                  type="text"
                  value={newTitle}
                  onChange={e => setNewTitle(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                  required
                />
              </div>
              <div className="mb-3">
                <label className="block mb-1 font-medium">설명</label>
                <textarea
                  value={newDesc}
                  onChange={e => setNewDesc(e.target.value)}
                  className="w-full border rounded px-3 py-2"
                  rows={2}
                />
              </div>
              <div className="mb-3">
                <label className="block mb-1 font-medium">썸네일 이미지(선택)</label>
                <input type="file" accept="image/*" onChange={handleThumbChange} />
                {preview && (
                  <img
                    src={preview}
                    alt="썸네일 미리보기"
                    className="mt-2 w-20 h-20 object-cover rounded border"
                  />
                )}
              </div>
              <button
                type="submit"
                className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 mt-2"
                disabled={loading}
              >
                {loading ? "생성 중..." : "생성"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlaylistsPage; 