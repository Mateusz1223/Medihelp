import tkinter as tk
from .menu_bar import MenuBar
from .medicine_list_view import MedicineListView


class GUI(tk.Tk):
    '''
    Responsible for providing a way of communication with the user. Comunicates with System object via _system handler.
    Inherites from tkinter.Tk so it is a window of the application.

    Attributes
    ----------
    :ivar _system: hander to system
    :vartype _system: System
    '''

    def __init__(self, system_handler):
        self._system = system_handler

        super().__init__()
        self.title("Medihelp")
        self.geometry("960x540")

        self._menu_bar = MenuBar(self, self._system)
        self.config(menu=self._menu_bar)

        self._medicine_list_view = MedicineListView(self)
        self._medicine_list_view.pack(fill='x')

        self.mainloop()
