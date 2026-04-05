import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
  startOnLoad: true,
  theme: 'dark',
  securityLevel: 'loose',
  flowchart: {
    useMaxWidth: true,
    htmlLabels: true
  }
});

export default function Mermaid({ chart }) {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) {
      ref.current.removeAttribute('data-processed');
      mermaid.contentLoaded();
    }
  }, [chart]);

  return <div className="mermaid" ref={ref}>{chart}</div>;
}
