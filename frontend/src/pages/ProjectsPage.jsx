import { motion } from 'framer-motion';
import { FiGithub, FiExternalLink } from 'react-icons/fi';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const projects = [
  {
    name: 'AI Resume Portfolio — PageIndex RAG Assistant',
    date: '2025',
    desc: 'Multi-page AI portfolio with context-aware assistant using Vectorless PageIndex RAG. Hierarchical tree retrieval, keyword-based navigation, Groq LLM inference, and React frontend.',
    tech: ['Python', 'React', 'FastAPI', 'PageIndex RAG', 'LLMs', 'Groq', 'NLP'],
    github: 'https://github.com/ChandrashekharRobbi/AI-Resume-Portfolio-RAG-Powered-Assistant',
  },
  {
    name: 'GenMed — Medicine Information Chatbot',
    date: '2024',
    desc: 'AI-powered chatbot providing generic medicine prices and nearest Jan Aushadi Kendra search by pincode. NLP-based interaction with web scraping and LLM integration.',
    tech: ['Python', 'Streamlit', 'NLP', 'Web Scraping', 'LLM Integration'],
    github: 'https://github.com/ChandrashekharRobbi/GenMed',
  },
  {
    name: 'Paddy Doctor — Crop Disease Classification',
    date: '2024',
    desc: 'AI-powered crop disease classification using deep learning and VGG16 transfer learning. Achieved 98% accuracy for automated paddy disease detection.',
    tech: ['Python', 'TensorFlow', 'VGG16', 'Deep Learning', 'Computer Vision'],
    github: 'https://github.com/ChandrashekharRobbi/Convolutional-Neural-Network-with-Tensorflow',
  },
  {
    name: 'Movie & Series Watchlist Automation',
    date: '2024',
    desc: 'End-to-end automation pipeline: OMDB API → Google Sheets → Notion database. Automated movie metadata logging with zero manual entry.',
    tech: ['Python', 'OMDB API', 'Google Sheets', 'Apps Script', 'Notion API'],
    github: 'https://github.com/ChandrashekharRobbi/Movie-Series-Watchlist-Automation-Pipeline',
  },
  {
    name: 'LipNet — Visual Speech Recognition',
    date: '2023',
    desc: 'Deep learning system that predicts spoken text from lip movement without audio. Custom model training pipeline with Streamlit interface.',
    tech: ['Python', 'Deep Learning', 'Computer Vision', 'Video Processing', 'Streamlit'],
    github: 'https://github.com/ChandrashekharRobbi/LipNet',
  },
  {
    name: 'GitHub Automation Watchdog',
    date: '2023',
    desc: 'Detects new functions using git diff + regex, auto-generates commit messages, and pushes to GitHub. Improved dev workflow efficiency.',
    tech: ['Python', 'Git', 'Regex', 'Automation'],
    github: 'https://github.com/ChandrashekharRobbi',
  },
];

export default function ProjectsPage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>🚀 Projects</h1>
        <p>Selected work demonstrating impact and technical expertise</p>
      </div>

      <div className="timeline">
        {projects.map((proj, i) => (
          <motion.div
            key={proj.name}
            className="timeline-item"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <div className="card" style={{ margin: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 10, marginBottom: 12 }}>
                <h3 style={{ fontSize: 17 }}>{proj.name}</h3>
                <span className="badge badge-accent">{proj.date}</span>
              </div>
              <p>{proj.desc}</p>
              <div style={{ marginTop: 14, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {proj.tech.map(t => <span key={t} className="badge">{t}</span>)}
              </div>
              <div style={{ marginTop: 16 }}>
                <a href={proj.github} target="_blank" rel="noreferrer" style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 13, fontWeight: 600 }}>
                  <FiGithub /> View on GitHub <FiExternalLink size={12} />
                </a>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
