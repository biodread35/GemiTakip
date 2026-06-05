import pandas as pd
from collections import Counter
import os

CSV_FILE = "data/departures.csv"
REPORT_FILE = "data/weekly_report.txt"

os.makedirs("data", exist_ok=True)

# CSV oku
df = pd.read_csv(CSV_FILE)

# datetime
df['arrival'] = pd.to_datetime(df['arrival'], dayfirst=True, errors='coerce')
df['departure'] = pd.to_datetime(df['departure'], dayfirst=True, errors='coerce')

# stay hesapla
df['stay'] = df['departure'] - df['arrival']

# hafta
df['week'] = df['departure'].dt.isocalendar().week

# rapor satırları
report_lines = ["Week - Agent - ShipCount - TotalTime"]

for week in sorted(df['week'].unique()):
    week_df = df[df['week'] == week]
    for agent in week_df['agent'].unique():
        agent_df = week_df[week_df['agent'] == agent]
        ship_count = len(agent_df)
        total_stay = agent_df['stay'].sum()  # timedelta toplamı

        # timedelta'yi saat:dakika formatına çevir
        total_seconds = int(total_stay.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        total_time_str = f"{hours}:{minutes:02d}"

        report_lines.append(f"{week} - {agent} - {ship_count} - {total_time_str}")

# txt yaz
with open(REPORT_FILE, "w", encoding="utf-8") as f:
    for line in report_lines:
        f.write(line + "\n")

print(f"Weekly report created: {REPORT_FILE}")
