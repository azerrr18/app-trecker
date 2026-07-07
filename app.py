import streamlit as st
import pandas as pd
import database
import openpyxl
from datetime import datetime

st.title("Learning  Tracker")
database.create_table()
if "edit_session_id" not in st.session_state:
    st.session_state.edit_session_id = None
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



if st.session_state.edit_session_id is not None:
    session = database.get_learning_session_by_id(st.session_state.edit_session_id)
    if session:
        session_id,title,category ,date_added,duration_minutes,additional_notes = session

        st.subheader("Edit learning session")
        with st.form(key = f"edit_form_{session_id}"):
            new_title = st.text_input("Title", value=title)
            new_category = st.selectbox(
                "Category",
                ["Programming", "Language", "Framework", "Other"],
                index=["Programming", "Language", "Framework", "Other"].index(category),)
            new_duration = st.number_input("Duration (minutes)",min_value=1,value=duration_minutes)
            new_notes = st.text_area("Notes", value=additional_notes or "")

            col_save, col_cancel = st.columns(2)
            save = col_save.form_submit_button("Save changes")
            cancel = col_cancel.form_submit_button("Cancel")

        if save:
            if not new_title.strip():
                st.error("Please enter the title")
            elif new_duration <=0:
                st.error("Duration must be more then 0")
            else:
                database.update_learning_session(
                    session_id, new_title, new_category, new_duration, new_notes
                )
                st.session_state.edit_session_id = None
                st.success("Session updated")
                st.rerun()
        
        if cancel:
            st.session_state.edit_session_id = None
            st.rerun()





sessions = database.get_all_learning_sessions()
if sessions:
    for session in sessions:
        session_id, sess_title, sess_category, date_added, sess_duration, notes = session

        col1,col2,col3 = st.columns([4,1,1])
        with col1:
            st.write(
                f"**{sess_title}** ({sess_category}) — {sess_duration} min — {date_added}"
            )
            if notes:
                st.caption(notes)
        with col2:
            if st.button("Edit",key = f"edit_{session_id}"):
                st.session_state.edit_session_id = session_id
                st.rerun()

        with col3:
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
        ]
        
    )
    st.dataframe(df)
else:
    st.info("No learning sessions yet.")

csv = df.to_csv(index = False)
st.download_button(
    label = "Download data as CSV",
    data = csv,
    file_name = "learning_sessions.csv",
    mime = "text/csv"
)


st.subheader("Import learning sessions from Excel")
uploaded_file = st.file_uploader("Choose an excel file", type = ['xlsx'])
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("### Imported Data")
        st.dataframe(df)
        for index, row in df.iterrows():
            title = row.get("Title")
            category = row.get("category")
            duration_minutes = row.get("duration_minutes")
            additional_notes = row.get("additional_notes")
            if title and category and duration_minutes:
                database.add_learning_session(title, category, duration_minutes, additional_notes)
                st.success(f"Added learning session:{title=}{category}={duration_minutes}={additional_notes}")
                if st.button("Rerun after import"):
                    st.success("Import completed. Rerunning the app to reflect changes.")
                    st.rerun()

    except Exception as e:
        st.error(f"Error processing the file: {e}") 

st.subheader("Learning session Timer")

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_start_time" not in st.session_state:
    st.session_state.timer_start_time = None
if "timer_end_time" not in st.session_state:
    st.session_state.timer_end_time = None


if st.button("Start Timer"):
    if not st.session_state.timer_running:
        st.session_state.timer_running = True
        st.session_state.timer_start_time = datetime.now()
        st.info("Timer started. You can now focus on your learning session.")

if st.button("Stop Timer"):
    if not st.session_state.timer_running:
        st.session_state.timer_running = False
        st.session_state.timer_end_time = datetime.now()
        st.info("Timer stopped. You can now save your learning session.")

if  st.session_state.timer_start_time is not None and st.session_state.timer_end_time is not None:
    elapsed_time = st.session_state.timer_end_time - st.session_state.timer_start_time
    minutes = max(1, round(elapsed_time.total_seconds() // 60))
    st.success(f"Timer completed! Total time: {minutes} minutes.")
    st.info("You can now add this session to your learning sessions.")

    st.subheader("Save this session")
    timer_title = st.text_input("Enter the title of the learning session",key="timer_title")
    timer_category = st.selectbox(
        "Select the category of the learning session",
        ["Programming", "Language", "Framework", "Other"],
        key="timer_category",
    )
    timer_notes = st.text_area("Enter any additional notes", value="", key="timer_notes")
    st.info(f"Duration: {minutes} minutes")

    if st.button("Save this session"):
        if not timer_title.strip():
            st.error("Please enter a title for the learning session.")
        else:
            database.add_learning_session(timer_title, timer_category, minutes, timer_notes)
            st.success("Saved learning session")
            st.session_state.timer_start_time = None
            st.session_state.timer_end_time = None
            st.rerun()



