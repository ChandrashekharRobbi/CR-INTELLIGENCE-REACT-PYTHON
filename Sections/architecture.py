import streamlit as st
from pathlib import Path


def page_architecture():
    """System Architecture Page — Vectorless PageIndex RAG Portfolio"""

    # ---------- CONFIG ----------
    IMAGE_PATH = Path("img/Architecture.png")

    # ---------- PAGE HEADER ----------
    st.title("🏗️ System Architecture")
    st.caption("Understanding how the Vectorless PageIndex RAG System operates")

    st.divider()

    # ---------- OVERVIEW ----------
    st.markdown(
        """
### 🚀 Overview

This portfolio uses **Vectorless RAG with PageIndex** to deliver intelligent,
context-aware responses about experience, projects, and skills — **without any vector database
or embedding models**.

The system combines:

- ⚡ **Streamlit** → Interactive UI
- 🌳 **PageIndex Hierarchical Tree** → Structured document navigation
- 🔎 **Keyword-Based Retrieval** → Fast, transparent context selection
- 🧠 **LLM Inference (Groq + Llama)** → Response generation
- 📚 **Knowledge Base Indexing** → Tree-structured data organization
"""
    )

    st.divider()

    # ---------- ARCHITECTURE DIAGRAM ----------
    st.subheader("📊 Architecture Diagram")

    if IMAGE_PATH.exists():
        st.image(
            IMAGE_PATH,
            caption="Vectorless PageIndex RAG Pipeline",
            width='stretch',
        )
    else:
        st.warning("⚠️ Architecture diagram not found")
        st.info("Place your architecture image inside the **img/** folder.")

    st.divider()

    # ---------- PAGEINDEX TREE ----------
    st.subheader("🌳 PageIndex Document Tree")

    st.markdown(
        """
The **PageIndex** organizes all portfolio data into a navigable hierarchy:

```
📄 Portfolio (Root)
├── 📁 About Me
│   ├── 📑 Professional Summary
│   ├── 📑 Academic Excellence
│   ├── 📑 Technical Expertise
│   └── 📑 Career Objectives
├── 📁 Experience
│   ├── 📑 eClerx — Analyst
│   ├── 📑 Qodeit — Intern
│   └── 📑 Teaching Experience
├── 📁 Skills
│   ├── 📑 Programming Languages
│   ├── 📑 Backend Development
│   ├── 📑 AI & Machine Learning
│   └── 📑 Automation Engineering
├── 📁 Education
│   ├── 📑 B.E. Computer Science (AIML)
│   └── 📑 Academic Performance
├── 📁 Projects
│   ├── 📑 Paddy Doctor
│   ├── 📑 LipNet
│   ├── 📑 GenMed
│   ├── 📑 AI Resume Portfolio
│   └── 📑 Automation Tools
├── 📁 Achievements
│   ├── 📑 Awards & Recognition
│   ├── 📑 Certifications
│   └── 📑 Publications
├── 📁 Contact
│   └── 📑 Contact Info & Social Links
├── 📁 Why Hire
│   ├── 📑 Key Strengths
│   └── 📑 Value Proposition
└── 📁 Resume
    └── 📑 Complete Professional Summary
```

Each query navigates this tree using keyword matching to find
the most relevant pages — no embeddings or similarity search needed.
"""
    )

    st.divider()

    # ---------- PIPELINE FLOW ----------
    st.subheader("⚙️ System Workflow")

    steps = [
        (
            "1️⃣ User Interaction",
            """
- User submits query via Streamlit chat interface
- Request forwarded to Vectorless RAG pipeline
""",
        ),
        (
            "2️⃣ Query Classification",
            """
- Greeting detection (no LLM call needed)
- Profile question classification
- Cache lookup for instant response
""",
        ),
        (
            "3️⃣ Hierarchical Tree Retrieval (PageIndex)",
            """
- **Pass 1:** Score document branches via keyword matching
- **Pass 2:** Drill into top branches, score individual pages
- Select top-3 most relevant pages (no embeddings!)
- Transparent, traceable retrieval decisions
""",
        ),
        (
            "4️⃣ Context Assembly",
            """
- Combine content from selected pages
- Include tree structure summary for LLM awareness
- Keep context focused and minimal
""",
        ),
        (
            "5️⃣ AI Response Generation",
            """
- Context + query sent to Groq LLM
- Llama model generates answer
- Answer cached for future similar queries
""",
        ),
    ]

    for title, description in steps:
        with st.expander(title, expanded=True):
            st.markdown(description)

    st.divider()

    # ---------- VECTOR vs VECTORLESS COMPARISON ----------
    st.subheader("⚡ Vector RAG vs Vectorless PageIndex")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
### ❌ Traditional Vector RAG
- Requires embedding model (~80MB download)
- FAISS vector database storage
- Opaque similarity scoring
- Fixed-size chunking breaks context
- Heavy dependencies (PyTorch ~2GB)
- Cold start: 30-60 seconds
"""
        )

    with col2:
        st.markdown(
            """
### ✅ Vectorless PageIndex (Current)
- No embedding model needed
- Hierarchical tree navigation
- Transparent keyword matching
- Natural section boundaries preserved
- Zero ML dependencies
- Cold start: <1 second
"""
        )

    st.divider()

    # ---------- TECH STACK ----------
    st.subheader("🧰 Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
### 🎨 Frontend
- Streamlit
- Python
- Interactive UI Components
"""
        )

    with col2:
        st.markdown(
            """
### 🌳 PageIndex Retrieval
- Hierarchical Tree Structure
- Keyword-Based Matching
- Section-Aware Navigation
"""
        )

    with col3:
        st.markdown(
            """
### 🧠 AI / Backend
- Groq API
- Llama 3.1
- Vectorless RAG
"""
        )

    st.divider()

    # ---------- OPTIMIZATION ----------
    with st.expander("🚀 Performance Optimizations"):
        st.markdown(
            """
- **Zero cold start** — No model downloads, tree builds from text in <1s
- **Response caching** — Identical queries served instantly
- **Greeting detection** — No LLM call for simple greetings
- **Focused context** — Only relevant pages sent to LLM (not entire knowledge base)
- **Tree-aware prompts** — LLM understands document structure for better answers
- **Lightweight deployment** — ~50MB vs ~5GB with vector approach
"""
        )

    # ---------- FOOTER ----------
    st.caption("Built with Vectorless PageIndex RAG architecture — no embeddings, no vectors, just intelligent tree retrieval.")