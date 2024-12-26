from .gui import GUI
from .view import View
from .modify_user_form import ModifyUserForm
from .prescription_tile import PrescriptionTile
from .add_prescription_tile import AddPrescriptionTile
from medihelp.system import System
import customtkinter as ctk
from . import global_settings as gs


class ModifyUserView(View):
    '''
    Class ModifyUserView responsible for displaying user info and providing an interface to edit it.
    '''

    def __init__(self, system_handler: System, gui_handler: GUI, parent):
        super().__init__(system_handler, gui_handler, parent)

        self._system = system_handler
        self._gui = gui_handler
        self._parent = parent

        self.columnconfigure(0, weight=1)

        # indicates first empty row
        self._empty_row = 0

        self._user_label = ctk.CTkLabel(self, text='Użytkownik',
                                        font=(gs.font_name, 14, 'bold'))
        self._user_label.grid(row=self._empty_row, column=0, padx=20, pady=5, sticky='w')
        self._empty_row += 1

        # Form used to modify all user info except for perscriptions
        self._modify_user_form = ModifyUserForm(self._system, self._gui, self)
        self._modify_user_form.grid(row=self._empty_row, column=0, padx=20, pady=10, sticky='we')
        self._empty_row += 1

        self._prescriptions_label = ctk.CTkLabel(self, text='Przyjmowane leki',
                                                 font=(gs.font_name, 14, 'bold'))
        self._prescriptions_label.grid(row=self._empty_row, column=0, padx=20, pady=5, sticky='w')
        self._empty_row += 1

        # Add prescription tile
        self._add_prescription_tile = AddPrescriptionTile(self._system, self._gui, self)
        self._add_prescription_tile.grid(row=self._empty_row, column=0, padx=20, pady=10, sticky='we')
        self._empty_row += 1

        # Tiles responsble for displaying precriptions info and providing an interface to edit it
        self._prescription_tiles = []
        self.update_view()

    def update_view(self):
        super().update_view()
        self._modify_user_form.clear_form()

        # tiles
        for tile in self._prescription_tiles:
            tile.destroy()
        self._prescription_tiles.clear()
        user = self._system.users().get(self._gui.current_user_id())
        if not user:
            return
        for prescription in user.prescriptions().values():
            self._prescription_tiles.append(PrescriptionTile(self._system, self._gui, self, prescription))
        for tile in self._prescription_tiles:
            tile.grid(row=self._empty_row, column=0, padx=20, pady=10, sticky='we')
            self._empty_row += 1
