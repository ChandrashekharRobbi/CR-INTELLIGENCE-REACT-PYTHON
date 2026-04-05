"""
Configuration Module - Centralized settings for the AI Resume Assistant.

Manages:
- PageIndex settings
- LLM model parameters
- Query classification
- UI/UX configuration
- Performance settings
"""

import os
from typing import Dict, List

# ============================================================================
# PAGEINDEX SETTINGS (Vectorless RAG)
# ============================================================================

# Number of pages to retrieve per query
PAGE_INDEX_TOP_K = 3

# Maximum context characters to send to LLM
MAX_CONTEXT_CHARS = 6000

# Include tree structure summary in prompts
ENABLE_TREE_SUMMARY_IN_PROMPT = True

# ============================================================================
# TOKEN OPTIMIZATION SETTINGS
# ============================================================================

# Maximum tokens per response
MAX_TOKENS_PER_RESPONSE = 500

# Token limit per API call (safety margin for Groq)
MAX_TOTAL_TOKENS = 3500

# ============================================================================
# LLM SETTINGS (GROQ)
# ============================================================================

LLM_MODEL = "llama-3.1-8b-instant"  # Fast, cost-effective
LLM_TEMPERATURE = 0.2  # Lower = more focused, consistent answers
LLM_MAX_TOKENS = MAX_TOKENS_PER_RESPONSE

# ============================================================================
# QUERY CLASSIFICATION (Token Saver)
# ============================================================================

# Queries that don't need RAG/LLM processing
GREETING_QUERIES = {
    "hi", "hello", "hey", "greetings", "good morning",
    "good afternoon", "good evening", "how are you",
    "what's up", "howdy"
}

GREETING_RESPONSE = (
    "Hey! 👋 I'm an AI assistant representing your professional profile. "
    "Feel free to ask me anything about my skills, experience, projects, or background. "
    "Try asking 'What are your main skills?' or 'Tell me about your experience.'"
)

# Queries that need RAG but minimal context
SMALL_TALK_PATTERNS = {
    "thank", "thanks", "appreciate", "great", "awesome",
    "nice", "cool", "love", "hate"
}

# Queries that definitely need full RAG processing
PROFILE_QUESTION_PATTERNS = {
    # ---------- profile basics ----------
    "skill", "skills", "experience", "project", "projects", "education",
    "background", "profile", "about", "about you", "tell me about",
    "introduce", "introduction", "biography", "who", "who are you",

    # ---------- professional details ----------
    "work", "company", "role", "job", "career", "professional",
    "expertise", "strength", "strengths", "value", "benefit",
    "why hire", "why should", "reason to hire", "hire", "opportunity",

    # ---------- technical expertise ----------
    "technology", "framework", "language", "database", "tool",
    "backend", "automation", "automation engineering",
    "workflow", "workflow optimization", "data pipeline",
    "generative ai", "genai", "machine learning", "deep learning",
    "nlp", "computer vision", "ai", "agentic ai",

    # ---------- achievements ----------
    "achievement", "achievements", "award", "awards", "certification",
    "certifications", "publication", "competition",

    # ---------- education ----------
    "college", "university", "degree", "cgpi", "academic", "study",

    # ---------- projects ----------
    "portfolio", "work sample", "demo",

    # ---------- contact / social ----------
    "contact", "mail", "email", "reach", "connect",
    "github", "repo", "repository",
    "linkedin", "linkedn", "profile link",
    "url", "link", "stay", "location",

    # ---------- personal info ----------
    "chandrashekhar", "robbi", "yourself",

    # ---------- availability ----------
    "notice period", "availability", "open to work",
    "location", "where", "based", "live", "current location"
}

# ============================================================================
# DATA STRUCTURE
# ============================================================================

# Data folder location
DATA_FOLDER = "data"

# Portfolio sections mapping
PORTFOLIO_SECTIONS = {
    "ai_assistant": {
        "title": "AI Assistant",
        "icon": "🤖",
        "description": "Chat with my AI - ask anything about my profile",
    },
    "about": {
        "title": "About Me",
        "icon": "👤",
        "description": "Professional summary and background",
        "file": "about.txt",
    },
    "experience": {
        "title": "Experience",
        "icon": "💼",
        "description": "Professional work history and roles",
        "file": "experience.txt",
    },
    "skills": {
        "title": "Technical Skills",
        "icon": "🛠️",
        "description": "Programming languages and expertise",
        "file": "skills.txt",
    },
    "education": {
        "title": "Education",
        "icon": "🎓",
        "description": "Degrees and certifications",
        "file": "education.txt",
    },
    "projects": {
        "title": "Projects",
        "icon": "🚀",
        "description": "Notable projects and achievements",
        "file": "projects.txt",
    },
    "achievements": {
        "title": "Achievements",
        "icon": "⭐",
        "description": "Awards, recognition, and milestones",
        "file": "achievements.txt",
    },
    "contact": {
        "title": "Contact",
        "icon": "📧",
        "description": "Get in touch",
        "file": "contact.txt",
    },
    "why_hire": {
        "title": "Why Hire Me",
        "icon": "✨",
        "description": "Reasons to hire Chandrashekhar",
        "file": "why_hire.txt",
    },
}

