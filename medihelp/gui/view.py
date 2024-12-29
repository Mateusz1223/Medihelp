import customtkinter as ctk
from .gui import GUI
from medihelp.system import System


class View(ctk.CTkScrollableFrame):
    '''
    Parent class for all the views.
    '''
    def __init__(self, system_handler: System, gui_handler: GUI, parent, width=200, height=200, corner_radius=None, border_width=None, bg_color="transparent", fg_color=None, border_color=None, scrollbar_fg_color=None, scrollbar_button_color=None, scrollbar_button_hover_color=None, label_fg_color=None, label_text_color=None, label_text="", label_font=None, label_anchor="center", orientation="vertical"):
        '''
        :param system_handler: System object handler
        :type system_handler: System

        :param gui_handler: GUI object handler
        :type gui_handler: GUI

        :param parent: parent object used for initialization of tkinter objects
        :type parent: tkinter.Misc

        CTkScrollableFrame __init__parameters...
        '''
        super().__init__(parent, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)
        self._system = system_handler
        self._gui = gui_handler

    def update_view(self):
        '''
        Called when informations in databases change so that the view can update its content.
            Each view modifies it to it's own needs.
        '''
        self._parent_canvas.yview_moveto(0)

    def scroll_up(self, e):
        scroll_poition_from_the_top = self._parent_canvas.yview()[0]
        if scroll_poition_from_the_top > 0.0001:  # makes sure it wont scroll up when it's already at the top
            self._parent_canvas.yview("scroll", -1, "units")

    def scroll_down(self, e):
        scroll_poition_from_the_bottom = self._parent_canvas.yview()[1]
        if scroll_poition_from_the_bottom > 0.0001:  # makes sure it wont scroll down when it's already at the bottom
            self._parent_canvas.yview("scroll", 1, "units")
