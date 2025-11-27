import os
from InquirerPy import inquirer
from prettytable import PrettyTable

def pause():
    input("\ntekan enter untuk lanjut...")
    clear()

def clear():
    os.system('cls || clear')

def choice(pesan, daftar_pilihan):
    menu = inquirer.select(
        message=pesan,
        choices=[c.upper() for c in daftar_pilihan],
        default=daftar_pilihan[0].upper(),
        qmark="",
        amark=""
    ).execute()

    return menu

def table(headers, rows):

    tables = PrettyTable()
    tables.field_names = headers
        
    for row in rows:
        tables.add_row(row)
    print(tables)