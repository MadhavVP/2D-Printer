import customtkinter as ctk
from tkinter import filedialog, Canvas

class Importer(ctk.CTkFrame):
    def __init__(self, parent, importing_func):
        super().__init__(master=parent)
        self.grid(column = 0, columnspan = 2, row = 0, sticky = 'nswe')
        self.import_func = importing_func

        ctk.CTkButton(self, text = 'click to open', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):
        path  = filedialog.askopenfile().name
        self.import_func(path)


class ImgOut(Canvas):
    def __init__(self, parent, resize_img):
            super().__init__(master=parent, bd = 0, highlightthickness=0, relief='ridge')
            self.grid(row = 0, column=1, sticky='nsew')
            self.bind('<Configure>', resize_img)