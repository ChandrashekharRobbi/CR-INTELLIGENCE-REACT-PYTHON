import { motion } from 'framer-motion';
import IsometricArchitecture from '../components/IsometricArchitecture';
import PageIndexTree from '../components/PageIndexTree';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

export default function ArchitecturePage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>🏗️ System Architecture</h1>
        <p>How the Vectorless PageIndex RAG system works</p>
      </div>

      <IsometricArchitecture />

      <div className="card card-accent" style={{ marginTop: 24 }}>
        <h3>Overview</h3>
        <p>
          This portfolio uses <strong>Vectorless RAG with PageIndex</strong> — no vector database, no embedding models.
          Data is organized into a hierarchical tree and retrieved through keyword-based navigation.
        </p>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 14 }}>
          <span className="badge badge-accent">React + Vite</span>
          <span className="badge badge-accent">FastAPI</span>
          <span className="badge badge-accent">PageIndex Tree</span>
          <span className="badge badge-accent">Keyword Retrieval</span>
          <span className="badge badge-accent">Groq + Llama 3.1</span>
        </div>
      </div>

      <div className="divider" />

      <h3 style={{ marginBottom: 16 }}>🌳 PageIndex Document Tree</h3>
      <PageIndexTree />

      <div className="divider" />

      <h3 style={{ marginBottom: 16 }}>⚙️ Pipeline Flow</h3>
      <div className="grid-2">
        {[
          { step: '1', title: 'User Query', desc: 'User submits question through React chat UI → API call to FastAPI backend' },
          { step: '2', title: 'Query Classification', desc: 'Greeting detection, cache lookup, profile question classification — avoid unnecessary LLM calls' },
          { step: '3', title: 'Tree Retrieval', desc: 'Pass 1: Score document branches via keywords → Pass 2: Drill into top branches for page-level matching' },
          { step: '4', title: 'AI Response', desc: 'Context + tree summary sent to Groq LLM (Llama 3.1) → Response cached for future queries' },
        ].map((s, i) => (
          <motion.div key={s.step} className="card" initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}>
            <div style={{ display: 'flex', gap: 14, alignItems: 'flex-start' }}>
              <div style={{ width: 36, height: 36, borderRadius: '50%', background: 'linear-gradient(135deg, var(--accent), var(--accent-dark))', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: 16, flexShrink: 0 }}>{s.step}</div>
              <div>
                <h3 style={{ fontSize: 15, marginBottom: 6 }}>{s.title}</h3>
                <p>{s.desc}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="divider" />

      <h3 style={{ marginBottom: 16 }}>⚡ Vector RAG vs Vectorless PageIndex</h3>
      <div className="grid-2">
        <div className="card" style={{ borderLeft: '3px solid #ef4444' }}>
          <h3 style={{ color: '#f87171', fontSize: 15 }}>❌ Traditional Vector RAG</h3>
          <ul style={{ paddingLeft: 18, marginTop: 10 }}>
            <li>Embedding model (~80MB download)</li>
            <li>FAISS vector database storage</li>
            <li>Opaque similarity scoring</li>
            <li>Heavy dependencies (PyTorch ~2GB)</li>
            <li>Cold start: 30–60 seconds</li>
          </ul>
        </div>
        <div className="card" style={{ borderLeft: '3px solid var(--green)' }}>
          <h3 style={{ color: 'var(--green)', fontSize: 15 }}>✅ Vectorless PageIndex</h3>
          <ul style={{ paddingLeft: 18, marginTop: 10 }}>
            <li>No embedding model needed</li>
            <li>Hierarchical tree navigation</li>
            <li>Transparent keyword matching</li>
            <li>Zero ML dependencies</li>
            <li>Cold start: &lt;1 second</li>
          </ul>
        </div>
      </div>
    </motion.div>
  );
}
