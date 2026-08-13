from typing import List, Dict, Any

class TextChunker:
    """Recursively splits documents into chunks with configurable size and overlap."""
    
    def __init__(self, chunk_size: int = 400, overlap: int = 80):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_document(self, page_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        text = page_data["text"]
        metadata = page_data["metadata"]
        
        if len(text) <= self.chunk_size:
            return [{
                "text": text,
                "metadata": {**metadata, "chunk_id": 0}
            }]

        chunks = []
        start = 0
        chunk_idx = 0
        text_len = len(text)

        while start < text_len:
            end = start + self.chunk_size
            
            # If not at the end of text, look for natural paragraph/sentence boundary
            if end < text_len:
                boundary = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
                if boundary != -1 and boundary > start + (self.chunk_size // 2):
                    end = boundary + 1

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "metadata": {
                        **metadata,
                        "chunk_id": chunk_idx
                    }
                })
                chunk_idx += 1

            start = end - self.overlap
            if start >= text_len - self.overlap:
                break

        return chunks

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        all_chunks = []
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        return all_chunks
