import re
from datetime import datetime, timedelta
from collections import defaultdict

def is_valid_gt_filename(filename):
    # Match files that contain 'GT' and a valid date ending in .docx
    return bool(re.search(r'GT.*\d{4}-\d{2}-\d{2}\.docx$', filename, re.IGNORECASE))

def extract_date_from_gt_file(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            return None
    return None

def group_files_by_week(filenames, start_date):
    # Align start_date to the start of the week (Monday)
    aligned_start = start_date - timedelta(days=start_date.weekday())
    weeks = defaultdict(list)

    for f in filenames:
        dt = extract_date_from_gt_file(f)
        if not dt:
            continue
        if dt < aligned_start:
            continue
        delta_days = (dt - aligned_start).days
        week_num = delta_days // 7 + 1
        week_key = f"week_{week_num}"
        weeks[week_key].append(f)

    return weeks

def find_misnamed_files(filenames):
    return [f for f in filenames if not is_valid_gt_filename(f)]
