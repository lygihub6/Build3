import streamlit as st
from steps.base import StepModule
from state import SRLState

# New helper function
def classify_goal(goal: str) -> str:
    text = goal.lower()
    mastery_keywords = ["learn", "understand", "improve", "develop", "practice", "skill", "knowledge", "explore"]
    performance_keywords = ["grade", "score", "exam", "test", "rank", "win", "pass"]
    has_mastery = any(word in text for word in mastery_keywords)
    has_performance = any(word in text for word in performance_keywords)
    if has_performance and not has_mastery:
        return "performance"
    if has_mastery:
        return "mastery"
    return "performance"

class GoalsStep(StepModule):
    key, label, icon = "goals", "Goals", "🎯"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Set Mastery Goals")
        g = st.text_area("What will you be able to **know/do** by the end? (1–2 goals)")
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Add Goal"):
                if g.strip():
                    goal_text = g.strip()
                    goal_type = classify_goal(goal_text)
                    state.learning_goals.append(goal_text)
                    state.goal_types.append(goal_type)
                    if goal_type == "mastery":
                        st.success("Goal added. This is a mastery goal focused on building knowledge or skills.")
                    else:
                        st.warning("Goal added. This seems like a performance goal; try rephrasing it to emphasize learning and improvement.")
                    st.rerun()
        with c2:
            if st.button("Clear Goals"):
                state.learning_goals.clear()
                state.goal_types.clear()
                st.rerun()
        if state.learning_goals:
            st.markdown("**Your goals:**")
            for i, goal in enumerate(state.learning_goals, 1):
                goal_type = state.goal_types[i - 1]
                label = "Mastery" if goal_type == "mastery" else "Performance"
                st.write(f"{i}. {goal} ({label} goal)")
