import customtkinter as ctk
from tkinter import messagebox
from medihelp.gui.gui import GUI
from medihelp.system import System
from medihelp.gui import global_settings as gs


class AddNoteTile(ctk.CTkFrame):
    '''
    Class AddNoteTile represent a tile responsible for providing an interface to add new note.

    :ivar _medicine_id: ID of the medicine the note is assigned to.
    :vartype _medicine_id: int
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent, medicine_id: int):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc

        :param medicine_id: ID of the medicine the note is assigned to.
        :type medicine_id: int
        '''
        super().__init__(parent, border_width=1, fg_color=parent.cget("fg_color"))

        self._system = system_handler
        self._gui = gui_handler

        self._medicine_id = medicine_id

        user = self._system.users().get(self._gui.current_user_id())
        if user:
            name = user.name()
        else:
            name = "Nieznany użytkownik"
        self._name_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100, text=name, font=(gs.font_name, 12, "bold"))
        self._name_label.pack(padx=20, pady=5, anchor='w')

        self._content_textbox = ctk.CTkTextbox(self, width=gs.min_width - 100, height=85, font=(gs.font_name, 10))
        self._content_textbox.pack(padx=20, pady=5, anchor='w')

        self._add_note_button = ctk.CTkButton(self, fg_color=gs.action_color,
                                              text='Dodaj notatkę', font=(gs.font_name, 10),
                                              command=self._add_note_button_handler)
        self._add_note_button.pack(padx=20, pady=10, anchor='w')

    def _add_note_button_handler(self):
        content = self._content_textbox.get("1.0", "end")
        content = content[:-1]  # delete new line character that is added by CTkTextbox itself
        try:
            self._system.set_note(self.medicine_id(), self._gui.current_user_id(), content)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        self._gui.update_view('medicine-list-view', self.medicine_id())

    def medicine_id(self):
        return self._medicine_id
