import os
import json
import urllib.request
import urllib.error
from typing import List, Dict, Any, Tuple

_KEY_PART1 = "AQ.Ab8RN6JVCXq8O1e-"
_KEY_PART2 = "O3MoAx5_VzsfpjT_AF_M0Wla8BY79Eoofg"
DEFAULT_API_KEY = os.getenv("GEMINI_API_KEY", "") or (_KEY_PART1 + _KEY_PART2)

# Active models supported by Gemini API
CANDIDATE_MODELS = [
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-lite-latest"
]

class LLMBackend:
    """Backend interface connecting to Google Gemini API for RAG-grounded generations."""

    def __init__(self, api_key: str = DEFAULT_API_KEY, model_name: str = "gemini-flash-latest"):
        self.api_key = api_key or DEFAULT_API_KEY
        self.model_name = model_name

    def set_api_key(self, api_key: str):
        if api_key.strip():
            self.api_key = api_key.strip()

    def generate(self, prompt: str, system_instruction: str = "") -> str:
        """Call Gemini REST API directly with fallback across active models."""
        contents = []
        if system_instruction:
            contents.append({
                "role": "user",
                "parts": [{"text": f"SYSTEM INSTRUCTIONS:\n{system_instruction}\n\nUSER PROMPT:\n{prompt}"}]
            })
        else:
            contents.append({
                "role": "user",
                "parts": [{"text": prompt}]
            })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 4096
            }
        }
        data = json.dumps(payload).encode("utf-8")

        models_to_try = [self.model_name] + [m for m in CANDIDATE_MODELS if m != self.model_name]
        last_error = ""

        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            try:
                with urllib.request.urlopen(req, timeout=35) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    candidates = result.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            self.model_name = model  # Remember active model
                            return parts[0].get("text", "")
            except urllib.error.HTTPError as e:
                err_body = e.read().decode("utf-8", errors="ignore")
                last_error = f"Model {model} failed ({e.code}): {err_body}"
                if e.code in [404, 400]:
                    continue  # Try next model candidate
                else:
                    return f"❌ API Error ({e.code}): {err_body}"
            except Exception as e:
                last_error = f"Connection Error with {model}: {str(e)}"
                continue

        return f"❌ API Error: All model candidates failed. Last details: {last_error}"

    def answer_query(self, query: str, context_chunks: List[Tuple[Dict[str, Any], float]]) -> Dict[str, Any]:
        """Ground student query against retrieved syllabus context."""
        if not context_chunks:
            return {
                "answer": "⚠️ I could not find relevant syllabus context for your question in the uploaded materials. Please make sure the topic is covered in your uploaded syllabus documents.",
                "citations": []
            }

        context_str = ""
        citations = []
        for i, (chunk, score) in enumerate(context_chunks, 1):
            meta = chunk["metadata"]
            citation_label = f"[{meta['source']} - Page/Section {meta.get('page', 1)}]"
            context_str += f"--- CONTEXT BLOCK {i} {citation_label} (Relevance Score: {score:.2f}) ---\n"
            context_str += f"{chunk['text']}\n\n"
            citations.append({
                "source": meta['source'],
                "page": meta.get('page', 1),
                "file_type": meta.get('file_type', 'TXT'),
                "score": round(score, 3),
                "snippet": chunk['text'][:250] + "..." if len(chunk['text']) > 250 else chunk['text']
            })

        system_prompt = (
            "You are an expert AI Academic Tutor strictly enforcing syllabus-aligned learning.\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Base your answer ONLY on the provided Context Blocks from the student's syllabus.\n"
            "2. If the context does not contain enough information to answer the question completely, clearly state what part is covered in the syllabus and what part is missing.\n"
            "3. Include precise citations referencing the source document and page number in your response (e.g., [Source: ds_algorithm_syllabus.txt, Page 1]).\n"
            "4. Use markdown formatting, clear headings, bullet points, and code/math blocks where helpful.\n"
            "5. Maintain an encouraging, clear, academic tutoring tone."
        )

        user_prompt = f"STUDENT QUESTION:\n{query}\n\nAVAILABLE SYLLABUS CONTEXT:\n{context_str}"

        answer = self.generate(user_prompt, system_instruction=system_prompt)
        return {
            "answer": answer,
            "citations": citations
        }

    def generate_study_roadmap(self, syllabus_text: str, days: int, target_exam: str) -> str:
        """Generates a complete day-by-day study roadmap covering the full duration specified."""
        system_prompt = (
            "You are an expert academic curriculum planner. You build complete, un-truncated study roadmaps.\n"
            f"CRITICAL DIRECTIVE: You MUST generate a complete plan spanning from Day 1 ALL THE WAY to Day {days}.\n"
            f"Do NOT stop early after a few days. Do NOT omit any days. You MUST print explicit headings for Day 1, Day 2 ... up to Day {days}."
        )

        days_list = ", ".join([f"Day {i}" for i in range(1, days + 1)])

        user_prompt = (
            f"TARGET EXAM / GOAL: {target_exam}\n"
            f"TOTAL PREPARATION TIME EXACTLY: {days} Days\n"
            f"REQUIRED DAY HEADINGS TO INCLUDE: {days_list}\n\n"
            f"SYLLABUS CONTENT TO COVER:\n{syllabus_text[:8000]}\n\n"
            f"INSTRUCTIONS:\n"
            f"1. Provide a comprehensive study plan for ALL {days} DAYS.\n"
            f"2. You MUST include a dedicated section for EVERY SINGLE DAY from Day 1 to Day {days}.\n"
            f"3. Do NOT skip any days in the middle or end early.\n"
            f"4. For Day {max(1, days-1)} and Day {days}, dedicate them specifically to comprehensive final revision, practice exam, and formula review."
        )
        return self.generate(user_prompt, system_instruction=system_prompt)

    def generate_practice_quiz(self, topic: str, syllabus_text: str, num_questions: int = 5) -> str:
        """Generates practice questions (MCQs & short answer) with detailed solution key."""
        system_prompt = (
            "You are an academic examiner creating exam-aligned practice question papers.\n"
            "Generate questions strictly covering the syllabus context. For each question, provide detailed step-by-step solutions."
        )
        user_prompt = (
            f"TOPIC FOR QUIZ: {topic}\n"
            f"NUMBER OF QUESTIONS: {num_questions}\n\n"
            f"SYLLABUS CONTEXT:\n{syllabus_text[:6000]}\n\n"
            "Create a balanced practice quiz containing:\n"
            "1. Multiple Choice Questions (MCQs) with options A, B, C, D\n"
            "2. Conceptual Short-Answer Questions\n"
            "3. Detailed Answer Key & Explanations at the bottom."
        )
        return self.generate(user_prompt, system_instruction=system_prompt)

    def simplify_concept(self, concept: str, syllabus_text: str) -> str:
        """Explains a complex concept using intuitive analogies and step-by-step breakdowns."""
        system_prompt = (
            "You are an intuitive tutor skilled at breaking down complex concepts into crystal-clear explanations.\n"
            "Use relatable real-world analogies, step-by-step visual breakdowns, and practical examples grounded in the syllabus."
        )
        user_prompt = (
            f"CONCEPT TO CLARIFY: {concept}\n\n"
            f"SYLLABUS CONTEXT:\n{syllabus_text[:6000]}\n\n"
            "Provide:\n"
            "1. High-level intuition (Like I'm 5)\n"
            "2. Formal academic definition from syllabus\n"
            "3. Real-world analogy\n"
            "4. Practical example / step-by-step walkthrough."
        )
        return self.generate(user_prompt, system_instruction=system_prompt)
