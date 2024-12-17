import customtkinter as ctk


class View(ctk.CTkScrollableFrame):
    '''
    Base class for all the views in the GUI.

    Attributes
    ----------
    :ivar _system: system handler
    :vartype _system: System
    '''
    def __init__(self, system_handler, gui_handler, master, width=200, height=200, corner_radius=None, border_width=None, bg_color="transparent", fg_color=None, border_color=None, scrollbar_fg_color=None, scrollbar_button_color=None, scrollbar_button_hover_color=None, label_fg_color=None, label_text_color=None, label_text="", label_font=None, label_anchor="center", orientation="vertical"):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)
        self._system = system_handler
        self._gui = gui_handler

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        pass
