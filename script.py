import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "http://www.tceege.com.tr/gemi-izleme.aspx"
CSV_FILE = "data/departures.csv"

print("Sayfa çekiliyor...")

r = requests.get(URL, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

print(f"{len(tables)} tablo bulundu")

# ✅ SADECE AYRILAN GEMİLER (tablo 2)
target_table = tables[2]

rows = target_table.find_all("tr")

ships = []

for row in rows:
    cols = [c.get_text(strip=True) for c in row.find_all("td")]

    # 4 kolon: gemi, geliş, ayrılış, acente
    if len(cols) == 4:
        ships.append(cols)

print(f"{len(ships)} gemi bulundu")

# klasör yoksa oluştur
os.makedirs("data", exist_ok=True)

existing = set()

if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) >= 3:
                existing.add(row[0] + row[2])

new_rows = 0

with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    if os.stat(CSV_FILE).st_size == 0:
        writer.writerow(["ship", "arrival", "departure", "agent"])

    for s in ships:
        key = s[0] + s[2]

        if key not in existing:
            writer.writerow(s)
            new_rows += 1

print(f"Yeni eklenen kayıt: {new_rows}")
