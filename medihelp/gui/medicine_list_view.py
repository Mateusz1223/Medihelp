import customtkinter as ctk
from . import global_settings as gs
from .medicine_tile import MedicineTile
from .view import View
from medihelp.errors import MedicineDoesNotExist


class MedicineListView(View):
    '''
    View that shows informations about all the medicines stored in a database
    '''
    def __init__(self, system_handler, gui_handler, parent):
        super().__init__(system_handler, gui_handler, parent)

        self._system = system_handler
        self._gui = gui_handler

        self.columnconfigure(0, weight=1)

        self._add_medicine_button = ctk.CTkButton(self, fg_color=gs.action_color, text='Dodaj lek +', font=(gs.font_name, 12))
        self._add_medicine_button.grid(row=0, column=0, padx=20, pady=30, sticky='w')
        self._medicine_tiles = {}

        self.update_view()

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        for tile in self._medicine_tiles.values():
            tile.destroy()
        self._medicine_tiles.clear()

        row = 0
        for medicine in self._system.medicines().values():
            self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
            self._medicine_tiles[medicine.id()].grid(row=row + 1, column=0, padx=20, pady=10, sticky='we')
            row += 1

    def update_tile(self, medicine_id):
        '''
        Updates tile responsible for displaying info about the medicine with specific id

        :param medicine_id: ID of the medicine whose tile is to be updated
        :type medicine_id: int
        '''
        medicine = self._system.medicines().get(medicine_id)
        if not medicine:
            raise MedicineDoesNotExist(medicine_id)
        try:
            tile = self._medicine_tiles.pop(medicine_id)
            row = tile.grid_info()['row']
            tile.destroy()
            self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
            self._medicine_tiles[medicine.id()].grid(row=row + 1, column=0, padx=20, pady=10, sticky='we')
        except Exception:
            raise MedicineDoesNotExist(medicine_id)
