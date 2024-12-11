import tkinter as tk
from .global_settings import font_name


class MedicineListView(tk.Frame):
    '''
    First frame showing when application is open. Allow to log in as a certain user.
    '''
    def __init__(self, parent):
        super().__init__(parent)

        self._label = tk.Label(self, text="Lista leków", font=(font_name, 30))
        self._label.pack(padx=0, pady=40)
