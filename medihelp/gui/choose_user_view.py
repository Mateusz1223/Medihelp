import customtkinter as ctk
from . import global_settings as gs
from .view import View


class ChooseUserView(View):
    def __init__(self, system_handler, gui_handler, parent, width=200, height=200, corner_radius=None, border_width=None, bg_color="transparent", fg_color=None, border_color=None, scrollbar_fg_color=None, scrollbar_button_color=None, scrollbar_button_hover_color=None, label_fg_color=None, label_text_color=None, label_text="", label_font=None, label_anchor="center", orientation="vertical"):
        super().__init__(system_handler, gui_handler, parent, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)

        # Make scrollbar transparent
        self.configure(scrollbar_button_color=self.cget("fg_color"))
        self.configure(scrollbar_button_hover_color=self.cget("fg_color"))

        self._welcome_label = ctk.CTkLabel(self, text="Witaj w Medihelp!", font=(gs.font_name, 30, 'bold'))
        self._welcome_label.pack(pady=80)

        self._name_to_id_map = {}
        names = []
        for user_id, user in self._system.users().items():
            names.append(user.name())
            self._name_to_id_map[user.name()] = user_id
        self._selected_name = ctk.StringVar(value='Wybierz użytkownika')
        self._choose_user_dropdown = ctk.CTkOptionMenu(self, variable=self._selected_name,
                                                       values=["Mama", "Tata", "Dziecko"],
                                                       width=300,
                                                       height=50,
                                                       button_color=gs.action_color,
                                                       fg_color='grey',
                                                       font=(gs.font_name, 20),
                                                       dropdown_font=(gs.font_name, 18))
        self._choose_user_dropdown.pack()

        self._select_button = ctk.CTkButton(self, text="Zatwierdź",
                                            width=120,
                                            height=50,
                                            corner_radius=10,
                                            fg_color=gs.action_color,
                                            font=(gs.font_name, 15),
                                            command=self._select_button_handler)
        self._select_button.pack(pady=40)

    def _select_button_handler(self):
        '''
        Sets gui's current user, shows gui's menubar and changes view to medicine-view-list.
        '''
        if self._selected_name.get() == 'Wybierz użytkownika':
            return
        user_id = self._name_to_id_map[self._selected_name.get()]
        self._gui.set_current_user_id(user_id)
        self._gui.show_menubar()
        self._gui.set_current_view('medicine-list-view')
