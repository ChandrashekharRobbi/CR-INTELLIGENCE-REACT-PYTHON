import { motion } from 'framer-motion';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const skills = [
  { name: 'Python', pct: 95 },
  { name: 'Automation Engineering', pct: 92 },
  { name: 'Backend Development (FastAPI / Flask)', pct: 88 },
  { name: 'Generative AI / LLMs', pct: 85 },
  { name: 'RAG / PageIndex Systems', pct: 90 },
  { name: 'SQL & Data Processing', pct: 82 },
  { name: 'Deep Learning / Computer Vision', pct: 78 },
  { name: 'NLP & Chatbot Development', pct: 80 },
];

const categories = [
  { title: '💻 Programming', items: ['Python (Primary)', 'SQL', 'Data Structures & Algorithms'] },
  { title: '⚡ Backend & APIs', items: ['FastAPI', 'Flask', 'REST API Development', 'Session Management & Caching'] },
  { title: '🤖 AI & Generative AI', items: ['LLMs', 'Generative AI Applications', 'Prompt Engineering', 'RAG Systems', 'AI Assistants'] },
  { title: '🧠 NLP & Intelligent Systems', items: ['Natural Language Processing', 'Semantic Search', 'Conversational AI'] },
  { title: '⚙️ Automation Engineering', items: ['Workflow Automation', 'Process Optimization', 'Task Pipelines', 'Automation Tools'] },
  { title: '📊 Data Engineering', items: ['Data Processing Pipelines', 'Batch Processing', 'Performance Optimization', 'Caching'] },
  { title: '🏗️ AI System Design', items: ['AI Pipeline Architecture', 'Modular System Design', 'Scalable AI Applications'] },
  { title: '☁️ Cloud & Tools', items: ['Azure', 'Git', 'Streamlit', 'Web Scraping', 'Regex', 'LangChain'] },
  { title: '🤗 AI Frameworks', items: ['HuggingFace', 'TensorFlow', 'Groq Inference', 'VGG16 Transfer Learning'] },
];

export default function SkillsPage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>🛠️ Technical Skills</h1>
        <p>Core competencies and expertise areas</p>
      </div>

      {/* Skill Bars */}
      <div className="card" style={{ marginBottom: 30 }}>
        <h3 style={{ marginBottom: 20 }}>Proficiency Levels</h3>
        {skills.map((s, i) => (
          <motion.div key={s.name} className="skill-bar-wrapper" initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}>
            <div className="skill-bar-header">
              <span className="name">{s.name}</span>
              <span className="pct">{s.pct}%</span>
            </div>
            <div className="skill-bar-track">
              <motion.div className="skill-bar-fill" initial={{ width: 0 }} animate={{ width: `${s.pct}%` }} transition={{ delay: i * 0.08 + 0.3, duration: 0.8 }} />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Category Cards */}
      <h3 style={{ marginBottom: 20 }}>Full Skill Set</h3>
      <div className="grid-3">
        {categories.map((cat, i) => (
          <motion.div key={cat.title} className="card" initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.06 }}>
            <h3 style={{ fontSize: 15, marginBottom: 12 }}>{cat.title}</h3>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {cat.items.map(item => <span key={item} className="badge">{item}</span>)}
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
