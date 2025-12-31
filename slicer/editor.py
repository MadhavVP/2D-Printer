import customtkinter as ctk
from panels import *
class Menu(ctk.CTkTabview):
    def __init__(self, parent, preptext, prepvars, thresh, sobelksize,
        pencilksize,
        dgksize,
        gamma):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.add('Prepare')
        self.add('Slice')
        self.add('Export')

        PrepareFrame(self.tab('Prepare'), preptext, prepvars, thresh, sobelksize,
        pencilksize,
        dgksize,
        gamma)
        SliceFrame(self.tab('Slice'))
        ExportFrame(self.tab('Export'))

class PrepareFrame(ctk.CTkFrame):
    def __init__(self, parent, textargs, varargs, threshvar, sobelksize,
        pencilksize,
        dgksize,
        gamma):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        Checkbox(self, textargs, varargs)
        Slider(self, 'Threshold', threshvar, 0, 255, False)
        Slider(self, 'Sobel Kernel Size', sobelksize, 1, 21, False)
        Slider(self, 'Pencil Kernel Size', pencilksize, 1, 21, False)
        Slider(self, 'Divide Gaussian Kernel Size', dgksize, 1, 21, False)
        Slider(self, 'Gamma', gamma, 0, 1, True)

class SliceFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=TERTIARY)
        self.pack(expand=True, fill='both')

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=TERTIARY)
        self.pack(expand=True, fill='both')
