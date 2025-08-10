import streamlit as st
import pandas as pd

st.set_page_config(page_title="Human-Aware Operations Assistant", page_icon="🤖")
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
        st.dataframe(df, use_container_width=True)

        def is_overloaded(row):
            try:
                return (row['Task Duration (hrs)'] > 5) or (row['Fatigue Score (1–5)'] >= 4)
            except KeyError:
                st.error("Check your column names! Expect: 'Task Duration (hrs)' and 'Fatigue Score (1–5)'.")
                return False

        df['Overloaded'] = df.apply(is_overloaded, axis=1)

        st.subheader("⚠️ Overload Recommendations")
        overloaded = df[df['Overloaded']]

        if overloaded.empty:
            st.success("All employees are within healthy workload levels!")
        else:
            for _, row in overloaded.iterrows():
                emp = row.get('Employee Name', '(name missing)')
                task = row.get('Task Name', '(task missing)')
                st.warning(f"{emp} is overloaded. Consider reassigning '{task}'.")

        st.subheader("📬 Feedback")
        feedback = st.radio("Was this recommendation helpful?", ["Yes", "No"], horizontal=True)
        if feedback:
            st.write("✅ Thanks for your feedback!")

        # ==============================
        # 💬 Chat about the uploaded data
        # ==============================
        from groq import Groq
        from streamlit_chat import message
        import json

        st.divider()
        st.subheader("💬 Ask questions about this data")

        def build_context(df):
            """Summarize key info for the model (keep it small for speed)."""
            cols = df.columns.tolist()
            ctx = {"row_count": int(len(df)), "columns": cols}

            # Overloaded summary
            if 'Overloaded' in df.columns:
                ctx["overloaded_count"] = int(df['Overloaded'].sum())
                keep = [c for c in ['Employee Name','Task Name','Task Duration (hrs)','Fatigue Score (1–5)'] if c in cols]
                ctx["top_overloaded"] = df[df['Overloaded']][keep].head(8).to_dict(orient="records")

            # Optional: department view if present
            if 'Department' in cols and 'Overloaded' in cols:
                dept = (df.groupby('Department')['Overloaded']
                          .agg(['sum','count'])
                          .reset_index()
                          .rename(columns={'sum':'overloaded','count':'total'}))
                ctx["department_overview"] = dept.to_dict(orient="records")
            return ctx

        # Keep short chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_q = st.text_input("Type a question (e.g., 'Who is most overloaded?' or 'Which department needs help?')")

        def ask_groq(context_dict, question):
            """Send a question + context to Groq and return the answer."""
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            system_prompt = (
                "You are an operations analyst. Answer ONLY from the JSON context. "
                "If info is missing, say you don't have it. Keep answers concise.\n\n"
                f"JSON context:\n{json.dumps(context_dict, ensure_ascii=False)}"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                *st.session_state.chat_history[-4:],  # a little history for continuity
                {"role": "user", "content": question}
            ]
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # fast + free-tier-friendly
                messages=messages,
                temperature=0.2,
                max_tokens=400,
            )
            return resp.choices[0].message.content.strip()

        if user_q:
            context = build_context(df)
            answer = ask_groq(context, user_q)
            st.session_state.chat_history.append({"role": "user", "content": user_q})
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # Render chat
        for turn in st.session_state.chat_history:
            message(turn["content"], is_user=(turn["role"] == "user"))

else:
    st.info("Please upload a file to begin.")

