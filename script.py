import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "http://www.tceege.com.tr/gemi-izleme.aspx"
CSV_FILE = "data/departures.csv"

print("Sayfa çekiliyor...")

# sayfayı çek
r = requests.get(URL, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

# tabloları bul
tables = soup.find_all("table")
print(f"{len(tables)} tablo bulundu")
for i, table in enumerate(tables):
    print(f"--- TABLO {i} ---")
    print(table.get_text(" ", strip=True)[:200])

# ✅ Dinamik olarak "Ayrılan Gemiler" tablosunu bul
target_table = None
for table in tables:
    th = table.find("th")
    if th and "Ayrılan Gemiler" in th.text:
        target_table = table
        break

if target_table is None:
    print("⚠ Ayrılan Gemiler tablosu bulunamadı. Bu hafta veri yok olabilir.")
    exit(0)  # workflow fail olmasın, success olarak bırak

# satırları al
rows = target_table.find_all("tr")

ships = []

for row in rows[1:]:  # başlık satırını atla
    cols = [c.get_text(strip=True) for c in row.find_all("td")]

    # 4 kolon: gemi, acente, geliş, ayrılış
    if len(cols) == 4:
        ships.append(cols)

print(f"{len(ships)} gemi bulundu")

# klasör yoksa oluştur
os.makedirs("data", exist_ok=True)

# mevcut kayıtları set olarak al
existing = set()
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # header atla
        for row in reader:
            if len(row) >= 3:
                existing.add("|".join([x.strip() for x in row]))

# yeni kayıtları ekle
new_rows = 0
with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    if os.stat(CSV_FILE).st_size == 0:
        writer.writerow(["ship", "agent", "arrival", "departure"])
    
    for s in ships:
        key = "|".join([x.strip() for x in s])
        if key not in existing:
            writer.writerow(s)
            new_rows += 1

print(f"Yeni eklenen kayıt: {new_rows}")
