

# Initialize pygame mixer
pygame.mixer.init()

# Load and play the sound
sound_path = "/Users/maria/PycharmProjects/Tech_Basics_2/Tech_Basics_2.2/FinalProject/sounds/piano.wav"
sound = pygame.mixer.Sound(sound_path)
sound.play()

# Keep the program running for a few seconds to hear the sound
pygame.time.delay(3000)


# pygame.mixer.Sound(sound_path).play()  # Comment this line


import streamlit as st
import time
import random

# Initialize session state for Pomodoro tracking
if "pomodoro_sessions" not in st.session_state:
    st.session_state.pomodoro_sessions = 0
if "active_task" not in st.session_state:
    st.session_state.active_task = ""
if "pomodoro_running" not in st.session_state:
    st.session_state.pomodoro_running = False

st.subheader("⏳ Stay Focused with Pomodoro Timer")

# Task Input Box
task_focus = st.text_input("Enter Task to Focus On", st.session_state.active_task)

if task_focus:
    st.session_state.active_task = task_focus
    st.write(f"🎯 **Focusing on:** {st.session_state.active_task}")
else:
    st.write("⚠️ Enter a task to focus on.")

# User-defined Pomodoro cycle settings
work_time = st.slider("Work Duration (minutes)", 5, 60, 25, key="work_duration")
break_time = st.slider("Break Duration (minutes)", 1, 15, 5, key="break_duration")

col1, col2 = st.columns(2)

# Start Pomodoro Timer Button
with col1:
    if st.button("▶ Start Pomodoro Session", use_container_width=True):
        st.session_state.pomodoro_running = True
        st.write("🚀 **Work Session Started! Stay focused.**")

        progress_bar = st.progress(0)

        # Work session countdown
        for i in range(work_time):
            if not st.session_state.pomodoro_running:
                st.warning("⏹️ Pomodoro session ended early.")
                progress_bar.empty()
                break
            progress_bar.progress((i + 1) / work_time)
            time.sleep(60)  # Wait for 1 minute

        if st.session_state.pomodoro_running:
            st.success("✅ Work Session Complete! Take a Break.")

            # Break session countdown
            st.write("🛑 **Time for a break!**")
            progress_bar.empty()
            for i in range(break_time):
                if not st.session_state.pomodoro_running:
                    st.warning("⏹️ Pomodoro session ended early.")
                    progress_bar.empty()
                    break
                progress_bar.progress((i + 1) / break_time)
                time.sleep(60)  # Wait for 1 minute

            # Session Completed
            st.session_state.pomodoro_sessions += 1
            st.success(f"🎉 Pomodoro Session {st.session_state.pomodoro_sessions} Completed!")

            # Motivational Break Suggestion
            break_suggestions = [
                "🌿 Stretch for 5 minutes.",
                "💧 Drink some water.",
                "🚶 Take a short walk.",
                "🧘 Do deep breathing exercises.",
                "📖 Read a few pages of a book."
            ]
            st.info(f"💡 **Break Tip:** {random.choice(break_suggestions)}")

# Finish Pomodoro Timer Button (ALWAYS VISIBLE)
with col2:
    if st.button("❌ Finish Pomodoro Timer", use_container_width=True):
        st.session_state.pomodoro_running = False
        st.warning("⏹️ Pomodoro session ended early.")
        st.rerun()  # Restart the script to stop the session
