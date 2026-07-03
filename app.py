import streamlit as st
import pandas as pd
import database

st.title("Learning Session Tracker")
database.create_table()

st.subheader("Add a new learning session")

title = st.text_input("Enter the title of the learning session")
category = st.selectbox(
    "Select the category of the learning session",
    ["Programming", "Language", "Framework", "Other"],
)
duration_minutes = st.number_input(
    "Enter the duration of the learning session in minutes",
    min_value=1,
    step=1,
    value=30,
)
additional_notes = st.text_area("Enter any additional notes", value="")

if st.button("Add learning session"):
    if not title.strip():
        st.error("Please enter a title for the learning session.")
    elif duration_minutes <= 0:
        st.error("Please enter a valid duration for the learning session.")
    else:
        database.add_learning_session(title, category, duration_minutes, additional_notes)
        st.success("Saved learning session")
        st.rerun()

st.subheader("Learning sessions")

sessions = database.get_all_learning_sessions()
if sessions:
    for session in sessions:
        session_id, sess_title, sess_category, date_added, sess_duration, notes = session

        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(
                f"**{sess_title}** ({sess_category}) — {sess_duration} min — {date_added}"
            )
            if notes:
                st.caption(notes)
        with col2:
            if st.button("Delete", key=f"delete_{session_id}"):
                database.delete_learning_session(session_id)
                st.success("Deleted learning session")
                st.rerun()

    df = pd.DataFrame(
        sessions,
        columns=[
            "Session ID",
            "Title",
            "Category",
            "Date Added",
            "Duration Minutes",
            "Additional Notes",
        ],
    )
    st.dataframe(df)
else:
    st.info("No learning sessions yet.")
