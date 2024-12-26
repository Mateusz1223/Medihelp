import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from . import global_settings as gs
from medihelp.medicine import Medicine
from .gui import GUI
from .user_note_tile import UserNoteTile
from .add_note_tile import AddNoteTile
from .common import set_of_strings_to_string, normalize_list_of_names, normalize_name
from medihelp.errors import IllegalCharactersInANameError, UserDoesNotExistError
from medihelp.system import System


class MedicineTile(ctk.CTkFrame):
    '''
    Class MedicineTile is responsible for displaying informations contained in medicine object
        and provides an interface to modify the medicine instance in the database it is responsible for.
    '''

    def __init__(self, system_handler: System, gui_handler: GUI, parent, medicine: Medicine):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param medicine: Medicine object that is to be visualized
        :type medicine: Medicine
        '''

        super().__init__(parent, border_width=1)

        self._system = system_handler
        self._gui = gui_handler

        self._medicine = medicine

        self.columnconfigure(0, weight=1)

        # Change the look of the tile when medicine is expired
        if self._medicine.is_expired():
            self._expired_warning_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                       text='Lek jest przeterminowany. Proszę go zutylizować!',
                                                       font=(gs.font_name, 14, 'bold'))
            self._expired_warning_label.grid(row=0, column=0, padx=21.5, pady=10, sticky='w')

            self.configure(fg_color=gs.problem_color)

        self._info_tile = MedicineInfoTile(self._system, self._gui, self, medicine)
        self._info_tile.grid(row=1, column=0, padx=1.5, pady=1.5, sticky='we')

        self._edit_tile = MedicineEditTile(self._system, self._gui, self, medicine)

        self._edit_button = ctk.CTkButton(self, fg_color=gs.edit_color,
                                          text='Edytuj', font=(gs.font_name, 10),
                                          command=self._edit_button_handler)
        self._edit_button.grid(row=2, column=0, padx=21.5, pady=10, sticky='w')

        self._cancel_button = ctk.CTkButton(self, fg_color=gs.edit_color,
                                            text='Anuluj', font=(gs.font_name, 10),
                                            command=self._cancel_button_handler)

    def _edit_button_handler(self):
        self._info_tile.grid_forget()
        self._edit_tile.clear_form()
        self._edit_tile.grid(row=1, column=0, padx=1.5, pady=1.5, sticky='we')

        self._edit_button.grid_forget()
        self._cancel_button.grid(row=2, column=0, padx=21.5, pady=10, sticky='w')

    def _cancel_button_handler(self):
        self._edit_tile.grid_forget()
        self._info_tile.grid(row=1, column=0, padx=1.5, pady=1.5, sticky='we')

        self._cancel_button.grid_forget()
        self._edit_button.grid(row=2, column=0, padx=21.5, pady=10, sticky='w')


class MedicineInfoTile(ctk.CTkFrame):
    '''
    MedicineInfoTile is a component of a MedicineTile
        and is responsible for displaying medicine informations and take dose and delete button.
    '''
    def __init__(self, system_handler: System, gui_handler, parent, medicine: Medicine):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param medicine: Medicine object that is to be visualized
        :type medicine: Medicine
        '''

        super().__init__(parent, border_width=0, fg_color=parent.cget('fg_color'))

        self._system = system_handler
        self._gui = gui_handler

        self._medicine = medicine

        self._show_notes = False

        self.padx = 20
        self.pady = 2

        # Display info about the medicine
        self._name_and_manufacturer_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                         text=f'{self._medicine.name()} (productent: {self._medicine.manufacturer()})',
                                                         font=(gs.font_name, 14, "bold"))
        self._name_and_manufacturer_label.pack(padx=self.padx, pady=self.pady + 10, anchor='w')

        self._doses_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                         text=f'(Pozostałe dawki: {self._medicine.doses_left()} na {self._medicine.doses()})',
                                         font=(gs.font_name, 10))
        self._doses_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._for_ilnesses_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                text=f'Na następujące choroby: {set_of_strings_to_string(self._medicine.illnesses())}',
                                                font=(gs.font_name, 10))
        self._for_ilnesses_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._substances_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text=f'Substancje czynne: {set_of_strings_to_string(self._medicine.substances())}',
                                              font=(gs.font_name, 10))
        self._substances_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._reccomended_age_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                   text=f'Zalecany wiek: {self._medicine.recommended_age()}',
                                                   font=(gs.font_name, 10, "bold"))
        self._reccomended_age_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._expiration_date_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                   text=f'Data ważności: {self._medicine.expiration_date()}',
                                                   font=(gs.font_name, 10, "bold"))
        self._expiration_date_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        recipients = set()
        for id in self._medicine.recipients():
            user = self._system.users().get(id)
            if user:
                name = user.name()
            else:
                name = "Nieznany użytkownik"
            recipients.add(name)
        self._recipients_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text=f'Użytkownicy przyjmujący lek: {set_of_strings_to_string(recipients)}',
                                              font=(gs.font_name, 10))
        self._recipients_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        # Buttons Take Dose, Show Notes and Delete
        self._buton_frame = ctk.CTkFrame(self, fg_color=parent.cget("fg_color"))
        self._buton_frame.columnconfigure(0, weight=1)
        self._buton_frame.columnconfigure(1, weight=1)
        self._buton_frame.columnconfigure(2, weight=1)
        self._take_dose_button = ctk.CTkButton(self._buton_frame, fg_color=gs.action_color,
                                               text='Weź dawkę', font=(gs.font_name, 10),
                                               command=self._take_dose_button_handler)
        self._take_dose_button.grid(row=0, column=0, sticky='w')
        self._show_notes_button = ctk.CTkButton(self._buton_frame, fg_color=gs.neutral_color,
                                                text='↓ Pokaż notatki użytkowników ↓', font=(gs.font_name, 10),
                                                command=self._show_notes_button_handler)
        self._show_notes_button.grid(row=0, column=1, sticky='w' + 'e')
        self._delete_button = ctk.CTkButton(self._buton_frame, fg_color=gs.edit_color,
                                            text='Usuń', font=(gs.font_name, 10),
                                            command=self._delete_button_handler)
        self._delete_button.grid(row=0, column=2, sticky='e')
        self._buton_frame.pack(padx=self.padx, pady=self.pady + 10, anchor='w', fill='x')

        # Load users' notes
        self._notes_frame = self._buton_frame = ctk.CTkFrame(self, fg_color=parent.cget("fg_color"))
        self._notes_frame.columnconfigure(0, weight=1)
        self._user_notes_tiles = []
        create_add_note_tile = True
        for author_id, content in self._medicine.notes().items():
            if content:
                self._user_notes_tiles.append(UserNoteTile(system_handler=self._system,
                                                           gui_handler=self._gui,
                                                           parent=self._notes_frame,
                                                           medicine_id=self._medicine.id(),
                                                           author_id=author_id,
                                                           content=content,
                                                           editable=(True if self._gui.current_user_id() == author_id else False)))
                if self._gui.current_user_id() == author_id:
                    create_add_note_tile = False
        if create_add_note_tile:
            # Create add_note_button if there is no note belonging to the current user already
            self._add_note_tile = AddNoteTile(system_handler=self._system, gui_handler=self._gui,
                                              parent=self._notes_frame, medicine_id=self._medicine.id())
            self._add_note_tile.grid(row=0, column=0, padx=0, pady=self.pady, sticky='we')

        row_counter = 1
        for note_tile in self._user_notes_tiles:
            note_tile.grid(row=row_counter, column=0, padx=0, pady=self.pady, sticky='we')
            row_counter += 1

    def _show_notes_button_handler(self):
        if not self._show_notes:
            self._show_notes = True
            self._show_notes_button.configure(text='↑ Schowaj notatki użytkowników ↑')
            self._notes_frame.pack(padx=self.padx, pady=self.pady + 10, anchor='w', fill='x')
        else:
            self._show_notes = False
            self._show_notes_button.configure(text='↓ Pokaż notatki użytkowników ↓')
            self._notes_frame.pack_forget()

    def _take_dose_button_handler(self):
        '''
        Takes doese of a medicine
        '''
        user = self._system.users().get(self._gui.current_user_id())
        if not user:
            raise UserDoesNotExistError(self._gui.current_user_id())
        try:
            self._system.take_dose(self._medicine.id(), user)
        except Exception as e:
            messagebox.showwarning(title="Uwaga!", message=e)
            return
        messagebox.showinfo(title="Informacja", message=f"Wzięto jedną dawkę leku {self._medicine.name()}.")
        self._gui.update_view('medicine-list-view', self._medicine.id())

    def _delete_button_handler(self):
        '''
        Deletes the medicine from the database
        '''
        # Ask user for confirmation.
        answer = messagebox.askyesno(title="Zatwierdź",
                                     message=f"Czy na pewno chcesz usunąć lek o nazwie {self._medicine.name()}")
        if answer:
            # Delete medicine
            medicine_id = self._medicine.id()
            medicine_name = self._medicine.name()
            self._system.del_medicine(medicine_id)
            messagebox.showinfo(title='Informacja',
                                message=f'Lek o nazwie {medicine_name} został usunięty!')
            self._gui.update_view('medicine-list-view', medicine_id)


