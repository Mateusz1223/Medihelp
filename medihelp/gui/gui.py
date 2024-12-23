import customtkinter as ctk
from .menu_bar import MenuBar
from .medicine_list_view import MedicineListView
from . import global_settings as gs
from medihelp.errors import WrongArgumentsError, ViewDoesNotExist


class GUI(ctk.CTk):
    '''
    Responsible for providing a way of communication with the user. Comunicates with System object via _system handler.
    Inherites from tkinter.Tk so it is a window of the application.

    Attributes
    ----------
    :ivar _system: hander to system
    :vartype _system: System

    :ivar _menu_bar: object representing menu bar at the top of the screen
    :vartype _menu_bar: MenuBar

    :ivar _views: List of views of the app
    :vartype _views: list[View]

    :ivar _current_user_id: ID of the user currently using the Gui
    :vartype _current_user_id: int
    '''

    def __init__(self, system_handler):
        super().__init__()
        self._system = system_handler

        # It doesn't work on all systems unfortunatelly
        self.minsize(width=gs.min_width, height=300)

        self.geometry(f'{gs.resolution['x']}x{gs.resolution['y']}')
        self.title('Medihelp')

        self._current_user_id = None

        # Temporary TO DO
        self._current_user_id = 0
        self.title('Medihelp - Tata')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._menu_bar = MenuBar(self._system, self)
        self.config(menu=self._menu_bar)

        self._views = {
            'medicine-list-view': MedicineListView(self._system, self, self)
        }
        for view in self._views.values():
            view.grid(row=0, column=0, sticky="nsew")

        self.mainloop()

    def current_user_id(self):
        return self._current_user_id

    def update_view(self, view: str, medicine_id: int = None):
        '''
        1) If medicine_id is not given then update the given view
        2) If both view and medicine_id are given then view must be set to medicine-list-view
           this will update only the medicine tile that is responsible for displaying info about the medicine with specific id

        :param view: name of the view
        :type view: str

        :param medicine_id: ID of the medicine whose tile is to be updated
        :type medicine_id: int
        '''

        if medicine_id and view != 'medicine-list-view':
            raise WrongArgumentsError

        view = self._views.get(view)
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
            view.grid(row=0, column=0, sticky="nsew")
