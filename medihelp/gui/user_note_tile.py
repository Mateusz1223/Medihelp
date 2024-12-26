import customtkinter as ctk
from tkinter import messagebox
from . import global_settings as gs
from .gui import GUI
from medihelp.system import System


class UserNoteTile(ctk.CTkFrame):
    '''
    Class UserNoteTile responsible for displaying user note attached to a medicine
        and providing an interface to edit the note.

    :ivar _author_id: Id of the author
    :vartype _author_id: int

    :ivar _medicine_id: ID of the medicine the note is assigned to.
    :vartype _medicine_id: int

    :ivar _content: Content of the note.
    :vartype _content: str

    :param _editable: Whether this tile should be editable or not.
    :type _editable: bool
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent, medicine_id: int, author_id: int, content: str, editable: bool = False):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc

        :param author_id: ID of the author.
        :type author_id: int

        :param medicine_id: ID of the medicine the note is assigned to.
        :type medicine_id: int

        :param content: The note itself
        :type content: str

        :param editable: Whether this tile should be editable or not.
        :type editable: bool
        '''
        super().__init__(parent, border_width=1, fg_color=parent.cget("fg_color"))

        self._system = system_handler
        self._gui = gui_handler

        self._medicine_id = medicine_id
        self._author_id = author_id
        self._content = content
        self._editable = editable

        user = self._system.users().get(self._author_id)
        if user:
            name = user.name()
        else:
            name = "Nieznany użytkownik"
        # Always to be shown
        self._name_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100, text=name, font=(gs.font_name, 12, "bold"))

        # To be shown when NOT in edit mode
        self._content_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100, text=content, font=(gs.font_name, 10))

        if self._editable:
            # Always to be shown
            self._buttons_frame = ctk.CTkFrame(self, fg_color=parent.cget("fg_color"))
            self._buttons_frame.columnconfigure(0, weight=1)
            self._buttons_frame.columnconfigure(1, weight=1)

            # To be shown when NOT in edit mode
            self._modify_button = ctk.CTkButton(self._buttons_frame, fg_color=gs.action_color,
                                                text='Edytuj notatkę', font=(gs.font_name, 10),
                                                command=self._modify_button_handler)
            self._delete_button = ctk.CTkButton(self._buttons_frame, fg_color=gs.edit_color,
                                                text='Usuń notatkę', font=(gs.font_name, 10),
                                                command=self._delete_button_handler)

            # To be shown when in edit mode
            self._modify_content_textbox = ctk.CTkTextbox(self, width=gs.min_width - 100, height=85, font=(gs.font_name, 10))
            self._cancel_button = ctk.CTkButton(self._buttons_frame, fg_color=gs.edit_color,
                                                text='Anuluj', font=(gs.font_name, 10),
                                                command=self._cancel_button_handler)
            self._save_changes_button = ctk.CTkButton(self._buttons_frame, fg_color=gs.action_color,
                                                      text='Zapisz zmiany', font=(gs.font_name, 10),
                                                      command=self._save_changes_button_handler)

        self._show_non_edit_mode()

    def author_id(self):
        return self._author_id

    def medicine_id(self):
        return self._medicine_id

    def content(self):
        return self._content

    def editable(self):
        return self._editable

    def _modify_button_handler(self):
        self._hide_all()
        self._show_edit_mode()

    def _cancel_button_handler(self):
        self._hide_all()
        self._show_non_edit_mode()

    def _delete_button_handler(self):
        try:
            self._system.del_note(self.medicine_id(), self.author_id())
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        self._gui.update_view('medicine-list-view', self.medicine_id())

    def _save_changes_button_handler(self):
        content = self._modify_content_textbox.get("1.0", "end")
        content = content[:-1]  # delete new line character that is added by CTkTextbox itself
        try:
            self._system.set_note(self.medicine_id(), self.author_id(), content)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return
        self._content = content
        self._hide_all()
        self._show_non_edit_mode()

    def _hide_all(self):
        '''
        Hides everything
        '''
        self._name_label.pack_forget()
        self._content_label.pack_forget()
        self._modify_content_textbox.pack_forget()

        self._buttons_frame.pack_forget()
        self._cancel_button.grid_forget()
        self._modify_button.grid_forget()
        self._delete_button.grid_forget()
        self._save_changes_button.grid_forget()

    def _show_non_edit_mode(self):
        self._name_label.pack(padx=20, pady=2, anchor='w')
        self._content_label.configure(text=self._content)
        self._content_label.pack(padx=20, pady=4, anchor='w')
        if self._editable:
            self._modify_button.grid(row=0, column=0, sticky='w')
            self._buttons_frame.pack(padx=20, pady=10, anchor='w')
            self._delete_button.grid(row=0, column=1, padx=10, sticky='w')

    def _show_edit_mode(self):
        self._name_label.pack(padx=20, pady=2, anchor='w')

        self._modify_content_textbox.delete("1.0", "end")
        self._modify_content_textbox.insert('0.0', self._content)
        self._modify_content_textbox.pack(padx=20, pady=2, anchor='w')

        self._save_changes_button.grid(row=0, column=0, sticky='w')
        self._cancel_button.grid(row=0, column=1, padx=10, sticky='w')
        self._buttons_frame.pack(padx=20, pady=10, anchor='w')
