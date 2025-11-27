import os
from utils import clear, pause, table
from crud_kamar import csv_file, csv, check

def show_ready():
    if not os.path.exists(csv_file):
        print("Belum ada kamar.")
        pause()
        return
    
    headers = ["No Kamar", "Status", "Harga"]
    rows = []

    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] == "READY":
                rows.append([
                    row["no_kamar"],
                    row["status"],
                    row["harga"],
                ])

    if not rows:
        print("Tidak ada kamar ready.")
    else:
        table(headers, rows)

def pesan_kamar(username):
    while True:
        clear()
        print("PEMESANAN KAMAR")
        print("-" * 80)

        show_ready()

        target = input("Masukan nomor kamar yang ingin di pesan: ").strip()
        if target == "":
            print("nomor kamar tidak boleh kosong!".upper())
            pause()
            return
        
        if not check(target):
            print("nomor kamar tidak di temukan!".upper())
            pause()
            return
        
        rows = []
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        found = False
        for row in rows:
            if row["no_kamar"] == target:
                found = True
                print(f"No kamar : {row['no_kamar']}")
                print(f"Status   : {row['status']}")
                print(f"Harga    : {row['harga']}")

                # jaga jaga
                if row["status"] != "READY":
                    print("Kamar ini tidak tersedia.")
                    pause()
                    return

                print(f"\nKamar akan di pesan atas nama: {username}")
                konfirm = input("Lanjutkan? (y/n): ").strip().lower()
                if konfirm != "y":
                    print("Pemesanan dibatalkan.")
                    pause()
                    return
                
                row["status"] = "PENDING"
                row["nama_pemesan"] = username
                break

        if not found:
            print("Kamar tidak di temukan")
            pause()
            return
        
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["no_kamar", "status", "harga", "nama_pemesan"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print("Pemesanan berhasil.")
        pause()
        return
    
def show_pesanan(username):
    clear()
    print("PESANAN KAMAR")
    print("-" * 80)

    if not os.path.exists(csv_file):
        print("Belum ada kamar.")
        pause()
        return
    
    headers = ["No Kamar", "Status", "Harga"]
    rows = []

    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("nama_pemesan", "") == username:
                rows.append([
                    row["no_kamar"],
                    row["status"],
                    row["harga"]
                ])

    if not rows:
        print("belum pesanan kamar.")
    else:
        table(headers, rows)
    
    pause()
