import { motion } from 'framer-motion';
import { FiMail, FiLinkedin, FiGithub, FiTwitter, FiMapPin, FiClock } from 'react-icons/fi';

const p = { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0, transition: { duration: 0.4 } }, exit: { opacity: 0 } };

const contacts = [
  { icon: <FiMail />, label: 'Email', value: 'chandrashekarrobbi789@gmail.com', href: 'mailto:chandrashekarrobbi789@gmail.com' },
  { icon: <FiLinkedin />, label: 'LinkedIn', value: 'linkedin.com/in/ChandrashekharRobbi', href: 'https://linkedin.com/in/ChandrashekharRobbi' },
  { icon: <FiGithub />, label: 'GitHub', value: 'github.com/ChandrashekharRobbi', href: 'https://github.com/ChandrashekharRobbi' },
  { icon: <FiTwitter />, label: 'Twitter (X)', value: '@Robbi_Chandra20', href: 'https://twitter.com/Robbi_Chandra20' },
  { icon: <FiMapPin />, label: 'Location', value: 'Thane, Maharashtra, India', href: null },
  { icon: <FiClock />, label: 'Notice Period', value: '30 Days', href: null },
];

export default function ContactPage() {
  return (
    <motion.div {...p}>
      <div className="page-header">
        <h1>📧 Contact</h1>
        <p>Get in touch — open to opportunities</p>
      </div>

      <div className="card card-accent" style={{ marginBottom: 30 }}>
        <h3>Professional Availability</h3>
        <p>Actively open to <strong>Python Developer</strong>, <strong>GenAI Engineer</strong>, and <strong>Agentic AI</strong> roles.
          Interested in service-based and product-based organizations.</p>
      </div>

      {contacts.map((c, i) => (
        <motion.div key={c.label} initial={{ opacity: 0, x: -15 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}>
          {c.href ? (
            <a href={c.href} target="_blank" rel="noreferrer" style={{ textDecoration: 'none' }}>
              <div className="contact-item">
                <div className="contact-icon">{c.icon}</div>
                <div>
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 2 }}>{c.label}</div>
                  <div style={{ color: 'var(--text-primary)', fontWeight: 500, fontSize: 14 }}>{c.value}</div>
                </div>
              </div>
            </a>
          ) : (
            <div className="contact-item">
              <div className="contact-icon">{c.icon}</div>
              <div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 2 }}>{c.label}</div>
                <div style={{ color: 'var(--text-primary)', fontWeight: 500, fontSize: 14 }}>{c.value}</div>
              </div>
            </div>
          )}
        </motion.div>
      ))}
    </motion.div>
  );
}
