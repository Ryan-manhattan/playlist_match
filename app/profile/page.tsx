"use client";
import React, { useState, useEffect } from "react";

const ProfilePage = () => {
  const [name, setName] = useState("");
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 사용자 정보 불러오기
  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch("/api/user");
        if (!res.ok) throw new Error("사용자 정보를 불러오지 못했습니다.");
        const data = await res.json();
        setName(data.name || "");
        if (data.image) setPreview(data.image);
        console.log("[Profile] 사용자 정보 불러오기:", data);
      } catch (err) {
        setError((err as Error).message);
        console.error("[Profile] 사용자 정보 불러오기 에러:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  // 이름 입력 변경 핸들러
  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
    console.log("[Profile] 이름 입력 변경:", e.target.value);
  };

  // 이미지 파일 선택 핸들러
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
      console.log("[Profile] 프로필 이미지 선택:", file.name);
    }
  };

  // 저장 버튼 클릭 핸들러
  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("name", name);
      if (image) formData.append("image", image);
      const res = await fetch("/api/user", {
        method: "PUT",
        body: formData,
      });
      if (!res.ok) throw new Error("프로필 저장 실패");
      const data = await res.json();
      setName(data.name || "");
      setPreview(data.image || null);
      setImage(null);
      console.log("[Profile] 프로필 저장 성공:", data);
      alert("프로필이 저장되었습니다.");
    } catch (err) {
      setError((err as Error).message);
      console.error("[Profile] 프로필 저장 에러:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold mb-6">프로필 수정</h2>
      {error && <div className="mb-4 text-red-500">{error}</div>}
      <form onSubmit={handleSave}>
        <div className="mb-4">
          <label className="block mb-1 font-medium">이름</label>
          <input
            type="text"
            value={name}
            onChange={handleNameChange}
            className="w-full border rounded px-3 py-2"
            placeholder="이름을 입력하세요"
            disabled={loading}
          />
        </div>
        <div className="mb-4">
          <label className="block mb-1 font-medium">프로필 이미지</label>
          <input type="file" accept="image/*" onChange={handleImageChange} disabled={loading} />
          {preview && (
            <img
              src={preview}
              alt="프로필 미리보기"
              className="mt-2 w-24 h-24 object-cover rounded-full border"
            />
          )}
        </div>
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
          disabled={loading}
        >
          {loading ? "저장 중..." : "저장"}
        </button>
        <button
          type="button"
          className="w-full mt-3 bg-gray-200 text-gray-800 py-2 rounded hover:bg-gray-300"
          onClick={() => {
            console.log("[Profile] 메인 페이지로 돌아가기 클릭");
            window.location.href = "/";
          }}
          disabled={loading}
        >
          메인 페이지로 돌아가기
        </button>
      </form>
    </div>
  );
};

export default ProfilePage; 