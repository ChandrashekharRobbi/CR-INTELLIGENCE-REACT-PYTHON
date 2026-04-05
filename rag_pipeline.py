"""
RAG Pipeline Module — Vectorless PageIndex-based Retrieval Augmented Generation.

Features:
- Hierarchical tree-structured document indexing (PageIndex)
- Keyword-based reasoning retrieval (no embeddings, no vector DB)
- Smart query classification (greeting detection, small talk filtering)
- Token-efficient prompt templates with tree-aware context
- Query caching to avoid repeated API calls
- Token usage monitoring
"""

import os
import glob
import re
from typing import List, Optional, Dict
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from page_index import PageIndex
from config import (
    PAGE_INDEX_TOP_K,
    MAX_CONTEXT_CHARS,
    LLM_MODEL,
    LLM_TEMPERATURE,
    MAX_TOKENS_PER_RESPONSE,
    SYSTEM_PROMPT,
    RAG_PROMPT_TEMPLATE,
    GREETING_QUERIES,
    GREETING_RESPONSE,
    PROFILE_QUESTION_PATTERNS,
    DEBUG_MODE,
    LOG_TOKEN_USAGE,
    ENABLE_TREE_SUMMARY_IN_PROMPT,
)


class RAGPipeline:
    """
    Vectorless RAG Pipeline using PageIndex hierarchical retrieval.

    Implements:
    1. Query classification (reduce unnecessary API calls)
    2. Hierarchical keyword-based retrieval (no embeddings)
    3. Tree-aware context assembly
    4. Token-efficient prompt construction
    5. Response caching
    6. Token usage monitoring
    """

    def __init__(self, groq_api_key: str):
        """
        Initialize RAG pipeline.

        Args:
            groq_api_key: Groq API key
        """
        self.groq_api_key = groq_api_key
        self.page_index = PageIndex()
        self.llm = None
        self.response_cache = {}
        self.token_usage_log = []
        self._initialize_llm()

    def _initialize_llm(self) -> None:
        """Initialize Groq LLM with token-optimized settings."""
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=MAX_TOKENS_PER_RESPONSE
        )

    def _classify_query(self, query: str) -> str:
        """
        Classify query type to optimize processing.

        Returns:
            "greeting", "small_talk", "profile_question", or "general"
        """
        query_lower = query.lower().strip().split()
        # Check for greeting
        if any(query in GREETING_QUERIES for query in query_lower):
            return "greeting"

        # Check for profile questions (need RAG)
        if any(query in PROFILE_QUESTION_PATTERNS for query in query_lower):
            return "profile_question"

        # Default to general (needs LLM but maybe not RAG)
        return "general"

    def _is_cached_response(self, query: str) -> Optional[str]:
        """Check if we have a cached response (exact match)."""
        if query in self.response_cache:
            return self.response_cache[query]
        return None

    def _log_token_usage(self, query: str, context: str, response: str, query_type: str):
        """Log token usage for monitoring."""
        if not LOG_TOKEN_USAGE:
            return

        # Estimate tokens (rough: 1 token ≈ 4 chars)
        context_tokens = len(context) // 4
        response_tokens = len(response) // 4
        total_tokens = context_tokens + response_tokens

        log_entry = {
            "query": query,
            "type": query_type,
            "context_tokens": context_tokens,
            "response_tokens": response_tokens,
            "total_tokens": total_tokens
        }

        self.token_usage_log.append(log_entry)

        if DEBUG_MODE:
            print(f"📊 Tokens — Context: {context_tokens}, Response: {response_tokens}, Total: {total_tokens}")

    def load_knowledge_base(self, data_folder: str = "data") -> None:
        """
        Build the PageIndex tree from data files.

        This replaces the old build_index/load_index flow.
        No persistence needed — tree builds in <1s from text files.

        Args:
            data_folder: Path to folder containing .txt data files
        """
        self.page_index.build_tree(data_folder)

        stats = self.page_index.get_stats()
        if DEBUG_MODE:
            print(f"📊 Index Stats: {stats}")

    def retrieve_context(self, query: str, top_k: int = PAGE_INDEX_TOP_K) -> str:
        """
        Retrieve relevant context using hierarchical PageIndex retrieval.

        Two-pass approach:
        1. Keyword matching against tree structure to find relevant branches
        2. Assemble context from top-k matched pages

        Args:
            query: User query
            top_k: Number of pages to retrieve

        Returns:
            Formatted context string from relevant pages
        """
        # Retrieve relevant pages from the tree
        pages = self.page_index.retrieve(query, top_k=top_k)

        if not pages:
            return ""

        # Assemble context from matched pages
        context = self.page_index.get_context(pages, max_length=MAX_CONTEXT_CHARS)

        if DEBUG_MODE:
            retrieved_titles = [p.title for p in pages]
            print(f"🔍 Retrieved pages: {retrieved_titles}")

        return context

    def _construct_minimal_prompt(self, query: str, context: str = "") -> str:
        """
        Construct minimal prompt to save tokens.

        Optionally includes tree summary for LLM awareness of document structure.

        Args:
            query: User query
            context: Retrieved context (optional)

        Returns:
            Minimal prompt string
        """
        parts = [f"System: {SYSTEM_PROMPT}"]

        # Optionally include tree summary for structural awareness
        if ENABLE_TREE_SUMMARY_IN_PROMPT and self.page_index.is_ready():
            tree_summary = self.page_index.get_tree_summary()
            parts.append(f"\nDocument Structure:\n{tree_summary}")

        if context:
            parts.append(f"\nRelevant Context:\n{context}")

        parts.append(f"\nQuestion: {query}\n\nAnswer:")

        return "\n".join(parts)

    def generate_answer(self, query: str, context: str = "") -> str:
        """
        Generate answer using Groq LLM.

        Args:
            query: User query
            context: Retrieved context

        Returns:
            Generated answer
        """
        # Construct minimal prompt
        prompt = self._construct_minimal_prompt(query, context)

        try:
            # Get response from Groq
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"❌ Error generating response: {str(e)}"

    def query(self, user_query: str, top_k: int = PAGE_INDEX_TOP_K) -> Dict:
        """
        Complete vectorless RAG query pipeline.

        Args:
            user_query: User's question
            top_k: Number of context pages to retrieve

        Returns:
            Dict with query, context, answer, and metadata
        """
        # Validate index
        if not self.page_index.is_ready():
            raise RuntimeError("PageIndex not built. Call load_knowledge_base() first.")

        try:
            # Step 1: Classify query
            query_type = self._classify_query(user_query)

            # Step 2: Handle greeting (no API call needed!)
            if query_type == "greeting":
                return {
                    "query": user_query,
                    "answer": GREETING_RESPONSE,
                    "query_type": "greeting",
                    "context_chunks": 0,
                    "status": "success"
                }

            # Step 3: Check cache
            cached = self._is_cached_response(user_query)
            if cached:
                return {
                    "query": user_query,
                    "answer": cached,
                    "query_type": query_type,
                    "context_chunks": 0,
                    "cached": True,
                    "status": "success"
                }

            # Step 4: Retrieve context via PageIndex tree
            context = self.retrieve_context(user_query, top_k=top_k)
            context_chunks = len(context.split("\n\n---\n\n")) if context else 0

            # Step 5: Generate answer
            answer = self.generate_answer(user_query, context)

            # Step 6: Cache response
            self.response_cache[user_query] = answer

            # Step 7: Log token usage
            self._log_token_usage(user_query, context, answer, query_type)

            return {
                "query": user_query,
                "context_chunks": context_chunks,
                "query_type": query_type,
                "answer": answer,
                "status": "success"
            }

        except Exception as e:
            return {
                "query": user_query,
                "answer": f"❌ Error: {str(e)}",
                "status": "error"
            }

    def get_token_usage_stats(self) -> Dict:
        """Get token usage statistics."""
        if not self.token_usage_log:
            return {"total_queries": 0, "total_tokens": 0}

        total_tokens = sum(log["total_tokens"] for log in self.token_usage_log)

        return {
            "total_queries": len(self.token_usage_log),
            "total_tokens": total_tokens,
            "avg_tokens_per_query": total_tokens / len(self.token_usage_log) if self.token_usage_log else 0,
            "cache_size": len(self.response_cache)
        }

    def get_index_stats(self) -> Dict:
        """Get PageIndex statistics."""
        return self.page_index.get_stats()
