import streamlit as st
import csv
from io import StringIO
from csv_profiler.profile import basic_profile  as profile_rows
from csv_profiler.render import write_json, write_markdown

def main() -> None:
    st.set_page_config(page_title="CSV Profiler",layout="wide") ##Sets global app configuration
    st.title("CSV Profiler")
    st.caption("Upload CSV → profile → export JSON + Markdown")

    st.sidebar.header("Upload CSV File")

    rows=None
    report=st.session_state.get("report") ##If "report" exists → load it f not → report = None

    uploaded=st.file_uploader("Choose a CSV file",type=["csv"])
    show_preview=st.sidebar.checkbox("Show Preview",value=True)

    if uploaded is None:
        st.info("Please upload a CSV file to profile.")
        return

    if uploaded is not None:
        text=uploaded.getvalue().decode("utf-8")
        rows=list(csv.DictReader(StringIO(text)))

        if not rows:
            st.error("The uploaded CSV file has no rows.")
            st.stop()

        if rows and len(rows[0].keys())==0:
            st.warning("No columns detected in the CSV file.")

        if show_preview:
            st.subheader("CSV Preview")
            st.dataframe(rows[:5])  ##Show first 5 rows

    else:
        st.info("Please upload a CSV file to profile.")


    if rows is not None and len(rows)>0:
        if st.button("Generate Profile Report"):
            with st.spinner("Profiling CSV data..."):
                report=profile_rows(rows)
                st.session_state["report"]=report ##Store report in session state

    report=st.session_state.get("report")
    if report is not None:
        summary = report.get("summary", {})

        c1, c2 = st.columns(2)
        c1.metric("Rows", summary.get("rows", 0))
        c2.metric("Columns", summary.get("columns", 0))

    if st.button("export json + markdown"):
        write_json(report, "outputs/report.json")
        write_markdown(report, "outputs/report.md") 
        st.success("Exported report to outputs/report.json and outputs/report.md")


if __name__ == "__main__":
    main()
    
    


