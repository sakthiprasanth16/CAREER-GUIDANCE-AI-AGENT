# ======================================================================
# CAREER AI AGENT - INTELLIGENT CAREER GUIDANCE SYSTEM
# ======================================================================
# Description: A professional AI-powered career guidance agent using 
#              Google's Gemini 2.5 Flash model. Provides personalized
#              career advice, salary insights, skill recommendations,
#              interview preparation, and career growth guidance.
#              ONLY answers career-related questions.
# ======================================================================

# ======================================================================
# MODULE IMPORTS
# ======================================================================
# streamlit: Web application framework for building the UI
# google.generativeai: Google's Gemini AI model integration
# os: Operating system interface for environment variables
# ======================================================================
import streamlit as st
import google.generativeai as genai
import os

# ======================================================================
# PAGE CONFIGURATION
# ======================================================================
# Configures the Streamlit page settings including title, icon,
# layout style, and sidebar default state
# ======================================================================
st.set_page_config(
    page_title="Career AI Agent",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ======================================================================
# CUSTOM CSS STYLING
# ======================================================================
# Professional UI styling with gradient backgrounds, glass morphism,
# custom chat bubbles, sidebar theming, and responsive design
# ======================================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* ============================= */
/* REMOVE STREAMLIT WHITE HEADER */
/* ============================= */

header {visibility: hidden;}
.block-container {padding-top: 0rem !important;}

/* ============================= */
/* GLOBAL */
/* ============================= */

.stApp {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* ============================= */
/* MAIN CONTAINER */
/* ============================= */

.main-container {
    max-width: 1000px;
    margin: 1.5rem auto;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 32px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

/* ============================= */
/* HEADER */
/* ============================= */

.agent-header {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 2rem;
    border-radius: 24px;
    margin-bottom: 1.5rem;
    text-align: center;
}

.agent-header h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
}

.agent-header p {
    color: rgba(255,255,255,0.9);
}

.status-badge {
    display: inline-block;
    padding: 0.4rem 1rem;
    background: rgba(255,255,255,0.2);
    border-radius: 50px;
    color: white;
    font-size: 0.8rem;
    margin-top: 0.8rem;
}

/* ============================= */
/* SIDEBAR FIX FOR LIGHT THEME */
/* ============================= */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* ============================= */
/* FIX SIDEBAR INPUT TEXT COLOR */
/* ============================= */

[data-testid="stSidebar"] .stTextInput input {
    color: #000000 !important;
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    color: #000000 !important;
}

[data-testid="stSidebar"] textarea {
    color: #000000 !important;
    background-color: #ffffff !important;
}

[data-testid="stSidebar"] input::placeholder {
    color: #666666 !important;
}

/* ============================= */
/* FIX NEW CONVERSATION BUTTON  */
/* ============================= */

/* Target the button container */
[data-testid="stSidebar"] .stButton {
    display: block !important;
}

/* Target the button element directly */
[data-testid="stSidebar"] .stButton button {
    color: #000000 !important;
    background-color: #ffffff !important;
    border: 1px solid #cccccc !important;
    font-weight: 500 !important;
}

/* Target any paragraph or text inside the button */
[data-testid="stSidebar"] .stButton button p {
    color: #000000 !important;
}

/* Target any span inside the button */
[data-testid="stSidebar"] .stButton button span {
    color: #000000 !important;
}

/* Target when button is not hovered, not focused, etc. */
[data-testid="stSidebar"] .stButton button:not(:hover):not(:focus) {
    color: #000000 !important;
    background-color: #ffffff !important;
}

/* Hover state - optional */
[data-testid="stSidebar"] .stButton button:hover {
    color: #ffffff !important;
    background-color: #2563eb !important;
    border-color: #2563eb !important;
}



/* ============================= */
/* CHAT */
/* ============================= */

.chat-container {
    margin: 1.5rem 0;
    max-height: 60vh;
    overflow-y: auto;
}

/* Hide accidental code rendering */

.chat-container pre {
display:none;
}

.chat-container code {
display:none;
}

/* USER MESSAGE */

.user-message-wrapper {
    display: flex;
    justify-content: flex-end;
    margin: 1rem 0;
}

.user-message {
    background: linear-gradient(135deg, #2563eb, #4f46e5);
    color: white;
    padding: 0.8rem 1.2rem;
    border-radius: 20px 20px 4px 20px;
    max-width: 70%;
}

/* ASSISTANT MESSAGE */

.assistant-message-wrapper {
    display: flex;
    gap: 0.8rem;
    margin: 1rem 0;
}

.assistant-avatar {
    width: 35px;
    height: 35px;
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    border-radius: 50%;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
}

.assistant-message {
    background: white;
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 20px 4px;
    max-width: 70%;
    border:1px solid #e2e8f0;
}

/* ============================= */
/* WELCOME CARD */
/* ============================= */

.welcome-card {
    background: white;
    padding: 2rem;
    border-radius: 24px;
    text-align: center;
    border: 1px solid #e2e8f0;
}

.welcome-title {
    font-size: 2rem;
    font-weight: 700;
}

.welcome-subtitle {
    color: #64748b;
}

/* FEATURE GRID */

.features-grid {
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:1rem;
    margin-top:2rem;
}

.feature-item {
    background:white;
    padding:1rem;
    border-radius:16px;
    border:1px solid #e2e8f0;
}

.feature-icon {
    font-size:2rem;
}

.tip-box{
margin-top:2rem;
padding:1rem;
background:#eef2ff;
border-radius:16px;
}

/* ============================= */
/* ERROR MESSAGE STYLING */
/* ============================= */

.error-message-wrapper {
    display: flex;
    gap: 0.8rem;
    margin: 1rem 0;
}

.error-avatar {
    width: 35px;
    height: 35px;
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    border-radius: 50%;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size: 1.2rem;
}

.error-message {
    background: #fee2e2;
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 20px 4px;
    max-width: 70%;
    border: 1px solid #fecaca;
    color: #991b1b;
}

.error-message strong {
    color: #b91c1c;
    display: block;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}

</style>
""", unsafe_allow_html=True)

# ======================================================================
# MAIN CONTAINER START
# ======================================================================
# Opens the main container div for consistent spacing and styling
# ======================================================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ======================================================================
# HEADER SECTION
# ======================================================================
# Displays the application header with title, subtitle, and status badge
# ======================================================================
st.markdown("""
<div class="agent-header">
<h1>🎯 Career AI Agent</h1>
<p>Your Intelligent Career Companion - Ask me anything about your career</p>
<div class="status-badge">🟢 Online • 🤖 Gemini • ⚠️ Career Questions Only</div>
</div>
""", unsafe_allow_html=True)

# ======================================================================
# API KEY CONFIGURATION
# ======================================================================
# Retrieves Google API key from environment variables or Streamlit secrets
# Exits gracefully if no API key is found
# ======================================================================
API_KEY = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)

if not API_KEY:
    st.error("⚠️ Google API Key not found")
    st.stop()

# ======================================================================
# MODEL CONFIGURATION
# ======================================================================
# Using Gemini 2.5 Flash model for optimal performance and response quality
# ======================================================================
MODEL_NAME="gemini-2.5-flash"

# ======================================================================
# SESSION STATE INITIALIZATION
# ======================================================================
# Maintains conversation history, user profile data, and UI state
# across reruns using Streamlit's session state
# ======================================================================
if "messages" not in st.session_state:
    st.session_state.messages=[]

if "user_profile" not in st.session_state:
    st.session_state.user_profile={
    "name":None,
    "current_role":None,
    "target_role":None,
    "experience":None,
    "location":None
}

if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent=False

# ======================================================================
# SIDEBAR PROFILE SECTION
# ======================================================================
# User profile form with expander for better UX
# Collects: Name, Current Role, Target Role, Experience, Location
# Includes reset button for new conversations
# ======================================================================
with st.sidebar:

    st.header("👤 Your Profile")

    with st.expander("Edit Profile"):

        st.session_state.user_profile["name"]=st.text_input("Name")
        st.session_state.user_profile["current_role"]=st.text_input("Current Role")
        st.session_state.user_profile["target_role"]=st.text_input("Target Role")

        st.session_state.user_profile["experience"]=st.selectbox(
        "Experience",
        ["Fresher (0-1 years)","1-3 years","3-6 years","6-10 years"]
        )

        st.session_state.user_profile["location"]=st.text_input("Location")

    if st.button("🔄 New Conversation"):
        st.session_state.messages=[]
        st.session_state.first_message_sent=False
        st.rerun()

# ======================================================================
# CHAT HISTORY DISPLAY
# ======================================================================
# Renders all previous messages with appropriate styling:
# - User messages: Right-aligned with gradient blue background
# - Assistant messages: Left-aligned with avatar and white background
# - Error messages: Red background for non-career questions
# ======================================================================
if st.session_state.messages:

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for msg in st.session_state.messages:

        if msg["role"]=="user":

            st.markdown(f"""
            <div class="user-message-wrapper">
            <div class="user-message">{msg["content"]}</div>
            </div>
            """,unsafe_allow_html=True)

        else:
            # Check if this is an error message (non-career question response)
            if "⚠️ CAREER-RELATED QUESTIONS ONLY" in msg["content"]:
                st.markdown(f"""
                <div class="error-message-wrapper">
                <div class="error-avatar">⚠️</div>
                <div class="error-message">{msg["content"]}</div>
                </div>
                """,unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message-wrapper">
                <div class="assistant-avatar">🤖</div>
                <div class="assistant-message">{msg["content"]}</div>
                </div>
                """,unsafe_allow_html=True)

    st.markdown("</div>",unsafe_allow_html=True)

# ======================================================================
# WELCOME CARD DISPLAY
# ======================================================================
# Shown only on first visit (no messages and first_message_sent=False)
# Features:
# - Welcome title
# - Feature grid (Salary, Skills, Interview, Growth)
# - Example question tip
# - Note about career-only questions
# ======================================================================
if not st.session_state.messages and not st.session_state.first_message_sent:

    st.markdown("""
<div class="welcome-card">

<div class="welcome-title">
👋 Welcome to Career AI Agent
</div>

<div class="welcome-subtitle">
Ask anything about your career - jobs, skills, interviews, salaries, and growth
</div>

<div class="features-grid">

<div class="feature-item">
<div class="feature-icon">💰</div>
Salary Insights
</div>

<div class="feature-item">
<div class="feature-icon">📚</div>
Skills Required
</div>

<div class="feature-item">
<div class="feature-icon">🎯</div>
Interview Prep
</div>

<div class="feature-item">
<div class="feature-icon">📈</div>
Career Growth
</div>

</div>

<div class="tip-box">
<strong>⚠️ IMPORTANT: Career-Related Questions Only</strong>
<br>
This assistant ONLY answers questions about:
<br><br>
• Job roles and responsibilities
• Skills required for specific careers
• Salary ranges and compensation
• Interview preparation and questions
• Qualifications and certifications
• Career path and growth opportunities
• Industry trends and job market
• Resume and portfolio tips
<br><br>
💡 Try asking:
<br>
• "What skills are needed to become a Data Scientist?"
• "What is the salary range for a Software Engineer in Bangalore?"
• "How to prepare for a Product Manager interview?"
• "What are the key responsibilities of a DevOps engineer?"
</div>

</div>
""",unsafe_allow_html=True)

# ======================================================================
# RELEVANCE CHECKER FUNCTION
# ======================================================================
# Checks if the user's question is career-related using Gemini
# Returns: (is_relevant boolean, reason string)
# ======================================================================
def check_question_relevance(question, profile):
    """
    Use Gemini to check if the question is career-related
    """
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Build profile context for better understanding
        profile_context = ""
        for key, value in profile.items():
            if value:
                profile_context += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        if not profile_context:
            profile_context = "No profile information available"
        
        relevance_prompt = f"""You are a strict career guidance filter. Your ONLY job is to determine if a user's question is related to CAREER, JOB, PROFESSION, or WORK.

USER PROFILE (for context, but don't use this to accept non-career questions):
{profile_context}

USER QUESTION: "{question}"

CATEGORIZE THIS QUESTION:
- Is this question about jobs, careers, professions, work, employment, skills for work, interviews, salaries, professional growth, industry trends, or any work-related topic?
- If YES, it's relevant.
- If NO, it's irrelevant.

RELEVANT TOPICS EXAMPLES:
- "What skills do I need for data science?" ✅ RELEVANT
- "How to prepare for a software engineer interview?" ✅ RELEVANT
- "What is the salary of a product manager?" ✅ RELEVANT
- "Tell me about cloud computing careers" ✅ RELEVANT
- "How to become a pilot?" ✅ RELEVANT
- "What qualifications for teaching?" ✅ RELEVANT

IRRELEVANT TOPICS EXAMPLES:
- "What is the best food in Chennai?" ❌ IRRELEVANT
- "Tell me a joke" ❌ IRRELEVANT
- "What is the capital of France?" ❌ IRRELEVANT
- "How to cook pasta?" ❌ IRRELEVANT
- "What is the weather today?" ❌ IRRELEVANT
- "Tell me about movies" ❌ IRRELEVANT
- "Who won the cricket match?" ❌ IRRELEVANT
- "How to lose weight?" ❌ IRRELEVANT (unless specifically about fitness career)
- "What is the meaning of life?" ❌ IRRELEVANT

IMPORTANT RULES:
1. If the question asks about ANY topic that is NOT directly about careers, jobs, professions, work, or professional development, mark it as IRRELEVANT.
2. Be strict - if there's any doubt, mark as IRRELEVANT.
3. Even if the user asks about their profile but it's not career-related (e.g., "What's my name?"), mark as IRRELEVANT unless it's about their career.
4. Questions about hobbies, entertainment, general knowledge, health (unless health career), etc. are ALL IRRELEVANT.

Respond with EXACTLY one of these formats:
RELEVANT||[brief reason why it's career-related]
IRRELEVANT||[brief reason why it's not career-related]

Example:
RELEVANT||Question asks about software engineering skills
IRRELEVANT||Question is about food recommendations, not career-related"""
        
        response = model.generate_content(
            relevance_prompt,
            generation_config={
                "temperature": 0.1,  # Low temperature for consistent classification
                "max_output_tokens": 100,
            }
        )
        
        result = response.text.strip()
        
        if result.startswith("RELEVANT||"):
            return True, result.replace("RELEVANT||", "").strip()
        else:
            return False, result.replace("IRRELEVANT||", "").strip() if "||" in result else "Question is not related to careers or professional development"
            
    except Exception as e:
        # If relevance check fails, default to relevant to avoid blocking users
        # But log the error (in production, you'd want to log this)
        print(f"Relevance check error: {e}")
        return True, "Relevance check unavailable, allowing question"

# ======================================================================
# CONVERSATION PROMPT BUILDER
# ======================================================================
# Constructs a comprehensive prompt for the AI model including:
# - User profile data (if available)
# - Conversation history (last 6 messages for context)
# - Current user query
# - Detailed instructions for response formatting
# ======================================================================
def get_conversation_prompt(user_message, profile, history):
    
    # Build profile context
    profile_context = ""
    for key, value in profile.items():
        if value:
            profile_context += f"- {key.replace('_', ' ').title()}: {value}\n"
    
    if not profile_context:
        profile_context = "No profile information yet"
    
    # Build conversation history (last 5 exchanges for memory)
    history_context = ""
    if len(history) > 0:
        history_context = "\nPrevious conversation:\n"
        # Get last 5 messages (or less if fewer)
        recent_msgs = history[-6:]  # Last 3 exchanges (6 messages)
        for msg in recent_msgs:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_context += f"{role}: {msg['content']}\n"
    
    system_prompt = f"""You are a career guidance AI assistant. You ONLY answer questions about careers, jobs, professions, work, and professional development.

USER PROFILE:
{profile_context}

{history_context}

Current user message: {user_message}

IMPORTANT INSTRUCTIONS:
1. This question has ALREADY been verified as career-related. ONLY provide career guidance.
2. Remember what was discussed before - use the conversation history
3. If user asks follow-up questions, refer to previous answers
4. Be conversational and natural
5. Give detailed but concise answers (4-7 sentences)
6. For salary questions: give realistic ranges in INR based on experience and location
7. For skill questions: list specific technologies with brief explanations
8. For interview questions: provide practical tips and common questions
9. For role questions: explain responsibilities, required skills, qualifications
10. Use the user's profile information when relevant
11. If user says "hi" or "hello", greet them warmly and ask about their career interests
12. Always end with an open question to continue the conversation about their career

Respond naturally with career-focused guidance:"""
    
    return system_prompt

# ======================================================================
# CHAT INPUT HANDLER
# ======================================================================
# Main interaction loop:
# 1. Captures user input from chat box
# 2. Updates session state
# 3. Checks if question is career-related
# 4. If relevant: builds context-aware prompt and calls Gemini API
# 5. If irrelevant: shows error message
# 6. Displays and stores response
# 7. Handles errors gracefully
# ======================================================================
prompt = st.chat_input("Ask career question...")

if prompt:

    st.session_state.first_message_sent = True

    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        # Check if question is career-related
        is_relevant, reason = check_question_relevance(prompt, st.session_state.user_profile)
        
        if not is_relevant:
            # Show error message for non-career questions
            error_response = f"""⚠️ **CAREER-RELATED QUESTIONS ONLY**

I'm a Career AI Agent designed specifically to help with career-related questions. Your question appears to be about: **{reason}**

**I can only assist with:**
• Job roles and responsibilities
• Skills required for specific careers
• Salary ranges and compensation
• Interview preparation and questions
• Qualifications and certifications
• Career path and growth opportunities
• Industry trends and job market
• Resume and portfolio tips

**Please ask a career-related question, and I'll be happy to help!** 😊"""
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_response
            })
            
        else:
            # Question is relevant, proceed with normal response
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(MODEL_NAME)
            
            # Get conversation prompt with memory
            conversation_prompt = get_conversation_prompt(
                prompt, 
                st.session_state.user_profile,
                st.session_state.messages[:-1]  # Exclude current message
            )
            
            # Generate response with context
            response = model.generate_content(
                conversation_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 800,
                }
            )

            reply = response.text if response.text else "I'm here to help with your career. What would you like to know about jobs, skills, or professional growth?"

            # Add assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

    except Exception as e:
        st.error(f"Error: {str(e)}")
        # Add fallback response
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I'm here to help with your career questions. Could you please ask again about jobs, skills, or professional development?"
        })

    st.rerun()

# ======================================================================
# MAIN CONTAINER CLOSE
# ======================================================================
# Closes the main container div
# ======================================================================
st.markdown("</div>", unsafe_allow_html=True)

# ======================================================================
# END OF APPLICATION
# ======================================================================
