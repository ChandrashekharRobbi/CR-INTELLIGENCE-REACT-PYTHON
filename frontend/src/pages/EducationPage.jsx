import { motion } from 'framer-motion';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const semesters = [
  { sem: 'Semester 1', sgpi: 9.89 }, { sem: 'Semester 2', sgpi: 9.60 },
  { sem: 'Semester 3', sgpi: 9.86 }, { sem: 'Semester 4', sgpi: 9.00 },
  { sem: 'Semester 5', sgpi: 9.59 }, { sem: 'Semester 6', sgpi: 9.87 },
  { sem: 'Semester 7', sgpi: 10.00 }, { sem: 'Semester 8', sgpi: 9.29 },
];

export default function EducationPage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>🎓 Education</h1>
        <p>Academic qualifications and performance</p>
      </div>

      <div className="card card-accent">
        <h3>Bachelor of Engineering (B.E)</h3>
        <p style={{ color: 'var(--accent-light)', fontWeight: 600, margin: '6px 0' }}>
          Computer Science Engineering — Artificial Intelligence & Machine Learning
        </p>
        <p>Saraswati College of Engineering, Mumbai University</p>
        <div style={{ display: 'flex', gap: 20, marginTop: 16, flexWrap: 'wrap' }}>
          <div className="stat-card" style={{ flex: 1, minWidth: 120 }}>
            <div className="value">9.63</div>
            <div className="label">Overall CGPI</div>
          </div>
          <div className="stat-card" style={{ flex: 1, minWidth: 120 }}>
            <div className="value">10.00</div>
            <div className="label">Best SGPI (Sem 7)</div>
          </div>
          <div className="stat-card" style={{ flex: 1, minWidth: 120 }}>
            <div className="value">2024</div>
            <div className="label">Graduation Year</div>
          </div>
        </div>
      </div>

      <div className="divider" />

      <h3 style={{ marginBottom: 20 }}>Semester-wise Performance</h3>
      <div className="grid-4">
        {semesters.map((s, i) => (
          <motion.div key={s.sem} className="stat-card" initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.06 }}>
            <div className="value" style={{ fontSize: s.sgpi === 10 ? 36 : 28 }}>{s.sgpi.toFixed(2)}</div>
            <div className="label">{s.sem}</div>
          </motion.div>
        ))}
      </div>

      <div className="divider" />

      <h3 style={{ marginBottom: 16 }}>Core Areas of Study</h3>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        {['AI Fundamentals', 'Machine Learning', 'Data Structures & Algorithms', 'Database Management', 'Software Engineering', 'Computer Networks', 'Backend Development', 'Problem Solving'].map(a => (
          <span key={a} className="badge">{a}</span>
        ))}
      </div>
    </motion.div>
  );
}
