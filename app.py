import os
import time
import uuid
from typing import Dict, List, Any

import streamlit as st
from PIL import Image
from google import genai
from google.genai import types

# --- Page Config -----------------------------------------------------------
st.set_page_config(
    page_title="Thrive in Learning – SRL Companion",
    page_icon="🌱",
    layout="wide",
)

# --- Secrets & Gemini Client ----------------------------------------------
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if not API_KEY:
    st.warning("⚠️ 'GEMINI_API_KEY' is not set in st.secrets. Add it before deploying.")

client = genai.Client(api_key=API_KEY) if API_KEY else None


# --- Identity / System Instructions ---------------------------------------
@st.cache_resource(show_spinner=False)
def load_developer_prompt() -> str:
    """
    Load identity.txt once and cache it.
    This is your main long-form system prompt.
    """
    try:
        with open("identity.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.warning("⚠️ 'identity.txt' not found. Using a minimal fallback prompt.")
        return (
            "You are 'Thrive in Learning', a self-regulated learning companion for college students. "
            "Help them set mastery-oriented goals, analyze tasks, choose strategies, plan time, "
            "find resources, and reflect on their learning. "
            "Be concrete, encouraging, and focused on growth, not perfection."
        )


SYSTEM_INSTRUCTIONS = load_developer_prompt()


# --- SRL Modules -----------------------------------------------------------
MODULES: List[Dict[str, str]] = [
    {
        "id": "goal",
        "label": "Goal Setting",
        "emoji": "🎯",
        "description": "Define mastery-oriented goals for your current task.",
    },
    {
        "id": "task",
        "label": "Task Analysis",
        "emoji": "🔍",
        "description": "Break the task into clear, manageable pieces.",
    },
    {
        "id": "strategies",
        "label": "Learning Strategies",
        "emoji": "💡",
        "description": "Choose evidence-based strategies for this task.",
    },
    {
        "id": "time",
        "label": "Time Management",
        "emoji": "⏱️",
        "description": "Plan and track your study time.",
    },
    {
        "id": "resources",
        "label": "Resources",
        "emoji": "📚",
        "description": "List and organize helpful materials and people.",
    },
    {
        "id": "reflection",
        "label": "Reflection",
        "emoji": "✨",
        "description": "Reflect on what worked and what to improve next time.",
    },
]


MODULE_HINTS: Dict[str, str] = {
    "goal": (
        "You are in the GOAL-SETTING module. Help the student turn vague or performance-only goals "
        "into clear mastery-oriented goals focused on understanding, skills, and growth. "
        "Use short bullet points and keep the tone encouraging."
    ),
    "task": (
        "You are in the TASK-ANALYSIS module. Help the student clarify requirements, break the task "
        "into subtasks, and notice prior knowledge and gaps. Be concrete and step-by-step."
    ),
    "strategies": (
        "You are in the LEARNING-STRATEGIES module. Recommend 3–7 specific, research-aligned strategies "
        "that match the task and the student's constraints. For each, briefly say how to use it."
    ),
    "time": (
        "You are in the TIME-MANAGEMENT module. Help the student estimate time, choose a work–break pattern, "
        "and plan a realistic schedule. Emphasize experimentation, not perfection."
    ),
    "resources": (
        "You are in the RESOURCES module. Suggest concrete resources (readings, videos, tools, people) "
        "for this task, and how to use them strategically rather than collecting too many."
    ),
    "reflection": (
        "You are in the REFLECTION module. Prompt the student to notice what they learned, which strategies "
        "worked, how they managed time and emotion, and what they want to do differently next time."
    ),
}


# --- Generation Configuration ----------------------------------------------
BASE_GENERATION_CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTIONS,
    temperature=0.8,
    max_output_tokens=1024,
    thinking_config=types.ThinkingConfig(thinking_budget=-1),  # dynamic thinking
)


