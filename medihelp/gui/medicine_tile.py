import tkinter as tk
from .global_settings import font_name
from medihelp.medicine import Medicine


def set_of_strings_to_string(set_of_strings):
    result = ''
    for s in set_of_strings:
        result += s + ', '
    return result[:-2]


class MedicineTile(tk.Frame):
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

        super().__init__(parent, bd=1, relief='solid')

        # Used for determining wheather users' notes are currently being shown or not
        self._show_notes = False

        padx = 20
        pady = 2

        self._name_label = tk.Label(self, text=medicine.name(), font=(font_name, 14, "bold underline"))
        self._name_label.pack(padx=padx, pady=pady+10, anchor='w')

        self._doses_label = tk.Label(self, text=f'(Pozostałe dawki: {medicine.doses_left()} na {medicine.doses()})', font=(font_name, 10))
        self._doses_label.pack(padx=padx, pady=pady, anchor='w')

        self._for_ilnesses_label = tk.Label(self, text=f'Na następujące choroby: {set_of_strings_to_string(medicine.illnesses())}', font=(font_name, 10))
        self._for_ilnesses_label.pack(padx=padx, pady=pady, anchor='w')

        self._substances_label = tk.Label(self, text=f'Substancje czynne: {set_of_strings_to_string(medicine.substances())}', font=(font_name, 10))
        self._substances_label.pack(padx=padx, pady=pady, anchor='w')

        self._reccomended_age_label = tk.Label(self, text=f'Zalecany wiek: {medicine.recommended_age()}', font=(font_name, 10))
        self._reccomended_age_label.pack(padx=padx, pady=pady, anchor='w')

        recipients = set()
        for id in medicine.recipients():
            recipients.add(users_id_to_name_dict.get(id, 'Nieznany użytkownik'))
        self._recipients_label = tk.Label(self, text=f'Użytkownicy przyjmujący lek: {set_of_strings_to_string(recipients)}', font=(font_name, 10))
        self._recipients_label.pack(padx=padx, pady=pady, anchor='w')

        self._buton_frame = tk.Frame(self)
        self._buton_frame.columnconfigure(0, weight=1)
        self._buton_frame.columnconfigure(1, weight=1)
        self._buton_frame.columnconfigure(2, weight=1)
        self._take_dose_button = tk.Button(self._buton_frame, bg='mediumseagreen', text='Weź dawkę', font=(font_name, 10))
        self._take_dose_button.grid(row=0, column=0, sticky=tk.W)
        self._show_notes_button = tk.Button(self._buton_frame, text='↓ Pokaż notatki użytkowników ↓', font=(font_name, 10))
        self._show_notes_button.grid(row=0, column=1, sticky=tk.W + tk.E)
        self._edit_button = tk.Button(self._buton_frame, bg='indianred', text='Edytuj', font=(font_name, 10))
        self._edit_button.grid(row=0, column=2, sticky=tk.E)
        self._buton_frame.pack(padx=padx, pady=pady + 10, anchor='w', fill='x')

    def _show_notes_button_handler():
        if not self._show_notes:
            self._show_notes = True
            # show notes
        else:
            self._show_notes = False
            # hide notes
