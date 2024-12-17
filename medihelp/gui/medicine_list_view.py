import customtkinter as ctk
from .global_settings import font_name, action_color
from .medicine_tile import MedicineTile
from .view import View


class MedicineListView(View):
    '''
    View that shows informations about all the medicines stored in a database
    '''
    def __init__(self, system_handler, parent):
        super().__init__(system_handler, parent)

        self.columnconfigure(0, weight=1)

        self._add_medicine_button = ctk.CTkButton(self, fg_color=action_color, text='Dodaj lek +', font=(font_name, 12))
        self._add_medicine_button.grid(row=0, column=0, padx=20, pady=30, sticky='w')
        self._medicine_tiles = []

        self.update_view()

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        # temporary solution
        # TO DO
        users_id_to_name_dict = {
            0: 'Tata',
            1: 'Mama',
            2: 'Dziecko'
        }

        for tile in self._medicine_tiles:
            tile.destroy()
        self._medicine_tiles.clear()

        self._list_of_medicines = self._system.get_medicines_list()

        index = 0
        for medicine in self._list_of_medicines:
            self._medicine_tiles.append(MedicineTile(self, medicine, users_id_to_name_dict))
            self._medicine_tiles[index].grid(row=index + 1, column=0, padx=20, pady=10, sticky='we')
            index += 1