class MedicineEditTile(ctk.CTkFrame):
    '''
    MedicineEditTile is a component of a MedicineTile
        and is responsible for providing an interface for editing medicine informations.
    '''
    def __init__(self, system_handler: System, gui_handler, parent, medicine: Medicine):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param medicine: Medicine object that is to be visualized
        :type medicine: Medicine
        '''
        super().__init__(parent, border_width=0, fg_color=parent.cget('fg_color'))

        self._system = system_handler
        self._gui = gui_handler

        self._medicine = medicine

        self.padx = 20
        self.pady = 2

        self.setup_form()

    def setup_form(self):
        self._name_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                        text='Nazwa leku: ', font=(gs.font_name, 10, 'bold'))
        self._name_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._name_entry = ctk.CTkEntry(self, width=gs.min_width / 2,
                                        font=(gs.font_name, 10), border_width=0.5)
        self._name_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._manufacturer_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                text='Producent', font=(gs.font_name, 10, 'bold'))
        self._manufacturer_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._manufacturer_entry = ctk.CTkEntry(self, width=gs.min_width / 2,
                                                font=(gs.font_name, 10), border_width=0.5)
        self._manufacturer_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._doses_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                         text='Ilość dawek w opakowaniu', font=(gs.font_name, 10, 'bold'))
        self._doses_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._doses_entry = ctk.CTkEntry(self, width=gs.min_width / 4, font=(gs.font_name, 10),
                                         border_width=0.5)
        self._doses_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._doses_left_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text='Ilość pozostałych dawek', font=(gs.font_name, 10, 'bold'))
        self._doses_left_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._doses_left_entry = ctk.CTkEntry(self, width=gs.min_width / 4,
                                              font=(gs.font_name, 10), border_width=0.5)
        self._doses_left_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._recommended_age_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                   text='Zalecany wiek', font=(gs.font_name, 10, 'bold'))
        self._recommended_age_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._recommended_age_entry = ctk.CTkEntry(self, width=gs.min_width / 4,
                                                   font=(gs.font_name, 10), border_width=0.5)
        self._recommended_age_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._expiration_date_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                   text='Data ważności', font=(gs.font_name, 10, 'bold'))
        self._expiration_date_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._expiration_date_entry = ctk.CTkEntry(self, width=gs.min_width / 4, font=(gs.font_name, 10),
                                                   border_width=0.5, placeholder_text='RRRR-MM-DD')
        self._expiration_date_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._substances_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text='Substancje', font=(gs.font_name, 10, 'bold'))
        self._substances_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._substances_textbox = ctk.CTkTextbox(self, width=gs.min_width - 100, height=50,
                                                  font=(gs.font_name, 10), border_width=0.5)
        self._substances_textbox.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._illnesses_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                             text='Na choroby', font=(gs.font_name, 10, 'bold'))
        self._illnesses_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._illnesses_textbox = ctk.CTkTextbox(self, width=gs.min_width - 100, height=50,
                                                 font=(gs.font_name, 10), border_width=0.5)
        self._illnesses_textbox.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._recipients_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text='Zaznacz odbiorów leku:', font=(gs.font_name, 10, 'bold'))
        self._recipients_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        # Create a dictionary of checkboxes where user id is the key and chackbox is the value
        self._recipients_checkboxes_variables = {}
        self._recipients_checkboxes = {}
        for user_id, user in self._system.users().items():
            variable = ctk.IntVar(value=0)
            checkbox = ctk.CTkCheckBox(self, text=user.name(), variable=variable,
                                       onvalue=1, offvalue=0, font=(gs.font_name, 10),
                                       hover_color=gs.action_color, fg_color=gs.action_color)
            checkbox.pack(padx=self.padx, pady=self.pady, anchor='w')
            self._recipients_checkboxes[user_id] = checkbox
            self._recipients_checkboxes_variables[user_id] = variable

        self._buton_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        self._buton_frame.pack(padx=self.padx, pady=self.pady + 10, anchor='w', fill='x')

        self._approve_button = ctk.CTkButton(self._buton_frame, fg_color=gs.action_color,
                                             text='Zatwierdź', font=(gs.font_name, 10),
                                             command=self._approve_button_handler)
        self._approve_button.grid(row=0, column=0, sticky='w')

        self.clear_form()

    def clear_form(self):
        '''
        Clears form entries, textboxes and check buttons
        '''
        self._name_entry.delete('0', ctk.END)
        self._name_entry.insert('0', self._medicine.name())

        self._manufacturer_entry.delete('0', ctk.END)
        self._manufacturer_entry.insert('0', self._medicine.manufacturer())

        self._doses_entry.delete('0', ctk.END)
        self._doses_entry.insert('0', str(self._medicine.doses()))

        self._doses_left_entry.delete('0', ctk.END)
        self._doses_left_entry.insert('0', str(self._medicine.doses_left()))

        self._recommended_age_entry.delete('0', ctk.END)
        self._recommended_age_entry.insert('0', str(self._medicine.recommended_age()))

        self._expiration_date_entry.delete('0', ctk.END)
        self._expiration_date_entry.insert('0', str(self._medicine.expiration_date()))

        self._substances_textbox.delete('0.0', ctk.END)
        substances_str = ', '.join(self._medicine.substances())
        self._substances_textbox.insert('0.0', substances_str)

        self._illnesses_textbox.delete('0.0', ctk.END)
        illnesses_str = ', '.join(self._medicine.illnesses())
        self._illnesses_textbox.insert('0.0', illnesses_str)

        for user_id in self._medicine.recipients():
            self._recipients_checkboxes_variables[user_id].set(1)

    def _approve_button_handler(self):
        '''
        Modifies medicine with the data from the form
        '''
        name = self._name_entry.get()
        try:
            name = normalize_name(name)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa lekarstwa: {e}")
            return
        manufacturer = self._manufacturer_entry.get()
        try:
            manufacturer = normalize_name(manufacturer)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa producenta: {e}")
            return
        illnesses = self._illnesses_textbox.get("1.0", "end").split(',')
        try:
            illnesses = normalize_list_of_names(illnesses)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy chorób: {e}")
            return
        substances = self._substances_textbox.get("1.0", "end").split(',')
        try:
            substances = normalize_list_of_names(substances)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy substancji: {e}")
            return
        try:
            recommended_age = int(self._recommended_age_entry.get())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy wiek!")
            return
        try:
            doses = int(self._doses_entry.get())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowa ilość dawek w opakowaniu!")
            return
        try:
            doses_left = int(self._doses_left_entry.get())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowa ilość pozostałych dawek!")
            return
        try:
            expiration_date = datetime.strptime(self._expiration_date_entry.get(), '%Y-%m-%d').date()
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy format daty!")
            return
        recipients = []
        for user_id, int_var in self._recipients_checkboxes_variables.items():
            if int_var.get():
                recipients.append(user_id)

        try:
            self._system.change_medicine(medicine_id=self._medicine.id(),
                                         name=name,
                                         manufacturer=manufacturer,
                                         illnesses=illnesses,
                                         substances=substances,
                                         recommended_age=recommended_age,
                                         doses=doses,
                                         doses_left=doses_left,
                                         expiration_date=expiration_date,
                                         recipients=recipients)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        messagebox.showinfo(title='Informacja', message='Zmiany zostały zapisane!')
        self._gui.update_view('medicine-list-view', self._medicine.id())
