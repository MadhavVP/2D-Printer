import customtkinter as ctk
from import_button import *
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        # self.attributes('--fullscreen', True)
        # self.state('zoomed')

        self.geometry("1000x720")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=6)

        self.image_import = Importer(self, self.import_img)

        self.mainloop()
    
    def import_img(self, path):
        self.image = Image.open(path)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_import.grid_forget()
        self.image_output = ImgOut(self, self.resize_image)

        self.resize_image()

    def resize_image(self, event):
        self.image_output.delete('all')
        self.image_output.create_image(event.width / 2, event.height / 2,image=self.image_tk)


App()