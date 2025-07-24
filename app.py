import streamlit as st
import pandas as pd

st.title("🤖 Human-Aware Operations Assistant")

# Google Sheets CSV export link - replace with your own
sheet_url = "https://docs.google.com/spreadsheets/d/1-D6dHq5aZHzLZMsbQdc0l6GFa8JVa4OmwiMxN_XjtfQ/export?format=csv"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

df = load_data(sheet_url)

if df is not None:
    st.subheader("📋 Task Data Overview")
    st.dataframe(df)

    # Adjust column names to exactly match your Google Sheet headers
    def is_overloaded(row):
        try:
            return (row['Task Duration (hrs)'] > 5) or (row['Fatigue Score (1–5)'] >= 4)
        except KeyError:
            st.error("Check your Google Sheet column names. They must exactly match!")
            return False

    df['Overloaded'] = df.apply(is_overloaded, axis=1)

    st.subheader("⚠️ Overload Recommendations")
    overloaded = df[df['Overloaded']]

    if overloaded.empty:
        st.success("All employees are within healthy workload levels!")
    else:
        for _, row in overloaded.iterrows():
            st.warning(f"{row['Employee Name']} is overloaded. Consider reassigning '{row['Task Name']}'.")

    st.subheader("📬 Feedback")
    feedback = st.radio("Was this recommendation helpful?", ["Yes", "No"], horizontal=True)
    if feedback:
        st.write("✅ Thanks for your feedback!")
else:
    st.write("No data to display.")
