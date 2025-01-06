import customtkinter as ctk
from medihelp.system import System
from medihelp.prescription import Prescription
from .prescription_form import PrescriptionForm
from medihelp.gui.gui import GUI
from medihelp.gui import global_settings as gs
from medihelp.gui.common import normalize_name
from tkinter import messagebox
from medihelp.errors import IllegalCharactersInANameError


class PrescriptionTile(ctk.CTkFrame):
    '''
    PrescriptionTile class represents a tile responsble for displaying precription info
        and providing an interface to edit it.
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent, prescription: Prescription):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc

        :param prescription: prescription that is to be visualized by the tile
        :type prescription: prescription
        '''
        super().__init__(parent, border_width=1)

        self._system = system_handler
        self._gui = gui_handler

        self._prescription = prescription

        self.columnconfigure(0, weight=1)

        self.padx = 20
        self.pady = 5

        self._form = PrescriptionForm(self._system, self._gui, self)
        self._form.clear_form(prescription)
        self._form.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='we')

        self._button_frame = ctk.CTkFrame(self, fg_color=parent.cget('fg_color'))
        self._button_frame.columnconfigure(0, weight=1)
        self._button_frame.columnconfigure(1, weight=1)
        self._button_frame.columnconfigure(2, weight=1)
        self._button_frame.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='we')

        self._approve_button = ctk.CTkButton(self._button_frame, text='Zatwierdź',
                                             fg_color=gs.action_color,
                                             font=(gs.font_name, 10),
                                             command=self._approve_button_handler)
        self._approve_button.grid(row=0, column=0, pady=self.pady, sticky='w')

        self._discard_changes_button = ctk.CTkButton(self._button_frame, text='Odrzuć zmiany',
                                                     fg_color=gs.edit_color,
                                                     font=(gs.font_name, 10),
                                                     command=self._discard_changes_button_handler)
        self._discard_changes_button.grid(row=0, column=1, pady=self.pady)

        self._delete_button = ctk.CTkButton(self._button_frame, text='Usuń',
                                            fg_color=gs.edit_color,
                                            font=(gs.font_name, 10),
                                            command=self._delete_button_handler)
        self._delete_button.grid(row=0, column=2, pady=self.pady, sticky='e')

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
            self._system.change_prescription(user_id=self._gui.current_user_id(),
                                             prescription_id=self._prescription.id(),
                                             medicine_name=medicine_name,
                                             dosage=dosage,
                                             weekday=weekday)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        messagebox.showinfo(title='Informacja', message='Zmiany zostały zapisane!')
        self._gui.update_view(view_name='modify-user-view')
        self._gui.update_view('calendar-view')

    def _discard_changes_button_handler(self):
        self._form.clear_form(self._prescription)

    def _delete_button_handler(self):
        answer = messagebox.askyesno(title='Zatwierdź', message='Czy na pewno chcesz usunąć receptę?')
        if not answer:
            return
        self._system.del_prescription(user_id=self._gui.current_user_id(),
                                      prescription_id=self._prescription.id())
        messagebox.showinfo(title='Informacja', message='Recepta została usunieta!')
        self._gui.update_view('modify-user-view')
        self._gui.update_view('calendar-view')
