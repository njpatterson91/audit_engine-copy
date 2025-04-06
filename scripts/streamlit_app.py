import streamlit as st
st.set_page_config(page_title="Youth Audit Dashboard", layout="wide")

import json
import subprocess
import os
import re
import calendar
import warnings
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import altair as alt
from PIL import Image

warnings.filterwarnings("ignore", message="The figure layout has changed to tight")

# -----------------------------
# Define Paths
# -----------------------------
AUDIT_RESULTS = Path("data/audit_results")
CALENDAR_DIR = AUDIT_RESULTS / "calendars"  # Folder where calendar PNGs are stored

# -----------------------------
# Sidebar: Navigation & Actions
# -----------------------------
st.sidebar.header("Navigation")
page = st.sidebar.radio("Select View", ["Detailed View", "Summary Dashboard"])

st.sidebar.header("Actions")
def run_command(cmd):
    project_root = str(Path(__file__).resolve().parent.parent)
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')
    result = subprocess.run(
        ["python"] + cmd,
        cwd=project_root,
        env=env,
        capture_output=True,
        text=True
    )
    return result

if st.sidebar.button("Generate New Data"):
    result = run_command(["scripts/generate_fake_data.py"])
    st.sidebar.write(result.stdout)
    st.write("Please refresh your browser to see changes.")

if st.sidebar.button("Run Audit"):
    result = run_command(["scripts/run_audit.py"])
    st.sidebar.write("Audit Script Output:")
    st.sidebar.write(result.stdout)
    if result.stderr:
        st.sidebar.error("Audit Script Errors:")
        st.sidebar.error(result.stderr)
    st.write("Please refresh your browser to see changes.")

# -----------------------------
# Detailed View Page
# -----------------------------
if page == "Detailed View":
    st.header("Detailed Youth Audit View")
    audit_files = sorted(AUDIT_RESULTS.glob("*.json"))
    youth_data = []
    for f in audit_files:
        if f.name.lower() == "summary.csv":
            continue
        try:
            with open(f, "r") as json_file:
                content = json.load(json_file)
            youth_data.append((content, f))
        except Exception as e:
            st.error(f"Error reading {f.name}: {e}")

    if not youth_data:
        st.warning("No audit files found. Please run the audit first.")
        st.stop()

    youth_names = [entry[0].get("youth", "Unknown") for entry in youth_data]
    selected_youth = st.sidebar.selectbox("Select a Youth", youth_names)
    selected_data = next((data for data in youth_data if data[0].get("youth", "") == selected_youth), None)
    if selected_data is None:
        st.error("Selected youth data not found.")
        st.stop()

    data, audit_path = selected_data
    youth_name = data.get("youth", "Unknown")
    start_date = data.get("start_date", "2024-01-01")
    files = data.get("files", [])

    st.subheader(f"Audit Details for {youth_name}")
    calendar_path = CALENDAR_DIR / f"{youth_name}_GT_Calendar.png"
    if calendar_path.exists():
        st.image(str(calendar_path), caption="Group Therapy Calendar", use_container_width=True)
    else:
        st.warning("Calendar image not found. Please run the audit to generate it.")

    st.subheader("Missing Group Therapy Weeks")
    missing_weeks = data.get("missing_gt_weeks", [])
    if missing_weeks:
        for item in missing_weeks:
            week_label = item.get("week", "")
            count = item.get("count", "")
            required = item.get("required", "")
            st.markdown(f"- `{week_label}`: {count} of {required} sessions")
    else:
        st.success("All GT requirements met!")

    st.subheader("Misnamed Files")
    misnamed = data.get("misnamed", [])
    if misnamed:
        st.code("\n".join(misnamed))
    else:
        st.success("No misnamed files found.")

    st.subheader("Debug Info")
    st.code(f"Audit file: {audit_path}")

# -----------------------------
# Summary Dashboard Page
# -----------------------------
elif page == "Summary Dashboard":
    st.header("Youth Audit Summary Dashboard")
    
    # Function to generate summary DataFrame from JSON files
    def generate_summary_from_json(audit_dir: Path):
        summary_data = []
        audit_files = sorted(audit_dir.glob("*.json"))
        for f in audit_files:
            if f.name.lower() == "summary.csv":
                continue
            try:
                with open(f, "r") as json_file:
                    content = json.load(json_file)
                youth = content.get("youth", "")
                security = content.get("security_level", "")
                start_date_str = content.get("start_date", "")
                files = content.get("files", [])
                total_sessions = len(files)
                missing_gt = sum(item.get("count", 0) for item in content.get("missing_gt_weeks", [])) if content.get("missing_gt_weeks") else 0
                misnamed = len(content.get("misnamed", []))
                summary_data.append({
                    "Youth": youth,
                    "Security Level": security,
                    "Start Date": start_date_str,
                    # "Total Sessions": total_sessions,   # Removed as requested
                    "Missing GT Sessions": missing_gt,
                    "Misnamed Files": misnamed,
                })
            except Exception as e:
                st.error(f"Error reading {f.name}: {e}")
        return pd.DataFrame(summary_data)

    df_summary = generate_summary_from_json(AUDIT_RESULTS)
    if df_summary.empty:
        st.warning("No audit summary data available. Please run the audit first.")
        st.stop()

    # Sidebar filters for summary (if desired)
    st.sidebar.header("Summary Filters")
    levels = sorted(df_summary["Security Level"].unique().tolist())
    selected_level = st.sidebar.selectbox("Security Level", ["All"] + levels)
    if selected_level != "All":
        df_summary = df_summary[df_summary["Security Level"] == selected_level]
    try:
        start_dates = pd.to_datetime(df_summary["Start Date"], errors="coerce")
        min_date = start_dates.min()
        max_date = start_dates.max()
        selected_date_range = st.sidebar.date_input("Start Date Range", value=(min_date, max_date))
        if selected_date_range:
            df_summary = df_summary[(start_dates >= pd.to_datetime(selected_date_range[0])) &
                                    (start_dates <= pd.to_datetime(selected_date_range[1]))]
    except Exception as e:
        st.sidebar.error("Error with date filter: " + str(e))

    # Display the summary table only (without key metrics, charts, etc.)
    st.subheader("Detailed Youth Audit Data")
    st.dataframe(df_summary)

    # Optional: Download button for the summary table
    csv_data = df_summary.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Summary Data as CSV",
        data=csv_data,
        file_name='youth_audit_summary_generated.csv',
        mime='text/csv'
    )