import customtkinter as ctk
from medihelp.system import System
from .prescription_form import PrescriptionForm
from .gui import GUI
from . import global_settings as gs
from .common import normalize_name
from tkinter import messagebox
from medihelp.errors import IllegalCharactersInANameError, DataLoadingError


class AddPrescriptionTile(ctk.CTkFrame):
    '''
    AddPrescriptionTile class represents a tile with an interface
        to add new prescription to the user.
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc
        '''
        super().__init__(parent, border_width=1)

        self._system = system_handler
        self._gui = gui_handler

        self.columnconfigure(0, weight=1)

        self.padx = 20
        self.pady = 5

        self._add_prescription_button = ctk.CTkButton(self, text='Dodaj receptę +',
                                                      fg_color=gs.action_color,
                                                      font=(gs.font_name, 10),
                                                      command=self._add_prescription_button_handler)
        self._add_prescription_button.grid(row=0, column=0, pady=10, padx=self.padx, sticky='w')

        self._form_frame = ctk.CTkFrame(self, fg_color=parent.cget('fg_color'))
        self._form_frame.columnconfigure(0, weight=1)

        self._form = PrescriptionForm(self._system, self._gui, self._form_frame)
        self._form.clear_form()
        self._form.grid(row=0, column=0, pady=self.pady, sticky='we')

        self._button_frame = ctk.CTkFrame(self._form_frame, fg_color=parent.cget('fg_color'))
        self._button_frame.columnconfigure(0, weight=1)
        self._button_frame.columnconfigure(1, weight=1)
        self._button_frame.grid(row=1, column=0, pady=self.pady, sticky='we')

        self._approve_button = ctk.CTkButton(self._button_frame, text='Dodaj receptę',
                                             fg_color=gs.action_color,
                                             font=(gs.font_name, 10),
                                             command=self._approve_button_handler)
        self._approve_button.grid(row=0, column=0, pady=self.pady, sticky='w')

        self._cancel_button = ctk.CTkButton(self._button_frame, text='Anuluj',
                                            fg_color=gs.edit_color,
                                            font=(gs.font_name, 10),
                                            command=self._cancel_button_handler)
        self._cancel_button.grid(row=0, column=1, pady=self.pady, sticky='e')

    def _add_prescription_button_handler(self):
        '''
        Hides Add prescription button, and shows form
        '''
        self._add_prescription_button.grid_forget()
        self._form_frame.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='we')

    def _approve_button_handler(self):
        # Extract data from the form
        try:
            medicine_name = normalize_name(self._form.medicine_name())
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa lekarstwa: {e}")
            return
        try:
            dosage = int(self._form.dosage())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowe dawkowanie!")
            return
        weekday = self._form.weekday()

        # Commit changes
        try:
            self._system.add_prescription(user_id=self._gui.current_user_id(),
                                          medicine_name=medicine_name,
                                          dosage=dosage,
                                          weekday=weekday)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        try:
            self._system.save_users_data()
        except DataLoadingError as e:
            messagebox.showerror(title='Błąd', message=f'{e}')
            return
        messagebox.showinfo(title='Informacja', message='Recepta została dodana!')
        self._cancel_button_handler()
        self._gui.update_view(view_name='modify-user-view')
        self._gui.update_view('calendar-view')

    def _cancel_button_handler(self):
        '''
        Hides form, clears it and shows Add prescription button
        '''
        self._form_frame.grid_forget()
        self._form.clear_form()
        self._add_prescription_button.grid(row=0, column=0, pady=10, padx=self.padx, sticky='w')
