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
        # Custom CSS for tutorial-specific styling (compact version)
        st.markdown(
            """
            <style>
            .tutorial-hero {
                text-align: center;
                padding: 1.25rem 0.75rem;
                background: linear-gradient(135deg, #d0ddfb 0%, #bad9f5 100%);
                border-radius: 0.75rem;
                margin-bottom: 1.25rem;
            }
            .tutorial-hero h1 {
                color: #1f2933;
                margin-bottom: 0.25rem;
                font-size: 1.75rem;
            }
            .tutorial-hero p {
                color: #52606d;
                font-size: 0.95rem;
                margin: 0;
            }
            .section-header {
                font-size: 1.3rem;
                color: #1f2933;
                margin-top: 1rem;
                margin-bottom: 0.75rem;
            }
            .step-card {
                background: white;
                border-radius: 0.5rem;
                padding: 0.875rem;
                margin-bottom: 0.625rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                border-left: 3px solid #f5aa07;
            }
            .step-card h4 {
                color: #f5aa07;
                margin: 0 0 0.375rem 0;
                font-size: 0.95rem;
            }
            .step-card p {
                margin: 0.25rem 0;
                font-size: 0.9rem;
                line-height: 1.4;
            }
            .step-card ul {
                margin: 0.375rem 0 0 1.25rem;
                padding: 0;
            }
            .step-card li {
                font-size: 0.9rem;
                margin-bottom: 0.25rem;
            }
            .feature-box {
                background: white;
                border-radius: 0.5rem;
                padding: 0.875rem;
                height: 100%;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                border-top: 3px solid #f5aa07;
            }
            .feature-box h3 {
                color: #1f2933;
                margin: 0 0 0.5rem 0;
                font-size: 1rem;
            }
            .feature-box p {
                color: #52606d;
                line-height: 1.4;
                font-size: 0.9rem;
                margin: 0;
            }
            .tip-box {
                background: #f2f5ff;
                border-radius: 0.5rem;
                padding: 0.75rem;
                margin-bottom: 0.625rem;
                border-left: 3px solid #b5aeaf;
            }
            .tip-box h4 {
                color: #1f2933;
                margin: 0 0 0.375rem 0;
                font-size: 0.95rem;
            }
            .tip-box p {
                color: #52606d;
                margin: 0;
                line-height: 1.4;
                font-size: 0.9rem;
            }
            .cta-box {
                background: linear-gradient(135deg, #f5aa07 0%, #f5c547 100%);
                border-radius: 0.5rem;
                padding: 0.875rem;
                text-align: center;
                margin-top: 1rem;
            }
            .cta-box p {
                color: white;
                font-size: 0.95rem;
                font-weight: 600;
                margin: 0;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # Hero Section
        st.markdown(
            """
            <div class="tutorial-hero">
                <h1>👋 Welcome to Thrive in Learning</h1>
                <p>Your personal learning companion for setting goals, planning strategies, staying focused, and reflecting on your progress.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Quick Start Section
        st.markdown('<h2 class="section-header">🚀 Quick Start</h2>', unsafe_allow_html=True)
        
        # Step 1
        st.markdown(
            """
            <div class="step-card">
                <h4>1️⃣ Set your goal</h4>
                <p>Tell Thrive in Learning what you're working on (homework, project, exam prep, etc.).</p>
                <p><strong>Example:</strong> <em>"Finish my chemistry worksheet on atoms."</em></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Step 2
        st.markdown(
            """
            <div class="step-card">
                <h4>2️⃣ Plan your strategy</h4>
                <p>Break your goal into smaller steps. The app can help you:</p>
                <ul>
                    <li>Decide where to start</li>
                    <li>Estimate how long each step might take</li>
                    <li>Choose strategies (review notes, practice problems, teach-back, etc.)</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Step 3
        st.markdown(
            """
            <div class="step-card">
                <h4>3️⃣ Work with the app beside you</h4>
                <p>As you work, use the AI assistant and tools to:</p>
                <ul>
                    <li>Ask for hints or explanations</li>
                    <li>Get feedback on your ideas</li>
                    <li>Adjust your plan if you get stuck</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Step 4
        st.markdown(
            """
            <div class="step-card">
                <h4>4️⃣ Reflect and improve</h4>
                <p>When you finish (or pause):</p>
                <ul>
                    <li>Log what you completed</li>
                    <li>Notice what worked well</li>
                    <li>Note what you want to do differently next time</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Main Areas Section
        st.markdown('<h2 class="section-header">🧭 Main Areas of the App</h2>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                """
                <div class="feature-box">
                    <h3>🎯 Goals & Plans</h3>
                    <p>Create or update your study goals. Break big tasks into small, 
                    doable steps and keep track of them.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col2:
            st.markdown(
                """
                <div class="feature-box">
                    <h3>💬 AI Assistant</h3>
                    <p>Talk to the AI like a study partner. Ask questions, share your 
                    progress, or say how you're feeling about your work.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col3:
            st.markdown(
                """
                <div class="feature-box">
                    <h3>✨ Reflection</h3>
                    <p>Look back on what you did, how it went, and what you learned. 
                    Use this space to build better habits over time.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # Tips Section
        st.markdown('<h2 class="section-header">💡 Tips for Thriving in Learning</h2>', unsafe_allow_html=True)
        
        tips_col1, tips_col2 = st.columns(2)
        
        with tips_col1:
            st.markdown(
                """
                <div class="tip-box">
                    <h4>🎯 Be specific with your goals</h4>
                    <p>Instead of "study math," try "review 10 practice problems on quadratic equations."</p>
                </div>
                
                <div class="tip-box">
                    <h4>🗣️ Share your obstacles</h4>
                    <p>If you're confused, bored, tired, or distracted, say so. The app can 
                    suggest strategies to help.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with tips_col2:
            st.markdown(
                """
                <div class="tip-box">
                    <h4>⏱️ Use short work cycles</h4>
                    <p>Work in short blocks (e.g., 15–25 minutes), then check in and update 
                    your plan or reflect.</p>
                </div>
                
                <div class="tip-box">
                    <h4>🔄 Come back often</h4>
                    <p>The more regularly you use Thrive in Learning, the better it can support 
                    your learning patterns over time.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        # Call to Action
        st.markdown(
            """
            <div class="cta-box">
                <p>✨ Ready to start? Head to <strong>Goal Setting</strong> to begin your learning journey! 🌱</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

