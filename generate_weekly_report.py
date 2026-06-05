import pandas as pd
from collections import Counter
import os

CSV_FILE = "data/departures.csv"
REPORT_FILE = "data/weekly_report.txt"

os.makedirs("data", exist_ok=True)

df = pd.read_csv(CSV_FILE)
df['departure'] = pd.to_datetime(df['departure'], errors='coerce')
df['week'] = df['departure'].dt.isocalendar().week

report_lines = ["Week - Agent - ShipCount"]

for week in sorted(df['week'].unique()):
    week_df = df[df['week'] == week]
    counts = Counter(week_df['agent'])
    for agent, count in counts.items():
        report_lines.append(f"{week} - {agent} - {count}")

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    for line in report_lines:
        f.write(line + "\n")

print(f"Weekly report created: {REPORT_FILE}")
