import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:
    """In-memory Vector Database using TF-IDF Vector Space Model & Cosine Similarity."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self.chunks: List[Dict[str, Any]] = []
        self.matrix = None
        self.is_indexed = False

    def remove_source(self, source_name: str):
        """Remove existing chunks for a source document before re-ingesting."""
        self.chunks = [c for c in self.chunks if c["metadata"]["source"] != source_name]
        self.rebuild_index()

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        if not chunks:
            return 0
            
        self.chunks.extend(chunks)
        self.rebuild_index()
        return len(chunks)

    def rebuild_index(self):
        if not self.chunks:
            self.matrix = None
            self.is_indexed = False
            return

        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        corpus = [c["text"] for c in self.chunks]
        self.matrix = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True

    def similarity_search(
        self, query: str, top_k: int = 6, source_filter: Optional[str] = None
    ) -> List[Tuple[Dict[str, Any], float]]:
        if not self.is_indexed or not self.chunks or self.matrix is None:
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.matrix).flatten()
        
        # Get sorted indices by similarity score
        sorted_indices = np.argsort(similarities)[::-1]
        
        results = []
        for idx in sorted_indices:
            chunk = self.chunks[idx]
            if source_filter and source_filter != "All Documents" and chunk["metadata"]["source"] != source_filter:
                continue
                
            score = float(similarities[idx])
            results.append((chunk, score))
            if len(results) >= top_k:
                break
                
        return results

    def get_multi_doc_context(self, max_total: int = 25, source_filter: Optional[str] = None) -> str:
        """Collects representative text chunks proportionally across all loaded documents."""
        if not self.chunks:
            return ""

        filtered_chunks = self.chunks
        if source_filter and source_filter != "All Documents":
            filtered_chunks = [c for c in self.chunks if c["metadata"]["source"] == source_filter]

        if not filtered_chunks:
            return ""

        # Group chunks by source document
        by_source: Dict[str, List[Dict[str, Any]]] = {}
        for c in filtered_chunks:
            src = c["metadata"]["source"]
            by_source.setdefault(src, []).append(c)

        selected_chunks = []
        chunks_per_src = max(1, max_total // len(by_source))
        
        for src, chunks in by_source.items():
            # Pick evenly distributed chunks from this document
            step = max(1, len(chunks) // chunks_per_src)
            for i in range(0, len(chunks), step):
                selected_chunks.append(chunks[i])
                if len(selected_chunks) >= max_total:
                    break
            if len(selected_chunks) >= max_total:
                break

        context_blocks = []
        for c in selected_chunks:
            meta = c["metadata"]
            context_blocks.append(f"[{meta['source']} - Page {meta.get('page', 1)}]\n{c['text']}")

        return "\n\n".join(context_blocks)

    def clear(self):
        self.chunks = []
        self.matrix = None
        self.is_indexed = False

    def get_stats(self) -> Dict[str, Any]:
        sources = set(c["metadata"]["source"] for c in self.chunks) if self.chunks else set()
        return {
            "total_chunks": len(self.chunks),
            "sources_count": len(sources),
            "sources": list(sources),
            "is_indexed": self.is_indexed
        }
