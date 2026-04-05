import { useState, useRef, useEffect, useMemo } from 'react';
import { motion } from 'framer-motion';
import { FiSend, FiTrash2, FiArrowRight } from 'react-icons/fi';
import { sendChat } from '../api';
import ReactMarkdown from 'react-markdown';

const suggestions = [
  { icon: '👤', title: 'Who is Chandrashekhar?', desc: 'Background, role, and career summary', query: 'Tell me about Chandrashekhar Robbi' },
  { icon: '🚀', title: 'Key Projects', desc: 'AI apps, automation tools, deep learning', query: 'Tell me about your key projects' },
  { icon: '⚡', title: 'Automation Impact', desc: '50-90% workflow optimization at eClerx', query: 'Tell me about your automation projects and their impact' },
  { icon: '🧠', title: 'AI & GenAI Work', desc: 'RAG systems, LLMs, NLP pipelines', query: 'Explain your AI and Generative AI work in detail' },
  { icon: '🏆', title: 'Awards & Achievements', desc: 'Super Achiever, Appreciation Award', query: 'What awards and achievements does Chandrashekhar have?' },
  { icon: '✨', title: 'Why Hire CR?', desc: 'Value proposition & differentiators', query: 'Why should a company hire Chandrashekhar Robbi?' },
];

/**
 * Extract follow-up questions from the AI response.
 * Looks for bullet points that end with "?" — these are the LLM's suggested follow-ups.
 * Returns { cleanedContent, followUps }
 */
function extractFollowUps(content) {
  const lines = content.split('\n');
  const followUps = [];
  const cleanedLines = [];
  let foundTrailingQuestions = false;
  let introLineRemoved = false;

  // First pass: find trailing bullet-point questions
  // Walk backwards to find the trailing block of "?" bullets
  let trailingStart = -1;
  for (let i = lines.length - 1; i >= 0; i--) {
    const trimmed = lines[i].trim();
    if (!trimmed) continue; // skip blank lines
    // Check if it's a bullet point ending with ?
    if (/^[-*•]\s+.+\?$/.test(trimmed) || /^\d+\.\s+.+\?$/.test(trimmed)) {
      trailingStart = i;
    } else {
      break;
    }
  }

  if (trailingStart !== -1) {
    for (let i = 0; i < lines.length; i++) {
      const trimmed = lines[i].trim();

      if (i >= trailingStart) {
        // Extract the question text from the bullet
        const match = trimmed.match(/^[-*•]\s+(.+)$/) || trimmed.match(/^\d+\.\s+(.+)$/);
        if (match) {
          followUps.push(match[1].trim());
          foundTrailingQuestions = true;
          continue;
        }
      }

      // Remove the intro line like "Would you like to know more about:" right before the bullets
      if (i === trailingStart - 1 || (i === trailingStart - 2 && !lines[trailingStart - 1].trim())) {
        const lower = trimmed.toLowerCase();
        
        // Match common intro phrases and everything after them
        const match = trimmed.match(/(would you like to know|want to know more|like to explore|interested in learning|want me to|shall i).*$/i);
        
        if (match) {
          introLineRemoved = true;
          // Only strip the matched intro phrase, keep the rest of the answer
          const strippedLine = trimmed.replace(match[0], '').trim();
          if (strippedLine) {
            cleanedLines.push(strippedLine);
          }
          continue;
        }
      }

      cleanedLines.push(lines[i]);
    }
  }

  if (!foundTrailingQuestions) {
    return { cleanedContent: content, followUps: [] };
  }

  // Trim trailing blank lines from cleaned content
  let cleaned = cleanedLines.join('\n').replace(/\n{3,}/g, '\n\n').trimEnd();
  
  if (!cleaned) {
    cleaned = "Here are some specific areas you can explore next:";
  }
  
  return { cleanedContent: cleaned, followUps };
}

