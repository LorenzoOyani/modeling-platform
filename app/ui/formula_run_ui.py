import streamlit as st
import pandas as pd
from app.db import get_db_session, init_db
from app.db import Formula, RunSession
from app.utility import start_run

st.set_page_config(page_title="⚙️ Formula Tracker", layout="wide")

# Initialize DB and session
init_db()
db = get_db_session()

st.title(" Formula Storage & Run Tracker")

# Create Streamlit Tabs
tab1, tab2 = st.tabs([" Add Formula", " View & Run Formulas"])

# TAB 1: Add Formula
with tab1:
    st.subheader("Add a new formula")

    name = st.text_input("Formula Name")
    expression = st.text_area("Expression (e.g. PV = CF / (1 + r) ** t)")
    tags = st.text_input("Tags or Notes")

    if st.button("Save Formula"):
        if not name or not expression:
            st.error(" Name and Expression are required!")
        else:
            new_formula = Formula(name=name, expression=expression, tags=tags)
            db.add(new_formula)
            db.commit()
            st.success(f" Formula '{name}' saved successfully!")

# TAB 2: View & Run Formulas

with tab2:
    st.subheader("Saved Formulas")

    formulas = db.query(Formula).all()

    if not formulas:
        st.info("No formulas found yet. Add one above.")
    else:
        # Display in DataFrame
        df = pd.DataFrame([{
            "ID": f.id,
            "Name": f.name,
            "Expression": f.expression,
            "Tags": f.tags,
            "Created At": f.created_at.strftime("%Y-%m-%d %H:%M")
        } for f in formulas])

        st.dataframe(df, use_container_width=True)

        selected = st.selectbox("Select Formula to Run", [f"{f.id} - {f.name}" for f in formulas])
        formula_id = int(selected.split(" - ")[0])

        input_file = st.text_input("Optional Input File Path (if any)")
        if st.button("Start Run"):
            run = start_run(db, formula_id, input_file)
            st.success(f" Run Started! Run ID: {run.run_id}")

    # Show run history
    st.divider()
    st.subheader(" Recent Runs")
    runs = db.query(RunSession).order_by(RunSession.start_time.desc()).limit(10).all()
    if runs:
        run_df = pd.DataFrame([{
            "Run ID": r.run_id,
            "Formula": r.formula.name,
            "Status": r.status,
            "Started": r.start_time.strftime("%Y-%m-%d %H:%M")
        } for r in runs])
        st.dataframe(run_df, use_container_width=True)
    else:
        st.info("No runs yet.")
