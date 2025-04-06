import json
import random
import shutil
from datetime import datetime, timedelta
from pathlib import Path
import csv

# Configurable parameters
YOUTH_COUNT = 100
RAW_LOG_DIR = Path("data/raw_logs")
AUDIT_RESULT_DIR = Path("data/audit_results")
GEN_LOG_CSV = Path("data/audit_results/file_generation_log.csv")

SECURITY_LEVELS = ["Staff Secure", "Hardware Secure"]
GT_SESSIONS_PER_WEEK = {"Staff Secure": 2, "Hardware Secure": 3}
FT_FREQUENCY = 2
IT_FREQUENCY = 1

MISNAME_CHANCE = 1 / 25  # 4% chance
MISSING_CHANCE = 1 / 50  # 2% chance
MISSING_OTHER_PERCENT = 0.15
JUNK_FILE_RATE = 0.05

START_DATE_RANGE = (datetime(2024, 1, 1), datetime(2024, 3, 1))

FIRST_NAMES = ["Jordan", "Taylor", "Morgan", "Skyler", "Casey", "Avery", "Elliott", "Reese", "Dakota", "Emerson"]
LAST_NAMES = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Davis", "Wilson", "Anderson", "Thomas", "Jackson"]

MONTHS = [datetime(2024, m, 1).strftime('%B') for m in range(2, 13)]

def clear_old_data():
    for path in [RAW_LOG_DIR, AUDIT_RESULT_DIR]:
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def generate_name(index):
    return f"{FIRST_NAMES[index % len(FIRST_NAMES)]}{LAST_NAMES[index % len(LAST_NAMES)]}"

def maybe_misname(filename):
    mistake_type = random.choice(["missing_spaces", "wrong_ext", "swap_order"])
    if mistake_type == "missing_spaces":
        return filename.replace(" ", "")
    elif mistake_type == "wrong_ext":
        return filename.replace(".docx", ".pdf") if filename.endswith(".docx") else filename
    elif mistake_type == "swap_order":
        parts = filename.split(" ")
        if len(parts) >= 3:
            parts[0], parts[1] = parts[1], parts[0]
            return " ".join(parts)
    return filename

def generate_weekly_files(youth, start_date, label, per_week, ext=".docx", every_other=False, log_writer=None):
    current = start_date
    week_counter = 0
    filenames = []

    while current <= datetime(2024, 12, 31):
        if every_other and week_counter % 2 != 0:
            current += timedelta(days=7)
            week_counter += 1
            continue

        days = [current + timedelta(days=i) for i in range(7)]
        session_days = random.sample(days, min(len(days), per_week))

        for day in session_days:
            original_name = f"{youth} {label} {day.strftime('%Y-%m-%d')}{ext}"
            status = "valid"

            if label == "GT" and random.random() < MISSING_CHANCE:
                status = "skipped"
                if log_writer:
                    log_writer.writerow([youth, label, day.strftime('%Y-%m-%d'), "", status])
                continue

            if label == "GT" and random.random() < MISNAME_CHANCE:
                misnamed = maybe_misname(original_name)
                filenames.append(misnamed)
                status = "misnamed"
                if log_writer:
                    log_writer.writerow([youth, label, day.strftime('%Y-%m-%d'), misnamed, status])
            else:
                filenames.append(original_name)
                if log_writer:
                    log_writer.writerow([youth, label, day.strftime('%Y-%m-%d'), original_name, status])

        current += timedelta(days=7)
        week_counter += 1

    return filenames

def generate_ipp_filenames(youth):
    filenames = []
    initial = f"{youth} Ipp Initial.pdf"
    if random.random() > MISSING_OTHER_PERCENT:
        filenames.append(initial)

    for month in MONTHS:
        update = f"{youth} IPP {month}.pdf"
        if random.random() > MISSING_OTHER_PERCENT:
            filenames.append(update)

    return filenames

def generate_junk_files(youth):
    junk_names = [
        f"{youth}_junk1.docx",
        f"{youth}-old.doc",
        f"{youth}_backup.txt",
        f"{youth}_archive_copy.pdf"
    ]
    return random.sample(junk_names, k=int(len(junk_names) * JUNK_FILE_RATE))

def main():
    clear_old_data()
    with open(GEN_LOG_CSV, "w", newline="") as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(["Youth", "Label", "Date", "Filename", "Status"])

        for i in range(YOUTH_COUNT):
            youth = generate_name(i)
            level = random.choice(SECURITY_LEVELS)
            start_date = random_date(*START_DATE_RANGE)

            gt_files = generate_weekly_files(youth, start_date, "GT", GT_SESSIONS_PER_WEEK[level], log_writer=log_writer)
            it_files = generate_weekly_files(youth, start_date, "IT", IT_FREQUENCY)
            ft_files = generate_weekly_files(youth, start_date, "FT", FT_FREQUENCY, every_other=True)
            ipp_files = generate_ipp_filenames(youth)
            junk_files = generate_junk_files(youth)

            final_files = gt_files + it_files + ft_files + ipp_files + junk_files

            json_data = {
                "youth": youth,
                "security_level": level,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "files": sorted(final_files)
            }

            with open(RAW_LOG_DIR / f"{youth}.json", "w") as f:
                json.dump(json_data, f, indent=2)

    print(f"✅ Generated {YOUTH_COUNT} youth logs and file generation log at {GEN_LOG_CSV}")

if __name__ == "__main__":
    main()