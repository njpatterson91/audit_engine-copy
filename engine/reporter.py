import csv
from pathlib import Path
from datetime import datetime, timedelta
import json

def save_results_to_json(results, output_dir):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for result in results:
        name = result["youth"]
        out_file = Path(output_dir) / f"{name}_audit.json"
        with open(out_file, "w") as f:
            json.dump(result, f, indent=2)
    print(f"✅ Saved {len(results)} JSON results to {output_dir}/")

def save_summary_to_csv(results, output_file):
    headers = [
        "youth", "security_level", "start_date",
        "misnamed_count", "weeks_missing_gt"
    ]

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for r in results:
            writer.writerow({
                "youth": r["youth"],
                "security_level": r["security_level"],
                "start_date": r["start_date"],
                "misnamed_count": len(r["misnamed"]),
                "weeks_missing_gt": len(r["missing_gt_weeks"])
            })

    print(f"📄 CSV summary saved to {output_file}")

def save_individual_csv_reports(results, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for result in results:
        youth = result["youth"]
        file_path = output_dir / f"{youth}_report.csv"

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Issue Type", "Details"])

            # Missing GT sessions
            for week_info in result.get("missing_gt_weeks", []):
                week_num = int(week_info["week"].replace("week_", ""))
                start_date = datetime.strptime(result["start_date"], "%Y-%m-%d")
                week_start = start_date + timedelta(days=(week_num - 1) * 7)
                week_label = week_start.strftime("Week of %Y-%m-%d")
                writer.writerow(["Missing GT", f"{week_label}: {week_info['count']} of {week_info['required']} sessions"])

            # Misnamed files
            for bad_file in result.get("misnamed", []):
                writer.writerow(["Misnamed File", bad_file])
