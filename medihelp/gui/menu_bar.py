import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from medihelp.errors import DataLoadingError, NoFileOpenedError, DataSavingError
from .global_settings import font_name


class MenuBar(tk.Menu):
    '''
    Class representing menu bar at the top of the screen.
    '''

    def __init__(self, system_handler, gui_handler):
        self._font = (font_name, 9)
        super().__init__(gui_handler, font=self._font)
        self._system = system_handler
        self._gui = gui_handler

        # File menu
        self._file_menu = tk.Menu(self, font=self._font, tearoff=False)
        self._file_menu.add_command(label='Załaduj bazę leków', command=self.load_file_button_handler)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Zapisz bazę leków', command=self.save_file_button_handler)
        self._file_menu.add_command(label='Zapisz bazę leków jako', command=self.save_file_as_button_handler)
        self.add_cascade(menu=self._file_menu, label=" Plik ")

        # View menu
        self._view_menu = tk.Menu(self, font=self._font, tearoff=False)
        self._view_menu.add_command(label='Wyświetl listę leków', command=None)
        self._view_menu.add_command(label="Wyświetl kalendarz", command=self.show_callender_button_handler)
        self._view_menu.add_separator()
        self._view_menu.add_command(label="Modyfikuj dane użytkowników", command=self.modify_users_info_button_handler)
        self.add_cascade(menu=self._view_menu, label=" Widok ")

        # Edit menu
        self._edit_menu = tk.Menu(self, font=self._font, tearoff=False)
        self._edit_menu.add_command(label='Dodaj lek', command=None)
        self.add_cascade(menu=self._edit_menu, label=" Edytuj ")

    def load_file_button_handler(self):
        if not self._system.medicines_file_saved():
            if not messagebox.askyesno(title="Załaduj inny plik",
                                       message="Czy na pewno chcesz załadować nowy plik, bez zapisania zmian w pliku obecnym?"):
                return
        path = askopenfilename(title="Wybierz plik do odczytu", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            self._system.load_medicines_database_from(path)
        except DataLoadingError as e:
            messagebox.showerror(title="Błąd", message=str(e))
        self._gui.update_views()

    def save_file_button_handler(self):
        try:
            self._system.save_medicines_database()
        except DataSavingError as e:
            messagebox.showerror(title="Błąd", message=str(e))
        except NoFileOpenedError as e:
            messagebox.showerror(title="Błąd", message=str(e))

    def save_file_as_button_handler(self):
        path = asksaveasfilename(title="Wybierz plik do zapisu", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            self._system.save_medicines_database(path)
        except DataSavingError as e:
            messagebox.showerror(title="Błąd", message=str(e))

    def modify_users_info_button_handler(self):
        pass

    def show_callender_button_handler(self):
        pass
