import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from medihelp.errors import IllegalCharactersInANameError
from medihelp.system import System
from medihelp.gui.gui import GUI
from .medicine_form import MedicineForm
from medihelp.gui import global_settings as gs
from medihelp.gui.common import normalize_list_of_names, normalize_name


class AddMedicineTile(ctk.CTkFrame):
    '''
    Class AddMedicineTile represents a tile responsible for providing an interface to add new medicine.
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc
        '''
        super().__init__(parent, border_width=1)

        self._system = system_handler
        self._gui = gui_handler

        self.padx = 20
        self.pady = 2

        self.columnconfigure(0, weight=1)

        self._add_medicine_button = ctk.CTkButton(self, fg_color=gs.action_color, text='Dodaj lek +',
                                                  font=(gs.font_name, 12), command=self._add_medicine_button_handler)
        self._add_medicine_button.grid(row=0, column=0, padx=self.padx, pady=30, sticky='w')

        # Form and buttons
        self._form_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        self._form_frame.columnconfigure(0, weight=1)
        self._form = MedicineForm(self._system, self._gui, self._form_frame)
        self._form.grid(row=0, column=0, padx=self.padx, pady=self.pady + 10, sticky='we')

        self._buton_frame = ctk.CTkFrame(self._form_frame, fg_color=self.cget("fg_color"))
        self._buton_frame.grid(row=1, column=0, padx=self.padx, pady=self.pady + 10, sticky='we')

        self._approve_button = ctk.CTkButton(self._buton_frame, fg_color=gs.action_color,
                                             text='Zatwierdź', font=(gs.font_name, 10),
                                             command=self._approve_button_handler)
        self._approve_button.grid(row=0, column=0, sticky='w')
        self._cancel_button = ctk.CTkButton(self._buton_frame, fg_color=gs.edit_color,
                                            text='Anuluj', font=(gs.font_name, 10),
                                            command=self._cancel_button_handler)
        self._cancel_button.grid(row=0, column=1, padx=10, sticky='w')

    def _add_medicine_button_handler(self):
        self._add_medicine_button.grid_forget()
        self._form.clear_form()
        self._form_frame.grid(row=1, column=0, padx=1.5, pady=1.5, sticky='we')

    def _approve_button_handler(self):
        '''
        Creates new medicine object in the database based on the data from the form
        '''
        # Extract data from the form
        name = self._form.name()
        try:
            name = normalize_name(name)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa lekarstwa: {e}")
            return
        manufacturer = self._form.manufacturer()
        try:
            manufacturer = normalize_name(manufacturer)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa producenta: {e}")
            return
        illnesses = self._form.illnesses().split(',')
        try:
            illnesses = normalize_list_of_names(illnesses)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy chorób: {e}")
            return
        substances = self._form.substances().split(',')
        try:
            substances = normalize_list_of_names(substances)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy substancji: {e}")
            return
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

        # Add medicine to the database
        try:
            medicine_id = self._system.add_medicine(name=name,
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

        messagebox.showinfo(title='Informacja', message='Lek został dodany do bazy danych!')
        self._form_frame.grid_forget()
        self._add_medicine_button.grid(row=0, column=0, padx=self.padx, pady=30, sticky='w')
        self._gui.update_view('medicine-list-view', medicine_id)

    def _cancel_button_handler(self):
        self._form_frame.grid_forget()
        self._add_medicine_button.grid(row=0, column=0, padx=self.padx, pady=30, sticky='w')
