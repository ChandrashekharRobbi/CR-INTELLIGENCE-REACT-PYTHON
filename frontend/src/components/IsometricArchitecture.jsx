import React, { useCallback } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Handle,
  Position
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

// --- CUSTOM NODE COMPONENTS ---

// Styling for different node types so we can reuse one component
const typeStyles = {
  client: { bg: 'rgba(30,27,75,0.7)', border: '#6366f1', icon: '💻' },
  server: { bg: 'rgba(6,78,59,0.7)', border: '#10b981', icon: '⚙️' },
  engine: { bg: 'rgba(76,29,149,0.7)', border: '#8b5cf6', icon: '🧠' },
  db: { bg: 'rgba(120,53,15,0.7)', border: '#f59e0b', icon: '🗄️' },
  external: { bg: 'rgba(15,23,42,0.7)', border: '#38bdf8', icon: '🌐' },
  user: { bg: 'rgba(0,0,0,0.5)', border: '#a855f7', icon: '👤' }
};

const CustomNode = ({ data, style }) => {
  const theme = typeStyles[data.type || 'client'];
  
  return (
    <div style={{
      background: theme.bg,
      border: `2px solid ${theme.border}`,
      borderRadius: '8px',
      padding: '10px 14px',
      minWidth: '200px',
      color: 'white',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
      backdropFilter: 'blur(4px)',
      ...style
    }}>
      <Handle type="target" position={Position.Top} style={{ background: '#555' }} />
      <div style={{ fontSize: '24px' }}>{theme.icon}</div>
      <div>
        <div style={{ fontSize: '13px', fontWeight: 'bold' }}>{data.label}</div>
        {data.sub && <div style={{ fontSize: '10px', color: 'rgba(255,255,255,0.6)', marginTop: '2px' }}>{data.sub}</div>}
      </div>
      <Handle type="source" position={Position.Bottom} style={{ background: '#555' }} />
    </div>
  );
};

// --- INITIAL DATA ---

const initialNodes = [
  // Parent Groups (Underlays)
  { id: 'group-client', type: 'group', position: { x: 700, y: 100 }, style: { width: 300, height: 350, backgroundColor: 'rgba(99,102,241,0.05)', border: '1px dashed #6366f1', borderRadius: '12px' }, zIndex: -1 },
  { id: 'group-server', type: 'group', position: { x: 100, y: 150 }, style: { width: 560, height: 280, backgroundColor: 'rgba(16,185,129,0.05)', border: '1px dashed #10b981', borderRadius: '12px' }, zIndex: -1 },
  { id: 'group-ai', type: 'group', position: { x: 250, y: 480 }, style: { width: 400, height: 250, backgroundColor: 'rgba(139,92,246,0.05)', border: '1px dashed #8b5cf6', borderRadius: '12px' }, zIndex: -1 },
  { id: 'group-data', type: 'group', position: { x: 50, y: 780 }, style: { width: 950, height: 160, backgroundColor: 'rgba(245,158,11,0.05)', border: '1px dashed #f59e0b', borderRadius: '12px' }, zIndex: -1 },

  // Group Labels
  { id: 'lbl-client', position: { x: 710, y: 110 }, data: { label: 'Client Architecture (React + Vite)' }, style: { border: 'none', background: 'transparent', color: '#6366f1', fontWeight: 'bold', fontSize: '12px' }, draggable: false, selectable: false },
  { id: 'lbl-server', position: { x: 110, y: 160 }, data: { label: 'Server Architecture (FastAPI)' }, style: { border: 'none', background: 'transparent', color: '#10b981', fontWeight: 'bold', fontSize: '12px' }, draggable: false, selectable: false },
  { id: 'lbl-ai', position: { x: 260, y: 490 }, data: { label: 'AI Engine (Vectorless RAG)' }, style: { border: 'none', background: 'transparent', color: '#8b5cf6', fontWeight: 'bold', fontSize: '12px' }, draggable: false, selectable: false },
  { id: 'lbl-data', position: { x: 60, y: 790 }, data: { label: 'Data & External Services' }, style: { border: 'none', background: 'transparent', color: '#f59e0b', fontWeight: 'bold', fontSize: '12px' }, draggable: false, selectable: false },

  // Nodes (Abs positions)
  { id: 'user', type: 'custom', position: { x: 750, y: 0 }, data: { label: 'User', type: 'user' } },

  // Client Nodes
  { id: 'app', type: 'custom', position: { x: 750, y: 150 }, data: { label: 'App.jsx', sub: 'React Router', type: 'client' } },
  { id: 'ui', type: 'custom', position: { x: 750, y: 250 }, data: { label: 'UI Pages & Components', sub: 'Glassmorphism', type: 'client' } },
  { id: 'api_f', type: 'custom', position: { x: 750, y: 350 }, data: { label: 'API Fetcher', sub: 'api.js via Axios', type: 'client' } },

  // Server Nodes
  { id: 'fastapi', type: 'custom', position: { x: 250, y: 200 }, data: { label: 'FastAPI Server', sub: 'api.py', type: 'server' } },
  { id: 'get_sec', type: 'custom', position: { x: 120, y: 340 }, data: { label: 'GET /api/sections/{id}', type: 'server' } },
  { id: 'post_chat', type: 'custom', position: { x: 380, y: 340 }, data: { label: 'POST /api/chat', type: 'server' } },
  { id: 'get_stats', type: 'custom', position: { x: 440, y: 200 }, data: { label: 'GET /api/stats', type: 'server' } },

  // AI Nodes
  { id: 'rag', type: 'custom', position: { x: 350, y: 530 }, data: { label: 'RAGPipeline', sub: 'rag_pipeline.py', type: 'engine' } },
  { id: 'pageindex', type: 'custom', position: { x: 350, y: 640 }, data: { label: 'PageIndex', sub: 'page_index.py', type: 'engine' } },

  // Data Nodes
  { id: 'config', type: 'custom', position: { x: 100, y: 830 }, data: { label: 'Config & Env', sub: '.env, config.py', type: 'db' } },
  { id: 'kb', type: 'custom', position: { x: 350, y: 830 }, data: { label: 'Local Knowledge Base', sub: 'data/', type: 'db' } },
  { id: 'groq', type: 'custom', position: { x: 670, y: 830 }, data: { label: 'Groq LLM API', sub: 'Llama 3.1 8B', type: 'external' } }
];

