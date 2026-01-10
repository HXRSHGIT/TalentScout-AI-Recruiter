import streamlit as st
import os
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
from textblob import TextBlob

# --- PROMPTS ---
MOCK_INTERVIEW_PROMPT = """
You are "TalentCoach," a strict but helpful Technical Interviewer.
1. Ask the candidate for their **Job Role** and **Tech Stack**.
2. Once you have that, ask ONE relevant, challenging technical question.
3. Wait for their answer.
4. Provide brief feedback (Strong/Weak) and then ask the NEXT technical question immediately.
Keep it strictly technical and professional.
"""

CAREER_GUIDE_PROMPT = """
You are "CareerGuide," an expert Tech Career Counselor.
1. The user will ask about a specific **Job Role** (e.g., "DevOps Engineer").
2. You must provide:
   - 📋 **Job Description**: A concise summary of what they do.
   - 🛠️ **Required Tech Stack**: The essential tools/languages to learn.
   - 🗺️ **Learning Path**: A step-by-step guide (Beginner -> Advanced).
3. Be structured, encouraging, and highly detailed.
"""

# 1. Setup & Config
load_dotenv()
st.set_page_config(
    page_title="TalentScout AI", 
    page_icon="✨", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. THE GEMINI UI STYLING
st.markdown("""
    <style>
    /* GLOBAL THEME */
    .stApp {
        background-color: #131314; 
        color: #E3E3E3;
    }
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #1E1F20 !important; 
        border-right: 1px solid #333;
    }

    /* FIX: SAFER SIDEBAR SPACING */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* CHAT INPUT */
    .stChatInputContainer {
        padding-bottom: 20px;
        background-color: transparent !important;
    }
    
    .stChatInputContainer textarea {
        background-color: #282A2C !important; 
        color: white !important;
        border: 1px solid #363739 !important;
        border-radius: 40px !important; 
        padding: 15px 25px !important;
    }
    
    .stChatInputContainer textarea:focus {
        border: 1px solid #555 !important;
        box-shadow: none !important;
    }

    /* WELCOME SCREEN TYPOGRAPHY */
    .welcome-text {
        font-family: 'Google Sans', sans-serif;
        background: -webkit-linear-gradient(45deg, #4285F4, #9B72CB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 3.5rem;
    }
    
    .sub-text {
        color: #6d6e70;
        font-size: 2rem;
        font-weight: 500;
    }

    /* CHAT BUBBLES */
    div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stChatMessageContent"] {
        background-color: #282A2C !important;
        border-radius: 20px;
        color: #E3E3E3;
    }

    div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #E3E3E3;
    }

    /* --- BUTTON STYLING (BIGGER FOR MAIN SCREEN) --- */
    .stButton button {
        background-color: #282A2C !important; 
        color: #E3E3E3 !important;
        border: 1px solid #363739 !important;
        border-radius: 15px !important;
        padding: 15px 30px !important; 
        font-size: 18px !important;    
        font-weight: 600 !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton button:hover {
        background-color: #4285F4 !important; 
        color: white !important;
        border-color: #4285F4 !important;
        transform: translateY(-2px);
    }

    /* --- SIDEBAR/TOP BUTTON OVERRIDE (KEEP SMALL) --- */
    [data-testid="stSidebar"] .stButton button, 
    div[data-testid="stHorizontalBlock"] .stButton button {
        padding: 8px 15px !important;
        font-size: 14px !important;
        border-radius: 10px !important;
    }

    /* METRIC CARDS IN SIDEBAR */
    .info-box {
        background-color: #282A2C;
        padding: 12px 15px;
        border-radius: 12px;
        border-left: 4px solid #4285F4; 
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .info-box:hover {
        transform: translateX(5px);
    }
    .info-label { 
        font-size: 11px; 
        text-transform: uppercase; 
        color: #888; 
        margin-bottom: 4px; 
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .info-value { 
        font-size: 14px; 
        font-weight: 500; 
        color: #fff; 
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* --- REVIEW CARD HOVER EFFECTS --- */
    .review-card {
        background-color: #1E1F20;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #333;
        flex: 1;
        min-width: 280px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .review-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        border-color: #4285F4;
    }

    /* PULSING DOT ANIMATION */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    .live-dot {
        height: 8px;
        width: 8px;
        background-color: #4ade80; /* Green */
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
        animation: pulse 2s infinite;
    }
    
    /* Custom Headers */
    .mode-header {
        font-family: 'Google Sans', sans-serif;
        font-size: 28px;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #4ade80, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-align: center;
    }
    .mock-header {
        font-family: 'Google Sans', sans-serif;
        font-size: 28px;
        font-weight: bold;
        background: -webkit-linear-gradient(45deg, #4ade80, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 20px;
        text-align: center;
    }

    /* --- HEADER VISIBILITY FIX --- */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Logic: Context-Aware Data Extraction
def extract_info(user_text):
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', user_text)
    phone_match = re.search(r'\b\d{10}\b', user_text)
    
    if email_match:
        st.session_state.candidate_data['Email'] = email_match.group(0)
    if phone_match:
        st.session_state.candidate_data['Phone'] = phone_match.group(0)
    
    if len(st.session_state.messages) >= 1:
        last_msg = st.session_state.messages[-1]
        if isinstance(last_msg, AIMessage):
            last_ai_msg = last_msg.content.lower()
            if "name" in last_ai_msg and len(user_text) < 50:
                 st.session_state.candidate_data['Name'] = user_text.strip()
            if any(x in last_ai_msg for x in ["role", "position", "job", "applying"]) and len(user_text) < 100:
                 st.session_state.candidate_data['Role'] = user_text.strip()
            if any(x in last_ai_msg for x in ["stack", "technologies", "language", "tools"]) and len(user_text) < 150:
                 st.session_state.candidate_data['Stack'] = user_text.strip()

# --- UPGRADED SENTIMENT ENGINE ---
def get_sentiment(text):
    text_lower = text.lower()
    nervous_triggers = ["maybe", "i think", "not sure", "i guess", "probably", "um", "uh", "sort of", "little bit", "struggle", "confused"]
    confident_triggers = ["expert", "led", "built", "deployed", "highly proficient", "mastered", "definitely", "absolutely", "specialist", "managed", "created"]
    
    if any(word in text_lower for word in nervous_triggers): return "Nervous 😟"
    if any(word in text_lower for word in confident_triggers): return "Confident 🚀"

    blob = TextBlob(text)
    if blob.sentiment.polarity > 0.15: return "Confident 🚀"
    elif blob.sentiment.polarity < 0.0: return "Nervous 😟"
    return "Neutral 😐"

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API Key missing.")
    st.stop()

llm = ChatGroq(temperature=0.5, model_name="llama-3.3-70b-versatile", groq_api_key=api_key)

# Initialize Session States
if "mode" not in st.session_state: st.session_state.mode = "screening"
if "show_home" not in st.session_state: st.session_state.show_home = True
if "messages" not in st.session_state: st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
if "mock_messages" not in st.session_state: st.session_state.mock_messages = [SystemMessage(content=MOCK_INTERVIEW_PROMPT)]
if "role_messages" not in st.session_state: st.session_state.role_messages = [SystemMessage(content=CAREER_GUIDE_PROMPT)]
if "sentiment" not in st.session_state: st.session_state.sentiment = "Neutral 😐"
if "candidate_data" not in st.session_state:
    st.session_state.candidate_data = {
        "Name": "Pending...", "Email": "Pending...", "Phone": "Pending...", "Role": "Pending...", "Stack": "Pending..."
    }

# ==========================================
# 4. SIDEBAR (ALWAYS RENDER FIRST)
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px; margin-top: 10px;">
            <div style="background: linear-gradient(135deg, #4285F4, #9B72CB); padding: 8px; border-radius: 10px;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
            </div>
            <div>
                <h1 style="margin: 0; font-size: 22px; font-weight: 700; color: white; line-height: 1.0;">TalentScout</h1>
                <p style="margin: 0; margin-top: -4px; font-size: 11px; color: #888; letter-spacing: 1px;">AI RECRUITER</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("➕ Start New Session", use_container_width=True):
        st.session_state.mode = "screening"
        st.session_state.show_home = True
        st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
        st.session_state.candidate_data = {k: "Pending..." for k in st.session_state.candidate_data}
        st.session_state.sentiment = "Neutral 😐"
        st.rerun() 
    
    if st.button("🎓 Mock Interview", use_container_width=True):
        st.session_state.mode = "mock"
        st.session_state.show_home = False 
        if len(st.session_state.mock_messages) == 1:
            # EXPLANATORY INTRO FOR MOCK INTERVIEW
            st.session_state.mock_messages.append(AIMessage(content="**Welcome to the Technical Interview Simulator!** ⚔️\n\nIn this mode, I will act as a strict technical coach. I'll ask you challenging questions specific to your stack to test your knowledge.\n\nTo begin, please tell me the **Job Role** you are targeting and your **Tech Stack**."))
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 10px; color: #888; font-size: 12px; font-weight: 600; letter-spacing: 1px;">
            <span class="live-dot"></span> LIVE DATA CAPTURE
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="info-box"><div class="info-label">CANDIDATE NAME</div><div class="info-value">{st.session_state.candidate_data['Name']}</div></div>
        <div class="info-box"><div class="info-label">EMAIL ADDRESS</div><div class="info-value">{st.session_state.candidate_data['Email']}</div></div>
        <div class="info-box"><div class="info-label">PHONE NUMBER</div><div class="info-value">{st.session_state.candidate_data['Phone']}</div></div>
        <div class="info-box"><div class="info-label">TARGET ROLE</div><div class="info-value">{st.session_state.candidate_data['Role']}</div></div>
        <div class="info-box"><div class="info-label">TECH STACK</div><div class="info-value">{st.session_state.candidate_data['Stack']}</div></div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-bottom: 10px; color: #888; font-size: 12px; font-weight: 600; letter-spacing: 1px;">
            🤖 AI ANALYSIS
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(66, 133, 244, 0.1), rgba(155, 114, 203, 0.1)); border: 1px solid rgba(66, 133, 244, 0.2); border-radius: 12px; padding: 15px; text-align: center;">
            <div style="font-size: 11px; color: #aaa; text-transform: uppercase; margin-bottom: 5px;">Candidate Vibe</div>
            <div style="font-size: 18px; font-weight: 700; color: #fff;">{st.session_state.sentiment}</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. MAIN CONTENT
# ==========================================
if st.session_state.mode == "screening":
    
    if st.session_state.show_home:
        # --- HOME SCREEN ---
        
        current_name = st.session_state.candidate_data['Name']
        if current_name == "Pending...":
             greeting_text = "Welcome to TalentScout!"
        else:
             first_name = current_name.split()[0]
             greeting_text = f"Hey, {first_name} :)"

        st.markdown(f"""
            <div style='text-align: left; padding-left: 10%; margin-top: 20px;'>
                <span class='welcome-text'>{greeting_text}</span><br>
                <span class='sub-text' style='color: #444746;'>Ready to validate your technical skills?</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1: 
            if st.button("🚀 Start Screening", use_container_width=True):
                st.session_state.show_home = False 
                if len(st.session_state.messages) == 1:
                    # EXPLANATORY INTRO FOR SCREENING
                    greeting = "**Welcome to Screening Mode!** 🕵️\n\nIn this mode, I will act as a recruiter to gather your details and validate your background.\n\nTo get started, could you please provide your **Full Name**?"
                    st.session_state.messages.append(AIMessage(content=greeting))
                st.rerun()

        with col2: 
            if st.button("📄 Update Profile", use_container_width=True):
                st.session_state.mode = "profile"
                st.session_state.show_home = False
                st.rerun()

        with col3: 
            if st.button("ℹ️ Curate Roadmap", use_container_width=True):
                st.session_state.mode = "role_insight"
                st.session_state.show_home = False
                if len(st.session_state.role_messages) == 1:
                    # EXPLANATORY INTRO FOR ROADMAP
                    st.session_state.role_messages.append(AIMessage(content="**Welcome to Career Roadmap Mode!** 🗺️\n\nIn this mode, I will help you define a clear learning path. Tell me the **Job Role** you are interested in (e.g., 'Full Stack Developer'), and I will generate a Job Description, Tech Stack, and Learning Path for you."))
                st.rerun()
        
        # --- SOCIAL PROOF SECTION ---
        st.markdown("""
<hr style="border-color: #333; margin-top: 60px; margin-bottom: 40px; opacity: 0.3;">
<div style="text-align: center; margin-bottom: 40px;">
    <h3 style="color: #E3E3E3; font-family: 'Google Sans', sans-serif; font-weight: 500; margin-bottom: 8px; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px;">Trusted by millions across the globe in their job search and prep 🌍</h3>
    <p style="color: #888; font-size: 14px; margin: 0;">Join the community acing their technical interviews.</p>
</div>
<div style="display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;">
    <div class="review-card">
        <div style="color: #FFD700; font-size: 18px; margin-bottom: 12px;">★★★★★</div>
        <p style="color: #CCCCCC; font-size: 14px; line-height: 1.6; font-style: italic; margin-bottom: 20px;">"The mock interview mode is brutal but necessary. It actually prepared me for the curveball questions I got at Amazon."</p>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #4285F4, #2b5cbf); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">A</div>
            <div>
                <div style="color: #FFF; font-size: 13px; font-weight: 600;">Harsh Thakur</div>
                <div style="color: #777; font-size: 11px;">Backend Dev</div>
            </div>
        </div>
    </div>
    <div class="review-card">
        <div style="color: #FFD700; font-size: 18px; margin-bottom: 12px;">★★★★★</div>
        <p style="color: #CCCCCC; font-size: 14px; line-height: 1.6; font-style: italic; margin-bottom: 20px;">"I love the career path feature. It gave me a clear roadmap for moving from Junior to Senior Data Scientist."</p>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #9B72CB, #6a4c9c); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">P</div>
            <div>
                <div style="color: #FFF; font-size: 13px; font-weight: 600;">Priya S.</div>
                <div style="color: #777; font-size: 11px;">Data Scientist</div>
            </div>
        </div>
    </div>
    <div class="review-card">
        <div style="color: #FFD700; font-size: 18px; margin-bottom: 12px;">★★★★★</div>
        <p style="color: #CCCCCC; font-size: 14px; line-height: 1.6; font-style: italic; margin-bottom: 20px;">"Finally, a recruiter bot that doesn't feel robotic. The vibe analysis helped me realize I sounded too nervous."</p>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 35px; height: 35px; background: linear-gradient(135deg, #4ade80, #2b9e58); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: white;">M</div>
            <div>
                <div style="color: #FFF; font-size: 13px; font-weight: 600;">Sargun Madan</div>
                <div style="color: #777; font-size: 11px;">Full Stack</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    else:
        top_c1, top_c2 = st.columns([6, 1])
        with top_c2:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.show_home = True
                st.rerun()
        
        for msg in st.session_state.messages:
            if isinstance(msg, AIMessage):
                with st.chat_message("assistant", avatar="✨"):
                    st.write(msg.content)
            elif isinstance(msg, HumanMessage):
                with st.chat_message("user", avatar="👤"):
                    st.write(msg.content)

        if user_input := st.chat_input("Message TalentScout..."):
            extract_info(user_input)
            st.session_state.sentiment = get_sentiment(user_input)
            st.session_state.messages.append(HumanMessage(content=user_input))
            
            with st.spinner("Analyzing..."):
                response = llm.invoke(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))
            st.rerun()

elif st.session_state.mode == "mock":
    st.markdown("<div class='mock-header'>🎓 Technical Interview Simulator</div>", unsafe_allow_html=True)
    
    if st.button("🏠 Back to Home"):
        st.session_state.mode = "screening"
        st.session_state.show_home = True
        st.rerun()

    for msg in st.session_state.mock_messages:
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🎓"): 
                st.write(msg.content)
        elif isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="👨‍💻"): 
                st.write(msg.content)

    if user_input := st.chat_input("Enter your answer..."):
        st.session_state.mock_messages.append(HumanMessage(content=user_input))
        with st.spinner("Coach is analyzing..."):
            response = llm.invoke(st.session_state.mock_messages)
            st.session_state.mock_messages.append(AIMessage(content=response.content))
        st.rerun()

elif st.session_state.mode == "role_insight":
    st.markdown("<div class='mode-header'>🗺️ Career Path & Role Insights</div>", unsafe_allow_html=True)
    
    if st.button("← Back to Home"):
        st.session_state.mode = "screening"
        st.session_state.show_home = True
        st.rerun()

    for msg in st.session_state.role_messages:
        if isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar="🧭"): st.write(msg.content)
        elif isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="👤"): st.write(msg.content)
            
    if user_input := st.chat_input("Enter a Job Role (e.g. Data Scientist)..."):
        st.session_state.role_messages.append(HumanMessage(content=user_input))
        with st.spinner("Generating Career Roadmap..."):
            response = llm.invoke(st.session_state.role_messages)
            st.session_state.role_messages.append(AIMessage(content=response.content))
        st.rerun()

elif st.session_state.mode == "profile":
    st.markdown("<div class='mode-header'>📝 Update Candidate Profile</div>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        st.markdown("### Edit Your Details")
        new_name = st.text_input("Full Name", value=st.session_state.candidate_data['Name'])
        new_email = st.text_input("Email Address", value=st.session_state.candidate_data['Email'])
        new_phone = st.text_input("Phone Number", value=st.session_state.candidate_data['Phone'])
        new_role = st.text_input("Target Role", value=st.session_state.candidate_data['Role'])
        new_stack = st.text_input("Tech Stack", value=st.session_state.candidate_data['Stack'])
        
        submitted = st.form_submit_button("💾 Save Changes")
        
        if submitted:
            st.session_state.candidate_data['Name'] = new_name
            st.session_state.candidate_data['Email'] = new_email
            st.session_state.candidate_data['Phone'] = new_phone
            st.session_state.candidate_data['Role'] = new_role
            st.session_state.candidate_data['Stack'] = new_stack
            st.success("Profile Updated Successfully!")
            st.session_state.mode = "screening"
            st.session_state.show_home = True
            st.rerun()
            
    if st.button("Cancel"):
        st.session_state.mode = "screening"
        st.session_state.show_home = True
        st.rerun()