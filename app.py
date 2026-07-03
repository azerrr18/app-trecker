import streamlit as st
import database

st.title("Learning Session Tracker")
database.create_table()

st.subheader("Add a new learning session")

title = st.text_input("Enter the title of the learning session")
category = st.selectbox("Select the category of the learning session", ["Programming", "Language", "Framework", "Other"])
duration_minutes = st.number_input("Enter the duration of the learning session in minutes", value=0, min_value=0, step=1)
additional_notes = st.text_area("Enter any additional notes", value="")

if st.button("Add learning session"):
    database.add_learning_session(title, category, duration_minutes, additional_notes)
    st.success("Saved learning session")

st.subheader("Learning sessions")

sessions = database.get_all_learning_sessions()
if sessions:
    for session in sessions:
        session_id, title, category, date_added, duration_minutes, notes = session
        st.write(f"**{title}** ({category}) — {duration_minutes} min — {date_added}")
        if notes:
            st.caption(notes)
else:
    st.info("No learning sessions yet.")


