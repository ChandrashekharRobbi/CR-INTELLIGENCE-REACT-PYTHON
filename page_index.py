"""
PageIndex Module — Vectorless RAG with Hierarchical Tree-Based Retrieval.

Implements the PageIndex pattern:
1. Parses text files into a hierarchical tree (Document → Sections → Subsections)
2. Builds a keyword-indexed structure for fast retrieval
3. Performs reasoning-based retrieval through tree navigation
4. Returns focused context from relevant pages only

No embeddings. No vector DB. No heavy ML dependencies.
"""

import os
import re
import glob
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple


@dataclass
class PageNode:
    """
    A node in the hierarchical page tree.

    Each node represents either:
    - A document (root level — represents an entire .txt file)
    - A section (mid level — a major heading within a file)
    - A subsection (leaf level — content under a heading)
    """
    title: str
    summary: str = ""
    content: str = ""
    level: int = 0  # 0 = root, 1 = document, 2 = section, 3 = subsection
    keywords: List[str] = field(default_factory=list)
    children: List['PageNode'] = field(default_factory=list)
    source_file: str = ""

    def has_children(self) -> bool:
        return len(self.children) > 0

    def get_all_content(self) -> str:
        """Get content from this node and all children recursively."""
        parts = []
        if self.content:
            parts.append(self.content)
        for child in self.children:
            child_content = child.get_all_content()
            if child_content:
                parts.append(child_content)
        return "\n\n".join(parts)

    def get_tree_display(self, indent: int = 0) -> str:
        """Get formatted tree display string."""
        prefix = "  " * indent
        icons = {0: "[DOC]", 1: "[DIR]", 2: "[SEC]", 3: "[PG]"}
        icon = icons.get(self.level, "[PG]")
        lines = [f"{prefix}{icon} {self.title}"]
        for child in self.children:
            lines.append(child.get_tree_display(indent + 1))
        return "\n".join(lines)


