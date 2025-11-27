from utils import pause, clear, choice
from auth import login, register, init_csv
from admin import menu_admin
from user import menu_user
from crud_kamar import init_csv_kamar
from crud_makanan import init_csv_makanan

clear()
init_csv()
init_csv_kamar()
init_csv_makanan()
print("selamat datang di web pemesanan hotel".upper())

def main():
    while True:
        pilihan = [
            "1. login",
            "2. register",
            "3. exit"
        ]

        menu = choice("", pilihan)
        clear()
        print("Kamu memilih: ", menu)


        if menu.startswith("1"):
            username, role = login()
            if role == "admin":
                menu_admin()
            if role == "user":
                menu_user(username)
        if menu.startswith("2"):
            register()
        if menu.startswith("3"):
            break


main()