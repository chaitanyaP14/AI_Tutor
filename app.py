import os
import streamlit as st
from rag_engine.document_loader import DocumentLoader
from rag_engine.text_chunker import TextChunker
from rag_engine.vector_store import VectorStore
from rag_engine.llm_backend import LLMBackend, DEFAULT_API_KEY
from styles import inject_custom_styles

# Set Page Config
st.set_page_config(
    page_title="AI Personalized Tutor (Multi-Syllabus RAG)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom Design System
inject_custom_styles()

# Initialize Session State
if "vector_store" not in st.session_state:
    st.session_state.vector_store = VectorStore()

if "text_chunker" not in st.session_state:
    st.session_state.text_chunker = TextChunker(chunk_size=450, overlap=90)

if "llm" not in st.session_state:
    st.session_state.llm = LLMBackend(api_key=DEFAULT_API_KEY)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "ingested_files" not in st.session_state:
    st.session_state.ingested_files = set()

if "sample_init_done" not in st.session_state:
    st.session_state.sample_init_done = False

# Pre-load sample data only once on initial startup
def load_sample_dataset():
    if st.session_state.sample_init_done:
        return
    sample_file_path = os.path.join(os.path.dirname(__file__), "sample_data", "ds_algorithm_syllabus.txt")
    if os.path.exists(sample_file_path) and not st.session_state.vector_store.is_indexed:
        with open(sample_file_path, "r", encoding="utf-8") as f:
            content = f.read().encode("utf-8")
        filename = "ds_algorithm_syllabus.txt"
        docs = DocumentLoader.load_txt(content, filename)
        chunks = st.session_state.text_chunker.chunk_documents(docs)
        st.session_state.vector_store.add_chunks(chunks)
        st.session_state.ingested_files.add(filename)
    st.session_state.sample_init_done = True

load_sample_dataset()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### System Configuration")
    
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=st.session_state.llm.api_key,
        type="password",
        help="Pre-filled with provided API key. You can update it anytime."
    )
    if api_key_input != st.session_state.llm.api_key:
        st.session_state.llm.set_api_key(api_key_input)
        st.success("API key updated successfully.")

    st.markdown("---")
    st.markdown("### Document Ingestion Hub")
    st.caption("Upload multiple Syllabi, Textbooks, PPTs, or Lecture Notes")
    
    uploaded_files = st.file_uploader(
        "Select files from your computer:",
        type=["pdf", "docx", "txt", "pptx"],
        accept_multiple_files=True,
        label_visibility="visible",
        help="Choose multiple files to build a comprehensive multi-subject knowledge base."
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            fname = uploaded_file.name
            with st.spinner(f"Processing {fname}..."):
                file_bytes = uploaded_file.getvalue()
                docs = DocumentLoader.load_file(file_bytes, fname)
                if docs:
                    # Remove existing chunks for this filename to allow clean updates
                    st.session_state.vector_store.remove_source(fname)
                    chunks = st.session_state.text_chunker.chunk_documents(docs)
                    added = st.session_state.vector_store.add_chunks(chunks)
                    st.session_state.ingested_files.add(fname)
                    st.toast(f"Ingested {fname} ({added} chunks)")

    with st.expander("Or Paste Text / Notes Directly"):
        custom_title = st.text_input("Document / Subject Title", "Custom_Notes_1")
        custom_text = st.text_area("Paste Syllabus Content or Notes Here", height=150)
        if st.button("Ingest Pasted Text", use_container_width=True):
            if custom_text.strip():
                fname = f"{custom_title}.txt"
                st.session_state.vector_store.remove_source(fname)
                docs = DocumentLoader.load_txt(custom_text.encode("utf-8"), fname)
                chunks = st.session_state.text_chunker.chunk_documents(docs)
                added = st.session_state.vector_store.add_chunks(chunks)
                st.session_state.ingested_files.add(fname)
                st.success(f"Ingested '{fname}' ({added} chunks)")
                st.rerun()
            else:
                st.warning("Please paste some text first.")

    st.markdown("---")
    st.markdown("### Knowledge Base Stats")
    stats = st.session_state.vector_store.get_stats()
    
    available_sources = list(st.session_state.ingested_files)
    st.markdown(f"**Loaded Files ({len(available_sources)}):**")
    for f in available_sources:
        st.caption(f"• `{f}`")
        
    st.markdown(f"**Total Vector Chunks:** `{stats['total_chunks']}`")
    st.markdown(f"**Vector Store Status:** {'Indexed' if stats['is_indexed'] else 'Empty'}")

    # Active Document Filter Selector
    doc_filter_options = ["All Documents"] + sorted(available_sources)
    selected_doc_filter = st.selectbox(
        "Target Syllabus Scope",
        options=doc_filter_options,
        index=0,
        help="Select 'All Documents' to query across all uploaded syllabi, or choose a specific document."
    )

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Clear DB", use_container_width=True, help="Wipe all loaded documents and chunks"):
            st.session_state.vector_store.clear()
            st.session_state.ingested_files.clear()
            st.session_state.chat_history.clear()
            st.session_state.sample_init_done = True
            st.toast("Database cleared successfully.")
            st.rerun()

    with col_btn2:
        if st.button("Sample Data", use_container_width=True, help="Load built-in Data Structures & ML syllabus"):
            sample_file_path = os.path.join(os.path.dirname(__file__), "sample_data", "ds_algorithm_syllabus.txt")
            if os.path.exists(sample_file_path):
                with open(sample_file_path, "r", encoding="utf-8") as f:
                    content = f.read().encode("utf-8")
                filename = "ds_algorithm_syllabus.txt"
                docs = DocumentLoader.load_txt(content, filename)
                chunks = st.session_state.text_chunker.chunk_documents(docs)
                st.session_state.vector_store.add_chunks(chunks)
                st.session_state.ingested_files.add(filename)
                st.toast("Sample data loaded.")
                st.rerun()

# ================= HERO HEADER =================
st.markdown(
    """
    <div class="hero-header">
        <span class="hero-tag">ENTERPRISE SYLLABUS INTELLIGENCE PLATFORM</span>
        <div class="hero-title">AI-Based Personalized Tutor</div>
        <div class="hero-subtitle">Multi-Syllabus Retrieval Augmented Generation (RAG) for Aligned Learning</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Top Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state.ingested_files)}</div>
            <div class="stat-label">Ingested Documents</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_chunks']}</div>
            <div class="stat-label">Vector Chunks</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        """
        <div class="stat-card">
            <div class="stat-number">Gemini Flash</div>
            <div class="stat-label">LLM Engine</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{selected_doc_filter}</div>
            <div class="stat-label">Active Scope</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs
tab_chat, tab_roadmap, tab_quiz, tab_explain, tab_inspector, tab_tech = st.tabs([
    "Instant Doubt Resolution",
    "Study Roadmap",
    "Practice Exam Builder",
    "Concept Clarifier",
    "Source Inspector",
    "Architecture & Tech Stack"
])

# ================= TAB 1: INSTANT DOUBT RESOLUTION =================
with tab_chat:
    st.markdown("### Multi-Syllabus Grounded Q&A")
    st.caption(f"Currently querying scope: **{selected_doc_filter}**. Ask any question to receive syllabus-grounded answers with exact citations.")

    # Render Chat History
    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(chat["user"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])
            if chat.get("citations"):
                with st.expander("View Retracted Source Citations"):
                    for c in chat["citations"]:
                        st.markdown(
                            f"""
                            <div class="citation-card">
                                <span class="citation-badge">{c['file_type']}</span>
                                <strong>{c['source']}</strong> (Page/Section {c['page']}) - Relevance: <code>{c['score']}</code>
                                <br><small>"{c['snippet']}"</small>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    # Chat Input Handling
    user_input = st.chat_input("Ask a question across your uploaded syllabus documents...")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Searching across all loaded syllabus documents & generating response..."):
                retrieved_chunks = st.session_state.vector_store.similarity_search(
                    user_input, top_k=8, source_filter=selected_doc_filter
                )
                result = st.session_state.llm.answer_query(user_input, retrieved_chunks)
                
                st.markdown(result["answer"])
                
                if result["citations"]:
                    with st.expander("View Retracted Source Citations"):
                        for c in result["citations"]:
                            st.markdown(
                                f"""
                                <div class="citation-card">
                                    <span class="citation-badge">{c['file_type']}</span>
                                    <strong>{c['source']}</strong> (Page/Section {c['page']}) - Relevance: <code>{c['score']}</code>
                                    <br><small>"{c['snippet']}"</small>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                st.session_state.chat_history.append({
                    "user": user_input,
                    "answer": result["answer"],
                    "citations": result["citations"]
                })

# ================= TAB 2: STUDY ROADMAP =================
with tab_roadmap:
    st.markdown("### Comprehensive Study Roadmap Generator")
    st.caption("Generates a combined day-by-day prep plan analyzing topics across all your loaded syllabus documents.")

    r_col1, r_col2 = st.columns([1, 2])
    with r_col1:
        target_exam = st.text_input("Target Exam / Subject Goal", "Comprehensive Exam Prep")
        days = st.slider("Preparation Days Available", min_value=3, max_value=60, value=14)
        generate_roadmap_btn = st.button("Generate Study Roadmap", use_container_width=True)

    with r_col2:
        if generate_roadmap_btn:
            if not st.session_state.vector_store.chunks:
                st.warning("Please upload syllabus documents or load sample data first.")
            else:
                with st.spinner("Aggregating topics across all uploaded syllabus documents..."):
                    context_str = st.session_state.vector_store.get_multi_doc_context(
                        max_total=30, source_filter=selected_doc_filter
                    )
                    roadmap = st.session_state.llm.generate_study_roadmap(context_str, days, target_exam)
                    st.markdown(roadmap)
        else:
            st.info("Set your exam goal and prep days, then click 'Generate Study Roadmap'.")

# ================= TAB 3: PRACTICE EXAM BUILDER =================
with tab_quiz:
    st.markdown("### Topic-Wise Practice Quiz Generator")
    st.caption("Generate multi-document practice questions (MCQs & short answer) with detailed solution keys.")

    q_col1, q_col2 = st.columns([1, 2])
    with q_col1:
        topic_input = st.text_input("Topic / Area for Quiz", "Core Algorithms and Machine Learning")
        num_q = st.slider("Number of Questions", min_value=3, max_value=10, value=5)
        generate_quiz_btn = st.button("Generate Practice Quiz", use_container_width=True)

    with q_col2:
        if generate_quiz_btn:
            if not st.session_state.vector_store.chunks:
                st.warning("Please upload syllabus documents or load sample data first.")
            else:
                with st.spinner("Retrieving topic context across documents & building quiz..."):
                    retrieved = st.session_state.vector_store.similarity_search(
                        topic_input, top_k=8, source_filter=selected_doc_filter
                    )
                    context = "\n\n".join([c[0]["text"] for c in retrieved])
                    quiz_text = st.session_state.llm.generate_practice_quiz(topic_input, context, num_q)
                    st.markdown(quiz_text)
        else:
            st.info("Enter a topic name and click 'Generate Practice Quiz'.")

# ================= TAB 4: CONCEPT CLARIFIER =================
with tab_explain:
    st.markdown("### Concept Simplifier & Real-World Analogies")
    st.caption("Struggling with a concept across your syllabus documents? Get clear explanations and step-by-step breakdowns.")

    e_col1, e_col2 = st.columns([1, 2])
    with e_col1:
        concept_query = st.text_input("Concept to Explain", "Shortest Path Algorithms vs Machine Learning Models")
        explain_btn = st.button("Explain Concept", use_container_width=True)

    with e_col2:
        if explain_btn:
            if not st.session_state.vector_store.chunks:
                st.warning("Please upload syllabus documents first.")
            else:
                with st.spinner("Retrieving syllabus context & generating explanation..."):
                    retrieved = st.session_state.vector_store.similarity_search(
                        concept_query, top_k=6, source_filter=selected_doc_filter
                    )
                    context = "\n\n".join([c[0]["text"] for c in retrieved])
                    explanation = st.session_state.llm.simplify_concept(concept_query, context)
                    st.markdown(explanation)
        else:
            st.info("Enter any syllabus concept to get an intuitive explanation.")

# ================= TAB 5: SOURCE INSPECTOR =================
with tab_inspector:
    st.markdown("### Vector Store & Multi-Syllabus Inspector")
    st.caption("Inspect stored document chunks, run search queries, and filter by source document.")

    test_search_query = st.text_input("Test Vector Similarity Query", "Algorithms")
    top_k_val = st.slider("Top K Chunks to Retrieve", 1, 15, 6)
    
    if test_search_query:
        results = st.session_state.vector_store.similarity_search(
            test_search_query, top_k=top_k_val, source_filter=selected_doc_filter
        )
        st.markdown(f"**Found `{len(results)}` matching chunks in scope `{selected_doc_filter}`:**")
        
        for idx, (chunk, score) in enumerate(results, 1):
            meta = chunk["metadata"]
            with st.expander(f"Chunk #{idx} | {meta['source']} (Page {meta.get('page',1)}) | Cosine Similarity: {score:.4f}"):
                st.markdown(f"**Metadata:** `{meta}`")
                st.markdown(f"**Chunk Text:**\n```text\n{chunk['text']}\n```")

# ================= TAB 6: ARCHITECTURE & TECH STACK =================
with tab_tech:
    st.markdown("### Multi-Syllabus RAG Architecture & Technology Stack")
    
    st.markdown(
        """
        ### Technical Architecture Overview
        This system supports multi-syllabus ingestion, filtering, and proportional context retrieval across multiple courses and textbooks.
        """
    )
    
    col_f, col_b = st.columns(2)
    
    with col_f:
        st.markdown(
            """
            #### Frontend Technology Stack
            - <span class="tech-pill">Streamlit 1.61+</span> **Multi-Document Interactive Web Framework**
            - <span class="tech-pill">Executive CSS Design System</span> **Slate Layout, Minimalist Typography**
            - <span class="tech-pill">Google Fonts (Inter & Plus Jakarta Sans)</span> **Clean Executive Typography**
            - <span class="tech-pill">Scope Selector</span> **All Documents vs Single Document Filter**
            """,
            unsafe_allow_html=True
        )

    with col_b:
        st.markdown(
            """
            #### Backend Technology Stack & RAG Pipeline
            - <span class="tech-pill">Multi-Source Ingestion</span> **PDF, DOCX, PPTX, TXT support with overwrite protection**
            - <span class="tech-pill">Filtered Vector DB</span> **TF-IDF Vector Space Model with source-level filtering**
            - <span class="tech-pill">Proportional Aggregator</span> **Cross-Document context sampling for Roadmaps & Quizzes**
            - <span class="tech-pill">LLM Inference Backend</span> **Google Gemini API (`gemini-flash-latest`)**
            """,
            unsafe_allow_html=True
        )

st.markdown(
    """
    <div class="footer-text">
        Capstone Project: AI-Based Personalized Tutor Using RAG for Syllabus-Aligned Learning | Streamlit & Google Gemini
    </div>
    """,
    unsafe_allow_html=True
)
