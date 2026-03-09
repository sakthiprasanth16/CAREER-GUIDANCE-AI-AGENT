# ========================
# CAREER GUIDANCE AI AGENT
# ========================
import streamlit as st
import google.generativeai as genai
import os

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Career Guidance AI",
    page_icon="🎯",
    layout="centered"
)

# ============================================
# PROFESSIONAL CSS
# ============================================
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #f8fafc;
    }
    
    /* Main Container */
    .main-container {
        max-width: 900px;
        margin: 1rem auto;
        padding: 2rem 2rem 1.5rem 2rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.05);
    }
    
    /* Title */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }
    
    .main-title span {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Chat Messages */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .user-message {
        background: #2563eb;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 4px 20px;
        max-width: 80%;
        margin-left: auto;
        line-height: 1.5;
        font-size: 0.95rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    .assistant-message {
        background: #f1f5f9;
        color: #0f172a;
        padding: 1.2rem 1.8rem;
        border-radius: 20px 20px 20px 4px;
        max-width: 85%;
        line-height: 1.6;
        font-size: 0.95rem;
        border-left: 4px solid #2563eb;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    
    /* Status Badges */
    .status-container {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    .badge {
        padding: 0.5rem 1.2rem;
        border-radius: 100px;
        font-size: 0.9rem;
        font-weight: 500;
        background: white;
        border: 1px solid #e2e8f0;
        color: #334155;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    .badge.name {
        background: #dbeafe;
        border-color: #2563eb;
        color: #1e40af;
    }
    
    .badge.role {
        background: #f3e8ff;
        border-color: #9333ea;
        color: #6b21a8;
    }
    
    .badge.ready {
        background: #dcfce7;
        border-color: #16a34a;
        color: #166534;
    }
    
    /* Button */
    .stButton > button {
        background: white;
        color: #2563eb;
        border: 2px solid #2563eb;
        padding: 0.6rem 1.5rem;
        border-radius: 100px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s;
        width: auto;
        margin: 0 auto;
    }
    
    .stButton > button:hover {
        background: #2563eb;
        color: white;
        border-color: #2563eb;
    }
    
    /* Quick Action Buttons */
    .quick-actions {
        display: flex;
        gap: 0.75rem;
        justify-content: center;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }
    
    /* Tips Box */
    .tips-box {
        background: #f0f9ff;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0 0.5rem 0;
        border-left: 4px solid #2563eb;
    }
    
    .tips-box h4 {
        color: #2563eb;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .tips-content {
        color: #334155;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .tips-content p {
        margin: 0.5rem 0;
    }
    
    /* Section Headers in Responses */
    .assistant-message h1, .assistant-message h2, .assistant-message h3 {
        color: #0f172a;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .assistant-message h2 {
        font-size: 1.3rem;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.3rem;
    }
    
    .assistant-message h3 {
        font-size: 1.1rem;
        color: #2563eb;
    }
    
    /* Chat Input */
    .stChatInputContainer {
        border: 2px solid #e2e8f0;
        border-radius: 100px;
        padding: 0.25rem;
        margin-top: 1rem;
    }
    
    .stChatInputContainer:focus-within {
        border-color: #2563eb;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MAIN CONTAINER
# ============================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
st.markdown('<div class="main-title"><span>Career Guidance AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your personal AI career counselor</div>', unsafe_allow_html=True)

# ============================================
# API KEY CONFIGURATION
# ============================================
def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY", None)
        except:
            pass
    return api_key

API_KEY = get_api_key()

# ============================================
# MODEL CONFIGURATION
# ============================================
MODEL_NAME = "gemini-2.5-flash"
TEMPERATURE = 0.7
MAX_TOKENS = 3000  # INCREASED TOKEN LIMIT FOR COMPLETE RESPONSES

# ============================================
# SESSION STATE
# ============================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "job_role" not in st.session_state:
    st.session_state.job_role = None
if "stage" not in st.session_state:
    st.session_state.stage = "awaiting_name"
if "guidance_provided" not in st.session_state:
    st.session_state.guidance_provided = False
if "quick_action_clicked" not in st.session_state:
    st.session_state.quick_action_clicked = False
if "quick_action_prompt" not in st.session_state:
    st.session_state.quick_action_prompt = None

# ============================================
# API KEY CHECK
# ============================================
if not API_KEY:
    st.error("⚠️ Google API Key not found. Please add GOOGLE_API_KEY to secrets.")
    st.stop()

# ============================================
# STATUS BADGES
# ============================================
if st.session_state.user_name or st.session_state.job_role:
    st.markdown('<div class="status-container">', unsafe_allow_html=True)
    if st.session_state.user_name:
        st.markdown(f'<span class="badge name">👤 {st.session_state.user_name}</span>', unsafe_allow_html=True)
    if st.session_state.job_role:
        st.markdown(f'<span class="badge role">🎯 {st.session_state.job_role}</span>', unsafe_allow_html=True)
    if st.session_state.guidance_provided:
        st.markdown('<span class="badge ready">✓ Ready for questions</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# WELCOME MESSAGE
# ============================================
if st.session_state.stage == "awaiting_name" and not st.session_state.messages:
    welcome = "👋 Hello! I'm your Career Guidance AI. What's your name?"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# ============================================
# RESET BUTTON
# ============================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 New Conversation"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ============================================
# CHAT HISTORY
# ============================================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# QUICK ACTIONS
# ============================================
if st.session_state.stage == "chatting" and st.session_state.guidance_provided:
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 Best courses?", key="courses_btn", use_container_width=True):
            st.session_state.quick_action_prompt = "What are the best courses for this role? Give a complete list with platform names and brief descriptions. Provide full sentences and complete information."
            st.session_state.quick_action_clicked = True
            st.rerun()
    with col2:
        if st.button("💰 Salary range?", key="salary_btn", use_container_width=True):
            st.session_state.quick_action_prompt = "What is the salary range for this role in Indian Rupees (INR)? Include Entry Level (0-2 years), Mid Level (3-5 years), and Senior Level (5+ years). Give approximate ranges for Indian market. Provide complete sentences and full details for each level."
            st.session_state.quick_action_clicked = True
            st.rerun()
    with col3:
        if st.button("🎯 Interview tips?", key="interview_btn", use_container_width=True):
            st.session_state.quick_action_prompt = "Give me complete interview tips for this role. Include preparation, technical questions, behavioral questions, and follow-up steps. Provide full sentences and complete information for each section."
            st.session_state.quick_action_clicked = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TIPS SECTION
# ============================================
st.markdown("""
<div class="tips-box">
    <h4>💡 Pro Tips for Best Results</h4>
    <div class="tips-content">
        <p>✨ <strong>Be specific</strong> - Instead of "developer", say "React frontend developer"</p>
        <p>✨ <strong>Ask follow-ups</strong> - Get deeper insights after initial guidance</p>
        <p>✨ <strong>Mention experience</strong> - "I'm a fresher" or "I have 3 years experience" for tailored advice</p>
        <p>✨ <strong>Try quick buttons above</strong> for instant answers on popular topics</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# MAIN CHAT LOGIC
# ============================================
# Check if quick action was clicked
if st.session_state.quick_action_clicked and st.session_state.quick_action_prompt:
    prompt = st.session_state.quick_action_prompt
    st.session_state.quick_action_clicked = False
    st.session_state.quick_action_prompt = None
else:
    prompt = st.chat_input("Type your message here...")

if prompt:
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config=genai.types.GenerationConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_TOKENS
            )
        )
        
        with st.spinner("Thinking..."):
            
            # STAGE 1: Getting name
            if st.session_state.stage == "awaiting_name":
                st.session_state.user_name = prompt.strip()
                st.session_state.stage = "awaiting_role"
                response = f"Nice to meet you, {st.session_state.user_name}! 🎯 What job role are you interested in?"
            
            # STAGE 2: Getting role and generating guidance - COMPLETE SENTENCES
            elif st.session_state.stage == "awaiting_role":
                st.session_state.job_role = prompt.strip()
                st.session_state.stage = "chatting"
                
                # PROMPT WITH INSTRUCTION FOR COMPLETE SENTENCES
                career_prompt = f"""You are a career counselor. Give COMPLETE guidance for {st.session_state.user_name} who wants to become a {st.session_state.job_role}.

IMPORTANT INSTRUCTIONS:
1. Use COMPLETE SENTENCES throughout - no bullet points without explanation
2. Every bullet point must be a complete sentence with proper punctuation
3. Provide FULL information without cutting off
4. Make it detailed but clear

Format with these sections:

## 🎯 Required Skills

**Technical Skills** (8-10 items):
- Each skill must be a complete sentence explaining what it is and why it's important. Example: "Python programming is essential because it's the primary language used for data manipulation, machine learning, and building analytical models in the industry."

**Soft Skills** (5 items only):
- Each soft skill must be a complete sentence explaining why it matters. Example: "Problem-solving ability is crucial because you will frequently encounter complex challenges that require analytical thinking to find effective solutions."

## 📚 Education & Qualifications

**Minimum Requirements:**
- Complete sentence about educational background needed

**Recommended Path:**
- Complete sentences about best degrees and certifications
- Complete sentences about alternative routes

## 💼 Key Responsibilities

**Daily Tasks** (5-7 items):
- Each task must be a complete sentence describing what you actually do. Example: "You will design and maintain data pipelines that collect, process, and store large volumes of structured and unstructured data from various sources."

**What This Role Does:**
- 2-3 complete sentences explaining the role and its business impact

**A Typical Day Looks Like:**
- Complete sentences describing morning, afternoon, and evening activities

## 🎯 Interview Guide (5 Steps)

**Step 1: Preparation Phase** - Complete sentences
**Step 2: Application Strategy** - Complete sentences
**Step 3: Technical Interview** - Complete sentences
**Step 4: Behavioral Interview** - Complete sentences
**Step 5: Follow-up** - Complete sentences

## 📖 Learning Resources

**Best Courses** (5 with platforms) - Complete sentences
**Essential Books** (5 must-read) - Complete sentences
**Practice Platforms** (3-4 websites) - Complete sentences

## 💰 Salary (Indian Rupees - INR)

- Entry Level (0-2 years): Complete sentence with approximate range
- Mid Level (3-5 years): Complete sentence with approximate range
- Senior Level (5+ years): Complete sentence with approximate range

Make it practical, encouraging, and tailored to {st.session_state.job_role}."""
                
                ai_response = model.generate_content(career_prompt)
                
                if ai_response and ai_response.text:
                    response = f"## Career Guidance: {st.session_state.job_role}\n\n{ai_response.text}\n\n---\nFeel free to ask me anything else about this career path!"
                    st.session_state.guidance_provided = True
                else:
                    response = f"I'll help you become a {st.session_state.job_role}. What specific aspect would you like to know about?"
            
            # STAGE 3: Follow-up questions - FIXED FOR COMPLETE ANSWERS
            else:
                followup = f"""Help {st.session_state.user_name} become a {st.session_state.job_role}.
Question: "{prompt}"

IMPORTANT INSTRUCTIONS:
1. Use COMPLETE SENTENCES throughout
2. Provide FULL information without cutting off
3. Every point must be a complete thought with explanation
4. Be specific and practical with examples
5. If this is about salary, provide complete ranges for all levels in INR
6. If this is about courses, list platforms with complete descriptions
7. If this is about interview tips, cover all steps completely

Give a comprehensive answer that the user can fully understand."""
                
                ai_response = model.generate_content(followup)
                
                if ai_response and ai_response.text:
                    # Check if response is cut off (ends with incomplete sentence)
                    response_text = ai_response.text
                    
                    # Add a check for completeness
                    if response_text.strip() and not response_text.strip().endswith(('.', '!', '?')):
                        # If response ends without punctuation, generate continuation
                        continuation_prompt = f"""Continue answering the previous question: "{prompt}" for {st.session_state.job_role} role.
                        
Complete the answer with full sentences. Do not leave any point incomplete."""
                        continuation = model.generate_content(continuation_prompt)
                        if continuation and continuation.text:
                            response_text += " " + continuation.text
                    
                    response = response_text
                else:
                    response = "I couldn't generate a complete response. Please try asking in a different way."
        
        # Add response
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

# ============================================
# CLOSE MAIN CONTAINER
# ============================================
st.markdown('</div>', unsafe_allow_html=True)
