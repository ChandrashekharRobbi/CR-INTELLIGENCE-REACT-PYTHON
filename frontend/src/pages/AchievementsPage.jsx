import { motion } from 'framer-motion';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const sections = [
  { title: '🏆 Professional Awards', items: [
    { name: 'Super Achiever Award — 2025', desc: 'Exceptional performance, automation improvements, and technical contribution' },
    { name: 'Appreciation Award — 2024', desc: 'Strong contribution, high-quality work, and effective team collaboration' },
  ]},
  { title: '🏅 Competitions', items: [
    { name: 'Avishkar — 3rd Rank', desc: 'Demonstrated innovation and problem-solving capability in technical competition' },
    { name: 'Hackoverflow — Participant', desc: 'Collaborative development and rapid solution building experience' },
  ]},
  { title: '📜 Certifications', items: [
    { name: 'Python Certification — IIT Bombay', desc: 'Structured Python programming training and best practices' },
    { name: 'Generative AI — University of Munich', desc: 'Modern AI approaches, concepts, and systems' },
    { name: 'Multiple Udemy Certifications', desc: 'Continuous learning in programming and AI technologies' },
  ]},
  { title: '📄 Research & Publication', items: [
    { name: 'GenMed Project Publication', desc: 'AI-based solution for generic medicine prices and Jan Aushadi Kendra discovery' },
  ]},
  { title: '👨‍🏫 Teaching Impact', items: [
    { name: '510+ Students Taught (Since 2020)', desc: 'English (8th–10th) and Chemistry (11th–12th). Concept-based, exam-focused teaching.' },
  ]},
];

export default function AchievementsPage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>⭐ Achievements</h1>
        <p>Awards, certifications, and recognition</p>
      </div>

      {sections.map((sec, si) => (
        <div key={sec.title} style={{ marginBottom: 30 }}>
          <h3 style={{ marginBottom: 16 }}>{sec.title}</h3>
          {sec.items.map((item, i) => (
            <motion.div key={item.name} className="card card-accent" style={{ marginBottom: 12 }}
              initial={{ opacity: 0, x: -15 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: si * 0.1 + i * 0.05 }}>
              <h3 style={{ fontSize: 15 }}>{item.name}</h3>
              <p>{item.desc}</p>
            </motion.div>
          ))}
        </div>
      ))}
    </motion.div>
  );
}
