'use client'

import React, { useRef, useState } from "react";

export default function SignupPage() {
  const [error, setError] = useState("");
  const passwordRef = useRef<HTMLInputElement>(null);
  const passwordConfirmRef = useRef<HTMLInputElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const pw = passwordRef.current?.value || "";
    const pwc = passwordConfirmRef.current?.value || "";
    if (pw !== pwc) {
      setError("비밀번호가 일치하지 않습니다.");
      return;
    }
    setError("");
    alert("회원가입 기능은 구현되지 않았습니다.");
  };

  return (
    <>
      <main id="signupPage" className="py-12 md:py-24 bg-gray-50 min-h-[80vh]">
        <div className="container mx-auto px-6">
          <div className="auth-form-container max-w-md mx-auto bg-white p-10 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">회원가입</h2>
            <form id="signup-form" onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="signup-email" className="block text-sm font-medium text-gray-700 mb-1">이메일</label>
                <input type="email" id="signup-email" name="email" required className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" placeholder="you@example.com" />
              </div>
              <div className="mb-4">
                <label htmlFor="signup-password" className="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
                <input ref={passwordRef} type="password" id="signup-password" name="password" required className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" placeholder="********" />
              </div>
              <div className="mb-2">
                <label htmlFor="signup-password-confirm" className="block text-sm font-medium text-gray-700 mb-1">비밀번호 확인</label>
                <input ref={passwordConfirmRef} type="password" id="signup-password-confirm" name="passwordConfirm" required className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" placeholder="********" />
                {error && <p className="error-message text-red-500 text-xs mt-1">{error}</p>}
              </div>
              <button type="submit" className="auth-button w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg transition duration-150 ease-in-out mt-4">회원가입</button>
            </form>
            <p className="text-center text-sm text-gray-600 mt-6">
              이미 계정이 있으신가요? <a href="/login" className="text-indigo-600 hover:underline font-medium">로그인</a>
            </p>
          </div>
        </div>
      </main>
    </>
  );
} 