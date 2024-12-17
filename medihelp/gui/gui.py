import customtkinter as ctk
from .menu_bar import MenuBar
from .medicine_list_view import MedicineListView
from .global_settings import resolution


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

    :ivar current_user_id: ID of the user currently using the Gui
    :vartype current_user_id: int
    '''

    def __init__(self, system_handler):
        super().__init__()
        self._system = system_handler

        self.geometry(f'{resolution['x']}x{resolution['y']}')
        self.title('Medihelp')

        self.current_user_id = None

        # Temporary TO DO
        self.current_user_id = 0
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

    def update_views(self):
        for view in self._views.values():
            view.update_view()
            view.grid(row=0, column=0, sticky="nsew")