def build_session_context(session: Dict[str, Any]) -> str:
    """
    Compact summary of the current SRL state.

    This gets injected silently into Gemini so it can refer
    to the student's task, goal, strategies, and time logged
    without re-asking for everything.
    """
    parts = []
    if session.get("task_name"):
        parts.append(f"Task: {session['task_name']}")
    if session.get("task_type"):
        parts.append(f"Task type: {session['task_type']}")
    if session.get("goal_type"):
        parts.append(f"Goal type: {session['goal_type']}")
    if session.get("goal_description"):
        parts.append(f"Goal description: {session['goal_description']}")
    if session.get("deadline"):
        parts.append(f"Deadline: {session['deadline']}")
    if session.get("chosen_strategies"):
        parts.append("Selected strategies: " + ", ".join(session["chosen_strategies"]))
    if session.get("total_time_minutes"):
        parts.append(f"Time spent so far: {session['total_time_minutes']} minutes")
    return "\n".join(parts)


def call_gemini_for_module(
    module_id: str,
    user_message: str,
    session: Dict[str, Any],
) -> str:
    """
    Single gateway for all Gemini calls.

    - Injects the long identity.txt as system instructions
    - Adds a short module-specific hint (silent prompt)
    - Adds compact session context (task, goal, time, etc.)
    """
    if not client:
        return (
            "Gemini API key is missing. Ask your instructor or app owner "
            "to add GEMINI_API_KEY to Streamlit secrets."
        )

    module_hint = MODULE_HINTS.get(module_id, "")
    context = build_session_context(session)

    prompt = (
        f"[Module guidance]\n{module_hint}\n\n"
        f"[Student task context]\n{context or 'Context not provided yet.'}\n\n"
        "[Instruction]\n"
        "Respond directly to the student. Don't mention that you saw any hidden prompts.\n\n"
        f"[Student message]\n{user_message}"
    )

    resp = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=[types.Content(parts=[types.Part.from_text(prompt)])],
        config=BASE_GENERATION_CONFIG,
    )
    return resp.text or "(No response from model.)"


# --- Session & Timer Helpers -----------------------------------------------
def init_app_state():
    """
    Initialize all Streamlit session_state keys used across modules.
    """
    if "sessions" not in st.session_state:
        st.session_state["sessions"] = {}

    if "current_session_id" not in st.session_state:
        _create_new_session(default_demo=True)

    if "active_module" not in st.session_state:
        st.session_state["active_module"] = "goal"

    if "ai_responses" not in st.session_state:
        st.session_state["ai_responses"] = {}  # module_id -> last response text

    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False

    if "timer_start_ts" not in st.session_state:
        st.session_state["timer_start_ts"] = None


def _create_new_session(default_demo: bool = False) -> str:
    """
    Internal: create a new SRL session and set it as current.

    Stored structure:
      - sessions: {session_id: {...session fields...}}
      - current_session_id: active session key
    """
    sid = str(uuid.uuid4())
    now = time.time()

    if default_demo:
        session = {
            "id": sid,
            "name": "Research paper on climate change",
            "created_at": now,
            "updated_at": now,
            "task_name": "Research paper on climate change",
            "task_type": "Research paper",
            "goal_type": "mastery",
            "goal_description": (
                "Deeply understand the mechanisms of climate change and their environmental impacts."
            ),
            "deadline": "",
            "requirements": "",
            "subtasks": "",
            "prior_knowledge": "",
            "knowledge_gaps": "",
            "anticipated_challenges": "",
            "contingency_plan": "",
            "chosen_strategies": [
                "Elaborative interrogation",
                "Self-explanation",
                "Concept mapping",
            ],
            "session_plan": "",
            "recent_sessions": [],
            "resources": [],
            "reflections": {
                "goal": "",
                "strategies": "",
                "time": "",
                "growth": "",
            },
            "total_time_minutes": 0,
        }
    else:
        session = {
            "id": sid,
            "name": "New session",
            "created_at": now,
            "updated_at": now,
            "task_name": "",
            "task_type": "",
            "goal_type": "mastery",
            "goal_description": "",
            "deadline": "",
            "requirements": "",
            "subtasks": "",
            "prior_knowledge": "",
            "knowledge_gaps": "",
            "anticipated_challenges": "",
            "contingency_plan": "",
            "chosen_strategies": [],
            "session_plan": "",
            "recent_sessions": [],
            "resources": [],
            "reflections": {
                "goal": "",
                "strategies": "",
                "time": "",
                "growth": "",
            },
            "total_time_minutes": 0,
        }

    st.session_state["sessions"][sid] = session
    st.session_state["current_session_id"] = sid
    return sid


