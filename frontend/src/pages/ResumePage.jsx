import { motion } from 'framer-motion';
import { FiDownload } from 'react-icons/fi';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

export default function ResumePage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>📄 Resume</h1>
        <p>Professional overview at a glance</p>
      </div>

      <div className="card card-accent">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <h3>Chandrashekhar Robbi</h3>
            <p style={{ color: 'var(--accent-light)', fontWeight: 600 }}>Analyst — Python Developer</p>
            <p>Thane, Maharashtra, India &bull; Notice Period: 30 Days</p>
          </div>
          <a href="/pdf/resume.pdf" download className="send-btn" style={{ textDecoration: 'none', padding: '12px 24px', borderRadius: 12, display: 'inline-flex', alignItems: 'center', gap: 8, fontSize: 14, fontWeight: 600 }}>
            <FiDownload /> Download PDF
          </a>
        </div>
      </div>

      <div className="divider" />

      <h3 style={{ marginBottom: 16 }}>Professional Summary</h3>
      <div className="card">
        <p>
          Analyst – Python Developer with 1 year 9 months of professional experience specializing in
          Automation Engineering, Backend Development, and Generative AI applications. Strong expertise
          in designing scalable workflows, reducing manual processes, and building production-grade systems.
        </p>
      </div>

      <div className="grid-2" style={{ marginTop: 20 }}>
        <div className="card">
          <h3>Technical Skills</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 10 }}>
            {['Python', 'SQL', 'FastAPI', 'Flask', 'GenAI', 'RAG', 'LLMs', 'TensorFlow', 'Azure', 'Git', 'Streamlit', 'NLP', 'Deep Learning'].map(s => (
              <span key={s} className="badge">{s}</span>
            ))}
          </div>
        </div>
        <div className="card">
          <h3>Key Highlights</h3>
          <ul style={{ paddingLeft: 20, marginTop: 8 }}>
            <li>50–90% automation speed improvement</li>
            <li>80–90% reduction in manual data handling</li>
            <li>Super Achiever Award 2025</li>
            <li>CGPI 9.63 (10.00 in Semester 7)</li>
            <li>510+ students taught</li>
          </ul>
        </div>
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <h3>Career Objective</h3>
        <p>
          Seeking roles as Python Developer, Generative AI Engineer, or Agentic AI Developer.
          Long-term goal is to grow into a Team Lead role driving technical excellence and AI-powered automation systems.
        </p>
      </div>
    </motion.div>
  );
}
