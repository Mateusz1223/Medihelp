import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from medihelp.gui import global_settings as gs
from medihelp.medicine import Medicine
from medihelp.gui.gui import GUI
from .medicine_form import MedicineForm
from .user_note_tile import UserNoteTile
from .add_note_tile import AddNoteTile
from medihelp.gui.common import set_of_strings_to_string
from medihelp.errors import UserDoesNotExistError
from medihelp.system import System


class MedicineTile(ctk.CTkFrame):
    '''
    Class MedicineTile represent a tile responsible for displaying informations contained in medicine object
        and providing an interface to modify the medicine instance it is responsible for.
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
        self._edit_tile.clear_form(self._medicine)
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
        super().__init__(parent, border_width=0, fg_color=parent.cget('fg_color'))

        self._system = system_handler
        self._gui = gui_handler

        self._medicine = medicine

        self.padx = 20
        self.pady = 2

        self.columnconfigure(0, weight=1)

        # Form
        self._form = MedicineForm(self._system, self._gui, self)
        self._form.clear_form(self._medicine)
        self._form.grid(row=0, column=0, sticky='we')

        # Button
        self._approve_button = ctk.CTkButton(self, fg_color=gs.action_color,
                                             text='Zatwierdź', font=(gs.font_name, 10),
                                             command=self._approve_button_handler)
        self._approve_button.grid(row=1, column=0, padx=self.padx, pady=self.pady + 10, sticky='w')

    def clear_form(self, medicine=None):
        self._form.clear_form(medicine)

    def _approve_button_handler(self):
        '''
        Modifies medicine with the data from the form
        '''
        # Extract data from the form
        name = self._form.name()
        manufacturer = self._form.manufacturer()
        illnesses = self._form.illnesses().split(',')
        substances = self._form.substances().split(',')
        try:
            recommended_age = int(self._form.recommended_age())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy wiek!")
            return
        try:
            doses = int(self._form.doses())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowa ilość dawek w opakowaniu!")
            return
        try:
            doses_left = int(self._form.doses_left())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowa ilość pozostałych dawek!")
            return
        try:
            expiration_date = datetime.strptime(self._form.expiration_date(), '%Y-%m-%d').date()
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy format daty!")
            return
        recipients = self._form.recipients()

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
