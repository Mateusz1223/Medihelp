import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from medihelp.errors import IllegalCharactersInANameError
from medihelp.system import System
from .gui import GUI
from . import global_settings as gs
from .common import normalize_list_of_names, normalize_name


class AddMedicineTile(ctk.CTkFrame):
    '''
    Class AddMedicineTile responsible for providing an interface to add new medicine.
    '''

    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: gui object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc
        '''

        super().__init__(parent, border_width=1)

        self._system = system_handler
        self._gui = gui_handler

        self.padx = 20
        self.pady = 2

        self._form_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        self._setup_form()

        self._add_medicine_button = ctk.CTkButton(self, fg_color=gs.action_color, text='Dodaj lek +',
                                                  font=(gs.font_name, 12), command=self._add_medicine_button_handler)
        self._add_medicine_button.pack(padx=self.padx, pady=30, anchor='w')

    def _setup_form(self):
        self._name_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                        text='Nazwa leku: ', font=(gs.font_name, 10, 'bold'))
        self._name_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._name_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 2,
                                        font=(gs.font_name, 10), border_width=0.5)
        self._name_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._manufacturer_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                                text='Producent', font=(gs.font_name, 10, 'bold'))
        self._manufacturer_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._manufacturer_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 2,
                                                font=(gs.font_name, 10), border_width=0.5)
        self._manufacturer_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._doses_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                         text='Ilość dawek w opakowaniu', font=(gs.font_name, 10, 'bold'))
        self._doses_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._doses_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 4, font=(gs.font_name, 10), border_width=0.5)
        self._doses_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._doses_left_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                              text='Ilość pozostałych dawek', font=(gs.font_name, 10, 'bold'))
        self._doses_left_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._doses_left_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 4,
                                              font=(gs.font_name, 10), border_width=0.5)
        self._doses_left_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._recommended_age_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                                   text='Zalecany wiek', font=(gs.font_name, 10, 'bold'))
        self._recommended_age_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._recommended_age_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 4,
                                                   font=(gs.font_name, 10), border_width=0.5)
        self._recommended_age_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._expiration_date_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                                   text='Data ważności', font=(gs.font_name, 10, 'bold'))
        self._expiration_date_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._expiration_date_entry = ctk.CTkEntry(self._form_frame, width=gs.min_width / 4, font=(gs.font_name, 10),
                                                   border_width=0.5, placeholder_text='RRRR-MM-DD')
        self._expiration_date_entry.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._substances_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                              text='Substancje', font=(gs.font_name, 10, 'bold'))
        self._substances_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._substances_textbox = ctk.CTkTextbox(self._form_frame, width=gs.min_width - 100, height=50,
                                                  font=(gs.font_name, 10), border_width=0.5)
        self._substances_textbox.insert('0.0', 'Podaj nazwy substancji oddzielone przecinkiem.')
        self._substances_textbox.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._illnesses_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                             text='Na choroby', font=(gs.font_name, 10, 'bold'))
        self._illnesses_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        self._illnesses_textbox = ctk.CTkTextbox(self._form_frame, width=gs.min_width - 100, height=50,
                                                 font=(gs.font_name, 10), border_width=0.5)
        self._illnesses_textbox.insert('0.0', 'Podaj nazwy chorób i dolegliwości oddzielone przecinkiem.')
        self._illnesses_textbox.pack(padx=self.padx, pady=self.pady, anchor='w')

        self._recipients_label = ctk.CTkLabel(self._form_frame, justify='left', wraplength=gs.min_width - 100,
                                              text='Zaznacz odbiorów leku:', font=(gs.font_name, 10, 'bold'))
        self._recipients_label.pack(padx=self.padx, pady=self.pady, anchor='w')
        # Create a dictionary of checkboxes where user id is the key and chackbox is the value
        self._recipients_checkboxes_variables = {}
        self._recipients_checkboxes = {}
        for user_id, user in self._system.users().items():
            variable = ctk.IntVar(value=0)
            checkbox = ctk.CTkCheckBox(self._form_frame, text=user.name(), variable=variable,
                                       onvalue=1, offvalue=0, font=(gs.font_name, 10),
                                       hover_color=gs.action_color, fg_color=gs.action_color)
            checkbox.pack(padx=self.padx, pady=self.pady, anchor='w')
            self._recipients_checkboxes[user_id] = checkbox
            self._recipients_checkboxes_variables[user_id] = variable

        self._buton_frame = ctk.CTkFrame(self._form_frame, fg_color=self.cget("fg_color"))
        self._buton_frame.pack(padx=self.padx, pady=self.pady + 10, anchor='w', fill='x')

        self._approve_button = ctk.CTkButton(self._buton_frame, fg_color=gs.action_color,
                                             text='Zatwierdź', font=(gs.font_name, 10),
                                             command=self._approve_button_handler)
        self._approve_button.grid(row=0, column=0, sticky='w')
        self._cancel_button = ctk.CTkButton(self._buton_frame, fg_color=gs.edit_color,
                                            text='Anuluj', font=(gs.font_name, 10),
                                            command=self._cancel_button_handler)
        self._cancel_button.grid(row=0, column=1, padx=10, sticky='w')

    def _clear_form(self):
        self._name_entry.delete(0, "end")
        self._manufacturer_entry.delete(0, "end")
        self._doses_entry.delete(0, "end")
        self._doses_left_entry.delete(0, "end")
        self._recommended_age_entry.delete(0, "end")
        self._expiration_date_entry.delete(0, "end")
        self._substances_textbox.delete(1.0, 'end')
        self._substances_textbox.insert('0.0', 'Podaj nazwy substancji oddzielone przecinkiem.')
        self._illnesses_textbox.delete(1.0, 'end')
        self._illnesses_textbox.insert('0.0', 'Podaj nazwy chorób i dolegliwości oddzielone przecinkiem.')

        for int_var in self._recipients_checkboxes_variables.values():
            int_var.set(0)

    def _add_medicine_button_handler(self):
        self._add_medicine_button.pack_forget()
        self._clear_form()
        self._form_frame.pack(padx=1.5, pady=1.5, anchor='w', fill='x')

    def _approve_button_handler(self):
        '''
        Creates new medicine object in the database based on the data from the form
        '''
        # Extract data from the form
        name = self._name_entry.get()
        try:
            name = normalize_name(name)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa lekarstwa: {e}")
            return
        manufacturer = self._manufacturer_entry.get()
        try:
            manufacturer = normalize_name(manufacturer)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowa nazwa producenta: {e}")
            return
        illnesses = self._illnesses_textbox.get("1.0", "end").split(',')
        try:
            illnesses = normalize_list_of_names(illnesses)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy chorób: {e}")
            return
        substances = self._substances_textbox.get("1.0", "end").split(',')
        try:
            substances = normalize_list_of_names(substances)
        except IllegalCharactersInANameError as e:
            messagebox.showerror(title="Błąd", message=f"Nieprawidłowe nazwy substancji: {e}")
            return
        try:
            recommended_age = int(self._recommended_age_entry.get())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy wiek!")
            return
        try:
            doses = int(self._doses_entry.get())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowa ilość dawek w opakowaniu!")
            return
        try:
            doses_left = int(self._doses_left_entry.get())
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowa ilość pozostałych dawek!")
            return
        try:
            expiration_date = datetime.strptime(self._expiration_date_entry.get(), '%Y-%m-%d').date()
        except Exception:
            messagebox.showerror(title="Błąd", message="Nieprawidłowy format daty!")
            return
        recipients = []
        for user_id, int_var in self._recipients_checkboxes_variables.items():
            if int_var.get():
                recipients.append(user_id)

        # Add medicine to the database
        try:
            medicine_id = self._system.add_medicine(name=name,
                                                    manufacturer=manufacturer,
                                                    illnesses=illnesses,
                                                    substances=substances,
                                                    recommended_age=recommended_age,
                                                    doses=doses,
                                                    doses_left=doses_left,
                                                    expiration_date=expiration_date,
                                                    recipients=recipients)
        except Exception as e:
            messagebox.showerror(title="Błąd", message=f"{e}")
            return

        messagebox.showinfo(title='Informacja', message='Lek został dodany do bazy danych!')
        self._form_frame.pack_forget()
        self._add_medicine_button.pack(padx=self.padx, pady=30, anchor='w')
        self._gui.update_view('medicine-list-view', medicine_id)

    def _cancel_button_handler(self):
        self._form_frame.pack_forget()
        self._add_medicine_button.pack(padx=self.padx, pady=30, anchor='w')
