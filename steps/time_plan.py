# steps/time_plan.py
import streamlit as st
from datetime import datetime, timedelta
from steps.base import StepModule
from state import SRLState

class TimePlanStep(StepModule):
    key, label, icon = "time_plan", "Time Plan", "⏰"

    def render(self, st, state: SRLState):
        st.subheader(f"{self.icon} Make a Time Plan")

        col1, col2 = st.columns(2)
        with col1:
            minutes = st.number_input("Focus block (minutes)", 10, 120, state.timer_duration_min, 5)
            blocks  = st.number_input("How many blocks today?", 1, 12, 2, 1)
            breaks  = st.number_input("Break between blocks (minutes)", 1, 30, 5, 1)
        with col2:
            start = st.time_input("Start time", value=datetime.now().time())
            today = st.date_input("Date")

        if st.button("Create Plan"):
            state.timer_duration_min = int(minutes)
            start_dt = datetime.combine(today, start)
            schedule = []
            t = start_dt
            for i in range(int(blocks)):
                end = t + timedelta(minutes=int(minutes))
                schedule.append(f"Block {i+1}: {t.strftime('%H:%M')}–{end.strftime('%H:%M')}")
                t = end + timedelta(minutes=int(breaks))
            state.time_plan = "\n".join(schedule)
            st.success("Time plan created.")
            st.rerun()

        if state.time_plan:
            st.markdown("---")
            st.markdown("**Today's Blocks**")
            st.info(state.time_plan)
