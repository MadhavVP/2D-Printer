import customtkinter as ctk
from panels import *
class Menu(ctk.CTkTabview):
    def __init__(self, parent, preptext, prepvars):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.add('Prepare')
        self.add('Slice')
        self.add('Export')

        PrepareFrame(self.tab('Prepare'), preptext, prepvars)
        SliceFrame(self.tab('Slice'))
        ExportFrame(self.tab('Export'))

class PrepareFrame(ctk.CTkFrame):
    def __init__(self, parent, textargs, varargs):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        Checkbox(self, textargs, varargs)

class SliceFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=TERTIARY)
        self.pack(expand=True, fill='both')

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=TERTIARY)
        self.pack(expand=True, fill='both')
