import os
import csv
from utils import clear, pause, choice, table

csv_file = "db_makanan.csv"

def init_csv_makanan():
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["no_makanan", "nama_makanan", "status", "harga"])

def check(nama_makanan=None, no_makanan=None):
    if not os.path.exists(csv_file):
        return False
    
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["no_makanan"] == no_makanan:
                return True
            if row["nama_makanan"] == nama_makanan:
                return True
    return False

def create_index():
    if not os.path.exists(csv_file):
        return 1
    
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return 1
    
    last_no = int(rows[-1]["no_makanan"])
    return last_no + 1

def re_index():
    if not os.path.exists(csv_file):
        return
    
    rows = []
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
            
    for i, row in enumerate(rows, start=1):
        row["no_makanan"] = str(i)

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["no_makanan", "nama_makanan", "status", "harga"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def show_makanan():
    if not os.path.exists(csv_file):
        print("Belum ada menu.")
        pause()
        return
    
    headers = ["no_makanan", "nama_makanan", "status", "harga"]
    rows = []

    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append([
                row["no_makanan"],
                row["nama_makanan"],
                row["status"],
                row["harga"]
            ])

    if not rows:
        print("Belum ada data makanan.")
    else:
        table(headers, rows)

def create_makanan():
    while True:
        clear()
        print("TAMBAH MAKANAN")
        print("-" * 80)

        nama_makanan =  input("Masukan nama makanan: ").strip()
        if nama_makanan == "":
            print("nama makanan tidak boleh kosong!".upper())
            pause()
            continue
        # while not nama_makanan.isdigit():
        #     print("input tidak sesuai, input hanya bisa di isi dengan angka!".upper())
        #     pause()
        #     return create()
        if check(nama_makanan):
            clear()
            print("Sudah ada nama makanan yang sama, coba yang lain!")
            pause()
            continue

        status = [
            "ready",
            "sold out"
        ] 
        menu = choice("Pilih status makanan", status)
        
        harga = input("Masukkan harga: ")
        if harga == "":
            harga = 0
        harga = int(harga)
        rupiah = f"Rp {harga:,.0f}".replace(",", ".")

        no_makanan = create_index()

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([no_makanan, nama_makanan, menu, rupiah])

        print("makanan berhasil di tambah")
        pause()
        break

def edit_makanan():
    while True:
        clear()
        print("EDIT")
        print("-" * 80)

        show_makanan()

        target = input("Masukan nomor makanan yang ingin di ubah: ").strip()
        if target == "":
            print("nomor makanan tidak boleh kosong!".upper())
            pause()
            return
        
        if not check(no_makanan=target):
            print("nomor makanan tidak di temukan!".upper())
            pause()
            return
        
        rows = []
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        found = False
        for row in rows:
            if row["no_makanan"] == target:
                found = True

                print("Data lama:")
                print(f"No        : {row['no_makanan']}")
                print(f"Nama      : {row['nama_makanan']}")
                print(f"Status    : {row['status']}")
                print(f"Harga     : {row['harga']}")

                print("\nKosongkan atau n jika tidak ingin mengubah nilai.")

                nama_baru = input("Nama baru (kosong = tidak di ubah): ").strip()
                if nama_baru != "":
                    duplicate = any(
                        r["nama_makanan"] == nama_baru and r["no_makanan"] != target
                        for r in rows
                    )
                    if duplicate:
                        print("Nama makanan sudah digunakan!")
                        pause()
                        return
                    else:
                        row["nama_makanan"] = nama_baru

                edit_status = input("Ubah status? (y/n): ").strip().lower()
                if edit_status == "y":
                    status_list = [
                        "ready",
                        "sold out"
                    ]
                    menu_status = choice("Pilih status baru: ", status_list)
                    row["status"] = menu_status

                edit_harga = input("Ubah harga? (y/n): ").strip().lower()
                if edit_harga == "y":
                    while True:
                        harga = input("Masukan harga baru kosong = batal: ").strip()
                        if harga == "":
                            break
                        if not harga.isdigit():
                            print("harga harus angka!".upper())
                            continue
                        harga_now = int(harga)
                        row["harga"] = f"Rp {harga_now:,.0f}".replace(",", ".")
                        break
                break

        if not found:
            print("makanan tidak di temukan")
            pause()
            return
        
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["no_makanan", "nama_makanan", "status", "harga"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print("Data berhasil di ubah.")
        pause()
        return
    
def delete_makanan():
    while True:
        clear()
        print("HAPUS")
        print("-" * 80)

        show_makanan()
        target = input("Masukan nomor makanan yang ingin di hapus: ").strip()
        if target == "":
            print("nomor makanan tidak boleh kosong!".upper())
            pause()
            return
        
        if not check(no_makanan=target):
            print("nomor makanan tidak di temukan!".upper())
            pause()
            return
        
        rows = []
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        new_rows = [row for row in rows if row["no_makanan"] != target]

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["no_makanan", "nama_makanan", "status", "harga"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)

        print(f"makanan {target} berhasil dihapus.")

        re_index()
        pause()
        return