import { NavLink } from 'react-router-dom';
import { FiMessageSquare, FiUser, FiBriefcase, FiTool, FiBook, FiFolder, FiAward, FiFileText, FiMail, FiCpu, FiLinkedin, FiGithub } from 'react-icons/fi';

const navItems = [
  { path: '/', label: 'AI Chat', icon: <FiMessageSquare /> },
  { path: '/about', label: 'About', icon: <FiUser /> },
  { path: '/experience', label: 'Experience', icon: <FiBriefcase /> },
  { path: '/skills', label: 'Skills', icon: <FiTool /> },
  { path: '/education', label: 'Education', icon: <FiBook /> },
  { path: '/projects', label: 'Projects', icon: <FiFolder /> },
  { path: '/achievements', label: 'Awards', icon: <FiAward /> },
  { path: '/resume', label: 'Resume', icon: <FiFileText /> },
  { path: '/contact', label: 'Contact', icon: <FiMail /> },
  { path: '/arch', label: 'Arch', icon: <FiCpu /> },
];

export default function Topbar() {
  return (
    <header className="topbar">
      {/* Brand */}
      <div className="topbar-brand">
        <div className="brand-avatar">CR</div>
        <span className="brand-name">Chandrashekhar Robbi</span>
        <span className="brand-tag">Open to Work</span>
      </div>

      {/* Nav pills */}
      <nav className="topbar-nav">
        {navItems.map(item => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`}
          >
            <span className="nav-icon">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* Social links */}
      <div className="topbar-actions">
        <a href="https://linkedin.com/in/chandrashekharrobbi" target="_blank" rel="noreferrer" className="topbar-social" title="LinkedIn"><FiLinkedin /></a>
        <a href="https://github.com/ChandrashekharRobbi" target="_blank" rel="noreferrer" className="topbar-social" title="GitHub"><FiGithub /></a>
        <a href="mailto:chandrashekarrobbi789@gmail.com" className="topbar-social" title="Email"><FiMail /></a>
      </div>
    </header>
  );
}
