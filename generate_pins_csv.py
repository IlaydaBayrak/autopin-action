import os
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import csv

# ——— AYARLAR ———
# GitHub raw URL’inizin temel kısmı
REPO_USER    = "ilaydabayrak"
REPO_NAME    = "autopin-action"
# to_post klasörünüzün yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TO_POST_DIR = os.path.join(BASE_DIR, "to_post2")
if not os.path.isdir(TO_POST_DIR):
    raise SystemExit(f"HATA: '{TO_POST_DIR}' klasörü bulunamadı. Lütfen dosya yolunu kontrol edin.")
# Çıktı CSV dosyası
OUTPUT_CSV   = "pins_schedule2.csv"

# Türkiye saati için yayınlanacak saatler
publish_hours = [0, 3, 6, 9, 12, 15, 18, 21]

# Sabit değerler
board_name = "AI ART"
hashtags   = "anime, animeçizimi, animekızları, animeerkekleri, yapayzeka"
# —————————————————

# Başlangıç tarihi olarak bugünü alın (UTC -> +3 saat)
start_date = datetime(2025, 8, 5, 0, 0)

# Klasördeki görselleri oku
files = sorted([
    f for f in os.listdir(TO_POST_DIR)
    if f.lower().endswith((".jpg", ".jpeg", ".png"))
])

rows = []
for idx, fname in enumerate(files):
    day_offset = idx // len(publish_hours)
    hour       = publish_hours[idx % len(publish_hours)]
    pub_dt     = (start_date
                  .replace(hour=hour, minute=0, second=0, microsecond=0)
                  + timedelta(days=day_offset))
    schedule_time = pub_dt.strftime("%Y-%m-%d %H:%M")

    # Raw GitHub URL
    encoded_name = urllib.parse.quote(fname, safe='')
    media_url = (f"https://raw.githubusercontent.com/"
                 f"{REPO_USER}/{REPO_NAME}/main/to_post2/{encoded_name}")

    rows.append({
        "Title": f"anime ai {idx+300}",
        "Media URL": media_url,
        "Pinterest board": board_name,
        "Thumbnail": "",
        "Description": "",
        "Link": "",
        "Publish date": schedule_time,
        "Keywords": hashtags
    })

# DataFrame’e çevir ve CSV’ye yaz
df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False, quoting=csv.QUOTE_ALL)

print(f"✅ {len(rows)} pinlik CSV oluşturuldu: {OUTPUT_CSV}")
