import { motion } from 'framer-motion';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const achievements = [
  { icon: '⚡', title: '50–90% Automation Optimization', desc: 'Reduced data processing time by redesigning production workflows at eClerx' },
  { icon: '🔄', title: 'Production Data Sync Systems', desc: 'Built bulk data pipelines and automated environment sync solutions' },
  { icon: '🤖', title: 'AI Solution Development', desc: 'Built AI applications including disease classification and automation tools' },
  { icon: '🏆', title: 'Industry Recognition', desc: 'Received Appreciation Award (2024) and Super Achiever Award (2025)' },
];

export default function AboutPage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>👤 About Me</h1>
        <p>Professional summary and background</p>
      </div>

      <div className="card card-accent">
        <p>
          Hello! I'm <strong>Chandrashekhar Robbi</strong>, a Backend and Automation-focused Python Developer specializing in
          <strong> Python, Generative AI, and scalable backend systems</strong>. I design data-driven solutions that reduce manual effort,
          optimize workflows, and deliver measurable operational impact.
        </p>
        <br />
        <p>
          Currently working as an <strong>Analyst – Python Developer at eClerx</strong>, I build automation pipelines,
          production-ready backend solutions, and AI-powered systems that improve efficiency and reliability.
          I hold a <strong>Bachelor's degree in Computer Science Engineering (AI & ML)</strong> from Mumbai University
          with a CGPI of <strong>9.63</strong>.
        </p>
      </div>

      <div className="divider" />

      <h3 style={{ marginBottom: 20 }}>🎯 Key Achievements</h3>
      <div className="grid-2">
        {achievements.map((a, i) => (
          <motion.div key={i} className="card" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
            <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start' }}>
              <span style={{ fontSize: 28 }}>{a.icon}</span>
              <div>
                <h3 style={{ fontSize: 15 }}>{a.title}</h3>
                <p>{a.desc}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="divider" />

      <div className="card card-accent">
        <p>
          <strong>Beyond Code:</strong> I enjoy exploring emerging AI technologies, building automation tools,
          and continuously learning new advancements in backend engineering and Generative AI.
          I am also passionate about teaching and knowledge sharing (510+ students taught), which has strengthened my communication
          skills and ability to explain complex technical concepts clearly.
        </p>
      </div>
    </motion.div>
  );
}
