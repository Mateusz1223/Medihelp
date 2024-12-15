import tkinter as tk
from .menu_bar import MenuBar
from .medicine_list_view import MedicineListView
from .global_settings import resolution


class GUI(tk.Tk):
    '''
    Responsible for providing a way of communication with the user. Comunicates with System object via _system handler.
    Inherites from tkinter.Tk so it is a window of the application.

    Attributes
    ----------
    :ivar _system: hander to system
    :vartype _system: System

    :ivar medicine_list_view: Main view that displays informations about all medicines in a database
    :vartype medicine_list_view: MedicineListView
    '''

    def __init__(self, system_handler):
        super().__init__()
        self._system = system_handler

        self.title('Medihelp')
        self.geometry(f'{resolution['x']}x{resolution['y']}')

        self._menu_bar = MenuBar(self._system, self)
        self.config(menu=self._menu_bar)

        self._views = {
            'medicine-list-view': MedicineListView(self._system, self)
        }
        for view in self._views.values():
            view.pack(fill='x')

        self.mainloop()

    def update_views(self):
        for view in self._views.values():
            view.update_view()
            view.pack(fill='x')
