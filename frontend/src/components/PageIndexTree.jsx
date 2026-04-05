import React, { useMemo } from 'react';
import { ReactFlow, Background, MarkerType, Handle, Position, Controls, MiniMap } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const treeData = [
  {
    id: 'root',
    name: 'Portfolio (Root)',
    type: 'root',
    children: [
      {
        id: 'about',
        name: 'About Me',
        type: 'folder',
        children: [
          { id: 'about-1', name: 'Professional Summary', type: 'file' },
          { id: 'about-2', name: 'Career Objectives', type: 'file' },
          { id: 'about-3', name: 'Technical Expertise', type: 'file' },
        ],
      },
      {
        id: 'experience',
        name: 'Experience',
        type: 'folder',
        children: [
          { id: 'exp-1', name: 'eClerx — Analyst', type: 'file' },
          { id: 'exp-2', name: 'Qodeit — Intern', type: 'file' },
          { id: 'exp-3', name: 'Teaching Experience', type: 'file' },
        ],
      },
      {
        id: 'skills',
        name: 'Skills',
        type: 'folder',
        children: [
          { id: 'skill-1', name: 'Programming Languages', type: 'file' },
          { id: 'skill-2', name: 'Backend Development', type: 'file' },
          { id: 'skill-3', name: 'AI & Machine Learning', type: 'file' },
          { id: 'skill-4', name: 'Automation Engineering', type: 'file' },
        ],
      },
      {
        id: 'education',
        name: 'Education',
        type: 'folder',
        children: [
          { id: 'edu-1', name: 'B.E. Computer Science (AIML)', type: 'file' },
        ],
      },
      {
        id: 'projects',
        name: 'Projects',
        type: 'folder',
        children: [
          { id: 'proj-1', name: 'Paddy Doctor / LipNet', type: 'file' },
          { id: 'proj-2', name: 'AI Resume Portfolio', type: 'file' },
          { id: 'proj-3', name: 'Automation Tools', type: 'file' },
        ],
      },
      {
        id: 'achievements',
        name: 'Achievements',
        type: 'folder',
        children: [
          { id: 'achv-1', name: 'Awards & Recognition', type: 'file' },
          { id: 'achv-2', name: 'Certifications', type: 'file' },
        ],
      },
      { id: 'contact', name: 'Contact', type: 'folder', children: [] },
      { id: 'why_hire', name: 'Why Hire', type: 'folder', children: [] },
      { id: 'resume', name: 'Resume', type: 'folder', children: [] },
    ],
  },
];

const CustomTreeNode = ({ data }) => {
  const getTheme = () => {
    if (data.type === 'root') return { bg: 'rgba(139,92,246,0.15)', border: '#8b5cf6', color: '#fff', icon: '🌳' };
    if (data.type === 'folder') return { bg: 'rgba(56,189,248,0.15)', border: '#38bdf8', color: '#e0f2fe', icon: '📁' };
    return { bg: 'rgba(16,185,129,0.15)', border: '#10b981', color: '#d1fae5', icon: '📑' };
  };
  const theme = getTheme();
  
  return (
    <div style={{
      background: theme.bg,
      border: `1px solid ${theme.border}`,
      borderRadius: '8px',
      padding: '8px 14px',
      color: theme.color,
      display: 'flex',
      alignItems: 'center',
      gap: '10px',
      fontSize: '13px',
      fontWeight: '600',
      whiteSpace: 'nowrap',
      boxShadow: '0 4px 10px rgba(0,0,0,0.5)',
      backdropFilter: 'blur(8px)',
      minWidth: '150px'
    }}>
      {data.type !== 'root' && <Handle type="target" position={Position.Left} style={{ background: theme.border, border: 'none', width: 6, height: 6 }} />}
      <span style={{ fontSize: '16px' }}>{theme.icon}</span>
      <span>{data.label}</span>
      {data.type !== 'file' && <Handle type="source" position={Position.Right} style={{ background: theme.border, border: 'none', width: 6, height: 6 }} />}
    </div>
  );
};

const nodeTypes = { customTree: CustomTreeNode };

function generateLayout(data) {
  let nodes = [];
  let edges = [];
  let yCounter = 0;
  
  const X_SPACING = 300;
  const Y_SPACING = 60;
  
  function traverse(node, depth, parentId) {
      const isLeaf = !node.children || node.children.length === 0;
      let startY = yCounter;
      
      if (!isLeaf) {
          node.children.forEach(child => {
              traverse(child, depth + 1, node.id);
          });
      } else {
          yCounter++;
      }
      
      let endY = yCounter - 1;
      if (endY < startY) endY = startY;
      
      let myY = isLeaf ? startY * Y_SPACING : ((startY + endY) / 2) * Y_SPACING;
      
      nodes.push({
          id: node.id,
          position: { x: depth * X_SPACING, y: myY },
          data: { label: node.name, type: node.type },
          type: 'customTree',
          sourcePosition: 'right',
          targetPosition: 'left'
      });
      
      if (parentId) {
          edges.push({
              id: `e-${parentId}-${node.id}`,
              source: parentId,
              target: node.id,
              type: 'smoothstep',
              animated: true,
              style: { stroke: node.type === 'file' ? 'rgba(16,185,129,0.5)' : 'rgba(56,189,248,0.5)', strokeWidth: 1.5 },
          });
      }
  }
  
  traverse(data[0], 0, null);
  
  return { nodes, edges };
}

export default function PageIndexTree() {
  const { nodes, edges } = useMemo(() => generateLayout(treeData), []);

  return (
    <div style={{ width: '100%', height: '700px', background: 'rgba(0,0,0,0.3)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.05)', overflow: 'hidden' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.2 }}
        minZoom={0.2}
        className="dark"
      >
        <Background color="#334155" gap={20} size={1} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
