import customtkinter as ctk
from .global_settings import font_name


class UserNoteTile(ctk.CTkFrame):
    '''
    Class UserNoteTile responsible for displaying user note attached to a medicine.
    '''
    def __init__(self, parent, name: str, content: str):
        '''
        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc

        :param name: Name of the user.
        :type name: str

        :param content: The note itself
        :type content: str
        '''
        super().__init__(parent, border_width=1, fg_color=parent.cget("fg_color"))

        self._name_label = ctk.CTkLabel(self, justify='left', wraplength=600, text=name, font=(font_name, 12, "bold"))
        self._name_label.pack(padx=20, pady=2, anchor='w')
        self._content_label = ctk.CTkLabel(self, justify='left', wraplength=600, text=content, font=(font_name, 10))
        self._content_label.pack(padx=20, pady=4, anchor='w')
