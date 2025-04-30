export default function PlaylistLoading() {
  return (
    <main className="container mx-auto px-4 py-8">
      <div className="animate-pulse">
        {/* 플레이리스트 헤더 스켈레톤 */}
        <div className="flex items-start gap-6 mb-8">
          <div className="w-48 h-48 bg-gray-200 rounded-lg"></div>
          <div className="flex-1">
            <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-6"></div>
            <div className="h-10 bg-gray-200 rounded w-32"></div>
          </div>
        </div>

        {/* 트랙 리스트 스켈레톤 */}
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <div className="w-12 h-12 bg-gray-200 rounded"></div>
              <div className="flex-1">
                <div className="h-4 bg-gray-200 rounded w-1/3 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/4"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
} 