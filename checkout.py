import os
from utils import pause, clear, table
from crud_kamar import csv, csv_file



def checkout_user(username):

    clear()
    print("CHECKOUT")
    print("-" * 80)

    pilih = input("Apakah anda yakin untuk melanjutkan checkout? (n/Enter)").strip().lower()
    if pilih == "n":
        print("Checkout dibatalkan.")
        pause()
        return
    
    if not os.path.exists(csv_file):
        print("Belum ada data kamar.")
        pause()
        return


    rows = []
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    kamar_user = [
        row for row in rows
        if row.get("nama_pemesan", "") == username
        and row.get("status", "") == "approve".upper()
    ]

    if not kamar_user:
        print("Kamu tidak punya kamar yang berstatus APPROVE.")     #jaga-jaga
        pause()
        return
    
    if len(kamar_user) > 1:
        print("Kamar yang sedang kamu tempati: \n")

        headers = ["no_kamar", "status", "harga"]
        rows_table = []

        for row in kamar_user:
            rows_table.append([row["no_kamar"], row["status"], row["harga"]])
        table(headers, rows_table)

        no = input("\nMasukan no kamar yang ingin di checkout: ").strip()

        target = None
        for row in kamar_user:
            if row["no_kamar"] == no:
                target = row
                break

        if no == "":
            print("nomor tidak boleh kosong!".upper())
            pause()
            return
        if target is None:
            print("nomor kamar tidak valid.".upper())
            pause()
            return
    else:
        target = kamar_user[0]

    clear()
    print("detail kamar".upper())
    print("-"*80)
    print(f"No Kamar     : {target['no_kamar']}")
    print(f"Nama Pemesan : {target['nama_pemesan']}")
    print(f"Status       : {target['status']}")
    print(f"Harga        : {target['harga']}")

    konfirm = input("Yakin ingin checkout kamar ini? (y/n): ").strip().lower()
    if konfirm != "y":
        print("Checkout dibatalkan.")
        pause()
        return

    for row in rows:
        if row["no_kamar"] == target["no_kamar"]:
            row["status"] = "ready".upper()
            row["nama_pemesan"] = ""
            break

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["no_kamar", "status", "harga", "nama_pemesan"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("checkout berhasil!")
    pause()