def get_current_session() -> Dict[str, Any]:
    sid = st.session_state.get("current_session_id")
    sessions = st.session_state.get("sessions", {})
    if not sid or sid not in sessions:
        sid = _create_new_session(default_demo=True)
    return st.session_state["sessions"][sid]


def update_current_session(updates: Dict[str, Any]):
    session = get_current_session()
    session.update(updates)
    session["updated_at"] = time.time()
    st.session_state["sessions"][session["id"]] = session


def save_session_snapshot():
    get_current_session()  # ensures it exists
    update_current_session({})
    st.toast("Session saved ✅")


def new_session_action():
    _create_new_session(default_demo=False)
    st.session_state["ai_responses"].clear()
    st.session_state["timer_running"] = False
    st.session_state["timer_start_ts"] = None
    st.toast("New session created 🌱")


def delete_session(session_id: str):
    sessions = st.session_state.get("sessions", {})
    if session_id in sessions:
        del sessions[session_id]
    if st.session_state.get("current_session_id") == session_id:
        if sessions:
            st.session_state["current_session_id"] = next(iter(sessions.keys()))
        else:
            _create_new_session(default_demo=False)


def sync_timer_with_session():
    """
    When timer_running is True and the script re-runs,
    add the elapsed time (in whole minutes) to total_time_minutes.
    """
    if not st.session_state.get("timer_running"):
        return
    start_ts = st.session_state.get("timer_start_ts")
    if not start_ts:
        return

    now = time.time()
    elapsed = now - start_ts
    if elapsed <= 0:
        return

    minutes = int(elapsed // 60)
    if minutes > 0:
        session = get_current_session()
        current = int(session.get("total_time_minutes", 0))
        update_current_session({"total_time_minutes": current + minutes})
        st.session_state["timer_start_ts"] = now  # reset base


def format_time_from_minutes(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    # simple hh:mm:ss display
    return f"{hours:02d}:{minutes:02d}:00"


# --- Layout helpers / CSS --------------------------------------------------
def inject_custom_css():
    """
    Pull styling from mockup.css if you decide to separate it,
    otherwise fall back to a small embedded theme that echoes
    your HTML mockup.
    """
    css_path = "mockup.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
    else:
        css = """
        :root {
            --color-primary: #2563eb;
            --color-primary-dark: #1e40af;
            --color-primary-light: #dbeafe;
            --color-bg-alt: #f9fafb;
            --color-surface: #ffffff;
            --color-border: #e5e7eb;
            --color-text: #1f2937;
            --color-text-secondary: #6b7280;
            --radius-lg: 0.75rem;
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1),
                         0 2px 4px -1px rgba(0,0,0,0.06);
        }
        body {
            background: var(--color-bg-alt);
        }
        .app-header {
            background: var(--color-surface);
            border-bottom: 1px solid var(--color-border);
            padding: 0.75rem 1.5rem;
            margin: -1rem -1rem 1rem -1rem;
        }
        .app-logo {
            font-weight: 700;
            font-size: 1.25rem;
            color: var(--color-primary);
            display: flex;
            align-items: center;
            gap: .5rem;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            font-size: 0.8rem;
            padding: 0.15rem 0.6rem;
            border-radius: 999px;
            border: 1px solid var(--color-border);
            color: var(--color-text-secondary);
            gap: 0.25rem;
            margin-right: 0.35rem;
        }
        .module-panel {
            background: var(--color-surface);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
        }
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_header(session: Dict[str, Any]):
    session_name = session.get("task_name") or session.get("name") or "New session"
    with st.container():
        st.markdown(
            f"""
            <div class="app-header">
              <div style="display:flex;align-items:center;justify-content:space-between;gap:1rem;">
                <div class="app-logo">
                    <span>🌱</span>
                    <span>Thrive in Learning</span>
                </div>
                <div style="display:flex;flex-wrap:wrap;align-items:center;gap:.5rem;font-size:.8rem;">
                    <span class="pill">📝 <span>{session_name}</span></span>
                    <span class="pill">🎯 <span>{session.get('goal_type', 'mastery').title()} goal</span></span>
                    <span class="pill">⏱️ <span>{session.get('total_time_minutes', 0)} min logged</span></span>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_session_toolbar():
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("💾 Save session", use_container_width=True):
            save_session_snapshot()

    with col2:
        if st.button("➕ New session", use_container_width=True):
            new_session_action()

    with col3:
        with st.expander("📂 Sessions", expanded=False):
            sessions = st.session_state.get("sessions", {})
            if not sessions:
                st.caption("No saved sessions yet.")
            else:
                for sid, sess in sessions.items():
                    label = sess.get("task_name") or sess.get("name") or "Untitled"
                    is_current = sid == st.session_state.get("current_session_id")
                    row = st.columns([4, 1, 1])
                    row[0].markdown(f"**{label}**" + ("  ✅" if is_current else ""))
                    if row[1].button("Load", key=f"load_{sid}"):
                        st.session_state["current_session_id"] = sid
                        st.experimental_rerun()
                    if row[2].button("🗑️", key=f"del_{sid}"):
                        delete_session(sid)
                        st.experimental_rerun()


def render_module_selector(active_module: str) -> str:
    st.markdown("#### Learning modules")
    for module in MODULES:
        is_active = module["id"] == active_module
        label = f"{module['emoji']}  {module['label']}"
        button_label = f"**{label}**" if is_active else label

        if st.button(button_label, key=f"module_{module['id']}", use_container_width=True):
            st.session_state["active_module"] = module["id"]
            active_module = module["id"]

        if is_active:
            st.caption(module["description"])
    return active_module


# --- Module renderers ------------------------------------------------------
def render_goal_module(session: Dict[str, Any]):
    st.subheader("🎯 Goal Setting")
    st.markdown(
        "Focus on **mastery goals** – goals about understanding, skills, and growth, not just grades."
    )

    col1, col2 = st.columns(2)

    with col1:
        task_name = st.text_input(
            "What task or assignment are you working on?",
            value=session.get("task_name", ""),
            key="goal_task_name",
            placeholder="e.g., Research paper on climate change",
        )

        task_type_options = [
            "",
            "Research paper",
            "Problem-solving assignment",
            "Reading / article",
            "Exam preparation",
            "Project",
            "Presentation",
            "Other",
        ]
        current_type = session.get("task_type", "")
        idx = task_type_options.index(current_type) if current_type in task_type_options else 0

        task_type = st.selectbox(
            "What type of task is this?",
            task_type_options,
            index=idx,
            key="goal_task_type",
        )

        deadline = st.date_input(
            "Target completion date (optional)",
            value=None,
            key="goal_deadline",
            help="You can leave this as the default if you're not sure.",
        )

    with col2:
        goal_type = st.radio(
            "Which best matches your main goal for this task?",
            options=["mastery (understand deeply)", "performance (get a grade/score)"],
            index=0 if session.get("goal_type", "mastery") == "mastery" else 1,
            key="goal_type_radio",
        )

        goal_description = st.text_area(
            "Describe your **mastery goal** in your own words",
            value=session.get("goal_description", ""),
            key="goal_description",
            placeholder="What do you want to understand or be able to do after this task?",
            height=120,
        )

    if st.button("Save goal", key="save_goal_main"):
        update_current_session(
            {
                "task_name": task_name.strip(),
                "task_type": task_type.strip(),
                "goal_type": "mastery"
                if goal_type.startswith("mastery")
                else "performance",
                "goal_description": goal_description.strip(),
                "deadline": str(deadline) if deadline else "",
            }
        )
        st.success("Goal saved. Next, you can analyze the task or pick strategies.")

    st.markdown("---")
    st.markdown("##### Ask AI to refine your goal")

    user_msg = st.text_area(
        "Describe what you want to achieve, and the assistant will suggest a clearer mastery goal.",
        key="goal_ai_input",
        height=100,
    )

    if st.button("✨ Improve my goal", key="goal_ai_button") and user_msg.strip():
        with st.spinner("Thinking about your goal..."):
            reply = call_gemini_for_module("goal", user_msg, get_current_session())
        st.session_state["ai_responses"]["goal"] = reply

    if st.session_state["ai_responses"].get("goal"):
        st.markdown("###### AI suggestion")
        st.markdown(st.session_state["ai_responses"]["goal"])


def render_task_module(session: Dict[str, Any]):
    st.subheader("🔍 Task Analysis")

    if not session.get("task_name"):
        st.info("Set a task and goal in **Goal Setting** first, then come back here.")
    else:
        st.markdown(
            f"**Current task:** {session['task_name']}  \n"
            f"**Goal type:** {session.get('goal_type', 'mastery').title()}  ｜  "
            f"**Task type:** {session.get('task_type', 'not specified')}"
        )

    requirements = st.text_area(
        "What are the key requirements or rubric criteria?",
        value=session.get("requirements", ""),
        key="task_requirements",
        height=120,
    )

    subtasks = st.text_area(
        "Break your task into smaller subtasks (one per line).",
        value=session.get("subtasks", ""),
        key="task_subtasks",
        height=120,
        placeholder="e.g.,\nFind 5 credible sources\nCreate an outline\nDraft introduction\n...",
    )

    col1, col2 = st.columns(2)

    with col1:
        prior_knowledge = st.text_area(
            "What do you already know that might help?",
            value=session.get("prior_knowledge", ""),
            key="task_prior",
            height=100,
        )

    with col2:
        knowledge_gaps = st.text_area(
            "What do you need to review or learn?",
            value=session.get("knowledge_gaps", ""),
            key="task_gaps",
            height=100,
        )

    challenges = st.text_area(
        "What challenges do you anticipate?",
        value=session.get("anticipated_challenges", ""),
        key="task_challenges",
        height=100,
    )

    contingency = st.text_area(
        "If those challenges happen, what is your plan B?",
        value=session.get("contingency_plan", ""),
        key="task_contingency",
        height=100,
    )

    if st.button("Save task analysis", key="save_task_analysis"):
        update_current_session(
            {
                "requirements": requirements.strip(),
                "subtasks": subtasks.strip(),
                "prior_knowledge": prior_knowledge.strip(),
                "knowledge_gaps": knowledge_gaps.strip(),
                "anticipated_challenges": challenges.strip(),
                "contingency_plan": contingency.strip(),
            }
        )
        st.success("Task analysis saved ✅")

    st.markdown("---")
    st.markdown("##### Ask AI to check your breakdown")

    msg = st.text_area(
        "Paste your assignment instructions or your notes, and the assistant can suggest a clearer breakdown.",
        key="task_ai_input",
        height=120,
    )

    if st.button("🔍 Improve my breakdown", key="task_ai_button") and msg.strip():
        with st.spinner("Analyzing your task..."):
            reply = call_gemini_for_module("task", msg, get_current_session())
        st.session_state["ai_responses"]["task"] = reply

    if st.session_state["ai_responses"].get("task"):
        st.markdown("###### AI suggestion")
        st.markdown(st.session_state["ai_responses"]["task"])


def render_strategies_module(session: Dict[str, Any]):
    st.subheader("💡 Learning Strategies")
    st.markdown(
        "Select strategies you'd like to try for this task. Start with a few and actually use them."
    )

    strategy_options = [
        "Elaborative interrogation (ask why/how questions)",
        "Self-explanation (teach it aloud or in writing)",
        "Spaced practice (short sessions over days)",
        "Practice testing (quiz yourself)",
        "Concept mapping / diagrams",
        "Worked examples then fading",
        "Interleaving different problem types",
    ]

    chosen = st.multiselect(
        "Which strategies do you plan to use?",
        options=strategy_options,
        default=[
            s
            for s in strategy_options
            if s in session.get("chosen_strategies", [])
        ],
        key="strategies_multiselect",
    )

    plan = st.text_area(
        "How will you use these strategies in this task?",
        value=session.get("session_plan", ""),
        key="strategies_plan",
        height=120,
        placeholder=(
            "Example: On Monday I will skim all articles, then on Tuesday I will do self-explanation "
            "notes for two of them..."
        ),
    )

    if st.button("Save strategy plan", key="save_strategies"):
        update_current_session(
            {
                "chosen_strategies": chosen,
                "session_plan": plan.strip(),
            }
        )
        st.success("Strategy plan saved ✅")

    st.markdown("---")
    st.markdown("##### Ask AI for strategy ideas")

    msg = st.text_area(
        "Describe your situation (time available, task type, how you like to study), "
        "and the assistant will suggest strategies.",
        key="strategies_ai_input",
        height=120,
    )

    if st.button("✨ Suggest strategies", key="strategies_ai_button") and msg.strip():
        with st.spinner("Brainstorming strategies with you..."):
            reply = call_gemini_for_module("strategies", msg, get_current_session())
        st.session_state["ai_responses"]["strategies"] = reply

    if st.session_state["ai_responses"].get("strategies"):
        st.markdown("###### AI suggestion")
        st.markdown(st.session_state["ai_responses"]["strategies"])


def render_time_module(session: Dict[str, Any]):
    st.subheader("⏱️ Time Management")

    # Update total_time_minutes based on timer state
    sync_timer_with_session()
    total_minutes = int(session.get("total_time_minutes", 0))

    st.markdown(
        f"**Logged study time for this task:** `{format_time_from_minutes(total_minutes)}`"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start / continue timer", key="timer_start", use_container_width=True):
            st.session_state["timer_running"] = True
            st.session_state["timer_start_ts"] = time.time()

        if st.button("⏸️ Pause timer", key="timer_pause", use_container_width=True):
            st.session_state["timer_running"] = False
            st.session_state["timer_start_ts"] = None

        if st.button("⏹️ Reset total logged time", key="timer_reset", use_container_width=True):
            update_current_session({"total_time_minutes": 0})
            st.session_state["timer_running"] = False
            st.session_state["timer_start_ts"] = None

    with col2:
        est_session_minutes = st.number_input(
            "For your **next** study session, how many minutes do you plan to work?",
            min_value=5,
            max_value=240,
            step=5,
            value=45,
            key="time_estimate",
        )

        break_pattern = st.selectbox(
            "Break schedule",
            [
                "Pomodoro (25 min work, 5 min break)",
                "50-10 (50 work, 10 break)",
                "Long focus (90 min work, 15 min break)",
                "Custom / flexible",
            ],
            key="time_break_pattern",
        )

    if st.button("Save time plan", key="save_time_plan"):
        recent = list(session.get("recent_sessions", []))
        recent.insert(
            0,
            {
                "estimated_minutes": int(est_session_minutes),
                "break_pattern": break_pattern,
                "created_at": time.time(),
            },
        )
        recent = recent[:10]  # keep last 10
        update_current_session({"recent_sessions": recent})
        st.success("Time plan saved ✅")

    if session.get("recent_sessions"):
        st.markdown("##### Recent planned sessions")
        for idx, s_item in enumerate(session["recent_sessions"], start=1):
            ts = time.strftime(
                "%b %d, %Y",
                time.localtime(s_item.get("created_at", time.time())),
            )
            st.markdown(
                f"- `{ts}` – planned {s_item.get('estimated_minutes', 0)} min ｜ {s_item.get('break_pattern', '')}"
            )

    st.markdown("---")
    st.markdown("##### Ask AI to adjust your schedule")

    msg = st.text_area(
        "Explain your weekly schedule and constraints, and the assistant can help you fit this task in realistically.",
        key="time_ai_input",
        height=120,
    )

    if st.button("🗓️ Help me plan my week", key="time_ai_button") and msg.strip():
        with st.spinner("Planning around your schedule..."):
            reply = call_gemini_for_module("time", msg, get_current_session())
        st.session_state["ai_responses"]["time"] = reply

    if st.session_state["ai_responses"].get("time"):
        st.markdown("###### AI suggestion")
        st.markdown(st.session_state["ai_responses"]["time"])


def render_resources_module(session: Dict[str, Any]):
    st.subheader("📚 Resources")
    st.markdown("List the key resources you will actually use for this task.")

    res_name = st.text_input(
        "Resource name or short description",
        key="res_name",
        placeholder="e.g., Chapter 5: Climate Systems (textbook)",
    )

    res_type = st.selectbox(
        "Type",
        [
            "",
            "Textbook / reading",
            "Academic article",
            "Video / tutorial",
            "Tool / software",
            "Person / tutor / office hours",
            "Other",
        ],
        key="res_type",
    )

    res_link = st.text_input(
        "Link or location (optional)",
        key="res_link",
        placeholder="https://... or 'Library, shelf QC 903'",
    )

    if st.button("➕ Add resource", key="add_resource"):
        if not res_name.strip():
            st.warning("Give the resource at least a short name.")
        else:
            resources = list(session.get("resources", []))
            resources.append(
                {
                    "name": res_name.strip(),
                    "type": res_type.strip(),
                    "link": res_link.strip(),
                }
            )
            update_current_session({"resources": resources})
            st.success("Resource added.")
            # clear widget values for the next entry
            st.session_state["res_name"] = ""
            st.session_state["res_type"] = ""
            st.session_state["res_link"] = ""

    resources = session.get("resources", [])
    if resources:
        st.markdown("##### Your resources")
        for idx, r in enumerate(resources, start=1):
            line = f"- **{r.get('name','(no name)')}**"
            if r.get("type"):
                line += f"  ·  {r['type']}"
            if r.get("link"):
                line += f"  ·  {r['link']}"
            st.markdown(line)

    st.markdown("---")
    st.markdown("##### Ask AI for resource ideas")

    msg = st.text_area(
        "Describe what kind of explanations, examples, or tools help you most, and the assistant can suggest resource types.",
        key="resources_ai_input",
        height=120,
    )

    if st.button("🔎 Suggest resources", key="resources_ai_button") and msg.strip():
        with st.spinner("Looking for resource ideas..."):
            reply = call_gemini_for_module("resources", msg, get_current_session())
        st.session_state["ai_responses"]["resources"] = reply

    if st.session_state["ai_responses"].get("resources"):
        st.markdown("###### AI suggestion")
        st.markdown(st.session_state["ai_responses"]["resources"])


def render_reflection_module(session: Dict[str, Any]):
    st.subheader("✨ Reflection")
    st.markdown(
        "Reflection helps you **close the loop**: connect what happened to what you want to change next time."
    )

    refs = session.get(
        "reflections",
        {"goal": "", "strategies": "", "time": "", "growth": ""},
    )

    goal_ref = st.text_area(
        "1. Goal achievement – What did you actually learn or understand? Did you reach your mastery goal?",
        value=refs.get("goal", ""),
        key="refl_goal",
        height=120,
    )

    strat_ref = st.text_area(
        "2. Strategies – Which strategies helped most? Which did you not use or found unhelpful?",
        value=refs.get("strategies", ""),
        key="refl_strategies",
        height=120,
    )

    time_ref = st.text_area(
        "3. Time & focus – How well did you stick to your plan? What affected your focus?",
        value=refs.get("time", ""),
        key="refl_time",
        height=120,
    )

    growth_ref = st.text_area(
        "4. Next steps – What will you do **differently** for the next similar task?",
        value=refs.get("growth", ""),
        key="refl_growth",
        height=120,
    )

    if st.button("Save reflection", key="save_reflection"):
        update_current_session(
            {
                "reflections": {
                    "goal": goal_ref.strip(),
                    "strategies": strat_ref.strip(),
                    "time": time_ref.strip(),
                    "growth": growth_ref.strip(),
                }
            }
        )
        st.success("Reflection saved 🌱")

    st.markdown("---")
    st.markdown("##### Ask AI to deepen your reflection")

    msg = st.text_area(
        "Paste a short summary of what happened (or the text above), and the assistant will ask a few deeper questions or highlight patterns.",
        key="reflection_ai_input",
        height=150,
    )

    if st.button("🪞 Help me reflect", key="reflection_ai_button") and msg.strip():
        with st.spinner("Thinking with you about this experience..."):
            reply = call_gemini_for_module("reflection", msg, get_current_session())
        st.session_state["ai_responses"]["reflection"] = reply

    if st.session_state["ai_responses"].get("reflection"):
        st.markdown("###### AI suggestion")
        st.markdown(st.session_state["ai_responses"]["reflection"])


# --- Main entrypoint -------------------------------------------------------
def main():
    init_app_state()
    inject_custom_css()
    session = get_current_session()

    # Optional: logo image in sidebar if you add bot.png
    if os.path.exists("bot.png"):
        with st.sidebar:
            st.image("bot.png", caption="Thrive in Learning", use_container_width=True)

    render_header(session)
    render_session_toolbar()

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        active_module = render_module_selector(
            st.session_state.get("active_module", "goal")
        )

    with col_right:
        st.markdown('<div class="module-panel">', unsafe_allow_html=True)

        if active_module == "goal":
            render_goal_module(session)
        elif active_module == "task":
            render_task_module(session)
        elif active_module == "strategies":
            render_strategies_module(session)
        elif active_module == "time":
            render_time_module(session)
        elif active_module == "resources":
            render_resources_module(session)
        elif active_module == "reflection":
            render_reflection_module(session)
        else:
            st.info("Pick a module on the left to begin.")

        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()

