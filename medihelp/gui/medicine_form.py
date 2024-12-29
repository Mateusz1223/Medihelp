import customtkinter as ctk
from . import global_settings as gs
from medihelp.medicine import Medicine
from .gui import GUI
from medihelp.system import System


class MedicineForm(ctk.CTkFrame):
    '''
    Class MedicineForm represents a form with inputs corresponding to Medicine class object attributes (except for notes)
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        :param medicine: Medicine object that is to be visualized
        :type medicine: Medicine
        '''
        super().__init__(parent, border_width=0, fg_color=parent.cget('fg_color'))

        self._system = system_handler
        self._gui = gui_handler

        self.padx = 20
        self.pady = 2

        self._name_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                        text='Nazwa leku: ', font=(gs.font_name, 10, 'bold'))
        self._name_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._name_entry = ctk.CTkEntry(self, width=gs.min_width / 2,
                                        font=(gs.font_name, 10), border_width=0.5)
        self._name_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._manufacturer_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                text='Producent', font=(gs.font_name, 10, 'bold'))
        self._manufacturer_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._manufacturer_entry = ctk.CTkEntry(self, width=gs.min_width / 2,
                                                font=(gs.font_name, 10), border_width=0.5)
        self._manufacturer_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._doses_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                         text='Ilość dawek w opakowaniu', font=(gs.font_name, 10, 'bold'))
        self._doses_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._doses_entry = ctk.CTkEntry(self, width=gs.min_width / 4, font=(gs.font_name, 10),
                                         border_width=0.5)
        self._doses_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._doses_left_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text='Ilość pozostałych dawek', font=(gs.font_name, 10, 'bold'))
        self._doses_left_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._doses_left_entry = ctk.CTkEntry(self, width=gs.min_width / 4,
                                              font=(gs.font_name, 10), border_width=0.5)
        self._doses_left_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._recommended_age_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                   text='Zalecany wiek', font=(gs.font_name, 10, 'bold'))
        self._recommended_age_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._recommended_age_entry = ctk.CTkEntry(self, width=gs.min_width / 4,
                                                   font=(gs.font_name, 10), border_width=0.5)
        self._recommended_age_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._expiration_date_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                                   text='Data ważności', font=(gs.font_name, 10, 'bold'))
        self._expiration_date_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._expiration_date_entry = ctk.CTkEntry(self, width=gs.min_width / 4, font=(gs.font_name, 10),
                                                   border_width=0.5, placeholder_text='RRRR-MM-DD')
        self._expiration_date_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._substances_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text='Substancje', font=(gs.font_name, 10, 'bold'))
        self._substances_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._substances_textbox = ctk.CTkTextbox(self, width=gs.min_width - 100, height=50,
                                                  font=(gs.font_name, 10), border_width=0.5)
        self._substances_textbox.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._illnesses_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                             text='Na choroby', font=(gs.font_name, 10, 'bold'))
        self._illnesses_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._illnesses_textbox = ctk.CTkTextbox(self, width=gs.min_width - 100, height=50,
                                                 font=(gs.font_name, 10), border_width=0.5)
        self._illnesses_textbox.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._recipients_label = ctk.CTkLabel(self, justify='left', wraplength=gs.min_width - 100,
                                              text='Zaznacz odbiorów leku:', font=(gs.font_name, 10, 'bold'))
        self._recipients_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        # Create a dictionary of checkboxes where user id is the key and chackbox is the value
        self._recipients_checkboxes_variables = {}
        self._recipients_checkboxes = {}
        for user_id, user in self._system.users().items():
            variable = ctk.IntVar(value=0)
            checkbox = ctk.CTkCheckBox(self, text=user.name(), variable=variable,
                                       onvalue=1, offvalue=0, font=(gs.font_name, 10),
                                       hover_color=gs.action_color, fg_color=gs.action_color)
            checkbox.pack(padx=self.padx, pady=self.pady, anchor='w')
            self._recipients_checkboxes[user_id] = checkbox
            self._recipients_checkboxes_variables[user_id] = variable

    def clear_form(self, medicine=None):
        '''
        1) When medicine is None just empties form
        2) Otherwise fills form with medicine data too
        '''
        self._name_entry.delete('0', ctk.END)
        self._manufacturer_entry.delete('0', ctk.END)
        self._doses_entry.delete('0', ctk.END)
        self._doses_left_entry.delete('0', ctk.END)
        self._recommended_age_entry.delete('0', ctk.END)
        self._expiration_date_entry.delete('0', ctk.END)
        self._substances_textbox.delete('0.0', ctk.END)
        self._substances_textbox.insert('0.0', 'Podaj nazwy substancji oddzielone przecinkiem.')
        self._illnesses_textbox.delete('0.0', ctk.END)
        self._illnesses_textbox.insert('0.0', 'Podaj nazwy chorób i dolegliwości oddzielone przecinkiem.')
        for int_var in self._recipients_checkboxes_variables.values():
            int_var.set(0)

        if medicine:
            self._name_entry.insert('0', medicine.name())
            self._manufacturer_entry.insert('0', medicine.manufacturer())
            self._doses_entry.insert('0', str(medicine.doses()))
            self._doses_left_entry.insert('0', str(medicine.doses_left()))
            self._recommended_age_entry.insert('0', str(medicine.recommended_age()))
            self._expiration_date_entry.insert('0', str(medicine.expiration_date()))

            substances_str = ', '.join(medicine.substances())
            self._substances_textbox.delete('0.0', ctk.END)
            self._substances_textbox.insert('0.0', substances_str)

            illnesses_str = ', '.join(medicine.illnesses())
            self._illnesses_textbox.delete('0.0', ctk.END)
            self._illnesses_textbox.insert('0.0', illnesses_str)

            for user_id in medicine.recipients():
                self._recipients_checkboxes_variables[user_id].set(1)

    def name(self):
        '''
        :return: Raw name string from the form
        :rtype: str
        '''
        return self._name_entry.get()

    def manufacturer(self):
        '''
        :return: Raw manufacturer string from the form
        :rtype: str
        '''
        return self._manufacturer_entry.get()

    def illnesses(self):
        '''
        :return: Raw illnesses string from the form
        :rtype: str
        '''
        illnesses = self._illnesses_textbox.get("1.0", "end")
        if illnesses == 'Podaj nazwy chorób i dolegliwości oddzielone przecinkiem.\n':
            illnesses = ''
        return illnesses

    def substances(self):
        '''
        :return: Raw substances string from the form
        :rtype: str
        '''
        substances = self._substances_textbox.get("1.0", "end")
        if substances == 'Podaj nazwy substancji oddzielone przecinkiem.\n':
            substances = ''
        return substances

    def recommended_age(self):
        '''
        :return: Raw recommended_age string from the form
        :rtype: str
        '''
        return self._recommended_age_entry.get()

    def doses(self):
        '''
        :return: Raw doses string from the form
        :rtype: str
        '''
        return self._doses_entry.get()

    def doses_left(self):
        '''
        :return: Raw doses_left string from the form
        :rtype: str
        '''
        return self._doses_left_entry.get()

    def expiration_date(self):
        '''
        :return: Raw expiration_date string from the form
        :rtype: str
        '''
        return self._expiration_date_entry.get()

    def recipients(self):
        '''
        :return: Recipient list from the form (list of user IDs)
        :rtype: list[int]
        '''
        recipients = []
        for user_id, int_var in self._recipients_checkboxes_variables.items():
            if int_var.get():
                recipients.append(user_id)

        return recipients
