import tkinter as tk


class View(tk.Frame):
    '''
    Base class for all the views in the GUI.

    Attributes
    ----------
    :ivar _system: system handler
    :vartype _system: System
    '''
    def __init__(self, system_handler, master = None, cnf = None, *, background = None, bd = 0, bg = None, border = 0, borderwidth = 0, class_ = "Frame", colormap = "", container = False, cursor = "", height = 0, highlightbackground = None, highlightcolor = None, highlightthickness = 0, name = None, padx = 0, pady = 0, relief = "flat", takefocus = 0, visual = "", width = 0):
        super().__init__(master, cnf, background=background, bd=bd, bg=bg, border=border, borderwidth=borderwidth, class_=class_, colormap=colormap, container=container, cursor=cursor, height=height, highlightbackground=highlightbackground, highlightcolor=highlightcolor, highlightthickness=highlightthickness, name=name, padx=padx, pady=pady, relief=relief, takefocus=takefocus, visual=visual, width=width)
        self._system = system_handler

    def update_view(self):
        '''
        Called when system informations like databases data change so that the view can update it's content.
        '''
        pass
