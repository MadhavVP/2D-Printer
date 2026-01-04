import customtkinter as ctk
from panels import *
class Menu(ctk.CTkTabview):
    def __init__(self, parent, paperh, paperw, preptext, prepvars, thresh, sobelksize,
        pencilksize,
        dgksize,
        gamma, rotation, zoom,
        steprate, sliced):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')

        self.add('Prepare')
        self.add('Slice')
        self.add('Export')

        PrepareFrame(self.tab('Prepare'), paperh, paperw, preptext, prepvars, thresh, sobelksize,
        pencilksize,
        dgksize,
        gamma, rotation, zoom)
        SliceFrame(self.tab('Slice'), steprate, sliced)
        ExportFrame(self.tab('Export'))

class PrepareFrame(ctk.CTkFrame):
    def __init__(self, parent, pheight, pwidth, textargs, varargs, threshvar, sobelksize,
        pencilksize,
        dgksize,
        gamma, rotation, zoom):
        super().__init__(master=parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        FillIn(self, 'Paper Height', pheight)
        FillIn(self, 'Paper Width', pwidth)
        Checkbox(self, textargs, varargs)
        Slider(self, 'Threshold', threshvar, 0, 255, False)
        Slider(self, 'Sobel Kernel Size', sobelksize, 1, 21, False)
        Slider(self, 'Pencil Kernel Size', pencilksize, 1, 21, False)
        Slider(self, 'Divide w/ Gamma Kernel Size', dgksize, 1, 21, False)
        Slider(self, 'Gamma', gamma, 0, 1, True)
        Slider(self, 'Rotation', rotation, -180, 180, True)
        Slider(self, 'Zoom', zoom, 0, 5, True)


class SliceFrame(ctk.CTkFrame):
    def __init__(self, parent, steprate, sliced):
        super().__init__(master=parent, fg_color=TERTIARY)
        self.pack(expand=True, fill='both')

        FillIn(self, 'Steps per mm', steprate)
        ctk.CTkButton(self, command=sliced, text='Slice').pack(fill='both', padx=5,pady=5)

class ExportFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=TERTIARY)
        self.pack(expand=True, fill='both')
