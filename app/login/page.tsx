'use client'

import Header from "../components/Header";
import Footer from "../components/Footer";

export default function LoginPage() {
  return (
    <>
      <Header />
      <main id="loginPage" className="py-12 md:py-24 bg-gray-50 min-h-[80vh]">
        <div className="container mx-auto px-6">
          <div className="auth-form-container max-w-md mx-auto bg-white p-10 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">로그인</h2>
            <form onSubmit={e => { e.preventDefault(); alert('로그인 기능은 구현되지 않았습니다.'); }}>
              <div className="mb-4">
                <label htmlFor="login-email" className="block text-sm font-medium text-gray-700 mb-1">이메일</label>
                <input type="email" id="login-email" name="email" required className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" placeholder="you@example.com" />
              </div>
              <div className="mb-2">
                <label htmlFor="login-password" className="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
                <input type="password" id="login-password" name="password" required className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" placeholder="********" />
              </div>
              <div className="text-right mb-4">
                <a href="#" className="text-sm text-indigo-600 hover:underline">비밀번호를 잊으셨나요?</a>
              </div>
              <button type="submit" className="auth-button w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg transition duration-150 ease-in-out">로그인</button>
            </form>
            <p className="text-center text-sm text-gray-600 mt-6">
              계정이 없으신가요? <a href="/signup" className="text-indigo-600 hover:underline font-medium">회원가입</a>
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
} 