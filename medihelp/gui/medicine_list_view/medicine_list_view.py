from .medicine_tile import MedicineTile
from .add_medicine_tile import AddMedicineTile
from medihelp.gui.gui import GUI
from medihelp.gui.view import View
from medihelp.errors import MedicineDoesNotExistError
from medihelp.system import System


class MedicineListView(View):
    '''
    View that shows informations about all the medicines stored in a database.
    Allows user to add new medicines, edit existing medicines informations and add notes.
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
        super().__init__(system_handler, gui_handler, parent)

        self._system = system_handler
        self._gui = gui_handler

        self.columnconfigure(0, weight=1)

        self._add_medicine_tile = AddMedicineTile(self._system, self._gui, self)
        self._add_medicine_tile.grid(row=0, column=0, padx=20, pady=10, sticky='we')

        # _free_row attribute is important when adding new medicine tiles.
        #   It's not decremented when a tile is deleted.
        self._free_row = 1

        self._medicine_tiles = {}

        self.update_view()

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        super().update_view()

        for tile in self._medicine_tiles.values():
            tile.destroy()
        self._medicine_tiles.clear()

        # Expired medicines first
        for medicine in self._system.medicines().values():
            if not medicine.is_expired():
                continue
            self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
            self._medicine_tiles[medicine.id()].grid(row=self._free_row, column=0, padx=20, pady=10, sticky='we')
            self._free_row += 1
        # Not expired medicines
        for medicine in self._system.medicines().values():
            if medicine.is_expired():
                continue
            self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
            self._medicine_tiles[medicine.id()].grid(row=self._free_row, column=0, padx=20, pady=10, sticky='we')
            self._free_row += 1

    def update_tile(self, medicine_id):
        '''
        1) Updates tile responsible for the medicine with given ID if the tile already exists
        2) Adds new tile if there is no tile responsible for the medicine with given ID
        3) Deletes a tile if it exists and there is no medicine with the given ID in the database

        :param medicine_id: ID of the medicine whose tile is to be updated
        :type medicine_id: int
        '''
        medicine = self._system.medicines().get(medicine_id)
        try:
            tile = self._medicine_tiles.pop(medicine_id)
        except Exception:
            tile = None
        if not medicine and not tile:
            raise MedicineDoesNotExistError(medicine_id)
        elif not tile:
            self._add_tile(medicine_id)
        elif not medicine:
            tile.destroy()
        else:
            try:
                row = tile.grid_info()['row']
                tile.destroy()
                self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
                self._medicine_tiles[medicine.id()].grid(row=row, column=0, padx=20, pady=10, sticky='we')
            except Exception:
                raise MedicineDoesNotExistError(medicine_id)

    def _add_tile(self, medicine_id):
        '''
        Adds tile responsible for displaying info about the medicine with given id

        :param medicine_id: ID of the medicine whose tile is to be added to the list
        :type medicine_id: int
        '''
        medicine = self._system.medicines().get(medicine_id)
        if not medicine:
            raise MedicineDoesNotExistError(medicine_id)
        self._medicine_tiles[medicine.id()] = MedicineTile(self._system, self._gui, self, medicine)
        self._medicine_tiles[medicine.id()].grid(row=self._free_row, column=0, padx=20, pady=10, sticky='we')
        self._free_row += 1
