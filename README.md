# 🎓 AI-Based Personalized Tutor Using RAG for Syllabus-Aligned Learning

A high-performance, visually stunning Streamlit application that provides intelligent, syllabus-grounded tutoring using Retrieval Augmented Generation (RAG) and Google Gemini API (`gemini-2.5-flash`).

---

## 🌟 Key Features

1. **Strict Syllabus Alignment**: Eliminates generic/out-of-context answers by generating responses strictly from uploaded syllabus documents.
2. **Multi-Format Ingestion**: Supports PDF, DOCX, TXT, and PPTX lecture notes, textbooks, and course outlines.
3. **Instant Doubt Resolution**: Interactive chat interface with real-time answer generation and expandable source citations (Document name, Page/Section).
4. **Personalized Study Roadmap**: Day-by-day revision schedule generator tailored to remaining exam days.
5. **Practice Quiz Builder**: Generates topic-wise practice question papers (MCQs & short answer) with detailed solution keys.
6. **Concept Simplifier**: Explains complex syllabus topics using real-world analogies and intuitive step-by-step breakdowns.
7. **Source Inspector**: Live inspection of vector store chunks, TF-IDF cosine similarity scores, and metadata transparency.

---

## 🛠️ Tech Stack

### Frontend
- **Framework**: Streamlit 1.61+
- **Styling**: Custom CSS Design System (Glassmorphism, Dark Mode, Google Fonts: Inter & Outfit)
- **UI Components**: Responsive chat interface, file drag-and-drop uploader, metric cards, tabbed views.

### Backend & RAG Pipeline
- **Language**: Python 3.14
- **Document Parsers**: `pypdf`, `python-docx`, `python-pptx`
- **Text Chunker**: Recursive splitting with overlap and source metadata tracking
- **Vector Database**: In-memory TF-IDF Vector Space Model & Cosine Similarity (`scikit-learn`)
- **LLM Provider**: Google Gemini REST API (`gemini-2.5-flash`)

---

## 🚀 How to Run

```bash
# Navigate to project directory
cd rag_personalized_tutor

# Install dependencies
pip install -r requirements.txt

# Run Streamlit Application
streamlit run app.py
```
