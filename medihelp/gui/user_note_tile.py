import customtkinter as ctk
from .global_settings import font_name, action_color, edit_color


class UserNoteTile(ctk.CTkFrame):
    '''
    Class UserNoteTile responsible for displaying user note attached to a medicine.
    '''
    def __init__(self, parent, name: str, content: str, editable: bool = False):
        '''
        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc

        :param name: Name of the user.
        :type name: str

        :param content: The note itself
        :type content: str

        :param editable: Whether this tile should include edit button or not.
        :type editable: bool
        '''
        super().__init__(parent, border_width=1, fg_color=parent.cget("fg_color"))

        self._name_label = ctk.CTkLabel(self, justify='left', wraplength=600, text=name, font=(font_name, 12, "bold"))
        self._name_label.pack(padx=20, pady=2, anchor='w')
        self._content_label = ctk.CTkLabel(self, justify='left', wraplength=600, text=content, font=(font_name, 10))
        self._content_label.pack(padx=20, pady=4, anchor='w')

        if editable:
            self._buttons_frame = ctk.CTkFrame(self, fg_color=parent.cget("fg_color"))
            self._buttons_frame.columnconfigure(0, weight=1)
            self._buttons_frame.columnconfigure(1, weight=1)

            self._modify_button = ctk.CTkButton(self._buttons_frame, fg_color=action_color, text='Edytuj notatkę', font=(font_name, 10))
            self._modify_button.grid(row=0, column=0, sticky='w')

            self._delete_button = ctk.CTkButton(self._buttons_frame, fg_color=edit_color, text='Usuń notatkę', font=(font_name, 10))
            self._delete_button.grid(row=0, column=1, padx=10, sticky='w')

            self._buttons_frame.pack(padx=20, pady=10, anchor='w')
