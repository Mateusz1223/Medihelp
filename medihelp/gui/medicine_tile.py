import customtkinter as ctk
from .global_settings import font_name
from medihelp.medicine import Medicine


def set_of_strings_to_string(set_of_strings):
    result = ''
    for s in set_of_strings:
        result += s + ', '
    return result[:-2]


class MedicineTile(ctk.CTkFrame):
    '''
    Class MedicineTile responsible for displaying informations contained in medicine object
    '''

    def __init__(self, parent, medicine: Medicine, users_id_to_name_dict: dict[int, str]):
        '''
        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param medicine: Medicine object that is to be visualized
        :type medicine: Medicine

        :param users_id_to_name_dict: A dictionary that maps user IDs (integers) to user names (strings).
        :type users_id_to_name_dict: dict[int, str]
        '''

        super().__init__(parent, border_width=1)

        # Used for determining wheather users' notes are currently being shown or not
        self._show_notes = False

        padx = 20
        pady = 2

        self._name_label = ctk.CTkLabel(self, justify='left', text=medicine.name(), font=(font_name, 14, "bold"))
        self._name_label.pack(padx=padx, pady=pady+10, anchor='w')

        self._doses_label = ctk.CTkLabel(self, justify='left', text=f'(Pozostałe dawki: {medicine.doses_left()} na {medicine.doses()})', font=(font_name, 10))
        self._doses_label.pack(padx=padx, pady=pady, anchor='w')

        self._for_ilnesses_label = ctk.CTkLabel(self, justify='left', text=f'Na następujące choroby: {set_of_strings_to_string(medicine.illnesses())}', font=(font_name, 10))
        self._for_ilnesses_label.pack(padx=padx, pady=pady, anchor='w')

        # TO DO: Dynamic wraplength adjustment
        self._substances_label = ctk.CTkLabel(self, justify='left', wraplength=600, text=f'Substancje czynne: {set_of_strings_to_string(medicine.substances())}', font=(font_name, 10))
        self._substances_label.pack(padx=padx, pady=pady, anchor='w')

        self._reccomended_age_label = ctk.CTkLabel(self, justify='left', text=f'Zalecany wiek: {medicine.recommended_age()}', font=(font_name, 10, "bold"))
        self._reccomended_age_label.pack(padx=padx, pady=pady, anchor='w')

        recipients = set()
        for id in medicine.recipients():
            recipients.add(users_id_to_name_dict.get(id, 'Nieznany użytkownik'))
        self._recipients_label = ctk.CTkLabel(self, justify='left', text=f'Użytkownicy przyjmujący lek: {set_of_strings_to_string(recipients)}', font=(font_name, 10))
        self._recipients_label.pack(padx=padx, pady=pady, anchor='w')

        self._buton_frame = ctk.CTkFrame(self)
        self._buton_frame.columnconfigure(0, weight=1)
        self._buton_frame.columnconfigure(1, weight=1)
        self._buton_frame.columnconfigure(2, weight=1)
        self._take_dose_button = ctk.CTkButton(self._buton_frame, fg_color='mediumseagreen', text='Weź dawkę', font=(font_name, 10))
        self._take_dose_button.grid(row=0, column=0, sticky='w')
        self._show_notes_button = ctk.CTkButton(self._buton_frame, fg_color='grey', text='↓ Pokaż notatki użytkowników ↓', font=(font_name, 10))
        self._show_notes_button.grid(row=0, column=1, sticky='w' + 'e')
        self._edit_button = ctk.CTkButton(self._buton_frame, fg_color='indianred', text='Edytuj', font=(font_name, 10))
        self._edit_button.grid(row=0, column=2, sticky='e')
        self._buton_frame.pack(padx=padx, pady=pady + 10, anchor='w', fill='x')

    def _show_notes_button_handler():
        if not self._show_notes:
            self._show_notes = True
            # show notes
            # TO DO
        else:
            self._show_notes = False
            # hide notes
            # TO DO