const pageMotion = {
  initial: { opacity: 0 },
  animate: { opacity: 1, transition: { duration: 0.3 } },
  exit: { opacity: 0, transition: { duration: 0.15 } },
};

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  useEffect(scrollToBottom, [messages, loading]);

  const handleSend = async (query) => {
    const q = query || input.trim();
    if (!q || loading) return;
    setInput('');

    const userMsg = { role: 'user', content: q };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      const res = await sendChat(q);
      setMessages(prev => [...prev, { role: 'assistant', content: res.answer }]);
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Something went wrong. Please try again.' }]);
    }

    setLoading(false);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Process messages to extract follow-ups from each assistant message
  const processedMessages = useMemo(() => {
    return messages.map((msg, i) => {
      if (msg.role === 'assistant') {
        const { cleanedContent, followUps } = extractFollowUps(msg.content);
        return { ...msg, displayContent: cleanedContent, followUps };
      }
      return { ...msg, displayContent: msg.content, followUps: [] };
    });
  }, [messages]);

  return (
    <motion.div {...pageMotion} className="chat-page">
      {messages.length === 0 ? (
        /* ===== WELCOME STATE ===== */
        <div className="welcome-section">
          <div className="welcome-header">
            <div className="welcome-icon">🧠</div>
            <h1>Ask me anything</h1>
            <p>
              I know everything about Chandrashekhar's experience, projects, skills, and achievements.
              Powered by Vectorless PageIndex RAG.
            </p>
          </div>

          <div className="suggestion-cards">
            {suggestions.map((s, i) => (
              <motion.button
                key={i}
                className="suggestion-card"
                onClick={() => handleSend(s.query)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.07, duration: 0.4 }}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <span className="card-icon">{s.icon}</span>
                <span className="card-title">{s.title}</span>
                <span className="card-desc">{s.desc}</span>
              </motion.button>
            ))}
          </div>
        </div>
      ) : (
        /* ===== CHAT STATE ===== */
        <div className="chat-active">
          <div className="chat-messages-list">
            {processedMessages.map((msg, i) => (
              <div key={i} className="message-group">
                {msg.role === 'user' ? (
                  <motion.div className="msg-user" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
                    <div className="msg-user-bubble">{msg.displayContent}</div>
                  </motion.div>
                ) : (
                  <motion.div className="msg-assistant" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
                    <div className="msg-ai-avatar">CR</div>
                    <div className="msg-ai-content">
                      <div className="msg-ai-bubble">
                        <ReactMarkdown>{msg.displayContent}</ReactMarkdown>
                      </div>
                      {/* Follow-up pills from the AI's own suggestions */}
                      {i === processedMessages.length - 1 && !loading && msg.followUps.length > 0 && (
                        <div className="followup-pills">
                          {msg.followUps.map((q, j) => (
                            <motion.button
                              key={j}
                              className="followup-pill"
                              onClick={() => handleSend(q)}
                              initial={{ opacity: 0, scale: 0.9 }}
                              animate={{ opacity: 1, scale: 1 }}
                              transition={{ delay: 0.3 + j * 0.1 }}
                              whileHover={{ scale: 1.04 }}
                              whileTap={{ scale: 0.96 }}
                            >
                              <FiArrowRight size={12} /> {q}
                            </motion.button>
                          ))}
                        </div>
                      )}
                    </div>
                  </motion.div>
                )}
              </div>
            ))}

            {loading && (
              <div className="typing-wrapper">
                <div className="msg-ai-avatar">CR</div>
                <div className="typing-bubble">
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                  <div className="typing-dot" />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>
      )}

      {/* ===== INPUT AREA ===== */}
      <div className="chat-input-area">
        {messages.length > 0 && (
          <div className="chat-controls">
            <button className="clear-chat-btn" onClick={() => setMessages([])}>
              <FiTrash2 size={12} /> New conversation
            </button>
          </div>
        )}
        <div className="chat-input-box">
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about experience, projects, skills..."
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={() => handleSend()}
            disabled={!input.trim() || loading}
          >
            <FiSend />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
