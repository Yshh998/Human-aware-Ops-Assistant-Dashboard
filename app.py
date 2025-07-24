import streamlit as st
import pandas as pd

st.title("🤖 Human-Aware Operations Assistant")

uploaded_file = st.file_uploader("Upload your task data (CSV or Excel)", type=["csv", "xlsx"])

def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file format.")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

if uploaded_file is not None:
    df = load_data(uploaded_file)

    if df is not None:
        st.subheader("📋 Task Data Overview")
        st.dataframe(df)

        def is_overloaded(row):
            try:
                return (row['Task Duration (hrs)'] > 5) or (row['Fatigue Score (1–5)'] >= 4)
            except KeyError:
                st.error("Check your column names!")
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
    st.info("Please upload a file to begin.")
