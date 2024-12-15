import tkinter as tk
from .global_settings import font_name
from .medicine_tile import MedicineTile
from .view import View
from medihelp.medicine import Medicine
from datetime import date


class MedicineListView(View):
    '''
    View that shows informations about all the medicines stored in a database
    '''
    def __init__(self, system_handler, parent):
        super().__init__(system_handler, parent)

        self.columnconfigure(0, weight=1)

        self._label = tk.Label(self, text="Lista leków", font=(font_name, 20))
        self._label.grid(row=0, column=0, padx=30, pady=30, sticky=tk.W)
        self._medicine_tiles = []

        self.update_view()

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        users_id_to_name_dict = {
            0: 'Tata',
            1: 'Mama',
            2: 'Dziecko'
        }
        illneses = ['przeziębienie', 'ból głowy', 'zatrucie pokarmowe']
        substances = ['węgiel aktywny', 'polopiryna']
        date_instance = date(2025, 12, 31)
        medicine = Medicine(0, name='Ivermectin', manufacturer='Polfarma',
                            illnesses=illneses, substances=substances,
                            recommended_age=18, doses=10, doses_left=6, expiration_date=date_instance, recipients=[0, 1, 2])
        self._medicine_tiles.append(MedicineTile(self, medicine, users_id_to_name_dict))
        self._medicine_tiles[0].grid(row=1, column=0, padx=20, pady=10, sticky=tk.W + tk.E)

        self._medicine_tiles.append(MedicineTile(self, medicine, users_id_to_name_dict))
        self._medicine_tiles[1].grid(row=2, column=0, padx=20, pady=10, sticky=tk.W + tk.E)

        for tile in self._medicine_tiles:
            tile.destroy()
        self._medicine_tiles.clear()

        self._list_of_medicines = self._system.get_medicines_list()

        index = 0
        for medicine in self._list_of_medicines:
            self._medicine_tiles.append(MedicineTile(self, medicine, users_id_to_name_dict))
            self._medicine_tiles[index].grid(row=index+1, column=0, padx=20, pady=10, sticky=tk.W + tk.E)
            index += 1
