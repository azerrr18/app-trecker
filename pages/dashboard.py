import plotly
import streamlit as st
import plotly.graph_objects as go
import database
import pandas as pd
from datetime import datetime, timedelta

st.title("Learning Session Tracker Dashboard")
st.subheader("Learning Sessions Overview")
col1, col2, col3 , col4 = st.columns(4)
col1.metric("Number of Sessions today", database.get_number_of_sessions_today() or 0)
col2.metric("Total Minutes today", database.get_today_minutes() or 0)
col3.metric("Number of Sessions This Month", database.get_number_of_sessions_this_month() or 0)
col4.metric("Total Minutes This Month", database.get_monthly_minutes() or 0)    


minutes_by_category = database.get_minutes_by_category()
df = pd.DataFrame(minutes_by_category, columns=["Category", "Total Minutes"]) 
fig = go.Figure(data=[go.Pie(labels=df["Category"], values=df["Total Minutes"], hole=.3)])
fig.update_layout(title_text="Total Minutes by Category")
plotly_chart = st.plotly_chart(fig, use_container_width=True)


minutes_by_day = database.get_minutes_by_day()
df_day = pd.DataFrame(minutes_by_day, columns = ["Date", "Minutes"])
df_day["Date"] = pd.to_datetime(df_day["Date"]).dt.strftime('%b %d')
st.write("### Total Minutes by Day (Last 7 Days)")
fig_day = go.Figure(data=[go.Bar(x=df_day["Date"], y=df_day["Minutes"])])
fig_day.update_layout(title_text="Total Minutes by Day (Last 7 Days)", xaxis_title="Date", yaxis_title="Minutes")
plotly_chart_day = st.plotly_chart(fig_day, use_container_width=True)



