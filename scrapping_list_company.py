import requests
from bs4 import BeautifulSoup
import time
import csv

start_time = time.time()

base_url = "https://modi.esdm.go.id/portal/dataPerusahaan?page="
output = []

# Ubah ini sesuai jumlah total halaman (380)
total_pages = 380

for page in range(1, total_pages + 1):
    url = f"{base_url}{page}"
    print(f"🔄 Ambil halaman {page}: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Gagal ambil halaman {page}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("tbody tr")

    for row in rows:
        try:
            company_cell = row.select_one("td:nth-child(2) a")
            if company_cell:
                name = company_cell.text.strip()
                href = company_cell['href']
                full_url = "https://modi.esdm.go.id" + href
                output.append([name, full_url])
        except Exception as e:
            print(f"❌ Error parsing row: {e}")

    time.sleep(0.5)  # Delay supaya tidak overload server

# Simpan ke CSV
with open("daftar_perusahaan_modi.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Nama Perusahaan", "URL"])
    writer.writerows(output)

print(f"✅ Selesai. Total: {len(output)} perusahaan disimpan ke CSV.")

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Waktu eksekusi: {elapsed_time:.2f} detik")
