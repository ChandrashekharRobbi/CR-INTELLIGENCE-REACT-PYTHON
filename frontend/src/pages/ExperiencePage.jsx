import { motion } from 'framer-motion';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const roles = [
  {
    company: 'eClerx',
    role: 'Analyst — Python Developer',
    type: 'Full-Time',
    period: 'June 2024 – Present',
    tech: ['Python', 'SQL', 'Azure', 'Automation'],
    highlights: [
      'Reduced automation execution time by 50–90% through workflow redesign',
      'Built bulk data synchronization pipeline, reducing manual effort by 80–90%',
      'Optimized regulatory document processing with scheduled downloads and DB caching (50–70% faster)',
      'Developed dynamic Chrome driver handling to eliminate version mismatch issues',
      'Created automated Production Disabled List and Error Reporting tools',
      'Built SQL execution automation tool for multi-environment deployment',
      'Designed code deployment validation script preventing configuration errors',
    ],
  },
  {
    company: 'Qodeit',
    role: 'Python AI Intern',
    type: 'Internship — 3 Months',
    period: '2023',
    tech: ['Python', 'AI Development'],
    highlights: [
      'Worked on AI-related development tasks and backend solutions',
      'Contributed to project development with practical AI implementation',
      'Gained hands-on experience in AI system development',
    ],
  },
  {
    company: 'Teaching Experience',
    role: 'Educator (Parallel)',
    type: 'Since 2020 · 510+ Students',
    period: '2020 – Present',
    tech: ['English (8th–10th)', 'Chemistry (11th–12th)'],
    highlights: [
      'Concept-based and exam-oriented teaching methodology',
      'Built strong communication and public interaction skills',
      'Demonstrated leadership and knowledge-sharing ability',
    ],
  },
];

export default function ExperiencePage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>💼 Experience</h1>
        <p>1 Year 9 Months of professional experience in Python development & automation</p>
      </div>

      <div className="timeline">
        {roles.map((r, i) => (
          <motion.div key={r.company} className="timeline-item" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.15 }}>
            <div className="card" style={{ margin: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 10, marginBottom: 8 }}>
                <div>
                  <h3 style={{ fontSize: 18 }}>{r.company}</h3>
                  <p style={{ color: 'var(--accent-light)', fontWeight: 600, fontSize: 14 }}>{r.role}</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span className="badge badge-accent">{r.period}</span>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', marginTop: 4 }}>{r.type}</div>
                </div>
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, margin: '12px 0' }}>
                {r.tech.map(t => <span key={t} className="badge">{t}</span>)}
              </div>
              <ul style={{ paddingLeft: 20 }}>
                {r.highlights.map((h, j) => <li key={j} style={{ marginBottom: 6 }}>{h}</li>)}
              </ul>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
