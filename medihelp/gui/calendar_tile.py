import customtkinter as ctk
from medihelp.system import System
from medihelp.prescription import Prescription
from . import global_settings as gs
from .gui import GUI


class CalendarTile(ctk.CTkFrame):
    '''
    Class CalendarTile represents a tile responsible for displaying single prescription.
    Used in the calendar.

    :ivar weekday: Prescription's weekday (Number from 1 to 7)
    :vartype weekday: int
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent,
                 color: str, prescription: Prescription, user_name: str = None):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param color: color of the tile
        :type color: str

        :param prescription: prescription object to be visualized
        :type prescription: Prescription

        :param user_name: Name of the user if it is to be shown (optional)
        :type user_name: str
        '''
        super().__init__(parent, border_width=1, fg_color=color)

        self._system = system_handler
        self._gui = gui_handler

        self.padx = 2
        self.pady = 5

        self._weekday = prescription.weekday()

        if user_name:
            self._user_name_label = ctk.CTkLabel(self, text=user_name, justify='left',
                                                 font=(gs.font_name, 12, 'bold'))
            self._user_name_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._medicine_name_label = ctk.CTkLabel(self, justify='left',
                                                 text=f'Lek:\n{prescription.medicine_name()}',
                                                 font=(gs.font_name, 12))
        self._medicine_name_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._dosage_label = ctk.CTkLabel(self, text=f'Dawkowanie: {prescription.dosage()}',
                                          justify='left', font=(gs.font_name, 12))
        self._dosage_label.pack(padx=self.padx, pady=self.pady, anchor='w')

    def weekday(self):
        return self._weekday