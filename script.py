import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "http://www.tceege.com.tr/gemi-izleme.aspx"
CSV_FILE = "data/departures.csv"

print("Sayfa çekiliyor...")

r = requests.get(URL, timeout=30)
soup = BeautifulSoup(r.text, "html.parser")

# ⚠️ Burayı daha sonra netleştireceğiz (tablo selector önemli)
tables = soup.find_all("table")

print(f"{len(tables)} tablo bulundu")

# şimdilik sadece sayfayı kaydedip bakacağız
with open("debug.html", "w", encoding="utf-8") as f:
    f.write(r.text)

print("HTML kaydedildi")
