'use client'

import { signIn } from "next-auth/react";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleGoogleSignIn = async () => {
    try {
      setLoading(true);
      console.log("Google 로그인 시도");
      const result = await signIn("google", { callbackUrl: "/" });
      console.log("Google 로그인 결과:", result);
    } catch (error) {
      console.error("Google 로그인 에러:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    try {
      setLoading(true);
      console.log("이메일/비밀번호 로그인 시도");
      const result = await signIn("credentials", {
        email,
        password,
        redirect: false,
      });
      console.log("로그인 결과:", result);

      if (result?.error) {
        alert(result.error);
      } else if (result?.ok) {
        router.push("/");
      }
    } catch (error) {
      console.error("로그인 에러:", error);
      alert("로그인 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <main id="loginPage" className="py-12 md:py-24 bg-gray-50 min-h-[80vh]">
        <div className="container mx-auto px-6">
          <div className="auth-form-container max-w-md mx-auto bg-white p-10 rounded-2xl shadow-lg">
            <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">로그인</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label htmlFor="login-email" className="block text-sm font-medium text-gray-700 mb-1">이메일</label>
                <input 
                  type="email" 
                  id="login-email" 
                  name="email" 
                  required 
                  className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" 
                  placeholder="you@example.com" 
                />
              </div>
              <div className="mb-2">
                <label htmlFor="login-password" className="block text-sm font-medium text-gray-700 mb-1">비밀번호</label>
                <input 
                  type="password" 
                  id="login-password" 
                  name="password" 
                  required 
                  className="auth-input w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500" 
                  placeholder="********" 
                />
              </div>
              <div className="text-right mb-4">
                <a href="#" className="text-sm text-indigo-600 hover:underline">비밀번호를 잊으셨나요?</a>
              </div>
              <button 
                type="submit" 
                className="auth-button w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg transition duration-150 ease-in-out mb-4"
                disabled={loading}
              >
                {loading ? "로그인 중..." : "로그인"}
              </button>
            </form>
            <div className="relative my-4">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">또는</span>
              </div>
            </div>
            <button
              onClick={handleGoogleSignIn}
              className="w-full flex items-center justify-center gap-2 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition duration-150 ease-in-out"
              disabled={loading}
            >
              <svg className="w-5 h-5" viewBox="0 0 24 24">
                <path
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                  fill="#4285F4"
                />
                <path
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                  fill="#34A853"
                />
                <path
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                  fill="#FBBC05"
                />
                <path
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                  fill="#EA4335"
                />
              </svg>
              <span className="text-gray-700 font-medium">Google로 로그인</span>
            </button>
            <p className="text-center text-sm text-gray-600 mt-6">
              계정이 없으신가요? <a href="/signup" className="text-indigo-600 hover:underline font-medium">회원가입</a>
            </p>
          </div>
        </div>
      </main>
    </>
  );
} 