class PageIndex:
    """
    Vectorless hierarchical document index.

    Organizes portfolio data into a navigable tree structure
    and performs keyword-based retrieval for RAG context assembly.
    """

    # Keyword maps for routing queries to the right branches
    SECTION_KEYWORDS = {
        "about": [
            "about", "who", "introduce", "introduction", "biography", "summary",
            "background", "chandrashekhar", "robbi", "yourself", "profile",
            "personal", "philosophy", "career", "objective", "notice", "period",
            "availability", "location", "thane", "maharashtra", "live", "based",
            "where", "current"
        ],
        "experience": [
            "experience", "work", "job", "role", "company", "eclerx", "qodeit",
            "analyst", "intern", "internship", "professional", "employment",
            "contribution", "responsibility", "teaching", "teacher", "teach",
            "student", "collaboration", "team", "career"
        ],
        "skills": [
            "skill", "skills", "technology", "technologies", "tech", "stack",
            "programming", "language", "python", "sql", "fastapi", "flask",
            "framework", "tool", "backend", "automation", "ai", "ml",
            "machine learning", "deep learning", "nlp", "genai", "generative",
            "agentic", "azure", "cloud", "database", "git", "streamlit",
            "computer vision", "tensorflow", "expertise", "capability",
            "soft skill", "communication", "problem solving"
        ],
        "education": [
            "education", "degree", "college", "university", "cgpi", "sgpi",
            "semester", "academic", "study", "graduation", "b.e", "engineering",
            "saraswati", "mumbai", "gpa", "marks", "score"
        ],
        "projects": [
            "project", "projects", "portfolio", "paddy", "doctor", "mnist",
            "lipnet", "genmed", "medicine", "chatbot", "watchdog", "leetcode",
            "movie", "automation", "pipeline", "demo", "sample", "work sample",
            "github", "build", "built", "developed", "created", "designed",
            "ai resume"
        ],
        "achievements": [
            "achievement", "achievements", "award", "awards", "recognition",
            "appreciation", "super achiever", "avishkar", "hackoverflow",
            "competition", "certification", "certifications", "certificate",
            "publication", "research", "iit", "bombay", "munich", "udemy"
        ],
        "contact": [
            "contact", "email", "mail", "linkedin", "github", "twitter",
            "reach", "connect", "url", "link", "phone", "social", "media",
            "network", "message", "stay"
        ],
        "why_hire": [
            "hire", "why", "reason", "benefit", "value", "strength",
            "strengths", "advantage", "worth", "fit", "suitable", "qualified",
            "candidate", "opportunity"
        ],
        "resume": [
            "resume", "cv", "curriculum", "vitae", "overview", "summary",
            "complete", "full", "everything", "all"
        ],
    }

    def __init__(self):
        self.root: Optional[PageNode] = None
        self.all_pages: List[PageNode] = []  # Flat list for quick access
        self._is_built = False

    def build_tree(self, data_folder: str = "data") -> None:
        """
        Build the hierarchical tree from text files in the data folder.

        Each .txt file becomes a branch node.
        Headings within each file become section/subsection nodes.

        Args:
            data_folder: Path to folder containing .txt files
        """
        txt_files = sorted(glob.glob(os.path.join(data_folder, "*.txt")))

        if not txt_files:
            raise FileNotFoundError(f"No .txt files found in {data_folder}")

        # Create root node
        self.root = PageNode(
            title="Chandrashekhar Robbi — Portfolio",
            summary="Complete professional portfolio including about, experience, skills, education, projects, achievements, contact, and hiring information.",
            level=0,
            keywords=["chandrashekhar", "robbi", "portfolio", "profile"]
        )

        print(f"\n[PageIndex] Building tree from {len(txt_files)} documents...")

        for file_path in txt_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                file_name = os.path.basename(file_path).replace('.txt', '')
                doc_node = self._parse_document(content, file_name, file_path)
                self.root.children.append(doc_node)

                # Collect all leaf pages
                self._collect_pages(doc_node)

                print(f"  + {file_name}.txt -> {len(doc_node.children)} sections")

            except Exception as e:
                print(f"  ! Error parsing {file_path}: {e}")

        self._is_built = True
        total_pages = len(self.all_pages)
        print(f"\n[OK] PageIndex Ready!")
        print(f"  Documents: {len(txt_files)}")
        print(f"  Total Pages: {total_pages}")
        print(f"  Tree Depth: 3 levels")

    def _parse_document(self, content: str, file_name: str, file_path: str) -> PageNode:
        """
        Parse a single text file into a document node with section children.

        Heuristic for detecting headings:
        - Lines that are relatively short (< 80 chars)
        - Don't end with common sentence-ending punctuation
        - Are preceded by a blank line
        - Are not just whitespace

        Args:
            content: Full text content of the file
            file_name: Base name of the file (without .txt)
            file_path: Full path to the file

        Returns:
            PageNode representing the document with section children
        """
        lines = content.split('\n')

        # First line is typically the document title
        doc_title = lines[0].strip() if lines else file_name
        doc_keywords = self.SECTION_KEYWORDS.get(file_name, [])

        doc_node = PageNode(
            title=doc_title,
            level=1,
            source_file=file_path,
            keywords=doc_keywords
        )

        # Parse sections by detecting headings
        sections = self._extract_sections(lines)

        for section_title, section_content in sections:
            # Generate summary from first 150 chars of content
            summary = section_content[:150].strip()
            if len(section_content) > 150:
                summary += "..."

            # Extract keywords from section title
            section_keywords = self._extract_keywords(section_title)

            section_node = PageNode(
                title=section_title,
                summary=summary,
                content=section_content,
                level=2,
                keywords=section_keywords + doc_keywords,
                source_file=file_path
            )
            doc_node.children.append(section_node)

        # Set document summary
        if doc_node.children:
            section_titles = [c.title for c in doc_node.children]
            doc_node.summary = f"Covers: {', '.join(section_titles[:5])}"
            if len(section_titles) > 5:
                doc_node.summary += f" (+{len(section_titles) - 5} more)"
        else:
            # If no sections detected, treat entire content as one page
            doc_node.content = content
            doc_node.summary = content[:200].strip()

        return doc_node

    def _extract_sections(self, lines: List[str]) -> List[Tuple[str, str]]:
        """
        Extract sections from document lines by detecting heading patterns.

        Returns list of (heading_title, section_content) tuples.
        """
        sections = []
        current_heading = None
        current_content_lines = []
        prev_was_blank = True  # Start as true so first heading is detected

        for i, line in enumerate(lines):
            stripped = line.strip()

            if not stripped:
                prev_was_blank = True
                if current_heading:
                    current_content_lines.append("")
                continue

            is_heading = self._is_heading(stripped, prev_was_blank, i, lines)

            if is_heading:
                # Save previous section
                if current_heading and current_content_lines:
                    content = "\n".join(current_content_lines).strip()
                    if content:  # Only add if there's actual content
                        sections.append((current_heading, content))

                current_heading = stripped
                current_content_lines = []
            else:
                if current_heading:
                    current_content_lines.append(stripped)
                else:
                    # Before first heading — skip or use as intro
                    pass

            prev_was_blank = False

        # Don't forget the last section
        if current_heading and current_content_lines:
            content = "\n".join(current_content_lines).strip()
            if content:
                sections.append((current_heading, content))

        return sections

    def _is_heading(self, line: str, prev_was_blank: bool, line_idx: int, all_lines: List[str]) -> bool:
        """
        Determine if a line is likely a section heading.

        Heuristics:
        1. Must be preceded by a blank line (or be first non-empty line)
        2. Must be relatively short (< 80 chars)
        3. Should not end with sentence-ending punctuation
        4. Should not start with common list markers
        """
        # Must follow a blank line
        if not prev_was_blank:
            return False

        # Too long for a heading
        if len(line) > 80:
            return False

        # Ends with sentence punctuation — likely not a heading
        if line.endswith(('.', '!', '?')) and len(line) > 40:
            return False

        # Starts with list markers — not a heading
        if re.match(r'^[-•*]\s', line):
            return False

        # Contains typical heading patterns
        heading_patterns = [
            r'^[A-Z]',  # Starts with capital
            r'—',  # Contains em-dash (common in titles)
            r'&',  # Contains ampersand
            r':$',  # Ends with colon
        ]

        matches_pattern = any(re.search(p, line) for p in heading_patterns)

        # Check if the next non-empty line is content (longer, has punctuation)
        # This helps confirm it's a heading
        next_content = None
        for j in range(line_idx + 1, min(line_idx + 4, len(all_lines))):
            next_line = all_lines[j].strip()
            if next_line:
                next_content = next_line
                break

        if next_content and len(next_content) > len(line):
            return matches_pattern

        return matches_pattern and len(line) < 60

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for matching."""
        # Lowercase and split
        words = re.findall(r'[a-zA-Z]+', text.lower())
        # Filter out very short and common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were',
            'be', 'been', 'has', 'have', 'had', 'do', 'does', 'did', 'not',
            'this', 'that', 'it', 'its', 'as'
        }
        return [w for w in words if len(w) > 2 and w not in stop_words]

    def _collect_pages(self, node: PageNode) -> None:
        """Recursively collect all leaf pages into flat list."""
        if not node.has_children():
            self.all_pages.append(node)
        else:
            for child in node.children:
                self._collect_pages(child)

    def retrieve(self, query: str, top_k: int = 3) -> List[PageNode]:
        """
        Retrieve the most relevant pages for a query using keyword matching.

        Two-pass approach:
        1. Score each document branch by keyword overlap
        2. Within top branches, score each section and return top-k pages

        Args:
            query: User's question
            top_k: Number of pages to retrieve

        Returns:
            List of most relevant PageNode objects
        """
        if not self._is_built or not self.root:
            raise RuntimeError("PageIndex not built. Call build_tree() first.")

        query_lower = query.lower()
        query_words = set(re.findall(r'[a-zA-Z]+', query_lower))

        # --- Pass 1: Score document branches ---
        branch_scores: List[Tuple[float, PageNode]] = []

        for doc_node in self.root.children:
            # Score against SECTION_KEYWORDS mapping
            score = self._score_node(doc_node, query_words, query_lower)
            branch_scores.append((score, doc_node))

        # Sort by score descending
        branch_scores.sort(key=lambda x: x[0], reverse=True)

        # --- Pass 2: Get pages from top branches ---
        scored_pages: List[Tuple[float, PageNode]] = []

        # Explore top 3 branches (or all if fewer)
        for branch_score, doc_node in branch_scores[:3]:
            if branch_score <= 0:
                continue

            for section_node in doc_node.children:
                page_score = self._score_node(section_node, query_words, query_lower)
                # Boost by branch score
                combined_score = page_score + (branch_score * 0.5)
                scored_pages.append((combined_score, section_node))

            # If document has no children, score the document itself
            if not doc_node.has_children() and doc_node.content:
                scored_pages.append((branch_score, doc_node))

        # Sort and return top-k
        scored_pages.sort(key=lambda x: x[0], reverse=True)

        # If no keyword matches, fall back to returning the "about" + "resume" pages
        if not scored_pages:
            return self._get_fallback_pages(top_k)

        return [page for _, page in scored_pages[:top_k]]

    def _score_node(self, node: PageNode, query_words: set, query_lower: str) -> float:
        """
        Score a node's relevance to the query.

        Scoring factors:
        1. Keyword overlap with node's keyword list
        2. Query words found in node title
        3. Query words found in node content
        4. Exact phrase matches in content
        """
        score = 0.0

        # Factor 1: Keyword overlap (highest weight)
        if node.keywords:
            keyword_matches = query_words.intersection(set(node.keywords))
            score += len(keyword_matches) * 3.0

            # Check multi-word keywords
            for kw in node.keywords:
                if ' ' in kw and kw in query_lower:
                    score += 5.0

        # Factor 2: Title matches
        title_lower = node.title.lower()
        title_words = set(re.findall(r'[a-zA-Z]+', title_lower))
        title_matches = query_words.intersection(title_words)
        score += len(title_matches) * 2.0

        # Factor 3: Content matches (lower weight since content is larger)
        if node.content:
            content_lower = node.content.lower()
            for word in query_words:
                if len(word) > 3:  # Only check meaningful words
                    count = content_lower.count(word)
                    score += min(count, 3) * 0.5  # Cap at 3 occurrences

        # Factor 4: Summary matches
        if node.summary:
            summary_lower = node.summary.lower()
            for word in query_words:
                if word in summary_lower:
                    score += 1.0

        return score

    def _get_fallback_pages(self, top_k: int) -> List[PageNode]:
        """Return default pages when no keyword match found."""
        fallback = []
        for doc_node in self.root.children:
            if doc_node.children:
                fallback.append(doc_node.children[0])  # First section of each doc
            if len(fallback) >= top_k:
                break
        return fallback

    def get_context(self, pages: List[PageNode], max_length: int = 6000) -> str:
        """
        Assemble context string from retrieved pages.

        Args:
            pages: List of relevant PageNode objects
            max_length: Maximum context length in characters

        Returns:
            Formatted context string
        """
        context_parts = []
        total_length = 0

        for page in pages:
            # Get content — either from this node or its children
            content = page.content if page.content else page.get_all_content()

            if not content:
                continue

            # Format with section header
            section_text = f"[{page.title}]\n{content}"

            if total_length + len(section_text) > max_length:
                # Truncate if needed
                remaining = max_length - total_length
                if remaining > 100:  # Only add if meaningful amount
                    section_text = section_text[:remaining] + "..."
                    context_parts.append(section_text)
                break

            context_parts.append(section_text)
            total_length += len(section_text)

        return "\n\n---\n\n".join(context_parts)

    def get_tree_summary(self) -> str:
        """
        Get a compact text representation of the tree.
        Used to give the LLM awareness of the full document structure.
        """
        if not self.root:
            return "No index built."

        lines = [f"Portfolio Structure:"]
        for doc_node in self.root.children:
            lines.append(f"\n  [DIR] {doc_node.title}")
            for section in doc_node.children:
                lines.append(f"    [SEC] {section.title}")

        return "\n".join(lines)

    def get_tree_display(self) -> str:
        """Get formatted tree for display purposes (Architecture page)."""
        if not self.root:
            return "No index built."
        return self.root.get_tree_display()

    def get_stats(self) -> Dict:
        """Get index statistics."""
        if not self.root:
            return {"status": "not_built"}

        doc_count = len(self.root.children)
        section_count = sum(len(d.children) for d in self.root.children)
        total_content_size = sum(len(p.content) for p in self.all_pages)

        return {
            "status": "ready",
            "documents": doc_count,
            "sections": section_count,
            "total_pages": len(self.all_pages),
            "total_content_chars": total_content_size,
            "estimated_tokens": total_content_size // 4,
        }

    def is_ready(self) -> bool:
        """Check if the index has been built."""
        return self._is_built
