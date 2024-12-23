from .medicine_tile import MedicineTile
from .add_medicine_tile import AddMedicineTile
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

        self._add_medicine_tile = AddMedicineTile(self._system, self._gui, self)
        self._add_medicine_tile.grid(row=0, column=0, padx=20, pady=10, sticky='we')

        self._medicine_tiles = {}

        self.update_view()

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        for tile in self._medicine_tiles.values():
            tile.destroy()
        self._medicine_tiles.clear()

        row = 1
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
        if not self._medicine_tiles.get(medicine_id):
            self._add_tile(medicine_id)
            return
        medicine = self._system.medicines().get(medicine_id)
        if not medicine:
            raise MedicineDoesNotExist(medicine_id)
        try:
            tile = self._medicine_tiles.pop(medicine_id)
            row = tile.grid_info()['row']
            tile.destroy()
            self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
            self._medicine_tiles[medicine.id()].grid(row=row, column=0, padx=20, pady=10, sticky='we')
        except Exception:
            raise MedicineDoesNotExist(medicine_id)

    def _add_tile(self, medicine_id):
        '''
        Adds tile responsible for displaying info about the medicine with specific id

        :param medicine_id: ID of the medicine whose tile is to be added to the list
        :type medicine_id: int
        '''
        medicine = self._system.medicines().get(medicine_id)
        if not medicine:
            raise MedicineDoesNotExist(medicine_id)
        # This part may be buggy !!! Watch out
        row = len(self._medicine_tiles.keys()) + 1
        self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
        self._medicine_tiles[medicine.id()].grid(row=row, column=0, padx=20, pady=10, sticky='we')
