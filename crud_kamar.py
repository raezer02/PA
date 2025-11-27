import os
import csv
from utils import clear, pause, choice, table


csv_file = "db_kamar.csv"

def init_csv_kamar():
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["no_kamar", "status", "harga", "nama_pemesan"])

def check(no_kamar):
    if not os.path.exists(csv_file):
        return False
    
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["no_kamar"] == no_kamar:
                return True
    return False

def show():
    if not os.path.exists(csv_file):
        print("Belum ada kamar.")
        pause()
        return
    
    headers = ["No Kamar", "Status", "Harga"]
    rows = []

    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append([
                row["no_kamar"],
                row["status"],
                row["harga"]
            ])

    if not rows:
        print("Belum ada data kamar.")
    else:
        table(headers, rows)

def create():
    while True:
        clear()
        print("TAMBAH KAMAR")
        print("-" * 80)

        no_kamar =  input("Masukan nomor kamar: ").strip()
        if no_kamar == "":
            print("nomor kamar tidak boleh kosong!".upper())
            pause()
            continue
        while not no_kamar.isdigit():
            print("input tidak sesuai, input hanya bisa di isi dengan angka!".upper())
            pause()
            return create()
        if check(no_kamar):
            clear()
            print("Sudah ada nama kamar yang sama, coba yang lain!")
            pause()
            continue

        status = [
            "ready",
            "approve",
            "pending",
            "rejected"
        ] 
        menu = choice("", status)
        
        harga = input("Masukkan harga: ")
        if harga == "":
            harga = 0
        harga = int(harga)
        rupiah = f"Rp {harga:,.0f}".replace(",", ".")

        
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([no_kamar, menu, rupiah, ""])

        print("Kamar berhasil di tambah")
        pause()
        break

def edit():
    while True:
        clear()
        print("EDIT")
        print("-" * 80)

        show()

        target = input("Masukan nomor kamar yang ingin di ubah: ").strip()
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

                print("Data lama: ")
                print(f"No kamar : {row['no_kamar']}")
                print(f"Status   : {row['status']}")
                print(f"Harga    : {row['harga']}")

                print("\nKosongkan atau n jika tidak ingin mengubah nilai.")

                edit_status = input("Ubah status? (y/n): ").strip().lower()
                if edit_status == "y":
                    status_list = ["ready",
                    "approve",
                    "pending",
                    "rejected"
                    ]
                    menu_status = choice("Pilih status baru: ", status_list)
                    row["status"] = menu_status

                edit_harga = input("Ubah harga? (y/n): ").strip().lower()
                if edit_harga == "y":
                    while True:
                        harga = input("Masukan harga baru: ").strip()
                        if harga == "":
                            print("harga tidak boleh kosong!".upper())
                            continue
                        if not harga.isdigit():
                            print("harga harus angka!".upper())
                            continue
                        harga_now = int(harga)
                        row["harga"] = f"Rp {harga_now:,.0f}".replace(",", ".")
                        break
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

        print("Data berhasil di ubah.")
        pause()
        return

def delete():
    while True:
        clear()
        print("HAPUS")
        print("-" * 80)

        show()
        target = input("Masukan nomor kamar yang ingin di hapus: ").strip()
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

        new_rows = [row for row in rows if row["no_kamar"] != target]

        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["no_kamar", "status", "harga", "nama_pemesan"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)

        print(f"Kamar {target} berhasil dihapus.")
        pause()
        return
    

def approval():
    while True:
        clear()
        print("APPROVAL")
        print("-" * 80)


        if not os.path.exists(csv_file):
            print("Belum ada kamar.")
            pause()
            return
        
        rows = []
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        pending_rows = [row for row in rows if row["status"] == "PENDING"]

        if not pending_rows:
            print("Tidak ada kamar yang di pesan")
            pause()
            return
        
        headers = ["no_kamar", "status", "harga", "nama_pemesan"]
        rows_table = []
        for row in pending_rows:
            rows_table.append([
                row["no_kamar"],
                row["status"],
                row["harga"],
                row.get("nama_pemesan", "")
            ])

        table(headers,rows_table)

        target = input("Masukan nomor kamar yang ingin di ubah: ").strip()
        if target == "":
            print("nomor kamar tidak boleh kosong!".upper())
            pause()
            return
        
        found = False
        for row in rows:
            if row["no_kamar"] == target and row["status"] == "pending".upper():
                found = True
                
                print("\nData kamar yang dipilih: ")
                print(f"No kamar : {row['no_kamar']}")
                print(f"Status   : {row['status']}")
                print(f"Harga    : {row['harga']}")
                print(f"Pemesan  : {row.get('nama_pemesan', '')}")

                edit_status = input("Ubah status? (y/n): ").strip().lower() #fix
                if edit_status == "y":
                    status_list = ["approve", "rejected"]
                    menu_status = choice("Pilih status baru: ", status_list)
                    row["status"] = menu_status
                break

        if not found:
            print("kamar dengan nomor itu tidak berstatus pending atau belum di pesan.".upper())
            pause()
            return
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["no_kamar", "status", "harga", "nama_pemesan"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        print("Status kamar berhasil diubah.")
        pause()
        return

        