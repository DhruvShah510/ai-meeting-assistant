import streamlit as st
import requests

# ==============================
# CONFIG
# ==============================
st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🤖",
    layout="wide"
)

API_TEXT_URL = "http://127.0.0.1:8000/summarize"
API_FILE_URL = "http://127.0.0.1:8000/summarize-file"

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.title("⚙️ Settings")
    st.markdown("This tool summarizes meetings using Llama 3.3 (Groq).")
    st.markdown("### Input Options:")
    st.markdown("- Paste transcript manually\n- Upload .txt file")
    st.markdown("---")
    st.write("Developed by **Dhruv Shah**")

# ==============================
# HEADER
# ==============================
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>
        🤖 AI Meeting Assistant
    </h1>
    <p style='text-align: center; font-size: 18px;'>
        Generate summaries, action items, decisions, and follow-up emails instantly.
    </p>
    """,
    unsafe_allow_html=True
)

# ==============================
# INPUT AREA
# ==============================
st.subheader("📥 Enter Meeting Transcript")

input_option = st.radio(
    "Choose input method:",
    ["Paste Text", "Upload File"],
    horizontal=True
)

transcript_text = None
file = None

if input_option == "Paste Text":
    transcript_text = st.text_area(
        "Paste your meeting transcript below:",
        height=300,
        placeholder="Paste raw meeting text here..."
    )

else:
    file = st.file_uploader("Upload a .txt file", type=["txt"])

# ==============================
# SUBMIT BUTTON
# ==============================
st.write("")
submit = st.button("🚀 Generate Summary", use_container_width=True)

# ==============================
# CALL BACKEND API
# ==============================
if submit:
    if input_option == "Paste Text" and not transcript_text.strip():
        st.error("Please enter a transcript.")
    
    elif input_option == "Upload File" and file is None:
        st.error("Please upload a .txt file.")
    
    else:
        with st.spinner("Analyzing meeting transcript... ⏳"):
            try:
                # ---- Call correct API ----
                if input_option == "Paste Text":
                    payload = {"transcript_text": transcript_text}
                    response = requests.post(API_TEXT_URL, json=payload)

                else:
                    response = requests.post(
                        API_FILE_URL,
                        files={"file": file}
                    )

                if response.status_code != 200:
                    st.error(f"API Error: {response.text}")
                else:
                    result = response.json()

                    # ==============================
                    # DISPLAY RESULTS
                    # ==============================
                    st.success("Analysis Complete ✅")

                    # --- Summary ---
                    st.markdown("### 📝 Summary")
                    st.markdown(
                        f"""
                        <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                            <p style="font-size: 16px; color: #222;">{result['summary']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # --- Action Items ---
                    st.markdown("### 📌 Action Items")
                    for item in result["action_items"]:
                        st.markdown(
                            f"""
                            <div style="background-color: #E3F2FD; padding: 12px; border-radius: 8px; margin-bottom: 5px; color: #222;">
                                <b>Task:</b> {item['task']}<br>
                                <b>Assigned To:</b> {item['assigned_to']}<br>
                                <b>Assigned By:</b> {item['assigned_by']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    # # --- Decisions ---
                    # st.markdown("### 🧠 Decisions Made")
                    # st.markdown(
                    #     f"""
                    #     <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; color: #222;">
                    #         <ul>
                    #             {''.join([f"<li>{d}</li>" for d in result['decisions']])}
                    #         </ul>
                    #     </div>
                    #     """,
                    #     unsafe_allow_html=True
                    # )
                    decision_items_html = ""

                    for d in result["decisions"]:
                        decision_items_html += f"<li>{d['decision']}</li>"
                        
                    st.markdown("### 🧠 Decisions Made")

                    st.markdown(
                        f"""
                        <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; color: #222;">
                            <ul style="margin: 0;">
                                {decision_items_html}
                            </ul>
                        </div>
                        """,
                        unsafe_allow_html=True)


                    # --- Follow-up Email ---
                    st.markdown("### 📧 Follow-Up Email")
                    st.markdown(
                        f"""
                        <div style="background-color: #FCE4EC; padding: 15px; border-radius: 10px; color: #222;">
                            <pre style="white-space: pre-wrap;">{result['follow_up_email']}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            except Exception as e:
                st.error(f"Frontend Error: {e}")
