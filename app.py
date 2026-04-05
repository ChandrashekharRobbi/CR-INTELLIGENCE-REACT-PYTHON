"""
AI Resume Portfolio - Multi-Page Application
Powered by Vectorless PageIndex RAG Pipeline
"""

import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from rag_pipeline import RAGPipeline
from Sections.experience import page_experience
from Sections.about_me import page_about
from Sections.skills import page_skills
from Sections.education import page_education
from Sections.projects import page_projects
from Sections.achievements import page_achievements
from Sections.resume import page_resume
from Sections.contact import page_contact
from Sections.architecture import page_architecture


def get_secret(key):
    return os.getenv(key) or st.secrets.get(key) 
# Load environment variables
load_dotenv()

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Chandrashekhar Robbi's Portfolio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="auto",
)

# ---------- PREMIUM DARK THEME CSS ----------
st.markdown("""
<style>
    /* ============================================
       GOOGLE FONTS
       ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ============================================
       GLOBAL STYLES
       ============================================ */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background: #0a0a14;
    }

    /* ============================================
       SIDEBAR STYLING
       ============================================ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1e 0%, #12122a 50%, #0f0f1e 100%) !important;
        border-right: 1px solid rgba(124, 58, 237, 0.15);
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #c4b5fd;
    }

    /* Sidebar nav item styling */
    .nav-link {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        border-radius: 10px !important;
        margin: 2px 0 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .nav-link:hover {
        background: rgba(124, 58, 237, 0.15) !important;
        transform: translateX(4px);
    }

    .nav-link-selected {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.4) !important;
        font-weight: 600 !important;
    }

    /* ============================================
       SCROLLBAR
       ============================================ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a14;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(124, 58, 237, 0.3);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(124, 58, 237, 0.5);
    }

    /* ============================================
       BUTTONS — GLOBAL OVERRIDE
       ============================================ */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        background: rgba(124, 58, 237, 0.08) !important;
        color: #c4b5fd !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
    }

    .stButton > button:hover {
        background: rgba(124, 58, 237, 0.2) !important;
        border-color: #7c3aed !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.25) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ============================================
       CHAT MESSAGES
       ============================================ */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 16px 20px !important;
        margin-bottom: 12px !important;
        border: 1px solid rgba(124, 58, 237, 0.1) !important;
        animation: messageSlide 0.4s ease-out !important;
    }

    /* User messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(59, 130, 246, 0.06) !important;
        border: 1px solid rgba(59, 130, 246, 0.15) !important;
        border-left: 3px solid #3b82f6 !important;
    }

    /* Assistant messages */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(124, 58, 237, 0.06) !important;
        border: 1px solid rgba(124, 58, 237, 0.15) !important;
        border-left: 3px solid #7c3aed !important;
    }

    /* Chat input */
    .stChatInput {
        border-radius: 16px !important;
    }

    .stChatInput > div {
        border-radius: 16px !important;
        border: 1px solid rgba(124, 58, 237, 0.3) !important;
        background: rgba(15, 15, 30, 0.8) !important;
        backdrop-filter: blur(10px) !important;
    }

    .stChatInput textarea {
        font-family: 'Inter', sans-serif !important;
        color: #e2e8f0 !important;
    }

    /* ============================================
       ANIMATIONS
       ============================================ */
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes pulse-glow {
        0%, 100% { box-shadow: 0 0 20px rgba(124, 58, 237, 0.15); }
        50% { box-shadow: 0 0 40px rgba(124, 58, 237, 0.3); }
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }

    /* ============================================
       EXPANDERS
       ============================================ */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        background: rgba(124, 58, 237, 0.05) !important;
        border-radius: 12px !important;
    }

    /* ============================================
       DIVIDERS
       ============================================ */
    hr {
        border-color: rgba(124, 58, 237, 0.15) !important;
    }

    /* ============================================
       LINKS
       ============================================ */
    a {
        color: #a78bfa !important;
        text-decoration: none !important;
        transition: color 0.2s ease !important;
    }
    a:hover {
        color: #c4b5fd !important;
        text-decoration: underline !important;
    }

    /* ============================================
       HEADINGS
       ============================================ */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }

    h1 {
        color: #f1f5f9 !important;
    }

    h2 {
        color: #e2e8f0 !important;
    }

    h3 {
        color: #cbd5e1 !important;
    }

    /* ============================================
       METRICS & CONTAINERS
       ============================================ */
    [data-testid="stMetric"] {
        background: rgba(124, 58, 237, 0.05);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 12px;
        padding: 16px;
    }

    /* ============================================
       CODE BLOCKS
       ============================================ */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background: rgba(124, 58, 237, 0.1) !important;
        color: #c4b5fd !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }

    pre {
        background: rgba(15, 15, 30, 0.9) !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------- INITIALIZE RAG PIPELINE ----------
@st.cache_resource
def initialize_rag_pipeline():
    """Initialize RAG pipeline with caching."""
    groq_api_key = get_secret("GROQ_API_KEY")
    
    if not groq_api_key:
        st.error("GROQ_API_KEY not found in environment variables")
        st.info("""
        **Setup Instructions:**
        1. Create a `.env` file in the project root
        2. Add: `GROQ_API_KEY=your_api_key_here`
        3. Get free API key from: https://console.groq.com
        """)
        return None
    
    try:
        pipeline = RAGPipeline(groq_api_key)
        pipeline.load_knowledge_base("data")
        return pipeline
    
    except Exception as e:
        st.error(f"Error initializing RAG pipeline: {str(e)}")
        return None


# ---------- SIDEBAR NAVIGATION ----------
with st.sidebar:
    # Profile card
    st.markdown("""
        <div style="
            text-align: center;
            padding: 25px 15px 20px;
            margin-bottom: 10px;
        ">
            <div style="
                width: 80px; height: 80px;
                border-radius: 50%;
                background: linear-gradient(135deg, #7c3aed, #6d28d9, #4f46e5);
                margin: 0 auto 15px;
                display: flex; align-items: center; justify-content: center;
                font-size: 36px;
                box-shadow: 0 8px 30px rgba(124, 58, 237, 0.4);
                animation: pulse-glow 3s ease-in-out infinite;
            ">
                <span>CR</span>
            </div>
            <h3 style="
                margin: 0; font-size: 18px; font-weight: 700;
                color: #f1f5f9;
                font-family: 'Inter', sans-serif;
            ">Chandrashekhar Robbi</h3>
            <p style="
                margin: 4px 0 0; font-size: 13px;
                color: #a78bfa; font-weight: 500;
                font-family: 'Inter', sans-serif;
            ">Python Developer &bull; GenAI Engineer</p>
            <div style="
                margin-top: 10px;
                display: inline-block;
                padding: 3px 12px;
                border-radius: 20px;
                background: rgba(34, 197, 94, 0.15);
                border: 1px solid rgba(34, 197, 94, 0.3);
                font-size: 11px;
                color: #4ade80;
                font-weight: 600;
            ">&#9679; Open to Work</div>
        </div>
    """, unsafe_allow_html=True)

    choose = option_menu(
        "",
        [
            "AI Assistant",
            "About Me",
            "Experience",
            "Technical Skills",
            "Education",
            "Projects",
            "Achievements",
            "Resume",
            "Contact",
            "Architecture",
        ],
        icons=[
            "robot",
            "person-fill",
            "briefcase-fill",
            "tools",
            "book-fill",
            "kanban-fill",
            "trophy-fill",
            "file-earmark-person",
            "envelope-fill",
            "diagram-3-fill",
        ],
        menu_icon="",
        default_index=0,
        styles={
            "container": {"padding": "0 !important", "background-color": "transparent"},
            "icon": {"color": "#a78bfa", "font-size": "15px"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "2px 0",
                "padding": "10px 15px",
                "border-radius": "10px",
                "color": "#94a3b8",
                "background-color": "transparent",
                "--hover-color": "rgba(124, 58, 237, 0.1)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)",
                "color": "white",
                "font-weight": "600",
                "box-shadow": "0 4px 15px rgba(124, 58, 237, 0.4)",
            },
        },
    )

    # Social icons
    st.markdown("""
        <div style='text-align: center; margin-top: 20px; padding: 15px 0;'>
            <a href='https://linkedin.com/in/chandrashekharrobbi' target='_blank'
               style="display: inline-block; width: 38px; height: 38px; line-height: 38px;
                      border-radius: 10px; text-align: center; margin: 0 6px;
                      background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);
                      text-decoration: none !important; transition: all 0.3s ease;">
                <img src='https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png' width='18' style="vertical-align: middle; opacity: 0.8;">
            </a>
            <a href='https://github.com/ChandrashekharRobbi' target='_blank'
               style="display: inline-block; width: 38px; height: 38px; line-height: 38px;
                      border-radius: 10px; text-align: center; margin: 0 6px;
                      background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);
                      text-decoration: none !important; transition: all 0.3s ease;">
                <img src='https://cdn-icons-png.flaticon.com/128/25/25657.png' width='18' style="vertical-align: middle; opacity: 0.8; filter: invert(0.7);">
            </a>
            <a href='mailto:chandrashekarrobbi789@gmail.com'
               style="display: inline-block; width: 38px; height: 38px; line-height: 38px;
                      border-radius: 10px; text-align: center; margin: 0 6px;
                      background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);
                      text-decoration: none !important; transition: all 0.3s ease;">
                <img src='https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png' width='18' style="vertical-align: middle; opacity: 0.8;">
            </a>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style='text-align: center; font-size: 11px; color: #4a5568;
                    padding: 15px 0 10px; margin-top: 10px;
                    border-top: 1px solid rgba(124, 58, 237, 0.1);
                    line-height: 1.6;'>
            Powered by <span style="color: #7c3aed; font-weight: 600;">PageIndex RAG</span><br>
            &copy; 2026 Chandrashekhar Robbi
        </div>
    """, unsafe_allow_html=True)


# ---------- LOAD PAGE CONTENT ----------
def load_content(section: str) -> str:
    """Load content from data files."""
    file_mapping = {
        "about": "about.txt",
        "experience": "experience.txt",
        "skills": "skills.txt",
        "education": "education.txt",
        "projects": "projects.txt",
        "achievements": "achievements.txt",
        "resume": "resume.txt",
        "contact": "contact.txt",
    }
    
    file_path = f"data/{file_mapping.get(section, 'about.txt')}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Content file not found: {file_path}"


# ---------- PAGE: AI ASSISTANT ----------
def page_ai_assistant():
    """Premium AI Chat page with glassmorphism design"""

    if pipeline is None:
        st.error("RAG Pipeline not initialized")
        return

    # ---------- HERO SECTION ----------
    st.markdown("""
    <div style="
        padding: 40px 45px;
        border-radius: 20px;
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 30%, #4c1d95 60%, #581c87 100%);
        color: white;
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(124, 58, 237, 0.2);
    ">
        <div style="
            position: absolute; top: -50px; right: -50px;
            width: 250px; height: 250px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(124, 58, 237, 0.35), transparent 70%);
        "></div>
        <div style="
            position: absolute; bottom: -40px; left: -30px;
            width: 180px; height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.25), transparent 70%);
        "></div>
        <div style="position: relative; z-index: 1;">
            <h1 style="margin: 0 0 8px 0; font-size: 34px; font-weight: 800; color: #f1f5f9; font-family: Inter, sans-serif;">
                CR Intelligence
            </h1>
            <p style="margin: 0 0 4px 0; font-size: 13px; color: #a5b4fc; font-weight: 600; letter-spacing: 2px; text-transform: uppercase;">
                Vectorless PageIndex RAG
            </p>
            <p style="font-size: 16px; color: #c7d2fe; line-height: 1.6; margin: 15px 0 0 0; max-width: 700px;">
                AI-powered interactive resume assistant. Ask anything about experience, projects,
                skills, or background &#8212; powered by hierarchical document intelligence.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # --------- Helper Function ----------
    def process_user_query(query):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": query
        })
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = pipeline.query(query, top_k=3)

                if response["status"] == "success":
                    answer = response["answer"]
                else:
                    answer = f"Error: {response['answer']}"

                st.markdown(answer)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

    # --------- Display Chat History ----------
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --------- Suggested Prompts ----------
    if not st.session_state.messages:
        st.markdown("""
        <div style="
            text-align: center; margin: 10px 0 25px;
            animation: fadeInUp 0.8s ease-out 0.2s both;
        ">
            <p style="color: #64748b; font-size: 14px; font-weight: 500;
                      letter-spacing: 1px; text-transform: uppercase;">
                Explore topics
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Row 1
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👤  Who is Chandrashekhar?", key="q1", use_container_width=True):
                process_user_query("Tell me about Chandrashekhar Robbi")
                st.rerun()
        with col2:
            if st.button("🚀  Show Projects", key="q2", use_container_width=True):
                process_user_query("Tell me about your key projects")
                st.rerun()
        with col3:
            if st.button("⚡  Automation Work", key="q3", use_container_width=True):
                process_user_query("Tell me about your automation projects")
                st.rerun()

        # Row 2
        col4, col5, col6 = st.columns(3)
        with col4:
            if st.button("🛠️  Technical Skills", key="q4", use_container_width=True):
                process_user_query("What are your main skills?")
                st.rerun()
        with col5:
            if st.button("🏆  Achievements", key="q5", use_container_width=True):
                process_user_query("What are your biggest achievements?")
                st.rerun()
        with col6:
            if st.button("🏗️  Architecture", key="q6", use_container_width=True):
                process_user_query("Explain your system architecture and technical design approach")
                st.rerun()

        # Row 3
        col7, col8, col9 = st.columns(3)
        with col7:
            if st.button("💼  Latest Experience", key="q7", use_container_width=True):
                process_user_query("Tell me about your latest role and experience")
                st.rerun()
        with col8:
            if st.button("🤖  AI & ML Work", key="q8", use_container_width=True):
                process_user_query("Explain your AI and machine learning work")
                st.rerun()
        with col9:
            if st.button("✨  Why Hire CR?", key="q9", use_container_width=True):
                process_user_query("Why should a company hire Chandrashekhar Robbi?")
                st.rerun()

    else:
        # Chat controls when messages exist
        st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
        col_clear, col_spacer = st.columns([1, 3])
        with col_clear:
            if st.button("🗑️  Clear Chat", key="clear_chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

    # --------- Chat Input ----------
    user_input = st.chat_input("Ask me anything about Chandrashekhar...")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        process_user_query(user_input)
        st.rerun()


# ---------- HANDLE PAGE NAVIGATION ----------
if "navigate" in st.session_state:
    choose = st.session_state.navigate
    del st.session_state.navigate

# Initialize pipeline
pipeline = initialize_rag_pipeline()


# ---------- PAGE ROUTING ----------
page_functions = {
    "AI Assistant": page_ai_assistant,
    "About Me": page_about,
    "Experience": page_experience,
    "Technical Skills": page_skills,
    "Education": page_education,
    "Projects": page_projects,
    "Achievements": page_achievements,
    "Resume": page_resume,
    "Contact": page_contact,
    "Architecture": page_architecture,
}

page_function = page_functions.get(choose, page_ai_assistant)
page_function()
