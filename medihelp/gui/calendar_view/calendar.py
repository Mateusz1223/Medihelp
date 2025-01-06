import customtkinter as ctk
from medihelp.system import System
from medihelp.prescription import Prescription
from medihelp.gui import global_settings as gs
from medihelp.gui.gui import GUI
from .calendar_tile import CalendarTile
from typing import Iterable
from medihelp.user import User


class Calendar(ctk.CTkFrame):
    '''
    Class Calendar represent calendar with users's prescriptions.
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
        super().__init__(parent)

        self._system = system_handler
        self._gui = gui_handler

        # One column for each day of the week
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)
        self.columnconfigure(6, weight=1)
        self.columnconfigure(7, weight=1)

        # Weekdays labels
        weekdays_list = [
            None,
            'Pon.',
            'Wt.',
            'Śr.',
            'Czw.',
            'Pi.',
            'Sob.',
            'Nie.'
        ]
        self._weekday_labels = [None, None, None, None, None, None, None, None]
        for weekday in range(1, 8):
            self._weekday_labels[weekday] = ctk.CTkLabel(self, text=weekdays_list[weekday], fg_color='grey',
                                                         corner_radius=5, font=(gs.font_name, 12, 'bold'))
            self._weekday_labels[weekday].grid(row=0, column=weekday, padx=2, pady=2, sticky='we')

        # Free row counter for each column
        #   (weekdays are indexed from 1 so ther is one additional value in the list)
        self._free_row = [1, 1, 1, 1, 1, 1, 1, 1]
        # Calendar tiles lists for each column
        #   (weekdays are indexed from 1 so ther is one additional value in the list)
        self._calendar_tiles = [[], [], [], [], [], [], [], []]

    def clear_calendar(self):
        for row in range(1, 8):
            for tile in self._calendar_tiles[row]:
                tile.destroy()
            self._calendar_tiles[row].clear()
        self._free_row = [1, 1, 1, 1, 1, 1, 1, 1]

    def load_prescriptions(self, users_list: Iterable[User]):
        '''
        Creates and displays calendar tiles based of users' prescriptions
        1) When ther is only one user in the users_list create calendar tiles without user names
        2) Otherwise creates calendar tiles with user names

        :param users_list: List of users whose prescriptions are to be displayed
        :type users_list: iterable of User
        '''
        for user in users_list:
            for prescription in user.prescriptions().values():
                if len(users_list) == 1:
                    tile = CalendarTile(self._system, self._gui, self,
                                        color=gs.lime__color, prescription=prescription)
                else:
                    tile = CalendarTile(self._system, self._gui, self,
                                        color=gs.lime__color, prescription=prescription,
                                        user_name=user.name())
                self._calendar_tiles[tile.weekday()].append(tile)
                tile.grid(row=self._free_row[tile.weekday()], column=tile.weekday(), sticky='we')
                self._free_row[tile.weekday()] += 1
