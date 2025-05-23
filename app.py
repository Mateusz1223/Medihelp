from medihelp.system import System
from medihelp.gui.gui import GUI
from medihelp.errors import DataLoadingError
from tkinter import messagebox


def main():
    system = System()
    try:
        system.load_users_data()
    except DataLoadingError as e:
        messagebox.showerror(title="Bład!",
                             message=f"Błąd krytyczny podczas ładowania danych niezbędnych do działania programu:\n{e} -> {e.__context__}")
        return

    # Load medicine database from data/medicines.csv on default
    system.load_medicines_database_from('data/medicines.csv')

    GUI(system)


if __name__ == '__main__':
    main()