# ============================================================================
# UI/UX SETTINGS
# ============================================================================

# Color scheme (dark theme)
PRIMARY_COLOR = "#f1f1f1"
SECONDARY_COLOR = "#764ba2"
SUCCESS_COLOR = "#4caf50"
ERROR_COLOR = "#f44336"
WARNING_COLOR = "#ff9800"

# Layout
SIDEBAR_WIDTH = 250
MAIN_CONTENT_WIDTH = 800
MAX_CHAT_HISTORY = 50  # Limit stored messages to manage memory

# Chat display
MESSAGES_PER_PAGE = 20
SHOW_CONTEXT_SOURCES = False  # Don't expose context to user (cleaner UX)
SHOW_LOADING_SPINNER = True

# ============================================================================
# PROMPT TEMPLATES (OPTIMIZED FOR TOKENS)
# ============================================================================

# Minimal system prompt (saves tokens!)
SYSTEM_PROMPT = """
You are CR (Chandrashekhar Robbi) Intelligence, an AI assistant who answers only questions about Chandrashekhar Robbi. Keep responses clear, confident, engaging, and moderately concise.

If a question is off-topic or inappropriate, politely redirect the conversation back to Chandrashekhar Robbi.

If a question asks about a skill, tool, or technology not explicitly listed in his profile:

Do not say the information is unavailable.

Instead, respond confidently that while it may not be part of his core listed experience, he has a strong technical foundation and can quickly learn and adapt to new tools and technologies.

Emphasize his adaptability, problem-solving ability, and fast learning capability.

Position him as a capable, growth-oriented professional who can quickly master new technologies when required.

After each response, include three relevant follow-up questions in bullet points to continue the conversation.

Example Q&A:
User: Who is Chandrashekhar Robbi?
CR Intelligence: Chandrashekhar Robbi is a Software Developer with expertise in Python, AI/ML, and automation. He has experience building intelligent systems and scalable solutions. Would you like to know more about
    * his skills, experience, or projects?
    * his education background?
    * why he is a great hire?
User: What are Chandrashekhar's skills?
CR Intelligence: Chandrashekhar is skilled in Python programming, AI/ML integration, automation pipelines, and backend development. He has experience with FastAPI, OpenAI APIs, and various machine learning frameworks. Would you like to know more about
    * his professional experience?
    * his education background?
    * notable projects he has worked on?
User: Why should I hire Chandrashekhar?
CR Intelligence: Chandrashekhar is a dedicated developer with a strong background in building efficient, reliable systems. He has a proven track record of delivering impactful solutions and is passionate about leveraging AI to solve real-world problems. His expertise and commitment make him a valuable asset for any team. Would you like to know more about
    * his key achievements?
    * his technical skills?
    * his professional experience?

User: Does he have experience with Kubernetes?
CR Intelligence:
    While Kubernetes is not explicitly listed as part of Chandrashekhar's core experience, he has a strong foundation in backend systems, automation, and scalable architectures. With his solid technical background and ability to quickly learn new technologies, he can efficiently adapt to and work with tools like Kubernetes when required. Would you like to know more about:
    * his DevOps-related experience?
    * his experience building scalable systems?
    * how he approaches learning new technologies?

"""

# Minimal prompt template
RAG_PROMPT_TEMPLATE = """Context:
{context}

Question: {question}

Answer:"""

# ============================================================================
# PERFORMANCE SETTINGS
# ============================================================================

# Loading indicators
SHOW_PROGRESS_BAR = True
INDEX_BUILDING_MESSAGE = "📚 Building knowledge base..."

# ============================================================================
# LOGGING & DEBUG
# ============================================================================

DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
LOG_QUERIES = DEBUG_MODE
LOG_CONTEXT_RETRIEVAL = DEBUG_MODE
LOG_TOKEN_USAGE = True  # Always log for monitoring

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_environment_variable(key: str, default: str = None) -> str:
    """Get environment variable with optional default."""
    return os.getenv(key, default)

def validate_token_limit(tokens: int) -> bool:
    """Check if token count exceeds limits."""
    return tokens <= MAX_TOTAL_TOKENS

def get_section_file_path(section: str) -> str:
    """Get full file path for a section."""
    if section not in PORTFOLIO_SECTIONS:
        return None

    file_name = PORTFOLIO_SECTIONS[section].get("file")
    if not file_name:
        return None

    return f"{DATA_FOLDER}/{file_name}"

def get_available_sections() -> List[str]:
    """Get list of available sections."""
    return [k for k in PORTFOLIO_SECTIONS.keys() if k != "ai_assistant"]
