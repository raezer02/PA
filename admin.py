from utils import clear, choice
from crud_kamar import create, show, edit, delete, approval
from crud_makanan import create_makanan, show_makanan, edit_makanan, delete_makanan 
from pesan_makan import show_pesanan_admin
from auth import add_account



def menu_admin():
    while True:
        pilihan = [
            "1. Menu kamar",    #done
            "2. Menu makanan",  #done
            "3. Lihat pesanan",  
            "4. Tambah staf",   #done
            "5. Approval",      #done
            "6. Keluar"         #done
        ]

        menu = choice("Menu admin: ", pilihan)
        clear()

        if menu.startswith("1"):
            menu_kamar()
        if menu.startswith("2"):
            menu_makanan()
        if menu.startswith("3"):
            show_pesanan_admin()
        if menu.startswith("4"):
            add_account()
        if menu.startswith("5"):
            approval()
        if menu.startswith("6"):
            return
    
def menu_kamar():
    while True:
        pilihan = [
            "1. Tambah kamar",
            "2. Edit",
            "3. Hapus",
            "4. Kembali"
        ]

        show()
        menu = choice("Menu kamar: ", pilihan)
        clear()
        
        if menu.startswith("1"):
            create()
        if menu.startswith("2"):
            edit()
        if menu.startswith("3"):
            delete()
        if menu.startswith("4"):
            return


def menu_makanan():
    while True:  
        pilihan = [
            "1. Tambah menu",
            "2. Edit",
            "3. Hapus",
            "4. Kembali"
        ]
        show_makanan()
        menu = choice("Menu kamar: ", pilihan)
        clear()

        if menu.startswith("1"):
            create_makanan()
        if menu.startswith("2"):
            edit_makanan()
        if menu.startswith("3"):
            delete_makanan()
        if menu.startswith("4"):
            return
        