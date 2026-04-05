import { Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import Topbar from './components/Sidebar';
import ChatPage from './pages/ChatPage';
import AboutPage from './pages/AboutPage';
import SkillsPage from './pages/SkillsPage';
import ProjectsPage from './pages/ProjectsPage';
import ExperiencePage from './pages/ExperiencePage';
import EducationPage from './pages/EducationPage';
import AchievementsPage from './pages/AchievementsPage';
import ResumePage from './pages/ResumePage';
import ContactPage from './pages/ContactPage';
import ArchitecturePage from './pages/ArchitecturePage';

function PageWrapper({ children }) {
  return <div className="page-container">{children}</div>;
}

export default function App() {
  const location = useLocation();

  return (
    <div className="app-layout">
      <Topbar />
      <main className="main-content">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<ChatPage />} />
            <Route path="/about" element={<PageWrapper><AboutPage /></PageWrapper>} />
            <Route path="/experience" element={<PageWrapper><ExperiencePage /></PageWrapper>} />
            <Route path="/skills" element={<PageWrapper><SkillsPage /></PageWrapper>} />
            <Route path="/education" element={<PageWrapper><EducationPage /></PageWrapper>} />
            <Route path="/projects" element={<PageWrapper><ProjectsPage /></PageWrapper>} />
            <Route path="/achievements" element={<PageWrapper><AchievementsPage /></PageWrapper>} />
            <Route path="/resume" element={<PageWrapper><ResumePage /></PageWrapper>} />
            <Route path="/contact" element={<PageWrapper><ContactPage /></PageWrapper>} />
            <Route path="/arch" element={<PageWrapper><ArchitecturePage /></PageWrapper>} />
          </Routes>
        </AnimatePresence>
      </main>
    </div>
  );
}
