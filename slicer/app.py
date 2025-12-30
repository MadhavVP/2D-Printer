import customtkinter as ctk
from import_button import *
from PIL import Image, ImageTk
from editor import Menu
from settings import *
import cv2
import numpy as np

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode(PRIMARY)
        # self.attributes('--fullscreen', True)
        # self.state('zoomed')

        self.geometry("1000x720")
        self.path = ''
        self.threshold = 150
        self.ksize = 11
        self.sigmaX = 5
        self.gamma = 0.15
        self.sobel = ctk.BooleanVar(value=False)
        self.pencil = ctk.BooleanVar(value=False)
        
        self.canvas_width = 0
        self.canvas_height = 0
        self.image_height = 0
        self.image_width = 0

        self.image_output = None
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        self.image_import = Importer(self, self.import_img)

        self.mainloop()
    
    def import_img(self, path):
        self.path = path
        self.sobel.trace('w', lambda *_: self.reload_cv2_img())
        self.pencil.trace('w', lambda *_: self.reload_cv2_img())
        self.reload_cv2_img()
    
    def reload_cv2_img(self):
        self.cv2_img = cv2.imread(self.path)
        self.cv2_img = cv2.cvtColor(self.cv2_img, cv2.COLOR_BGR2GRAY)
        if self.sobel.get():
            gx = cv2.Sobel(self.cv2_img, cv2.CV_64F, 1, 0, ksize=5)
            gy = cv2.Sobel(self.cv2_img, cv2.CV_64F, 0, 1, ksize=5)
            self.cv2_img = cv2.magnitude(gx, gy)
        if self.pencil.get():
            neg = 255 - self.cv2_img
            gblur = cv2.GaussianBlur(neg, (self.ksize,self.ksize), 0)
            neg_blur = 255 - gblur
            sketch = cv2.divide(self.cv2_img, neg_blur, scale=256)
            ret, thresh2 = cv2.threshold(sketch, self.threshold, 255, cv2.THRESH_BINARY)
            self.cv2_img = thresh2
        self.cv2_img = cv2.normalize(
                            self.cv2_img, None, 0, 255, cv2.NORM_MINMAX
                        ).astype(np.uint8)
        self.update_viewed_image()


    def update_viewed_image(self):
        self.image = Image.fromarray(self.cv2_img)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.img_ratio = self.image.size[0] / self.image.size[1]
        self.image_import.grid_forget()
        self.image_output = ImgOut(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit)
        self.menu = Menu(self, ['sobel', 'pencil'], [self.sobel, self.pencil])
        self.render_img()
    
    
    def close_edit(self):
        self.image_output.grid_forget()
        self.image_output.place_forget()
        self.menu.grid_forget()
        self.image_import = Importer(self, self.import_img)


    def resize_image(self, event):
        canvas_ratio = event.width / event.height
        self.canvas_width = event.width
        self.canvas_height = event.height
        if canvas_ratio > self.img_ratio:
            self.image_height = event.height
            self.image_width = self.image_height * self.img_ratio
        else:
            self.image_width = event.width
            self.image_height = self.image_width / self.img_ratio
        self.render_img()

    def render_img(self):
        if self.image_output is not None:
            self.image_output.delete('all')
        resized_img = self.image.resize((int(self.image_width), int(self.image_height)))
        self.image_tk = ImageTk.PhotoImage(resized_img)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2,image=self.image_tk)


App()