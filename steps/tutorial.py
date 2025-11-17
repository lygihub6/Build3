"""
Tutorial step implementation.

This module provides a comprehensive introduction to the Thrive in Learning
app. It explains the purpose of the app, guides students through the quick
start process, describes the main areas of the app, and offers tips for
effective use. This step serves as onboarding for new users.
"""

from __future__ import annotations

import streamlit as st
from typing import Any, Dict

from .base import BaseStep


class TutorialStep(BaseStep):
    """Tutorial and welcome SRL step."""

    id = "tutorial"
    label = "Tutorial"
    emoji = "👋"
    description = "Learn how to use Thrive in Learning effectively."

    def render(self, session: Dict[str, Any]) -> None:
        st.markdown(
            """
            # 👋 Welcome to Thrive in Learning
            
            **Thrive in Learning** is your learning companion. Use this app to set clear goals, 
            plan your strategies, stay focused while you work, and reflect on what you've learned.
            """
        )
        
        st.markdown("---")
        
        # Quick Start Section
        st.markdown("## 🚀 Quick Start")
        
        st.markdown(
            """
            #### 1. Set your goal
            Tell Thrive in Learning what you're working on (homework, project, exam prep, etc.).
            
            **Example:** *"Finish my chemistry worksheet on atoms."*
            """
        )
        
        st.markdown(
            """
            #### 2. Plan your strategy
            Break your goal into smaller steps. The app can help you:
            * Decide where to start
            * Estimate how long each step might take
            * Choose strategies (review notes, practice problems, teach-back, etc.)
            """
        )
        
        st.markdown(
            """
            #### 3. Work with the app beside you
            As you work, use the chat and tools to:
            * Ask for hints or explanations
            * Get feedback on your ideas
            * Adjust your plan if you get stuck
            """
        )
        
        st.markdown(
            """
            #### 4. Reflect and improve
            When you finish (or pause):
            * Log what you completed
            * Notice what worked well
            * Note what you want to do differently next time
            """
        )
        
        st.markdown("---")
        
        # Main Areas Section
        st.markdown("## 🧭 Main Areas of the App")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                """
                ### 🎯 Goals & Plans
                Create or update your study goals. Break big tasks into small, 
                doable steps and keep track of them.
                """
            )
        
        with col2:
            st.markdown(
                """
                ### 💬 Chat & Check-ins
                Talk to the AI like a study partner. Ask questions, share your 
                progress, or say how you're feeling about your work.
                """
            )
        
        with col3:
            st.markdown(
                """
                ### ✨ Reflection
                Look back on what you did, how it went, and what you learned. 
                Use this space to build better habits over time.
                """
            )
        
        st.markdown("---")
        
        # Tips Section
        st.markdown("## 💡 Tips for Thriving in Learning")
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown(
                """
                #### 🎯 Be specific with your goals
                Instead of "study math," try "review 10 practice problems on quadratic equations."
                
                #### 🗣️ Share your obstacles
                If you're confused, bored, tired, or distracted, say so. The app can 
                suggest strategies to help.
                """
            )
        
        with tips_col2:
            st.markdown(
                """
                #### ⏱️ Use short work cycles
                Work in short blocks (e.g., 15–25 minutes), then check in and update 
                your plan or reflect.
                
                #### 🔄 Come back often
                The more regularly you use Thrive in Learning, the better it can support 
                your learning patterns over time.
                """
            )
        
        st.markdown("---")
        
        # Call to Action
        st.info(
            "**Ready to start?** Head to the **Goal Setting** module on the left to begin your learning journey! 🌱"
        )
