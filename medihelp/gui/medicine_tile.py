import customtkinter as ctk
from .global_settings import font_name, action_color, edit_color, neutral_color, min_width
from medihelp.medicine import Medicine
from .user_note_tile import UserNoteTile


def set_of_strings_to_string(set_of_strings):
    result = ''
    for s in set_of_strings:
        result += s + ', '
    return result[:-2]


class MedicineTile(ctk.CTkFrame):
    '''
    Class MedicineTile responsible for displaying informations contained in medicine object
    '''

    def __init__(self, system_handler, gui_handler, parent, medicine: Medicine):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param medicine: Medicine object that is to be visualized
        :type medicine: Medicine

        :param users_id_to_name_dict: A dictionary that maps user IDs (integers) to user names (strings).
        :type users_id_to_name_dict: dict[int, str]
        '''

        super().__init__(parent, border_width=1)

        self._system = system_handler
        # Used for determining wheather users' notes are currently being shown or not
        self._gui = gui_handler

        self._medicine = medicine

        self._show_notes = False

        self.padx = 20
        self.pady = 2

        self._name_and_manufacturer_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'{self._medicine.name()} (productent: {self._medicine.manufacturer()})', font=(font_name, 14, "bold"))
        self._name_and_manufacturer_label.pack(padx=self.padx, pady=self.pady + 10, anchor='w')

        self._doses_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'(Pozostałe dawki: {self._medicine.doses_left()} na {self._medicine.doses()})', font=(font_name, 10))
        self._doses_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._for_ilnesses_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'Na następujące choroby: {set_of_strings_to_string(self._medicine.illnesses())}', font=(font_name, 10))
        self._for_ilnesses_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        # TO DO: Dynamic wraplength adjustment
        self._substances_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'Substancje czynne: {set_of_strings_to_string(self._medicine.substances())}', font=(font_name, 10))
        self._substances_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._reccomended_age_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'Zalecany wiek: {self._medicine.recommended_age()}', font=(font_name, 10, "bold"))
        self._reccomended_age_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._expiration_date_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'Data ważności: {self._medicine.expiration_date()}', font=(font_name, 10, "bold"))
        self._expiration_date_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        recipients = set()
        for id in self._medicine.recipients():
            user = self._system.users().get(id)
            if user:
                name = user.name()
            else:
                name = "Nieznany użytkownik"
            recipients.add(name)
        self._recipients_label = ctk.CTkLabel(self, justify='left', wraplength=min_width - 100, text=f'Użytkownicy przyjmujący lek: {set_of_strings_to_string(recipients)}', font=(font_name, 10))
        self._recipients_label.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._buton_frame = ctk.CTkFrame(self, fg_color=parent.cget("fg_color"))
        self._buton_frame.columnconfigure(0, weight=1)
        self._buton_frame.columnconfigure(1, weight=1)
        self._buton_frame.columnconfigure(2, weight=1)
        self._take_dose_button = ctk.CTkButton(self._buton_frame, fg_color=action_color, text='Weź dawkę', font=(font_name, 10))
        self._take_dose_button.grid(row=0, column=0, sticky='w')
        self._show_notes_button = ctk.CTkButton(self._buton_frame, fg_color=neutral_color, text='↓ Pokaż notatki użytkowników ↓', font=(font_name, 10), command=self._show_notes_button_handler)
        self._show_notes_button.grid(row=0, column=1, sticky='w' + 'e')
        self._edit_button = ctk.CTkButton(self._buton_frame, fg_color=edit_color, text='Edytuj', font=(font_name, 10))
        self._edit_button.grid(row=0, column=2, sticky='e')
        self._buton_frame.pack(padx=self.padx, pady=self.pady + 10, anchor='w', fill='x')

        # Load users' notes
        self._notes_frame = self._buton_frame = ctk.CTkFrame(self, fg_color=parent.cget("fg_color"))
        self._notes_frame.columnconfigure(0, weight=1)
        self._user_notes_tiles = []
        create_add_note_button = True
        for author_id, content in self._medicine.notes().items():
            if content:
                self._user_notes_tiles.append(UserNoteTile(self._system,
                                                           self._gui,
                                                           self._notes_frame,
                                                           self._medicine.id(),
                                                           author_id,
                                                           content,
                                                           editable=(True if self._gui.current_user_id == author_id else False)))
                if self._gui.current_user_id == author_id:
                    create_add_note_button = False
        if create_add_note_button:
            # Create add_note_button if there is no note belonging to the current user already
            self._add_note_button = ctk.CTkButton(self._notes_frame, fg_color=action_color, text='Dodaj notatkę +', font=(font_name, 10))
            self._add_note_button.grid(row=0, column=0, padx=0, pady=self.pady + 5, sticky='w')

        row_counter = 1
        for note_tile in self._user_notes_tiles:
            note_tile.grid(row=row_counter, column=0, padx=0, pady=self.pady, sticky='we')
            row_counter += 1

    def _show_notes_button_handler(self):
        if not self._show_notes:
            self._show_notes = True
            self._show_notes_button.configure(text='↑ Schowaj notatki użytkowników ↑')
            self._notes_frame.pack(padx=self.padx, pady=self.pady + 10, anchor='w', fill='x')
        else:
            self._show_notes = False
            self._show_notes_button.configure(text='↓ Pokaż notatki użytkowników ↓')
            self._notes_frame.pack_forget()
