import customtkinter as ctk
from settings import *
class Panel(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(master=parent, fg_color=SECONDARY)
        self.pack(fill = 'x', pady=4, ipady=8)

class Checkbox(Panel):
    def __init__(self, parent, textargs, varargs):
        super().__init__(parent=parent)

        self.rowconfigure((0, len(textargs)), weight=1)
        self.columnconfigure((0,1), weight=1)

        for i in range(0, len(textargs)):
            ctk.CTkCheckBox(self, text=textargs[i], variable=varargs[i]).grid(column=0, row=i, sticky='W', padx=5, pady=5)

class FillIn(Panel):
    def __init__(self, parent, text, var):
        super().__init__(parent=parent)
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)
        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        ctk.CTkEntry(self, textvariable=var, placeholder_text=f'{int(var.get())}').grid(row=1, column=1, sticky='E', padx=5, pady=5)

class Slider(Panel):
    def __init__(self, parent, text, var, min, max, double):
        super().__init__(parent=parent)
        self.double = double
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)
        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)
        self.num_label = ctk.CTkLabel(self, text=var.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)
        ctk.CTkSlider(self, variable=var, from_=min, to=max, command=self.update_text).grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

    def update_text(self, val):
        if self.double:
            self.num_label.configure(text = f'{round(val, 2)}')
        else:
            self.num_label.configure(text = f'{round(val)}')
