import os
import csv
from utils import pause, clear, choice

csv_file = "database.csv"

def init_csv():
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password", "role"])

def check(username):
    if not os.path.exists(csv_file):
        return False
    
    with open(csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return True
    return False

def role_select():
    role = [
        "admin",
        "user"
    ]
    menu = choice("", role)
    print("Kamu memilih role", menu)
    return menu.lower()

def add_account():
    while True:
        clear()    
        print("TAMBAH AKUN")
        print("-" * 80)
        username = input("Masukan username baru: ").strip()
        if username == "":
            print("USERNAME TIDAK BOLEH KOSONG!")
            pause()
            continue

        if check(username):
            clear()
            print("Username telah digunakan, coba yang lain!")
            pause()
            continue

        password = input("Buat password: ").strip()
        if password == "":
            print("PASSWORD TIDAK BOLEH KOSONG!")
            pause()
            continue

        role = role_select()

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        print(f"Akun {username} berhasil dibuat")
        pause()

        lagi = input("Tambah akun lagi? (y/n): ").strip().lower()
        if lagi != "y":
            break 
    
def login():
        clear()
        print("LOGIN")
        print("-" * 80)

        if not os.path.exists(csv_file):
            print("Akun tidak terdaftar, silahkan daftar terlebih dahulu!")
            pause()
            return None, None

        while True:
            username = input("Username: ").strip()
            if username == "":
                print("USERNAME TIDAK BOLEH KOSONG!")
                pause()
                continue

            password = input("Password: ")
            if password == "":
                print("PASSWORD TIDAK BOLEH KOSONG!")
                pause()
                continue

            found = False
            with open(csv_file, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["username"] == username:
                        found = True
                        if row["password"] == password:
                            role = row["role"]
                            clear()
                            print(f"Login berhasil! Selamat datang, {username.upper()}")
                            print(f"Kamu login sebagai {row['role'].upper()}")
                            pause()
                            return username, role
                        else:
                            print("Password salah!")
                            pause()
                            clear()
                            break
                        
            if not found:
                print("Username tidak ditemukan!")
                pause()
                clear()


def register():
    while True:
        clear()    
        print("TAMBAH AKUN")
        print("-" * 80)
        username = input("Masukan username baru: ").strip()
        if username == "":
            print("USERNAME TIDAK BOLEH KOSONG!")
            pause()
            continue

        if check(username):
            clear()
            print("Username telah digunakan, coba yang lain!")
            pause()
            continue

        password = input("Buat password: ").strip()
        if password == "":
            print("PASSWORD TIDAK BOLEH KOSONG!")
            pause()
            continue

        role = "user"

        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, role])

        print(f"Akun {username} berhasil dibuat")
        pause()
        break
