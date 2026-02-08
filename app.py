import streamlit as st
import os
from google import genai
from google.genai import types
from PIL import Image

# 1. PAGE SETUP
st.set_page_config(page_title="Ghost Engineer | Gemini 3", layout="wide")

# 2. INJECT CSS
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# 3. API INTEGRATION (Gemini 3 Pro)
API_KEY = "AIzaSyCZNXlQFbTp6a16r8I6Hz6U2-bSBgi4v9w"
client = genai.Client(api_key=API_KEY)

# 4. TOOL DEFINITION
def create_maintenance_ticket(part_name: str, urgency: str, observation: str):
    """Action: Logs an industrial repair ticket."""
    st.toast(f"Ticket Created for {part_name}", icon="🛠️")
    return {"status": "SUCCESS", "id": "GHOST-991"}

# 5. UI LAYOUT
st.markdown("""
    <div style="text-align: center; padding: 10px;">
        <h1 style="margin-bottom: 0;"> THE GHOST ENGINEER</h1>
        <p style="color: #00ffcc; font-size: 1.2rem;">Autonomous Multimodal Auditor | Powered by Gemini 3 Pro</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### VISUAL AUDIT FEED")
    img_file = st.file_uploader("Upload Component Image", type=["jpg", "png", "jpeg"])
    if img_file:
        st.image(img_file, use_container_width=True)
    
    st.markdown("### GROUNDING DATA")
    manual_file = st.file_uploader("Upload Service Manual (PDF)", type=["pdf"])

with col2:
    st.markdown("### AGENTIC REASONING")
    thought_area = st.empty()
    report_area = st.empty()

# 6. EXECUTION LOGIC (The Fix is Here)
if st.button("RUN FORENSIC AUDIT"):
    if img_file and manual_file:
        with st.spinner("Gemini 3 Pro is generating Thought Signatures..."):
            
            # --- THE FIX: PREPARE PDF DATA ---
            # We must convert the PDF to a Part with a mime_type
            pdf_bytes = manual_file.getvalue()
            pdf_part = types.Part.from_bytes(
                data=pdf_bytes,
                mime_type="application/pdf"
            )

            # --- THE FIX: PREPARE IMAGE DATA ---
            image_data = Image.open(img_file)

            # Gemini 3 Configuration
            config = types.GenerateContentConfig(
                tools=[create_maintenance_ticket],
                system_instruction="You are a mechanical auditor. Explain your reasoning deeply and use your tools if needed.",
                thinking_config=types.ThinkingConfig(include_thoughts=True, thinking_level="HIGH")
            )

            # API Call using the fixed pdf_part
            response = client.models.generate_content(
                model="gemini-3-pro-preview",
                contents=[
                    "Check this image against the provided service manual specifications.",
                    image_data,
                    pdf_part
                ],
                config=config
            )

            # 7. PARSE GEMINI 3 THOUGHT SIGNATURES
            thoughts = [p.text for p in response.candidates[0].content.parts if p.thought]
            final_text = "".join([p.text for p in response.candidates[0].content.parts if p.text])

            if thoughts:
                thought_area.info(f"**Internal Thoughts (System 2 Reasoning):**\n\n" + "\n".join(thoughts))
            
            if final_text:
                report_area.markdown(f"**Final Diagnosis:**\n\n{final_text}")
            else:
                report_area.warning("Audit complete. See internal thoughts for reasoning or tool calls.")
    else:
        st.error("Please provide both an image and a PDF manual.")