import streamlit as st
st.set_page_config(page_title="Youth Audit Viewer", layout="wide")  # MUST BE FIRST STREAMLIT COMMAND

import json
from pathlib import Path
from PIL import Image

# 📁 Paths
AUDIT_RESULTS = Path("data/audit_results")
CALENDAR_DIR = AUDIT_RESULTS / "calendars"

# 🔍 Load audit data
audit_files = sorted(AUDIT_RESULTS.glob("*.json"))
youth_data = []

for f in audit_files:
    if f.name == "summary.csv":
        continue
    try:
        with open(f) as json_file:
            content = json.load(json_file)
            youth_data.append((content, f))
    except Exception as e:
        st.error(f"Error reading {f.name}: {e}")

# 🧼 Handle empty data
if not youth_data:
    st.warning("No audit files found. Please run the audit first.")
    st.stop()

# 🗂 Create tabs
tabs = st.tabs([entry[0]["youth"] for entry in youth_data])

# 🖼 Per-youth content
for i, tab in enumerate(tabs):
    with tab:
        data, audit_path = youth_data[i]
        youth_name = data["youth"]
        calendar_path = CALENDAR_DIR / f"{youth_name}_GT_Calendar.png"

        st.header(f"🧒 {youth_name}")

        # 📅 Calendar image
        if calendar_path.exists():
            st.image(Image.open(calendar_path), caption="Group Therapy Calendar", use_container_width=True)
        else:
            st.warning("⚠️ No calendar image found for this youth.")

        # ❌ Missing GT weeks
        st.subheader("❌ Missing Group Therapy Weeks")
        missing_weeks = data.get("missing_gt_weeks", [])
        if missing_weeks:
            for item in missing_weeks:
                week_label = item["week"]
                count = item["count"]
                required = item["required"]
                st.markdown(f"- `{week_label}`: {count} of {required} sessions")
        else:
            st.success("All GT requirements met!")

        # 🛑 Misnamed files
        st.subheader("⚠️ Misnamed Files")
        misnamed = data.get("misnamed", [])
        if misnamed:
            st.code("\n".join(misnamed))
        else:
            st.success("No misnamed files found.")

        # 🛠 Debug
        st.subheader("🛠 Debug Info")
        st.code(f"Calendar path: {calendar_path}")
        st.write("File exists:", calendar_path.exists())