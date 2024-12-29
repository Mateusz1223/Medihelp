import customtkinter as ctk
from medihelp.system import System
from .calendar import Calendar
from medihelp.errors import UserDoesNotExistError
from . import global_settings as gs
from .gui import GUI
from .view import View


class CalendarView(View):
    '''
    View that shows a weekly calendar of prescriptions.
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        super().__init__(system_handler, gui_handler, parent)

        self.padx = 5
        self.pady = 10

        self._welcome_frame = ctk.CTkFrame(self)
        self._welcome_frame.grid(row=0, column=0, sticky='we')
        self._welcome_label = ctk.CTkLabel(self._welcome_frame, text="Kalendarz", font=(gs.font_name, 30, 'bold'))
        self._welcome_label.grid(row=0, column=0, padx=self.padx, pady=20, sticky='w')

        # Choose user dropdown
        self._name_to_id_map = {}
        for user_id, user in self._system.users().items():
            self._name_to_id_map[user.name()] = user_id
        self._name_to_id_map['Wszyscy użytkownicy'] = None
        self._selected_name = ctk.StringVar(value='Wszyscy użytkownicy')
        self._choose_user_dropdown = ctk.CTkOptionMenu(self._welcome_frame, variable=self._selected_name,
                                                       values=list(self._name_to_id_map.keys()),
                                                       button_color=gs.action_color,
                                                       fg_color='grey',
                                                       font=(gs.font_name, 12),
                                                       dropdown_font=(gs.font_name, 12),
                                                       command=self._choose_user_dropdown_handler)
        self._choose_user_dropdown.grid(row=0, column=1, padx=self.padx + 10, pady=self.pady, sticky='w')

        self.columnconfigure(0, weight=1)
        self._calendar = Calendar(self._system, self._gui, self)
        self._calendar.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='we')

        self._setup_calendar()

    def _setup_calendar(self):
        '''
        Loads prescription tiles to the calendar based on user's choice
        '''
        self._calendar.clear_calendar()
        user_id = self._name_to_id_map[self._selected_name.get()]
        if user_id is None:
            self._calendar.load_prescriptions(self._system.users().values())
        else:
            user = self._system.users().get(user_id)
            if not user:
                # Should never happen
                raise UserDoesNotExistError(user_id)
            self._calendar.load_prescriptions([user])

    def update_view(self):
        super().update_view()

        # recreate _name_to_id_map
        self._name_to_id_map.clear()
        for user_id, user in self._system.users().items():
            self._name_to_id_map[user.name()] = user_id
        self._name_to_id_map['Wszyscy użytkownicy'] = None

        # Update choose user dropdown
        self._choose_user_dropdown.configure(values=list(self._name_to_id_map.keys()))
        user = self._system.users().get(self._gui.current_user_id())
        if not user:
            self._selected_name.set('Wszyscy użytkownicy')
        else:
            self._selected_name.set(user.name())

        self._setup_calendar()

    def _choose_user_dropdown_handler(self, choice):
        self._setup_calendar()
