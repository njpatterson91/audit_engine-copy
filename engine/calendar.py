import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import calendar
import re
from datetime import datetime, timedelta
from pathlib import Path

import warnings
warnings.filterwarnings("ignore", message="The figure layout has changed to tight")

def generate_gt_calendar(youth_name, start_date, files, output_dir):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Extract session dates
    gt_dates, it_dates, ft_dates = [], [], []
    for file in files:
        match = re.search(r"\d{4}-\d{2}-\d{2}", file)
        if not match:
            continue
        date_str = match.group()
        if "GT" in file and file.endswith(".docx"):
            gt_dates.append(date_str)
        elif "IT" in file and file.endswith(".docx"):
            it_dates.append(date_str)
        elif "FT" in file and file.endswith(".docx"):
            ft_dates.append(date_str)

    gt_dates_dt = [datetime.strptime(d, "%Y-%m-%d") for d in sorted(set(gt_dates))]
    it_dates_dt = [datetime.strptime(d, "%Y-%m-%d") for d in sorted(set(it_dates))]
    ft_dates_dt = [datetime.strptime(d, "%Y-%m-%d") for d in sorted(set(ft_dates))]

    all_dates = pd.date_range(start="2024-01-01", end="2024-12-31")
    df = pd.DataFrame(index=all_dates)
    df["GT"] = df.index.isin(gt_dates_dt)
    df["IT"] = df.index.isin(it_dates_dt)
    df["FT"] = df.index.isin(ft_dates_dt)

    # Align weeks to Sunday–Saturday
    aligned_start = start_date - timedelta(days=start_date.weekday() + 1 if start_date.weekday() < 6 else 0)
    df["week"] = ((df.index - aligned_start).days // 7) + 1
    weekly_counts = df[df["GT"]].groupby("week").size().to_dict()

    # Create figure
    fig, axs = plt.subplots(3, 4, figsize=(16, 10), constrained_layout=True)
    fig.suptitle(f"Therapy Calendar for {youth_name} - 2024", fontsize=16)

    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

    for month in range(1, 13):
        ax = axs[(month - 1) // 4][(month - 1) % 4]
        month_dates = df[df.index.month == month]
        ax.set_title(calendar.month_name[month], fontsize=10)
        ax.set_xlim(0, 7)
        ax.set_ylim(0, 6.5)

        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())

        # Draw weekday headers
        for i, label in enumerate(day_labels):
            ax.text(i + 0.5, 6.3, label, ha="center", va="center", fontsize=6, weight="bold")

        # Redraw month boundary manually
        ax.add_patch(plt.Rectangle((0, 0), 7, 6.5, fill=False, edgecolor='black', linewidth=1))

        week_boxes = {}

        for date in month_dates.index:
            if date.month != month:
                continue

            weekday = (date.weekday() + 1) % 7  # Sunday = 0
            month_start = date.replace(day=1)
            first_day_weekday = (month_start.weekday() + 1) % 7
            week_of_month = (date.day + first_day_weekday - 1) // 7
            x = weekday
            y = 5 - week_of_month

            has_gt = df.loc[date, "GT"]
            has_it = df.loc[date, "IT"]
            has_ft = df.loc[date, "FT"]
            types = [c for c, v in zip(["GT", "IT", "FT"], [has_gt, has_it, has_ft]) if v]

            if len(types) == 0:
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color="lightgrey"))
            elif len(types) == 1:
                color = {"GT": "green", "IT": "orange", "FT": "blue"}[types[0]]
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color=color))
            elif len(types) == 2:
                color1 = {"GT": "green", "IT": "orange", "FT": "blue"}[types[0]]
                color2 = {"GT": "green", "IT": "orange", "FT": "blue"}[types[1]]
                ax.add_patch(plt.Rectangle((x, y + 0.5), 1, 0.5, color=color1))
                ax.add_patch(plt.Rectangle((x, y), 1, 0.5, color=color2))
            else:
                ax.add_patch(plt.Rectangle((x, y + 0.5), 0.5, 0.5, color="green"))
                ax.add_patch(plt.Rectangle((x + 0.5, y + 0.5), 0.5, 0.5, color="orange"))
                ax.add_patch(plt.Rectangle((x, y), 1, 0.5, color="blue"))

            ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=False, edgecolor="black", linewidth=0.5))
            ax.text(x + 0.5, y + 0.5, str(date.day), ha="center", va="center", fontsize=6)

            week_num = ((date - aligned_start).days // 7) + 1
            key = (y, x)
            week_boxes.setdefault(week_num, []).append(key)

        # Highlight weeks with insufficient GT
        for week, positions in week_boxes.items():
            count = weekly_counts.get(week, 0)
            required = 3 if "Hardware" in files[0] else 2
            if count < required:
                x0 = min(p[1] for p in positions)
                y0 = min(p[0] for p in positions)
                x1 = max(p[1] for p in positions)
                y1 = max(p[0] for p in positions)
                ax.add_patch(plt.Rectangle((x0, y0), x1 - x0 + 1, y1 - y0 + 1, fill=False, edgecolor="red", linewidth=2))

    # Legend
    green_patch = mpatches.Patch(color='green', label='GT')
    orange_patch = mpatches.Patch(color='orange', label='IT')
    blue_patch = mpatches.Patch(color='blue', label='FT')
    grey_patch = mpatches.Patch(color='lightgrey', label='No Session')
    red_border = mpatches.Patch(edgecolor='red', facecolor='none', label='Insufficient GT', linewidth=2)

    fig.legend(handles=[green_patch, orange_patch, blue_patch, grey_patch, red_border], loc='lower center', ncol=5, bbox_to_anchor=(0.5, 0.01))

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])

    # Save only PNG
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path / f"{youth_name}_GT_Calendar.png", dpi=300)
    plt.close(fig)