const edgeDefault = {
  type: 'smoothstep',
  animated: true,
  style: { stroke: '#94a3b8', strokeWidth: 2 },
  markerEnd: { type: MarkerType.ArrowClosed, color: '#94a3b8' }
};

const makeLabel = (label) => ({
  label,
  labelStyle: { fill: '#e2e8f0', fontSize: 11, fontWeight: 'bold' },
  labelBgStyle: { fill: 'rgba(15,23,42,0.8)' },
  labelBgPadding: [4, 4],
  labelBgBorderRadius: 4
});

const initialEdges = [
  { id: 'e-user-app', source: 'user', target: 'app', ...edgeDefault, ...makeLabel('Interacts') },
  { id: 'e-app-ui', source: 'app', target: 'ui', ...edgeDefault },
  { id: 'e-ui-apif', source: 'ui', target: 'api_f', ...edgeDefault },

  { id: 'e-fastapi-sec', source: 'fastapi', target: 'get_sec', ...edgeDefault },
  { id: 'e-fastapi-chat', source: 'fastapi', target: 'post_chat', ...edgeDefault },
  { id: 'e-fastapi-stats', source: 'fastapi', target: 'get_stats', ...edgeDefault },

  // Cross links
  { id: 'e-apif-sec', source: 'api_f', target: 'get_sec', ...edgeDefault, ...makeLabel('Gets Resume Data'), sourceHandle: 'bottom', targetHandle: 'top' },
  { id: 'e-apif-chat', source: 'api_f', target: 'post_chat', ...edgeDefault, ...makeLabel('Asks AI Questions') },
  { id: 'e-apif-stats', source: 'api_f', target: 'get_stats', ...edgeDefault, ...makeLabel('Gets Engine Stats') },

  // Inner AI links
  { id: 'e-chat-rag', source: 'post_chat', target: 'rag', ...edgeDefault, ...makeLabel('Submits Queries') },
  { id: 'e-stats-rag', source: 'get_stats', target: 'rag', ...edgeDefault, ...makeLabel('Fetches Metrics') },
  { id: 'e-rag-index', source: 'rag', target: 'pageindex', ...edgeDefault },

  // Data cross links
  { id: 'e-sec-kb', source: 'get_sec', target: 'kb', ...edgeDefault, ...makeLabel('Reads Markdown/Text') },
  { id: 'e-rag-config', source: 'rag', target: 'config', ...edgeDefault, animated: false, style: { stroke: '#94a3b8', strokeWidth: 2, strokeDasharray: '5 5' }, ...makeLabel('Reads API Key') },
  { id: 'e-index-kb', source: 'pageindex', target: 'kb', ...edgeDefault, ...makeLabel('Indexes & Ranks Documents') },
  { id: 'e-rag-groq', source: 'rag', target: 'groq', ...edgeDefault, ...makeLabel('Sends Formatted Context & Query'), style: { stroke: '#ec4899', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#ec4899' } },
  { id: 'e-groq-rag', source: 'groq', target: 'rag', ...edgeDefault, ...makeLabel('Returns AI Text'), style: { stroke: '#10b981', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#10b981' }, sourceHandle: 'top', targetHandle: 'bottom' }
];

const nodeTypes = { custom: CustomNode };

export default function SystemArchitecture() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div style={{ width: '100%', height: '800px', background: 'rgba(0,0,0,0.3)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)', overflow: 'hidden' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}
        fitView
        minZoom={0.2}
        className="dark" /* ensure dark mode classes if available */
        style={{ background: '#0f172a' }} // tailwind slate-900 background for the canvas
      >
        <Background color="#334155" gap={20} size={1} />
        <Controls />
        <MiniMap 
          nodeColor={(node) => {
            if (node.type === 'group') return 'rgba(255,255,255,0.05)';
            return '#6366f1';
          }}
          maskColor="rgba(0,0,0,0.7)"
          style={{ background: '#1e293b' }}
        />
      </ReactFlow>
    </div>
  );
}
