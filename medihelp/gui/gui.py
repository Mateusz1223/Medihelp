import customtkinter as ctk
import tkinter as tk
from medihelp.system import System
from . import global_settings as gs
from medihelp.errors import WrongArgumentsError, ViewDoesNotExist, UserDoesNotExistError


class GUI(ctk.CTk):
    '''
    Responsible for providing a way of communication with the user.
    Manages views and current user.
    Inherites from customtkinter.CTk so it is a window of the application.

    Attributes
    ----------
    :ivar _current_view: Name of the currently active view
    :vartype _current_view: str

    :ivar _current_user_id: ID of the user currently using the Gui
    :vartype _current_user_id: int
    '''

    def __init__(self, system_handler: System):
        # Imports here in order to avoid circular import
        from .menu_bar import MenuBar
        from .medicine_list_view import MedicineListView
        from .choose_user_view import ChooseUserView
        from .modify_user_view import ModifyUserView
        from .calendar_view import CalendarView

        super().__init__()
        self._system = system_handler

        # It doesn't work on all systems unfortunatelly
        self.minsize(width=gs.min_width, height=300)

        self.geometry(f'{gs.resolution['x']}x{gs.resolution['y']}')
        self.title('Medihelp')

        self._current_user_id = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._menu_bar = MenuBar(self._system, self)

        self._views = {
            'choose-user-view': ChooseUserView(self._system, self, self),
            'medicine-list-view': MedicineListView(self._system, self, self),
            'modify-user-view': ModifyUserView(self._system, self, self),
            'calendar-view': CalendarView(self._system, self, self)
        }
        self.set_current_view('choose-user-view')

        # fiixing a library key binding issue on linux
        # For Linux scroll up
        self.bind_all("<Button-4>", lambda e: self._views[self._current_view].scroll_up(e))
        # For Linux scroll down
        self.bind_all("<Button-5>", lambda e: self._views[self._current_view].scroll_down(e))

        self.mainloop()

    def current_user_id(self):
        return self._current_user_id

    def set_current_view(self, view_name: str):
        '''
        Changes currently displayed view
        Possible choices for view_name:
        1) 'choose-user-view'
        2) 'medicine-list-view'
        3) 'modify-user-view'
        4) 'calendar-view'

        :param view_name: name of the view that is to be displayed
        :type view_name: str
        '''
        view = self._views.get(view_name)
        if not view:
            raise ViewDoesNotExist
        try:
            self._views[self._current_view].grid_forget()
        except Exception:
            pass
        self._current_view = view_name
        view.grid(row=0, column=0, sticky="nsew")

    def set_current_user_id(self, user_id: int):
        '''
        Changes current user id, updates views and changes window title
        '''
        user = self._system.users().get(user_id)
        if not user:
            raise UserDoesNotExistError(user_id)
        self._current_user_id = user.id()
        self.update_views()
        self.title(f'Medihelp - {user.name()}')

    def update_view(self, view_name: str, medicine_id: int = None):
        '''
        1) If medicine_id is not given then update the given view
        2) If both view and medicine_id are given then view must be set to medicine-list-view
           this will update only the medicine tile that is responsible for displaying info about the medicine with specific id

        Possible choices for view_name:
        1) 'choose-user-view'
        2) 'medicine-list-view'
        3) 'modify-user-view'
        4) 'calendar-view'

        :param view_name: name of the view
        :type view_name: str

        :param medicine_id: ID of the medicine whose tile is to be updated
        :type medicine_id: int
        '''
        if medicine_id and view_name != 'medicine-list-view':
            raise WrongArgumentsError
        view = self._views.get(view_name)
        if not view:
            raise ViewDoesNotExist
        if medicine_id is None:
            view.update_view()
        else:
            view.update_tile(medicine_id)

    def update_views(self):
        '''
        Updates all views
        '''
        for view in self._views.values():
            view.update_view()
        self._views[self._current_view].grid(row=0, column=0, sticky="nsew")

    def show_menubar(self):
        '''
        Shows menubar
        '''
        self.config(menu=self._menu_bar)

    def hide_menubar(self):
        '''
        Hides menubar
        '''
        self.config(menu=tk.Menu())
