from utils import clear, pause, choice, table
from pesan_kamar import pesan_kamar, show_pesanan
from crud_kamar import csv, csv_file
from checkout import checkout_user
from pesan_makan import pesan_makan

def menu_user(username):
    while True:

        approved = False

        try:
            with open(csv_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["nama_pemesan"] == username and row["status"] == "approve".upper():
                        # print("cek: ", username, row["status"])       debug to catch username and status
                        approved = True
                        break
        except FileNotFoundError:
            approved = False

        if approved:
            pilihan = [
            "1. Pesan kamar",    
            "2. pesan makanan",
            "3. Lihat pesanan",
            "4. Checkout",
            "5. Keluar"
            ]
        else:
            pilihan = [
                    "1. Pesan kamar",    
                    "2. Lihat pesanan",
                    "3. Keluar"
            ]

        menu = choice("Menu user: ", pilihan)
        clear()

        if menu.startswith("1"):
            pesan_kamar(username)
        if menu.startswith("2"):
            if approved:
                pesan_makan(username)
            else:
                show_pesanan(username)
        if menu.startswith("3"):
            if approved:
                show_pesanan(username)
            else:
                return
        if menu.startswith("4"):
            checkout_user(username)
        if menu.startswith("5"):
            return
