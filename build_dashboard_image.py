import os
from PIL import Image, ImageDraw, ImageFont

def generate_dashboard_mockup(output_path="dashboard_mockup.png"):
    width, height = 1280, 720
    img = Image.new("RGB", (width, height), color="#0D1117")
    draw = ImageDraw.Draw(img)

    # Colors (Emerald & Amber Palette - Non Blue)
    COLOR_BG = "#0D1117"
    COLOR_PANEL = "#161B22"
    COLOR_BORDER = "#21262D"
    COLOR_EMERALD = "#10B981"
    COLOR_AMBER = "#F59E0B"
    COLOR_TEXT = "#F0F6FC"
    COLOR_MUTED = "#8B949E"

    try:
        title_font = ImageFont.truetype("arial.ttf", 26)
        heading_font = ImageFont.truetype("arial.ttf", 20)
        sub_font = ImageFont.truetype("arial.ttf", 15)
        text_font = ImageFont.truetype("arial.ttf", 13)
        bold_font = ImageFont.truetype("arialbd.ttf", 14)
        small_font = ImageFont.truetype("arial.ttf", 11)
    except:
        title_font = heading_font = sub_font = text_font = bold_font = small_font = ImageFont.load_default()

    # Sidebar (left panel)
    draw.rectangle([0, 0, 280, height], fill=COLOR_PANEL, outline=COLOR_BORDER, width=1)
    
    # Sidebar items
    draw.text((20, 20), "SYSTEM CONFIGURATION", fill=COLOR_EMERALD, font=bold_font)
    draw.rectangle((20, 45, 260, 75), fill=COLOR_BG, outline=COLOR_BORDER)
    draw.text((30, 52), "Google Gemini API Key: •••••••••", fill=COLOR_MUTED, font=small_font)

    draw.line((20, 90, 260, 90), fill=COLOR_BORDER, width=1)
    draw.text((20, 100), "DOCUMENT INGESTION HUB", fill=COLOR_TEXT, font=bold_font)
    draw.text((20, 120), "Upload Syllabi, Textbooks, PPTs", fill=COLOR_MUTED, font=small_font)
    
    # File drop area
    draw.rectangle((20, 140, 260, 200), fill=COLOR_BG, outline=COLOR_EMERALD, width=1)
    draw.text((40, 160), "Browse Files (PDF, DOCX, TXT, PPTX)", fill=COLOR_EMERALD, font=small_font)

    # Text paste expander
    draw.rectangle((20, 215, 260, 245), fill=COLOR_BORDER)
    draw.text((30, 225), "Or Paste Text / Notes Directly", fill=COLOR_TEXT, font=small_font)

    draw.line((20, 260, 260, 260), fill=COLOR_BORDER, width=1)
    draw.text((20, 270), "KNOWLEDGE BASE STATS", fill=COLOR_TEXT, font=bold_font)
    draw.text((20, 292), "• ds_algorithm_syllabus.txt", fill=COLOR_MUTED, font=small_font)
    draw.text((20, 310), "• ml_fundamentals_notes.pdf", fill=COLOR_MUTED, font=small_font)
    draw.text((20, 335), "Total Vector Chunks: 48", fill=COLOR_EMERALD, font=bold_font)
    draw.text((20, 355), "Vector Store Status: Indexed", fill=COLOR_EMERALD, font=bold_font)

    # Scope selector
    draw.text((20, 390), "TARGET SYLLABUS SCOPE", fill=COLOR_TEXT, font=bold_font)
    draw.rectangle((20, 410, 260, 440), fill=COLOR_BG, outline=COLOR_EMERALD)
    draw.text((30, 420), "All Documents (Combined)", fill=COLOR_TEXT, font=small_font)

    # Buttons
    draw.rectangle((20, 460, 130, 490), fill="#DC2626")
    draw.text((40, 470), "Clear DB", fill="#FFFFFF", font=bold_font)
    draw.rectangle((145, 460, 260, 490), fill=COLOR_EMERALD)
    draw.text((160, 470), "Sample Data", fill="#FFFFFF", font=bold_font)


    # Main Header Banner (Top Right Area)
    main_x = 300
    draw.rectangle((main_x, 20, width - 20, 100), fill=COLOR_PANEL, outline=COLOR_EMERALD, width=1)
    draw.rectangle((main_x + 20, 30, main_x + 260, 48), fill=COLOR_BORDER)
    draw.text((main_x + 25, 33), "ENTERPRISE SYLLABUS INTELLIGENCE PLATFORM", fill=COLOR_EMERALD, font=small_font)
    draw.text((main_x + 20, 52), "AI-Based Personalized Tutor", fill=COLOR_TEXT, font=title_font)
    draw.text((main_x + 360, 58), "Multi-Syllabus RAG for Aligned Learning", fill=COLOR_MUTED, font=sub_font)

    # Stat Metric Cards Row
    card_w = 225
    card_h = 70
    card_y = 115
    metrics = [
        ("2", "INGESTED DOCUMENTS", COLOR_EMERALD),
        ("48", "VECTOR CHUNKS", COLOR_EMERALD),
        ("Gemini Flash", "LLM ENGINE", COLOR_AMBER),
        ("All Documents", "ACTIVE SCOPE", COLOR_EMERALD)
    ]
    for idx, (val, lbl, color) in enumerate(metrics):
        cx = main_x + idx * (card_w + 15)
        draw.rectangle((cx, card_y, cx + card_w, card_y + card_h), fill=COLOR_PANEL, outline=COLOR_BORDER)
        draw.rectangle((cx, card_y, cx + card_w, card_y + 3), fill=color)
        draw.text((cx + 15, card_y + 12), val, fill=COLOR_TEXT, font=heading_font)
        draw.text((cx + 15, card_y + 45), lbl, fill=COLOR_MUTED, font=small_font)

    # Navigation Tabs
    tab_y = 200
    tabs = ["Instant Doubt Resolution", "Study Roadmap", "Practice Exam Builder", "Concept Clarifier", "Source Inspector"]
    tab_x = main_x
    for idx, tab_name in enumerate(tabs):
        tw = 180 if idx == 0 else 145
        bg_col = COLOR_EMERALD if idx == 0 else COLOR_PANEL
        txt_col = "#FFFFFF" if idx == 0 else COLOR_MUTED
        draw.rectangle((tab_x, tab_y, tab_x + tw, tab_y + 32), fill=bg_col, outline=COLOR_BORDER)
        draw.text((tab_x + 10, tab_y + 8), tab_name, fill=txt_col, font=small_font)
        tab_x += tw + 8

    # Tab Content Area (Instant Doubt Resolution Workspace)
    content_y = 245
    draw.text((main_x, content_y), "Multi-Syllabus Grounded Q&A", fill=COLOR_TEXT, font=heading_font)
    draw.text((main_x, content_y + 25), "Querying Scope: All Documents (Combined) | Grounded in uploaded course materials.", fill=COLOR_MUTED, font=small_font)

    # Chat Message 1 - User
    msg1_y = content_y + 55
    draw.rectangle((main_x, msg1_y, width - 20, msg1_y + 40), fill=COLOR_BORDER, outline="#30363D")
    draw.text((main_x + 15, msg1_y + 12), "Student: Explain the time complexity of Dijkstra's algorithm vs BST search.", fill=COLOR_TEXT, font=bold_font)

    # Chat Message 2 - Assistant Response
    msg2_y = msg1_y + 50
    draw.rectangle((main_x, msg2_y, width - 20, msg2_y + 240), fill=COLOR_PANEL, outline=COLOR_BORDER)
    draw.text((main_x + 15, msg2_y + 12), "AI Tutor (Grounded in Syllabus):", fill=COLOR_EMERALD, font=bold_font)
    
    resp_text = (
        "Based on your uploaded course syllabus (ds_algorithm_syllabus.txt):\n\n"
        "1. Dijkstra's Shortest Path Algorithm:\n"
        "   • Time Complexity: O((V + E) log V) using a Min-Heap / Priority Queue representation.\n"
        "   • Space Complexity: O(V) to maintain node distances and priority queue entries.\n\n"
        "2. Binary Search Tree (BST) Search:\n"
        "   • Average Time Complexity: O(log N) for balanced trees.\n"
        "   • Worst-Case Time Complexity: O(N) when the BST degenerates into a skewed linked list."
    )
    y_offset = msg2_y + 35
    for line in resp_text.split("\n"):
        draw.text((main_x + 15, y_offset), line, fill=COLOR_TEXT, font=small_font)
        y_offset += 16

    # Citation Card inside chat response
    cit_y = msg2_y + 160
    draw.rectangle((main_x + 15, cit_y, width - 40, cit_y + 65), fill=COLOR_BG, outline=COLOR_EMERALD)
    draw.rectangle((main_x + 25, cit_y + 10, main_x + 75, cit_y + 28), fill=COLOR_BORDER)
    draw.text((main_x + 32, cit_y + 13), "TXT", fill=COLOR_EMERALD, font=small_font)
    draw.text((main_x + 85, cit_y + 13), "Source: ds_algorithm_syllabus.txt (Page 1) | Relevance Score: 0.892", fill=COLOR_TEXT, font=bold_font)
    draw.text((main_x + 25, cit_y + 36), 'Snippet: "...Dijkstra algorithm: Greedy single-source shortest path, O((V+E) log V) with Min-Heap..."', fill=COLOR_MUTED, font=small_font)

    # Chat Input Box
    input_y = height - 55
    draw.rectangle((main_x, input_y, width - 20, input_y + 40), fill=COLOR_PANEL, outline=COLOR_EMERALD, width=1)
    draw.text((main_x + 15, input_y + 12), "Ask a question across your uploaded syllabus documents...", fill=COLOR_MUTED, font=text_font)

    img.save(output_path)
    print(f"Generated Emerald dashboard mockup screenshot: {output_path}")

if __name__ == "__main__":
    generate_dashboard_mockup()
