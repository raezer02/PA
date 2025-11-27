import os
from utils import clear, pause, table
from crud_makanan import csv_file, csv

csv_pesan = "db_pesanan_makanan.csv"

def init():
    if not os.path.exists(csv_pesan):
        with open(csv_pesan, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "id",
                "username",
                "no_makanan",
                "nama_makanan",
                "jumlah",
                "subtotal"
            ])
            
def get_id():
    if not os.path.exists(csv_pesan):
        return 1
    
    last_id = 0
    with open(csv_pesan, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                last_id = int(row["id"])
            except (KeyError, ValueError):
                continue
            
    return last_id + 1 if last_id != 0 else 1

def pesan_makan(username):
    init()
    while True:
        clear()
        print("PESAN MAKANAN")
        print("-"*80)
        
        if not os.path.exists(csv_file):
            print("Belum ada data makanan.")
            pause()
            return
        
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            makanan_ready = [
                row for row in reader
                if row["status"] == "ready".upper()
            ]
            
        if not makanan_ready:
            print("Belum ada makanan READY.")
            pause()
            return
        
        headers = ["no_makanan", "nama_makanan", "status", "harga"]
        rows = [
            [row["no_makanan"], row["nama_makanan"], row["status"], row["harga"]]
            for row in makanan_ready
        ]
        table(headers, rows)
        
        target_no = input("Masukan nomor makanan (kosong = batal): ")
        if target_no == "":
            print("Pesan di batalkan.")
            pause()
            return
        
        target =  None
        for row in makanan_ready:
            if row["no_makanan"] == target_no:
                target = row
                break
            
        if target is None:
            print("No makanan tidak di temukan.")
            pause()
            continue
        
        jumlah = input(
            f"Masukan jumlah untuk '{target['nama_makanan']}' (kosong = batal): "
        ).strip()
        if jumlah == "":
            print("Pesanan di batalkan.")
            pause()
            continue
        
        if not jumlah.isdigit() or int(jumlah) <= 0:
            print("jumlah harus angka & lebih besar dari 0".upper())
            pause()
            continue
        
        jumlah = int(jumlah)
        
        harga_str = target["harga"]
        angka = "".join(ch for ch in harga_str if ch.isdigit())
        harga_int = int(angka) if angka else 0
        
        subtotal = harga_int*jumlah
        subtotal_str = f"Rp {subtotal:,.0f}".replace(",", ".")
        
        pesan_id = get_id()
        with open(csv_pesan, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                pesan_id,
                username,
                target["no_makanan"],
                target["nama_makanan"],
                jumlah,
                subtotal_str
            ])
        print("\nPesanan berhasil disimpan!")
        print(f"User     : {username}")
        print(f"Makanan  : {target['nama_makanan']}")
        print(f"Jumlah   : {jumlah}")
        print(f"Subtotal : {subtotal_str}")
        
        lanjut = input("\nPesan makanan lain?(y/n): ").strip().lower()
        if lanjut != "y":
            break
        
    pause()
    
def show_pesanan_admin():
    clear()
    print("DAFTAR PESANAN MAKANAN")
    print("-"*80)
    
    if not os.path.exists(csv_pesan):
        print("Belum ada data pemesanan makanan.")
        pause()
        return
    
    rows = []
    total = 0
    
    with open(csv_pesan, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append([
                row["id"],
                row["username"],
                row["no_makanan"],
                row["nama_makanan"],
                row["jumlah"],
                row["subtotal"]
            ])
            
            subtotal_str = row["subtotal"]
            angka = "".join(ch for ch in subtotal_str if ch.isdigit())
            if angka:
                total += int(angka)
                
    if not rows:
        print("Belum ada data pemesanan makanan.")
        pause()
        return
    
    headers = ["ID", "Nama Pemesan", "No Makanan", "Nama Makanan", "Jumlah", "Subtotal"]
    table(headers,rows)
    
    total_rp = f"Rp {total:,.0f}".replace(",", ".")
    print("-"*80)
    print(f"Total Pendapatan Dari Makanan : {total_rp}")
    pause()