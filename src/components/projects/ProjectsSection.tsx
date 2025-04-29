import React from "react";

// 더미 프로젝트 데이터
const projects = [
  {
    name: "Portfolio Website",
    description: "개인 포트폴리오 및 기술 블로그 사이트",
    link: "https://your-portfolio.com",
  },
  {
    name: "Playlist Match",
    description: "Spotify API를 활용한 음악 추천 서비스",
    link: "https://your-playlist-match.com",
  },
];

const ProjectsSection: React.FC = () => {
  return (
    <section className="py-8">
      <h2 className="text-2xl font-bold mb-4">Projects</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        {projects.map((project) => (
          <div key={project.name} className="border rounded-lg p-4 shadow-sm bg-white dark:bg-gray-900">
            <h3 className="text-xl font-semibold mb-2">{project.name}</h3>
            <p className="mb-2 text-gray-700 dark:text-gray-300">{project.description}</p>
            <a
              href={project.link}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Visit
            </a>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ProjectsSection;
