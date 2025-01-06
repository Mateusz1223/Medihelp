import customtkinter as ctk
from medihelp.system import System
from medihelp.prescription import Prescription
from medihelp.gui.gui import GUI
from medihelp.gui import global_settings as gs


class PrescriptionForm(ctk.CTkFrame):
    '''
    Class PrescriptionForm represents a form allowing user to input
        informations neccesary to create a Prescription object
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects.
        :type parent: tkinter.Misc
        '''
        super().__init__(parent, fg_color=parent.cget('fg_color'))

        self._system = system_handler
        self._gui = gui_handler

        self.pady = 5

        # create form widgets
        self._medicine_name_label = ctk.CTkLabel(self, text='Nazwa leku',
                                                 font=(gs.font_name, 10))
        self._medicine_name_label.pack(anchor='w')
        self._medicine_name_entry = ctk.CTkEntry(self, width=gs.min_width / 2,
                                                 font=(gs.font_name, 10), border_width=0.5)
        self._medicine_name_entry.pack(anchor='w', pady=self.pady)

        self._dosage_label = ctk.CTkLabel(self, text='Dawkowanie',
                                          font=(gs.font_name, 10))
        self._dosage_label.pack(anchor='w')
        self._dosage_entry = ctk.CTkEntry(self, width=gs.min_width / 2,
                                          font=(gs.font_name, 10), border_width=0.5)
        self._dosage_entry.pack(anchor='w', pady=self.pady)

        self._weekday_to_number = {
            'Poniedziałek': 1,
            'Wtorek': 2,
            'Środa': 3,
            'Czwartek': 4,
            'Piątek': 5,
            'Sobota': 6,
            'Niedziela': 7
        }
        self._number_to_weekday = {
            1: 'Poniedziałek',
            2: 'Wtorek',
            3: 'Środa',
            4: 'Czwartek',
            5: 'Piątek',
            6: 'Sobota',
            7: 'Niedziela'
        }
        self._selected_weekday = ctk.StringVar(value='Poniedziałek')
        self._choose_weekday_dropdown = ctk.CTkOptionMenu(self, variable=self._selected_weekday,
                                                          values=list(self._weekday_to_number.keys()),
                                                          button_color=gs.action_color,
                                                          fg_color='grey',
                                                          font=(gs.font_name, 10),
                                                          dropdown_font=(gs.font_name, 10))
        self._choose_weekday_dropdown.pack(anchor='w', pady=self.pady)

    def clear_form(self, prescription: Prescription = None):
        '''
        1) When prescription is None empties form
        2) Otherwise fills form with prescription data
        '''
        self._medicine_name_entry.delete('0', 'end')
        self._dosage_entry.delete('0', 'end')
        self._selected_weekday.set('Poniedziałek')

        if prescription:
            self._medicine_name_entry.insert('0', prescription.medicine_name())
            self._dosage_entry.insert('0', str(prescription.dosage()))
            weekday_str = self._number_to_weekday[prescription.weekday()]
            self._selected_weekday.set(weekday_str)

    def medicine_name(self):
        '''
        :return: Raw medicine name string from the form
        :rtype: str
        '''
        return self._medicine_name_entry.get()

    def dosage(self):
        '''
        :return: Raw dosage string from the form
        :rtype: str
        '''
        return self._dosage_entry.get()

    def weekday(self):
        '''
        :return: Raw weekday number from the form (number from 1 to 7)
        :rtype: int
        '''
        return self._weekday_to_number[self._selected_weekday.get()]
