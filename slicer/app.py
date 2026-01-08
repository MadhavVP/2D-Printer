import customtkinter as ctk
from import_button import *
from PIL import Image, ImageTk
from editor import Menu
from settings import *
import cv2
import numpy as np
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode(PRIMARY)
        # self.attributes('--fullscreen', True)
        # self.state('zoomed')

        self.geometry("1000x720")
        self.path = ''
        self.threshold = ctk.IntVar(value=150)
        self.sobelksize = ctk.IntVar(value=5)
        self.pencilksize = ctk.IntVar(value=11)
        self.dgksize = ctk.IntVar(value=11)
        self.gamma = ctk.DoubleVar(value=0.15)
        self.sobel = ctk.BooleanVar(value=False)
        self.pencil = ctk.BooleanVar(value=False)
        self.divgamma = ctk.BooleanVar(value=False)
        self.paperheight = ctk.IntVar(value= 279)
        self.paperwidth = ctk.IntVar(value= 216)
        self.rotation = ctk.DoubleVar(value= 0)
        self.zoom = ctk.DoubleVar(value= 1)
        
        self.steprate = ctk.IntVar(value=75)
        self.sliced = ctk.BooleanVar(value=False)
        
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
        self.divgamma.trace('w', lambda *_: self.reload_cv2_img())
        self.threshold.trace('w', lambda *_: self.reload_cv2_img())
        self.sobelksize.trace('w', lambda *_: self.reload_cv2_img())
        self.pencilksize.trace('w', lambda *_: self.reload_cv2_img())
        self.dgksize.trace('w', lambda *_: self.reload_cv2_img())
        self.gamma.trace('w', lambda *_: self.reload_cv2_img())
        self.rotation.trace('w', lambda *_: self.reload_cv2_img())
        self.zoom.trace('w', lambda *_: self.reload_cv2_img())
        self.paperheight.trace('w', lambda *_: self.reload_cv2_img())
        self.sliced.trace('w', lambda *_: self.reload_cv2_img())
        self.menu = Menu(self, self.paperheight, self.paperwidth, ['sobel', 'pencil', 'Divide w/ Gamma'], [self.sobel, self.pencil, self.divgamma], self.threshold, self.sobelksize,
        self.pencilksize,
        self.dgksize,
        self.gamma,
        self.rotation,
        self.zoom,
        self.steprate,
        self.disp_sliced,
        self.export)
        self.reload_cv2_img()
    
    def reload_cv2_img(self):
        self.cv2_img = cv2.imread(self.path)
        self.cv2_img = cv2.cvtColor(self.cv2_img, cv2.COLOR_BGR2GRAY)
        if self.sobel.get():
            gx = cv2.Sobel(self.cv2_img, cv2.CV_64F, 1, 0, ksize=self.sobelksize.get())
            gy = cv2.Sobel(self.cv2_img, cv2.CV_64F, 0, 1, ksize=self.sobelksize.get())
            self.cv2_img = cv2.magnitude(gx, gy)
        if self.pencil.get():
            neg = 255 - self.cv2_img
            gblur = cv2.GaussianBlur(neg, (self.pencilksize.get(),self.pencilksize.get()), 0)
            neg_blur = 255 - gblur
            self.cv2_img = cv2.divide(self.cv2_img, neg_blur, scale=256)
        if self.divgamma.get():
            gblur = cv2.GaussianBlur(self.cv2_img, (self.dgksize.get(),self.dgksize.get()), 0)
            div = cv2.divide(self.cv2_img, gblur, scale = 256)
            self.cv2_img = self.adj_gamma(div, self.gamma.get())

        ret, self.cv2_img = cv2.threshold(self.cv2_img, self.threshold.get(), 255, cv2.THRESH_BINARY)
        self.cv2_img = cv2.normalize(
                            self.cv2_img, None, 0, 255, cv2.NORM_MINMAX
                        ).astype(np.uint8)
        self.disp_img = self.paperize()
        self.update_viewed_image()

    def paperize(self):
        ph = self.paperheight.get()
        pw = self.paperwidth.get()
        paper = np.full((ph, pw), 255, dtype=np.uint8)

        imgh, imgw = self.cv2_img.shape[:2]
        
        paper_center = (pw // 2, ph // 2)
        img_center = (imgw // 2, imgh // 2)

        rotate = cv2.getRotationMatrix2D(img_center, self.rotation.get(), self.zoom.get())

        rotate[0, 2] += paper_center[0] - img_center[0]
        rotate[1, 2] += paper_center[1] - img_center[1]

        cv2.warpAffine(self.cv2_img, rotate, (pw, ph), dst=paper, flags=cv2.INTER_LINEAR, borderValue=255)
        # resized = cv2.resize(self.cv2_img, (neww, newh), interpolation=cv2.INTER_AREA)

        # x_off = (pw - neww) // 2
        # y_off = (ph - newh) // 2

        # paper[y_off:y_off+newh, x_off:x_off+neww] = resized
        return paper
    
    def disp_sliced(self):
        self.reload_cv2_img()
        heightsteps = self.paperheight.get() * self.steprate.get()
        widthsteps = self.paperwidth.get() * self.steprate.get()
        printingres = cv2.resize(self.disp_img, (widthsteps, heightsteps), interpolation=cv2.INTER_NEAREST)
        _, self.disp_img = cv2.threshold(printingres, 127, 255, cv2.THRESH_BINARY)
        self.update_viewed_image()

    def export(self):
        self.disp_sliced()

        fp = filedialog.asksaveasfilename(
            title="Save mcode as",
            defaultextension=".mcode",
            filetypes=[("MCODE", "*.mcode")],
        )

        if not fp:
            return
        
        cur = 0
        with open(fp, "w") as f:
            height, width = self.disp_img.shape[:2] 
            for i in range(height):
                f.write(f"Z0\nX0 Y{i}\n")
                for j in range(width):
                    if self.disp_img[i][j] == 255:
                        if cur == 0:
                            f.write(f"X{j} Y{i}\nZ1\n")
                            cur = 1
                    else:
                        if cur == 0:
                            f.write(f"X{j} Y{i}\nZ0\n")
                            cur = 0
                    if j == width - 1:
                        f.write(f"X{j} Y{i}\n")


    def adj_gamma(self, img, gamma=1):
        invGamma = 1.0 / gamma
        table = np.array([((i/255)**invGamma)*255 for i in np.arange(0,256)])
        lut  = cv2.LUT(img.astype(np.uint8), table.astype(np.uint8))
        return lut

    def update_viewed_image(self):
        self.image = Image.fromarray(self.disp_img)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.img_ratio = self.image.size[0] / self.image.size[1]
        self.image_import.grid_forget()
        self.image_output = ImgOut(self, self.resize_image)
        self.close_button = CloseOutput(self, self.close_edit)
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