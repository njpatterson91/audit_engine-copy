from engine.validator import group_files_by_week, find_misnamed_files, is_valid_gt_filename, extract_date_from_gt_file
from datetime import datetime, timedelta
from math import ceil

def audit_youth(youth_data, audit_rules):
    name = youth_data["youth"]
    level = youth_data["security_level"]
    start_date_str = youth_data["start_date"]
    files = youth_data["files"]

    required_per_week = audit_rules["group_therapy"].get(level, 2)
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime(2024, 12, 31)

    valid_gt_files = [f for f in files if is_valid_gt_filename(f)]
    misnamed_files = find_misnamed_files(files)

    # Group valid GT files by week
    weekly_grouped = group_files_by_week(valid_gt_files, start_date)

    # Explicitly check every week from start_date to end_date
    total_weeks = ceil((end_date - start_date).days / 7)
    missing_weeks = []

    for week_index in range(1, total_weeks + 1):
        week_key = f"week_{week_index}"
        count = len(weekly_grouped.get(week_key, []))
        if count < required_per_week:
            missing_weeks.append({
                "week": week_key,
                "count": count,
                "required": required_per_week
            })

    return {
        "youth": name,
        "security_level": level,
        "start_date": start_date_str,
        "valid_gt_files": valid_gt_files,
        "misnamed": misnamed_files,
        "missing_gt_weeks": sorted(missing_weeks, key=lambda w: w["week"])
    }