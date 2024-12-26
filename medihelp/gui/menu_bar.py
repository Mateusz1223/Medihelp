import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from .gui import GUI
from medihelp.errors import DataLoadingError, NoFileOpenedError, DataSavingError
from medihelp.system import System
from .global_settings import font_name


class MenuBar(tk.Menu):
    '''
    Class representing menu bar at the top of the screen.
    '''

    def __init__(self, system_handler: System, gui_handler: GUI):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI
        '''
        self._font = (font_name, 9)
        super().__init__(gui_handler, font=self._font)
        self._system = system_handler
        self._gui = gui_handler

        # File menu
        self._file_menu = tk.Menu(self, font=self._font, tearoff=False)
        self._file_menu.add_command(label='Zapisz bazę leków', command=self.save_file_button_handler)
        self._file_menu.add_command(label='Zapisz bazę leków jako', command=self.save_file_as_button_handler)
        self._file_menu.add_separator()
        self._file_menu.add_command(label='Załaduj bazę leków', command=self.load_file_button_handler)
        self.add_cascade(menu=self._file_menu, label="Plik")

        # View menu
        self._view_menu = tk.Menu(self, font=self._font, tearoff=False)
        self._view_menu.add_command(label='Wyświetl listę leków', command=self.show_medicine_list_button_handler)
        self._view_menu.add_command(label="Wyświetl kalendarz", command=self.show_callender_button_handler)
        self._view_menu.add_separator()
        self._view_menu.add_command(label="Przełącz użytkownika", command=self.switch_users_button_handler)
        self._view_menu.add_command(label="Modyfikuj dane użytkownika", command=self.modify_users_info_button_handler)
        self.add_cascade(menu=self._view_menu, label="Widok")

    def load_file_button_handler(self):
        '''
        Asks user for path and loads medicine database from it.
        '''
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
        '''
        Saves medicine database to currently "opened" file
        '''
        try:
            self._system.save_medicines_database()
        except DataSavingError as e:
            messagebox.showerror(title="Błąd", message=str(e))
        except NoFileOpenedError as e:
            messagebox.showerror(title="Błąd", message=str(e))

    def save_file_as_button_handler(self):
        '''
        Asks user to choose path and saves medicine database under it.
        '''
        path = asksaveasfilename(title="Wybierz plik do zapisu", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            self._system.save_medicines_database(path)
        except DataSavingError as e:
            messagebox.showerror(title="Błąd", message=str(e))

    def modify_users_info_button_handler(self):
        '''
        Changes view to modify-user-view
        '''
        self._gui.set_current_view('modify-user-view')

    def show_callender_button_handler(self):
        '''
        Changes view to calendar-view
        '''
        self._gui.set_current_view('calendar-view')

    def switch_users_button_handler(self):
        '''
        Hides gui's menubar and changes view to choose-user-view
        '''
        self._gui.hide_menubar()
        self._gui.set_current_view('choose-user-view')

    def show_medicine_list_button_handler(self):
        '''
        Changes view to medicine-list-view
        '''
        self._gui.set_current_view('medicine-list-view')
