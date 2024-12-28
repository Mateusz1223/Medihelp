import customtkinter as ctk
from . import global_settings as gs
from .common import normalize_list_of_names, normalize_name
from .gui import GUI
from medihelp.errors import IllegalCharactersInANameError
from medihelp.system import System
from tkinter import messagebox
from datetime import datetime


class ModifyUserForm(ctk.CTkFrame):
    '''
    Class ModifyUserForm responsible for displaying user info (except for perscriptions)
        and providing an interface to edit it.
    '''

    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        super().__init__(parent, border_width=1)

        self._system = system_handler
        self._gui = gui_handler

        self.padx = 20
        self.pady = 2

        self.columnconfigure(0, weight=1)

        # This label should never be visible to the user
        self._user_not_choosen_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                    text='Użytkownik nie został wybrany!',
                                                    font=(gs.font_name, 30, 'bold'))

        self._form_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        self._form_frame.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='nw')
        self.setup_form()

    def setup_form(self):
        self._name_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                        text='Nazwa użytkownika: ', font=(gs.font_name, 10, 'bold'))
        self._name_label.pack(pady=self.pady, anchor='w')
        self._name_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 2,
                                        font=(gs.font_name, 10), border_width=0.5)
        self._name_entry.pack(pady=self.pady, anchor='w')

        self._birth_date_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                              text='Data urodzenia', font=(gs.font_name, 10, 'bold'))
        self._birth_date_label.pack(pady=self.pady, anchor='w')
        self._birth_date_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 4, font=(gs.font_name, 10),
                                              border_width=0.5, placeholder_text='RRRR-MM-DD')
        self._birth_date_entry.pack(pady=self.pady, anchor='w')

        self._allergies_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                             text='Allergie', font=(gs.font_name, 10, 'bold'))
        self._allergies_label.pack(pady=self.pady, anchor='w')
        self._allergies_textbox = ctk.CTkTextbox(self._form_frame, width=gs.min_width - 100, height=50,
                                                 font=(gs.font_name, 10), border_width=0.5)
        self._allergies_textbox.pack(pady=self.pady, anchor='w')

        self._illnesses_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                             text='Jednostki chorobowe', font=(gs.font_name, 10, 'bold'))
        self._illnesses_label.pack(pady=self.pady, anchor='w')
        self._illnesses_textbox = ctk.CTkTextbox(self._form_frame, width=gs.min_width - 100, height=50,
                                                 font=(gs.font_name, 10), border_width=0.5)
        self._illnesses_textbox.pack(pady=self.pady, anchor='w')

        # Create save button and discard changes button
        self._buton_frame = ctk.CTkFrame(self._form_frame, fg_color=self.cget("fg_color"))
        self._buton_frame.pack(pady=self.pady + 10, anchor='w', fill='x')

        self._save_changes_button = ctk.CTkButton(self._buton_frame, fg_color=gs.action_color,
                                                  text='Zapisz zmiany', font=(gs.font_name, 10),
                                                  command=self._save_changes_button_handler)
        self._save_changes_button.grid(row=0, column=0, sticky='w')
        self._discard_changes_button = ctk.CTkButton(self._buton_frame, fg_color=gs.edit_color,
                                                     text='Odrzuć zmiany', font=(gs.font_name, 10),
                                                     command=self._discard_changes_button_handler)
        self._discard_changes_button.grid(row=0, column=1, padx=10, sticky='w')

        # fill form with proper data
        self.clear_form()

    def clear_form(self):
        '''
        Fills form entries and textboxes with original gui's current user data.
        '''
        # Show proper message and hide form if there is no gui's current user choosen.
        user = self._system.users().get(self._gui.current_user_id())
        if not user:
            self._form_frame.grid_forget()
            self._user_not_choosen_label.grid(row=0, column=0, padx=20, pady=20, sticky='nw')
            return
        self._user_not_choosen_label.grid_forget()
        self._form_frame.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='nw')

        # fill form with proper data
        self._name_entry.delete('0', ctk.END)
        self._name_entry.insert('0', user.name())

        self._birth_date_entry.delete('0', ctk.END)
        self._birth_date_entry.insert('0', user.birth_date())

        self._allergies_textbox.delete('0.0', ctk.END)
        allergies_str = ', '.join(user.allergies())
        self._allergies_textbox.insert('0.0', allergies_str)
        if len(user.allergies()) == 0:
            self._allergies_textbox.insert('0.0', 'Podaj nazwy substancji oddzielone przecinkiem.')

        self._illnesses_textbox.delete('0.0', ctk.END)
        illnesses_str = ', '.join(user.illnesses())
        self._illnesses_textbox.insert('0.0', illnesses_str)
        if len(user.illnesses()) == 0:
            self._illnesses_textbox.insert('0.0', 'Podaj nazwy chorób i dolegliwości oddzielone przecinkiem.')

    def _save_changes_button_handler(self):
        # Save old user name in order to check whether it changed or not.
        # If so update all views
        user = self._system.users().get(self._gui.current_user_id())
        old_name = user.name()

        # Extract data from the form
        name = self._name_entry.get()
        try:
            name = normalize_name(name)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa lekarstwa: {e}")
            return

        illnesses = self._illnesses_textbox.get("1.0", "end")
        if illnesses == 'Podaj nazwy chorób i dolegliwości oddzielone przecinkiem.\n':
            illnesses = ''
        illnesses = illnesses.split(',')
        try:
            illnesses = normalize_list_of_names(illnesses)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy chorób: {e}")
            return

        allergies = self._allergies_textbox.get("1.0", "end")
        if allergies == 'Podaj nazwy substancji oddzielone przecinkiem.\n':
            allergies = ''
        allergies = allergies.split(',')
        try:
            allergies = normalize_list_of_names(allergies)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy substancji (alergie): {e}")
            return

        try:
            birth_date = datetime.strptime(self._birth_date_entry.get(), '%Y-%m-%d').date()
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy format daty!")
            return

        # Commit changes
        try:
            current_user = self._system.users().get(self._gui.current_user_id())
            self._system.change_user(user_id=current_user.id(),
                                     name=name,
                                     birth_date=birth_date,
                                     illnesses=illnesses,
                                     allergies=allergies)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        messagebox.showinfo(title='Informacja', message='Zmiany zostały zapisane!')

        if name != old_name:
            self._gui.update_views()
        else:
            self._gui.update_view('modify-user-view')

    def _discard_changes_button_handler(self):
        self.clear_form()
