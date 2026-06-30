import streamlit as st
import requests
import uuid
import json
from datetime import timedelta

# --- Configuration ---
# It's recommended to use st.secrets for storing sensitive information like API tokens
API_URL = "https://elastic.snaplogic.com/api/1/rest/slsched/feed/SIE_Health_Dev/SHS_IT_DEI_HC_AI/Integron_Agent/medha_integron_agent_task"
API_TOKEN = "SQ7Pe0a0DLl0stgI1KTH1TGd7GYP2BO1"  # or st.secrets["API_TOKEN"]


# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="HC Integron Agent",
    page_icon="🤖",
    layout="wide"
)

# --- Siemens Healthineers Brand Theme ---
def inject_custom_css():
    """Injects Siemens Healthineers branded styling into the app."""
    st.markdown(
        """
        <style>
        /* ---- Siemens Healthineers official palette ----
           Siemens Petrol  #009999  rgb(0,153,153,)
           Healthy Orange  #EC6602  rgb(236,102,2,)
        */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --sh-petrol: #009999;
            --sh-petrol-dark: #007A7A;
            --sh-orange: #EC6602;
            --sh-orange-dark: #C45402;
            --sh-gradient: linear-gradient(135deg, #009999 0%, #EC6602 100%);
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        .stApp {
            background: linear-gradient(180deg, #f6f8fb 0%, #eef1f6 100%);
        }

        /* ---- Layout spacing ---- */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 6rem !important;
            max-width: 1100px;
        }
        /* Tighten Streamlit's default large vertical gaps */
        [data-testid="stVerticalBlock"] { gap: 0.75rem; }

        /* ---- Header banner ---- */
        .sh-header {
            background: var(--sh-petrol);
            border-radius: 16px;
            padding: 26px 32px;
            margin-bottom: 22px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 153, 153, 0.25);
        }
        .sh-header::after {
            content: "";
            position: absolute;
            top: 0; right: 0; bottom: 0;
            width: 45%;
            background: var(--sh-orange);
            opacity: 0.95;
            clip-path: polygon(28% 0, 100% 0, 100% 100%, 0% 100%);
        }
        .sh-header-content { position: relative; z-index: 2; }
        .sh-title, .sh-header h1, .sh-header .sh-title a {
            color: #ffffff !important;
            font-size: 1.9rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.3px;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
        }
        .sh-subtitle {
            color: #d6f0f0;
            font-size: 0.98rem;
            font-weight: 400;
            margin-top: 6px;
        }
        .sh-badge {
            display: inline-block;
            background: rgba(255,255,255,0.12);
            color: #ffffff;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 20px;
            margin-bottom: 10px;
        }

        /* ---- Section subheaders ---- */
        h2, h3, .stSubheader {
            color: var(--sh-petrol) !important;
            font-weight: 600 !important;
        }
        [data-testid="stHeading"] { margin-top: 0.5rem; }

        /* ---- Buttons ---- */
        .stButton > button {
            background: var(--sh-orange);
            color: #ffffff;
            border: none;
            border-radius: 10px;
            padding: 0.5rem 1.1rem;
            font-weight: 600;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            box-shadow: 0 4px 14px rgba(236, 102, 2, 0.30);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            background: var(--sh-orange-dark);
            box-shadow: 0 6px 20px rgba(236, 102, 2, 0.40);
            color: #ffffff;
        }
        .stButton > button:active { transform: translateY(0); }

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {
            background: var(--sh-petrol);
        }
        section[data-testid="stSidebar"] * {
            color: #e6e7f0 !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] .stCode,
        section[data-testid="stSidebar"] code {
            background: rgba(255,255,255,0.12) !important;
            color: #ffd9b3 !important;
        }

        /* ---- Chat messages ---- */
        [data-testid="stChatMessage"] {
            border-radius: 14px;
            padding: 4px 8px;
            margin-bottom: 8px;
            box-shadow: 0 2px 10px rgba(0, 60, 70, 0.06);
            background: #ffffff;
        }

        /* ---- Chat input ---- */
        [data-testid="stChatInput"] textarea {
            border-radius: 12px !important;
        }
        [data-testid="stChatInput"] {
            border-top: 3px solid transparent;
            border-image: var(--sh-gradient) 1;
        }

        /* ---- Divider accent ---- */
        hr { border-top: 2px solid rgba(0,153,153,0.25); }

        /* ---- Intro line ---- */
        .sh-intro {
            color: #1f3a3f;
            font-size: 1.02rem;
            font-weight: 500;
            line-height: 1.55;
            margin: 0 0 16px 0;
        }

        /* ---- Description card ---- */
        .sh-desc-card {
            background: #ffffff;
            border-left: 5px solid var(--sh-petrol);
            border-radius: 12px;
            padding: 18px 22px;
            margin: 0 0 24px 0;
            box-shadow: 0 4px 16px rgba(0, 153, 153, 0.10);
            color: #2c3e44;
            font-size: 0.96rem;
            line-height: 1.6;
        }
        .sh-desc-card strong { color: var(--sh-petrol); }

        /* ---- Sample prompts heading ---- */
        .sh-section-title {
            color: var(--sh-petrol);
            font-weight: 700;
            font-size: 1.05rem;
            margin: 8px 0 14px 2px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
                    display: inline-block;
        }

        /* ---- Sample prompt buttons ---- */
        div[data-testid="column"] .stButton > button {
            background: #ffffff;
            color: #1f3a3f;
            border: 1.5px solid rgba(0, 153, 153, 0.35);
            border-radius: 12px;
            padding: 0.7rem 1rem;
            font-weight: 500;
            font-size: 0.86rem;
            text-align: left;
            box-shadow: 0 2px 8px rgba(0, 153, 153, 0.06);
            white-space: normal;
            line-height: 1.4;
            min-height: 64px;
            height: 100%;
            display: flex;
            align-items: center;
        }
        div[data-testid="column"] .stButton > button:hover {
            background: #f0fbfb;
            border-color: var(--sh-petrol);
            color: var(--sh-petrol);
            box-shadow: 0 4px 14px rgba(0, 153, 153, 0.18);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Caching the API Call ---
@st.cache_data(ttl=timedelta(minutes=10), show_spinner=False)
def get_assistant_response(session_id, messages_tuple):
    """
    Sends the user's prompt to the backend API and returns the response.
    This function is cached to avoid repeated API calls with the same input.
    """
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    # Convert the tuple back to a list of dictionaries
    messages = [dict(m) for m in messages_tuple]

    payload = [
        {
            "session_id": session_id,
            "messages": messages
        }
    ]

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=180
        )
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
        return {"error": f"Error communicating with agent: {e}"}


def extract_assistant_reply(data):
    """
    Normalize different possible API response formats to a single string.

    Handles:
    - dict with 'response' / 'answer' / 'message' / 'content' / 'error'
    - list of such dicts
    - fallback to string conversion
    """

    def from_dict(d):
        # Prefer explicit error if present
        if "error" in d and isinstance(d["error"], str):
            return f"⚠️ {d['error']}"
        for key in ("response", "answer", "message", "content"):
            if key in d and isinstance(d[key], str):
                return d[key]
        return None

    if isinstance(data, dict):
        extracted = from_dict(data)
        if extracted is not None:
            return extracted
        return str(data)

    if isinstance(data, list) and len(data) > 0:
        for item in data:
            if isinstance(item, dict):
                extracted = from_dict(item)
                if extracted is not None:
                    return extracted
        return str(data[0])

    return "I received an unexpected response format from the backend."


def initialize_session_state():
    """Initializes all necessary session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "active_category" not in st.session_state:
        st.session_state.active_category = "Install Base Insights"
    if "last_full_data" not in st.session_state:
        st.session_state.last_full_data = None
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


# --- Agent metadata ---
AGENT_DESCRIPTION = (
    "<strong>Integron Agent</strong> is an AI-powered Hybrid Cloud Integration "
    "Intelligence Assistant designed to provide real-time insights into enterprise "
    "integration platforms, including <strong>SnapLogic, APIM, TAAS, and BPS Proxy</strong>. "
    "It delivers comprehensive visibility into platform health, runtime performance, "
    "execution status, and integration asset information. The agent also offers intelligent "
    "diagnostics and actionable recommendations to accelerate issue resolution, improve "
    "operational efficiency, and enhance platform reliability."
)

SAMPLE_PROMPTS = [
    "What is the current SnapLogic platform health status?",
    "Are there any ongoing incidents or degraded services in SnapLogic PROD environment right now?",
    "List all active pipelines deployed in PROD under the PLM Project Space?",
    "List all active pipelines deployed under the CLMA Project?",
    "Show me all pipeline executions for the TREFF pipelines in last 4 hours",
    "Show all failed pipeline executions in PROD in the last 24 hours and provide probable cause and resolution steps.",
]


def add_message(role, content):
    """
    Adds a message to the session state chat history.
    role: 'USER' or 'ASSISTANT'
    """
    st.session_state.messages.append(
        {"sl_role": role, "content": content}
    )


def display_sidebar():
    """Displays the sidebar with configuration and session info."""
    with st.sidebar:
        st.title("🔧 Configuration")
        st.markdown("Manage your session below.")

        if st.button("♻️ New Session", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.last_full_data = None
            st.rerun()


def set_active_category(category):
    """Sets the active example category."""
    st.session_state.active_category = category


def handle_prompt_submission(prompt_text):
    """
    Handles sending of a prompt (from chat input or example button),
    calling the backend API, and updating the UI.
    """
    if not prompt_text.strip():
        return
    
    # Add user message to the chat history
    add_message("USER", prompt_text)
    
    # Prepare messages for the API call
    messages_tuple = tuple(
        {"sl_role": msg["sl_role"], "content": msg["content"]}
        for msg in st.session_state.messages
    )

    # Local spinner near the chat / button instead of global "Running …"
    with st.spinner("Agent is thinking..."):
        data = get_assistant_response(st.session_state.session_id, messages_tuple)
    
    # Store the full response (for raw view in sidebar)
    st.session_state.last_full_data = data
    
    # Extract a "nice" message to show in the main chat
    assistant_reply = extract_assistant_reply(data)
    
    # Add assistant message to the chat history
    add_message("ASSISTANT", assistant_reply)


def display_main_content():
    """Displays the main layout of the application."""
    st.markdown(
        """
        <div class="sh-header">
            <div class="sh-header-content">
                <span class="sh-badge">Siemens Healthineers</span>
                <h1 class="sh-title">🤖 HC Integron Agent</h1>
                <p class="sh-subtitle">
                    Hybrid Cloud Integration Intelligence Assistant
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Intro + description shown only on the landing view (before chat starts).
    if not st.session_state.messages:
        st.markdown(
            f"""
            <div class="sh-intro">
                👋 Welcome! I'm your Integron Agent — here to give you real-time
                visibility and intelligent diagnostics across your hybrid cloud
                integration platforms.
            </div>
            <div class="sh-desc-card">{AGENT_DESCRIPTION}</div>
            """,
            unsafe_allow_html=True,
        )


def display_sample_prompts():
    """Displays clickable sample prompt buttons."""
    # Only show suggestions before the conversation starts.
    if st.session_state.messages:
        return

    st.markdown('<div class="sh-section-title">Sample prompts</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, prompt in enumerate(SAMPLE_PROMPTS):
        with cols[idx % 2]:
            if st.button(prompt, key=f"sample_{idx}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()

def display_chat_interface():
    """Manages the chat display and response processing."""
    st.subheader("Chat with Agent")
    
    chat_container = st.container()
    with chat_container:
        # Display existing messages
        for msg in st.session_state.messages:
            with st.chat_message(msg["sl_role"].lower()):
                st.markdown(msg["content"])
    
    # Handle a queued prompt from a sample-prompt button
    if st.session_state.pending_prompt:
        queued = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
        handle_prompt_submission(queued)
        st.rerun()

    # Process new user message
    user_input = st.chat_input("Type your question here...")
    if user_input:
        handle_prompt_submission(user_input)
        st.rerun()


# --- Main App Execution ---
def main():
    inject_custom_css()
    initialize_session_state()
    display_sidebar()
    display_main_content()
    display_sample_prompts()
    display_chat_interface()  # debug panel removed from main()


if __name__ == "__main__":
    main()
