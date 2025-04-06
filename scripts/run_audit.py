from engine.loader import load_rules, load_youth_logs
from engine.auditor import audit_youth
from engine.reporter import save_results_to_json, save_summary_to_csv, save_individual_csv_reports
from engine.calendar import generate_gt_calendar

OUTPUT_DIR = "data/audit_results"
SUMMARY_FILE = f"{OUTPUT_DIR}/summary.csv"

def main():
    print("🔁 Loading rules and logs...")
    rules = load_rules()
    youth_logs = load_youth_logs()

    print(f"📦 Auditing {len(youth_logs)} youth...")
    results = [audit_youth(youth, rules) for youth in youth_logs]

    print("💾 Saving results...")
    save_results_to_json(results, OUTPUT_DIR)
    save_summary_to_csv(results, SUMMARY_FILE)
    save_individual_csv_reports(results, OUTPUT_DIR)
    calendar_dir = "data/audit_results/calendars"
    for result in results:
        generate_gt_calendar(
            youth_name=result["youth"],
            start_date=result["start_date"],
            files=result["valid_gt_files"] + result["misnamed"],
            output_dir=calendar_dir
        )
    print("✅ Audit complete.")

if __name__ == "__main__":
    main()