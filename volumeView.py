"""
=======================================
Volume View - Volumetric Data Viewer
Main module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v2
"""



from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

import platform
import os

from PIL import  Image, ImageDraw, ImageFont, ImageTk

from canvas_image import *
 
 
 
class CheckButtonNoIndicator(ttk.Checkbutton):
    def __init__(self,parent,**kwargs):
        self.parent=parent
        style = ttk.Style()
        style.layout(
            'no_indicator.TCheckbutton',[
                ('Checkbutton.padding', 
                    {'sticky': 'nswe', 
                     'children': [
                        # ('Checkbutton.indicator', 
                        #     {'side': 'left', 'sticky': ''}
                        # ),
                        ('Checkbutton.focus',
                            {'side': 'left', 'sticky': 'w', 'children':[
                                ('Checkbutton.label', {'sticky': 'nswe'})
                                ]
                            }
                        )
                    ]
                    }
                )
            ]
         )

        # style.configure('no_indicator.TCheckbutton', background=self.parent.cget("background"))
        style.configure('no_indicator.TCheckbutton', background=style.configure(".")["background"])
        
        def create_off_image(self,border,fill,size):
            off_border="black"
            off_fill="#ffaaff"
            # checkbutton off
            checkbutton_off = Image.new("RGBA", (134, 134))
            draw = ImageDraw.Draw(checkbutton_off)
            draw.rounded_rectangle(
                [2, 2, 132, 132],
                radius=16,
                outline=border,
                width=6,
                fill=fill,
            )
            self.off_image = ImageTk.PhotoImage(checkbutton_off.resize((size,size), Image.LANCZOS))

        def create_on_image(self,border,fill,check_color,size):
            checkbutton_on = Image.new("RGBA", (134, 134))
            draw = ImageDraw.Draw(checkbutton_on)
            draw.rounded_rectangle(
                [2, 2, 132, 132],
                radius=16,
                fill=fill,
                outline=border,
                width=6,
            )
            
            self.select_image_font()
            
            indicator = "✓"
            draw.text(self.position, indicator, font=self.fnt, fill=check_color)
            self.on_image = ImageTk.PhotoImage(checkbutton_on.resize((size,size), Image.LANCZOS))

        # fill=self.parent.cget("background")
        fill=style.configure(".")["background"]
        create_off_image(self,border="black",fill=fill,size=13)
        create_on_image(self,border="black",fill="green",check_color="white",size=13)
        
        super().__init__(self.parent,**kwargs, image=self.off_image, style='no_indicator.TCheckbutton')
        
        if self.instate(['!disabled', 'selected']):
            self['image']=self.on_image
        else :
            self['image']=self.off_image 
 
 
    def select_image_font(self):
            
        self.fnt = ImageFont.load_default()
        self.position = (0,0)  
            
        if platform.system() == 'Windows':
            try:
                # Segoe UI Symbol
                self.fnt = ImageFont.truetype("seguisym.ttf", 120)
                self.fnt = ImageFont.truetype("Symbola.ttf", 120)
                self.position = (20,-20)
                print("Font found: 'seguisym.ttf'")
            except :
                print("Font not found: 'seguisym.ttf'")
                pass
                
        if platform.system() == 'Linux' :
            try:
                self.fnt = ImageFont.truetype("FreeSerif.ttf", 130)
                self.position = (18,10)
                print("Font found: 'FreeSerif.ttf'")
            except:
                try:
                    self.fnt = ImageFont.truetype("DejaVuSans.ttf", 160)
                    self.position = (2,-24)
                    print("Font found: 'DejaVuSans.ttf'")
                except:
                    print("Fonts not found: 'FreeSerif.ttf', 'DejaVuSans.ttf'")
                    
        if platform.system() == 'Darwin' :
            try: 
                self.fnt = ImageFont.truetype("LucidaGrande.ttc", 120)
                self.position = (0,-10) 
                print("Font found: 'LucidaGrande.ttc'")
            except:
                print("Font not found: 'LucidaGrande.ttc'")

 
class FrameProcessing(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        
        self.image_generator=None
        if 'image_generator' in kwargs.keys() :
            self.image_generator=kwargs["image_generator"]
        
        if 'canvases' in kwargs.keys() :
            self.canvases=kwargs["canvases"]
        
        self.index=self.image_generator.index
        self.cocanvases=()
        
        super().__init__(*args)
        self['relief'] = 'sunken'
        self["padding"]=(5,5,5,5)
        
        self.helv10b = tkFont.Font(family='Helvetica',size=10, weight='bold')
        self.helv9b = tkFont.Font(family='Helvetica',size=9, weight='bold')
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=100)
        # print(self.style.configure('TCheckbutton'))
            
        labelTitle=ttk.Label(self,text="Image procesing")
        labelTitle.grid(row=0,column=0,columnspan=3,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelTitle.grid_propagate(0)
        labelTitle['font']=self.helv10b
        labelTitle['anchor']=tk.CENTER
        labelTitle['background']='#1e94f1'
        labelTitle['foreground']='white'

        self.varN = tk.BooleanVar(value=self.image_generator.normalize)        
        self.checkButtonN=CheckButtonNoIndicator(self, compound=None, onvalue=True, offvalue=False, takefocus=False,
                      variable=self.varN, command=self.set_normalization)
        self.checkButtonN.grid(row=1,column=0,padx=(0,0),pady=(5,2))
        
        labelN=ttk.Label(self,text="Normalization")
        labelN.grid(row=1,column=1,padx=(0,0),pady=(2,0),sticky=(tk.W, tk.N, tk.E, tk.S))
        
        self.varHE = tk.BooleanVar(value=self.image_generator.equalize_histogram)
        self.checkButtonHE=CheckButtonNoIndicator(self, compound=None, onvalue=True, offvalue=False, takefocus=False,
                      variable=self.varHE, command=self.set_histrogram_equalization)
        self.checkButtonHE.grid(row=2,column=0,padx=(0,0),pady=(2,2))
        
        labelHE=ttk.Label(self,text="Histogram equalization")
        labelHE.grid(row=2,column=1,padx=(0,0),pady=(2,0),sticky=(tk.W, tk.N, tk.E, tk.S))
        
    def set_normalization(self):
        if self.checkButtonN.instate(['!disabled', 'selected']):
            self.checkButtonN['image'] = self.checkButtonN.on_image
            if self.image_generator != None :
                self.image_generator.normalize=True
                for canvas in self.cocanvases:
                    canvas.update_canvas(self.index)
        else:
            self.checkButtonN['image'] = self.checkButtonN.off_image
            if self.image_generator != None :
                self.image_generator.normalize=False
                for canvas in self.cocanvases:
                    canvas.update_canvas(self.index)

    def set_histrogram_equalization(self):
        if self.checkButtonHE.instate(['!disabled', 'selected']):
            self.checkButtonHE['image'] = self.checkButtonHE.on_image
            if self.image_generator != None :
                self.image_generator.equalize_histogram=True
                for canvas in self.cocanvases:
                    canvas.update_canvas(self.index)
                
        else:
            self.checkButtonHE['image'] = self.checkButtonHE.off_image
            if self.image_generator != None :
                self.image_generator.equalize_histogram=False
                for canvas in self.cocanvases:
                    canvas.update_canvas(self.index)
                
                
class FrameInfo(ttk.Frame):
    def __init__(self, *args, **kwargs):
                
        # self.parent=args[0]
        super().__init__(*args)
        
        self['relief'] = 'sunken'
        self["padding"]=(5,5,5,5)

        self.volume=None
        if 'volume' in kwargs.keys() :
            self.volume=kwargs["volume"]

        if 'index' in kwargs.keys() :
            self.index=kwargs["index"]

        self.origin=None
        if 'origin' in kwargs.keys() :
            self.origin=kwargs["origin"]
        if self.origin == None :
            self.origin=(0.0,0.0,0.0)
        
        self.grid_size=None
        if 'grid_size' in kwargs.keys() :
            self.grid_size=kwargs["grid_size"]
        if self.grid_size == None :
            self.grid_size=(1.0,1.0,1.0)
        
        self.helv10b = tkFont.Font(family='Helvetica',size=10, weight='bold')
        self.helv9b = tkFont.Font(family='Helvetica',size=9, weight='bold')
        
        # print("Origin",self.origin)
        # print("Grid size",self.grid_size)
        # print("Index",self.index)

        labelTitle=ttk.Label(self,text="Data probe")
        labelTitle.grid(row=0,column=0,columnspan=3,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelTitle.grid_propagate(0)
        labelTitle['width']=24
        labelTitle['font']=self.helv10b
        labelTitle['anchor']=tk.CENTER
        labelTitle['background']='#1e94f1'
        labelTitle['foreground']='white'
        
        labelIndex=ttk.Label(self,text="Index")
        labelIndex.grid(row=1,column=0,columnspan=3,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelIndex.grid_propagate(0)
        labelIndex['width']=24
        labelIndex['font']=self.helv9b
        labelIndex['anchor']=tk.CENTER
        labelIndex['padding']=(0,2,0,0)
        labelIndex['background']='#1e94c1'
        labelIndex['foreground']='white'
        
        labelI0=ttk.Label(self,text="i")
        labelI0.grid(row=2,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelI0.grid_propagate(0)
        labelI0['width']=8
        labelI0['font']=self.helv9b
        labelI0['anchor']=tk.CENTER
        labelI0['background']='#1e94c1'
        labelI0['foreground']='white'
        
        labelJ0=ttk.Label(self,text="j")
        labelJ0.grid(row=2,column=1,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelJ0.grid_propagate(0)
        labelJ0['width']=8
        labelJ0['font']=self.helv9b
        labelJ0['anchor']=tk.CENTER
        labelJ0['background']='#1e94c1'
        labelJ0['foreground']='white'
        
        labelK0=ttk.Label(self,text="k")
        labelK0.grid(row=2,column=2,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelK0.grid_propagate(0)
        labelK0['width']=8
        labelK0['font']=self.helv9b
        labelK0['anchor']=tk.CENTER
        labelK0['background']='#1e94c1'
        labelK0['foreground']='white'
        
        self.labelI1=ttk.Label(self,text="0")
        self.labelI1.grid(row=3,column=0)
        self.labelI1['padding']=(0,3,0,0)
        
        self.labelJ1=ttk.Label(self,text="0")
        self.labelJ1.grid(row=3,column=1)
        self.labelJ1['padding']=(0,3,0,0)
        
        self.labelK1=ttk.Label(self,text="0")
        self.labelK1.grid(row=3,column=2)
        self.labelK1['padding']=(0,3,0,0)
        
        labelPosition=ttk.Label(self,text="Position")
        labelPosition.grid(row=4,column=0,columnspan=3,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelPosition.grid_propagate(0)
        labelPosition['width']=24
        labelPosition['font']=self.helv9b
        labelPosition['anchor']=tk.CENTER
        labelPosition['padding']=(0,2,0,0)
        labelPosition['background']='#1e94c1'
        labelPosition['foreground']='white'
        
        labelX0=ttk.Label(self,text="x")
        labelX0.grid(row=5,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelX0.grid_propagate(0)
        labelX0['width']=8
        labelX0['font']=self.helv9b
        labelX0['anchor']=tk.CENTER
        labelX0['background']='#1e94c1'
        labelX0['foreground']='white'
        
        labelY0=ttk.Label(self,text="y")
        labelY0.grid(row=5,column=1,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelY0.grid_propagate(0)
        labelY0['width']=8
        labelY0['font']=self.helv9b
        labelY0['anchor']=tk.CENTER
        labelY0['background']='#1e94c1'
        labelY0['foreground']='white'
        
        labelZ0=ttk.Label(self,text="z")
        labelZ0.grid(row=5,column=2,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelZ0.grid_propagate(0)
        labelZ0['width']=8
        labelZ0['font']=self.helv9b
        labelZ0['anchor']=tk.CENTER
        labelZ0['background']='#1e94c1'
        labelZ0['foreground']='white'
        
        self.labelX1=ttk.Label(self,text="0.0")
        self.labelX1.grid(row=6,column=0)
        self.labelX1['padding']=(0,3,0,0)
    
        self.labelY1=ttk.Label(self,text="0.0")
        self.labelY1.grid(row=6,column=1)
        self.labelY1['padding']=(0,3,0,0)
        
        self.labelZ1=ttk.Label(self,text="0.0")
        self.labelZ1.grid(row=6,column=2)
        self.labelZ1['padding']=(0,3,0,0)
        
        labelIntensity0=ttk.Label(self,text="Intensity")
        labelIntensity0.grid(row=7,column=0,columnspan=3,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelIntensity0.grid_propagate(0)
        labelIntensity0['width']=25
        labelIntensity0['font']=self.helv9b
        labelIntensity0['anchor']=tk.CENTER
        labelIntensity0['background']='#1e94c1'
        labelIntensity0['foreground']='white'

        self.labelIntensity1=ttk.Label(self,text="0")
        self.labelIntensity1.grid(row=8,column=0,columnspan=3)
        self.labelIntensity1['padding']=(0,3,0,0)
        
        self.update_frame(index)


    def update_frame(self,index,joint_update=False): 
        self.index=index
        self.z=(self.origin[2]+self.index[2])*self.grid_size[2]
        self.y=(self.origin[1]+self.index[1])*self.grid_size[1]
        self.x=(self.origin[0]+self.index[0])*self.grid_size[0]
        
        self.intensity=self.volume[index[2],index[1],index[0]]
        
        # print("Volume size :",self.volume.shape)
        # print("i,j,k :",index[0],index[1],index[2])
        # print("x,y,z :",self.x,self.y,self.z)
        # print("Intensity :", self.intensity)
        
        self.labelI1["text"]=index[0]
        self.labelJ1["text"]=index[1]
        self.labelK1["text"]=index[2]
        
        self.labelX1["text"]="{}".format(self.x)
        self.labelY1["text"]="{}".format(self.y)
        self.labelZ1["text"]="{}".format(self.z)
        
        self.labelIntensity1["text"]="{}".format(self.intensity)

 

from tkinter import filedialog 
import pathlib


from test_volume import *
from image_generator import *
from jm_volume import *
from settings import *



        
ctrl = False
shift = False
ctrl_shift = False      
def ctrl_on(event):
    global ctrl, shift, ctrl_shift
    ctrl=True
    if shift :
        ctrl_shift=True
        ctrl=False
        shift=False
    else :
        ctrl_shift=False
        
def ctrl_off(event):
    global ctrl, shift, ctrl_shift
    ctrl=False
    ctrl_shift=False
    
def shift_on(event):
    global ctrl, shift, ctrl_shift
    shift=True
    if ctrl :
        ctrl_shift=True
        ctrl=False
        shift=False
    else :
        ctrl_shift=False
        
def shift_off(event):
    global ctrl, shift, ctrl_shift
    shift=False
    ctrl_shift=False  
    

class Shortcuts():
    def __init__(self,parent):
        self.root=Toplevel()
        self.root.title("Shortcuts")  

        self.frameShortcuts=ttk.Frame(self.root)
        self.frameShortcuts.grid(row=0,column=0)
        self.frameShortcuts['relief'] = 'raised'  
        self.frameShortcuts['padding']=(5,5,5,5)
        
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
     
        self.helv10 = tkFont.Font(family='Helvetica',size=10, weight='normal')
       
        labelShortcut00=ttk.Label(self.frameShortcuts,text="Ctrl+O",font=self.helv10)       
        labelShortcut00.grid(row=0,column=0,padx=(10,5),sticky="e")
        labelShortcut01=ttk.Label(self.frameShortcuts,text="Load volume data from file",font=self.helv10)       
        labelShortcut01.grid(row=0,column=1,padx=(5,10),sticky="w")

        labelShortcut10=ttk.Label(self.frameShortcuts,text="Ctrl+T",font=self.helv10)       
        labelShortcut10.grid(row=1,column=0,padx=(10,5),sticky="e")
        labelShortcut11=ttk.Label(self.frameShortcuts,text="Load test volume data",font=self.helv10)       
        labelShortcut11.grid(row=1,column=1,padx=(5,10),sticky="w")
        
        labelShortcut20=ttk.Label(self.frameShortcuts,text="Ctrl+S",font=self.helv10)       
        labelShortcut20.grid(row=2,column=0,padx=(10,5),sticky="e")
        labelShortcut21=ttk.Label(self.frameShortcuts,text="Export volume data in nrrd-format",font=self.helv10)       
        labelShortcut21.grid(row=2,column=1,padx=(5,10),sticky="w")

        labelShortcut20=ttk.Label(self.frameShortcuts,text="Ctrl+Q / Q",font=self.helv10)       
        labelShortcut20.grid(row=3,column=0,padx=(10,5),sticky="e")
        labelShortcut21=ttk.Label(self.frameShortcuts,text="Quit",font=self.helv10)       
        labelShortcut21.grid(row=3,column=1,padx=(5,10),sticky="w")
        
        self.root.bind("<Key>",self.key)
        self.root.resizable(False,False)
        self.root.attributes('-topmost', True)
        
        self.root.update()
        W=parent.winfo_width()
        H=parent.winfo_height()
        X=parent.winfo_x()
        Y=parent.winfo_y()
        w=self.root.winfo_width()
        h=self.root.winfo_height()
        x=X+(W-w)//2
        y=Y+(H-h)//2
        self.root.geometry("{}x{}+{}+{}".format(w,h,x,y))
        self.root.focus_set()
        self.root.iconphoto(False,PhotoImage(file='volumeView-icon.png')) 
        
    def key(self,event):
        k = event.keysym
        if k == 'Escape' :
            self.root.destroy()

class About():
    def __init__(self,parent):
        self.root=Toplevel()
        self.root.title("About Volume View")  

        self.frameAbout=ttk.Frame(self.root)
        self.frameAbout.grid(row=0,column=0)
        self.frameAbout['relief'] = 'raised'  
        self.frameAbout['padding']=(5,5,5,5)

        # self.style = ttk.Style(self.root)
        # self.style.theme_use('clam')
     
        self.helv16b = tkFont.Font(family='Helvetica',size=12, weight='bold')
        self.helv9 = tkFont.Font(family='Helvetica',size=9, weight='normal')
        self.helv9b = tkFont.Font(family='Helvetica',size=9, weight='bold')

        labelVolumeView=ttk.Label(self.frameAbout,text="Volume View",font=self.helv16b)       
        labelVolumeView.grid(row=0,column=0,columnspan=2)
        
        labelSoftware=ttk.Label(self.frameAbout,text="Volumetric Data Viewer",font=self.helv9)       
        labelSoftware.grid(row=1,column=0,columnspan=2)
        
        labelVersion=ttk.Label(self.frameAbout,text="Version {}".format('0.1'),font=self.helv9)       
        labelVersion.grid(row=2,column=0,columnspan=2)
        
        
        labelAuthor0=ttk.Label(self.frameAbout,text="Author:",font=self.helv9)  
        labelAuthor1=ttk.Label(self.frameAbout,text="Sinan Güngör",font=self.helv9)
        labelAuthor0.grid(row=3,column=0,sticky="e",padx=(10,3))
        labelAuthor1.grid(row=3,column=1,sticky="w",padx=(0,10))
        labelLicense0=ttk.Label(self.frameAbout,text="License:",font=self.helv9)  
        labelLicense1=ttk.Label(self.frameAbout,text="GNU General Public License, Version 2",font=self.helv9)
        labelLicense0.grid(row=4,column=0,sticky="e",padx=(10,3))
        labelLicense1.grid(row=4,column=1,sticky="w",padx=(0,10))
        
        self.frameAbout.columnconfigure(1,minsize=200)
        
        self.root.bind("<Key>",self.key)
        self.root.resizable(False,False)
        self.root.attributes('-topmost', True)
    
        self.root.update()
        W=parent.winfo_width()
        H=parent.winfo_height()
        X=parent.winfo_x()
        Y=parent.winfo_y()
        w=self.root.winfo_width()
        h=self.root.winfo_height()
        x=X+(W-w)//2
        y=Y+(H-h)//2
        self.root.geometry("{}x{}+{}+{}".format(w,h,x,y))
        
        self.root.focus_set()
        self.root.iconphoto(False,PhotoImage(file='volumeView-icon.png')) 
        
    def key(self,event):
        k = event.keysym
        if k == 'Escape' :
            self.root.destroy()
    
# ----------------------------------------------------------------------------------------------

class FrameCanvas(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self['relief'] = 'raised'  
        self['padding']=(0,0,0,0)
   
class FrameApp(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self['relief'] = 'raised'  
        self['padding']=(5,5,5,5) 
 
# ----------------------------------------------------------------------------------------------   

import time

def mainmenu_label_padding():
    padding=(5,0,5,0)
    if platform.system() == 'Linux' :
        padding=(5,3,5,0)
    return padding

def menu_label_padding():
    padding=(5,0,5,0)
    if platform.system() == 'Linux' :
        padding=(5,4,5,0)
    return padding


class FrameMenuTestVolume(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.app_class=None
        if 'app_class' in kwargs.keys() :
            self.app_class=kwargs["app_class"]
            
        self.position=(0,0)
        if 'position' in kwargs.keys() :
            self.position=kwargs["position"]    

        self['relief'] = 'raised'
        self["padding"]=(5,5,5,5)

        labelTestVolume1=ttk.Label(self,text="Tapered Cone (8bit)", style='Menu.TLabel')
        labelTestVolume1.grid(row=0,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelTestVolume1["padding"]=menu_label_padding()
        labelTestVolume2=ttk.Label(self,text="Tapered Cone (16bit)", style='Menu.TLabel')
        labelTestVolume2.grid(row=1,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelTestVolume2["padding"]=menu_label_padding()
        labelTestVolume3=ttk.Label(self,text="Wikipedia Tomography", style='Menu.TLabel')
        labelTestVolume3.grid(row=2,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelTestVolume3["padding"]=menu_label_padding()

        self.rowconfigure(0,minsize=20)
        self.rowconfigure(1,minsize=20) 
        self.rowconfigure(2,minsize=20)
        
        self.place(x=self.position[0],y=self.position[1])
        

        labelTestVolume1.bind("<Button-1>",self.test_volume_1)
        labelTestVolume2.bind("<Button-1>",self.test_volume_2)
        labelTestVolume3.bind("<Button-1>",self.test_volume_3)

    def test_volume_1(self,event):
        self.app_class.create_test_volume('cone',np.uint8)
        
    def test_volume_2(self,event):
        self.app_class.create_test_volume('cone',np.uint16)
        
    def test_volume_3(self,event):
        self.app_class.create_test_volume('wiki',np.uint8)    
        

class FrameMenuFile(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        
        self['relief'] = 'raised'
        padding=(5,5,5,5)
        self["padding"]=padding
        
        self.app_class=None
        if 'app_class' in kwargs.keys() :
            self.app_class=kwargs["app_class"]
            
        self.position=(0,0)
        if 'position' in kwargs.keys() :
            self.position=kwargs["position"]
        
        self.menuList=list()    
            
        self.labelOpen=ttk.Label(self,text="Open", style='Menu.TLabel')
        self.labelOpen.grid(row=0,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        self.labelOpen["padding"]=menu_label_padding()

        self.labelTestVolume=ttk.Label(self,text="Test Volume Data", style='Menu.TLabel')
        self.labelTestVolume.grid(row=1,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        self.labelTestVolume["padding"]=menu_label_padding() 
        
        self.labelExport=ttk.Label(self,text="Export", style='Menu.TLabel')
        self.labelExport.grid(row=2,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        self.labelExport["padding"]=menu_label_padding() 
          
        self.labelQuit=ttk.Label(self,text="Quit", style='Menu.TLabel')
        self.labelQuit.grid(row=3,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        self.labelQuit["padding"]=menu_label_padding()
        self.labelQuit.bind("<Button-1>", self.quit)
        
        self.rowconfigure(0,minsize=20)
        self.rowconfigure(1,minsize=20) 
        self.rowconfigure(2,minsize=20)
        self.rowconfigure(3,minsize=20) 

        self.place(x=self.position[0],y=self.position[1])
        self.lift()
        
        self.labelOpen.bind("<Enter>", self.menu_open)
        self.labelTestVolume.bind("<Enter>", self.menu_test_volume)
        self.labelExport.bind("<Enter>", self.menu_export)
        self.labelQuit.bind("<Enter>", self.menu_quit)
        
        self.labelOpen.bind("<Button-1>", self.open)
        self.labelExport.bind("<Button-1>", self.export)
        
        self.update()

        x=self.grid_bbox(0, 0)[2]+padding[0]+padding[1]
        y=self.grid_bbox(0, 2)[1]+padding[1]
        self.positionMenuTest=(x,y)
        
    def open(self,event):
        self.app_class.open()
   
    def export(self,event):
        self.app_class.export()

    def menu_open(self,event):
        self.destroy_menus()
        
    def menu_test_volume(self,event):
        self.destroy_menus()
        menuTestVolume=FrameMenuTestVolume(app_class=self.app_class,position=self.positionMenuTest) # app_class=self.master
        self.menuList.append(menuTestVolume)
    
    def menu_export(self,event):  
        self.destroy_menus()
        
    def menu_quit(self,event):
        self.destroy_menus()
          
    def destroy_menus(self):
        for m in self.menuList:
            m.destroy()
            self.menuList.remove(m)
            
    def quit(self,event):
        self.master.quit()
        


class FrameMenuHelp(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
    
        self.app_class=None
        if 'app_class' in kwargs.keys() :
            self.app_class=kwargs["app_class"]
    
        self.position=(0,0)
        if 'position' in kwargs.keys() :
            self.position=kwargs["position"]
    
    
        self['relief'] = 'raised'
        padding=(5,5,5,5)
        self["padding"]=(5,5,5,5)
    
        self.menuList=list()
    
        labelShortcuts=ttk.Label(self,text="Shortcuts", style='Menu.TLabel')
        labelShortcuts.grid(row=0,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelShortcuts["padding"]=menu_label_padding()

        labelAbout=ttk.Label(self,text="About", style='Menu.TLabel')
        labelAbout.grid(row=1,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelAbout["padding"]=menu_label_padding()
        
        self.rowconfigure(0,minsize=20)
        self.rowconfigure(1,minsize=20)    
        
        self.place(x=self.position[0],y=self.position[1])
        
        labelShortcuts.bind("<Button-1>", self.dialog_shortcuts)
        labelAbout.bind("<Button-1>", self.dialog_about)
        
    def destroy_menus(self):
        for m in self.menuList:
            m.destroy()
            self.menuList.remove(m)
        
    def dialog_about(self,event):
        self.app_class.menuMain.destroy_menus()
        self.app_class.menuMain.disabled=True
        about=About(self.app_class.gui_root)
        self.app_class.gui_root.wait_window(about.root)
        self.app_class.menuMain.disabled=False

    def dialog_shortcuts(self,event):
        self.app_class.menuMain.destroy_menus()
        self.app_class.menuMain.disabled=True
        shortcuts=Shortcuts(self.app_class.gui_root)
        self.app_class.gui_root.wait_window(shortcuts.root)
        self.app_class.menuMain.disabled=False

class FrameMenuMain(ttk.Frame): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.grid(sticky=(tk.W, tk.N, tk.E, tk.S))
        self['relief'] = 'raised'
        padding=(5,5,5,5)
        self["padding"]=padding
        # On Windows OS
        # print(self["padding"]) outputs (<pixel object: '5'>,<pixel object: '5'>,<pixel object: '5'>,<pixel object: '5'>)
        # print(self["padding"][0]) outputs 5
        # but type of self["padding"][0] is '_tkinter.Tcl_Obj'  not 'int'.
        # See https://github.com/python/cpython/issues/101830
        # '_tkinter.Tcl_Obj' object has attributes 'string' and 'typename'.
        # 
        # A conversion is needed like int(self["padding"][0].string)
        # Instead of conversion, a variable (padding) is used.
        
        self.app_class=None
        if 'app_class' in kwargs.keys() :
            self.app_class=kwargs["app_class"]
        
        self.menuList=list()
        
        self.disabled=False
        
        labelFile=ttk.Label(self,text="File", style='Menu.TLabel')
        labelFile.grid(row=0,column=0,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelFile["padding"]=mainmenu_label_padding()
        # labelFile.bind("<Button-1>", self.menu_file)
        labelFile.bind("<Enter>", self.menu_file)
        
      
        labelHelp=ttk.Label(self,text="Help",style='Menu.TLabel')
        labelHelp.grid(row=0,column=2,sticky=(tk.W, tk.N, tk.E, tk.S))
        labelHelp["padding"]=mainmenu_label_padding()
        # labelHelp.bind("<Button-1>", self.menu_help)
        labelHelp.bind("<Enter>", self.menu_help)

        self.bind("<Button-1>", self.destroy_menus)
    
        self.rowconfigure(0,minsize=20)
    
        self.update()

        x=self.grid_bbox(0, 0)[0]-padding[0]
        y=self.grid_bbox(0, 0)[1]+self.grid_bbox(0,0)[3]+padding[3]
        self.positionMenuFile=(x,y)
        x=self.grid_bbox(2, 0)[0]-padding[0]
        y=self.grid_bbox(0, 0)[1]+self.grid_bbox(0,0)[3]+padding[3]
        self.positionMenuHelp=(x,y)
    

    def menu_file(self,event):
        if not self.disabled :
            self.destroy_menus()
            menuFile=FrameMenuFile(app_class=self.app_class,position=self.positionMenuFile)
            self.menuList.append(menuFile)
            
    def menu_help(self,event):
        if not self.disabled :
            self.destroy_menus()
            menuHelp=FrameMenuHelp(app_class=self.app_class,position=self.positionMenuHelp)
            self.menuList.append(menuHelp)
            
        
    def destroy_menus(self,event=None):
        for m in self.menuList:
            m.destroy_menus()
            m.destroy()
            self.menuList.remove(m)
            

# ---------------------------------------------------------------------------------------------- 

class VolumeView():  
    def __init__(self,image_generator,origin,grid_size):  
        
        self.image_generator=image_generator
        self.origin=origin
        self.grid_size=grid_size
    
        # ------------------------------------------------------
        self.version='0.1'
        # ------------------------------------------------------
        self.nrrdfile=''
        self.nrrd=None
    
        if self.image_generator.volume.dtype == np.uint8 :
            self.nrrd=NRRD(3,"uint8",(self.image_generator.volume.shape[2],self.image_generator.volume.shape[1],self.image_generator.volume.shape[0]),"raw")
        else :
            self.nrrd=NRRD(3,"uint16",(self.image_generator.volume.shape[2],self.image_generator.volume.shape[1],self.image_generator.volume.shape[0]),"raw")
        self.nrrd.space="LAS"
        self.nrrd.data=self.image_generator.volume
        self.nrrd.spacedirections=((self.grid_size[0],0,0),(0,self.grid_size[1],0),(0,0,self.grid_size[2]))
        self.nrrd.spaceorigin=(self.origin[0],self.origin[1],self.origin[2])    

        # --- Settings  ----------------------------------------        
        self.settings=Settings()
        self.settings.print()
        
        self.scale_ratio=0.7  # Max. wiew
        
        # GUI settings
        self.padx_canvasx=(4,8)
        self.pady_canvasx=(8,4)
        
        self.padx_canvasy=(8,4)
        self.pady_canvasy=(8,4)
        
        self.padx_canvasz=(8,4)
        self.pady_canvasz=(4,8)
        
        # ------------------------------------------------------ 
        self.gui_root = tk.Tk()
        self.gui_root.withdraw()
        
    
        self.gui_root.title("Volume View")  
        
        self.gui_root.event_add('<<ControlOn>>',  '<KeyPress-Control_L>',   '<KeyPress-Control_R>')
        self.gui_root.event_add('<<ControlOff>>', '<KeyRelease-Control_L>', '<KeyRelease-Control_R>')
        self.gui_root.event_add('<<ShiftOn>>',    '<KeyPress-Shift_L>',     '<KeyPress-Shift_R>')
        self.gui_root.event_add('<<ShiftOff>>',   '<KeyRelease-Shift_L>',   '<KeyRelease-Shift_R>')

        # self.gui_root.bind('<<ControlOn>>', lambda e: control_key(True))
        # self.gui_root.bind('<<ControlOff>>', lambda e: control_key(False))
        # self.gui_root.bind('<<ShiftOn>>', lambda e: shift_key(True))
        # self.gui_root.bind('<<ShiftOff>>', lambda e: shift_key(False))
        
        self.gui_root.bind('<<ControlOn>>', ctrl_on)
        self.gui_root.bind('<<ControlOff>>', ctrl_off)
        self.gui_root.bind('<<ShiftOn>>', shift_on)
        self.gui_root.bind('<<ShiftOff>>', shift_off)
        
        
        self.gui_root.bind('<Key>', self.key)
        

        # ------------------------------------------------------
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Menu.TLabel',
            # font=('Helvetica', 8, 'bold')
            ) 
        self.style.map('Menu.TLabel',
              background=[
                    ('hover', '#3daee9')],
              foreground=[('hover', 'white')])         
        
            
        self.build_gui()
        
    
 
        self.gui_root.iconphoto(False,PhotoImage(file='volumeView-icon.png')) 
        self.gui_root.resizable(False,False)

        
        self.gui_root.mainloop() 
  
  
    # ------------------------------------------------------------------------------------------
    def build_gui(self):
        
        # ------------------------------------------------------
        #  | menuMain               |
        #  | frameCanvas | frameApp |
        
        
        self.menuMain=FrameMenuMain(self.gui_root,app_class=self)
        self.menuMain.grid(row=0,column=0,columnspan=2)
       
        
        self.set_max_scale() 
        self.scale=self.scale_ratio*self.max_scale
        self.image_generator.scale=self.scale
        self.set_frame_canvas()
        
        
        self.frameApp = FrameApp(self.gui_root)
        self.frameApp.grid(row=1,column=1,padx=(1,0),pady=(0,0),sticky=(tk.W, tk.N, tk.E, tk.S))
        
        self.set_frame_info()
        self.canvases=list()
        self.set_frame_processing()
        
        # ------------------------------------------------------
        self.cursorColorX=("green","red")
        self.cursorColorY=("blue","red")
        self.cursorColorZ=("blue","green")
        
        self.set_canvases()
        self.set_cocanvases()
        self.set_coframes()
        
        # ------------------------------------------------------
        self.gui_root.rowconfigure(0, weight=0)
        self.gui_root.rowconfigure(1, weight=1)
        self.gui_root.columnconfigure(0, weight=1)
        self.gui_root.columnconfigure(1, weight=0)
        # ------------------------------------------------------
        self.set_geometry()
        self.gui_root.deiconify()
        



    def resize_gui(self):
        
        self.scale=self.scale_ratio*self.max_scale
        self.image_generator.scale=self.scale
        self.canvasImgX.grid_forget()
        self.canvasImgY.grid_forget()
        self.canvasImgZ.grid_forget()
        self.set_canvases()
        self.set_cocanvases()
        self.set_coframes()
        self.set_geometry()

    # ------------------------------------------------------------------------------------------  
    def set_geometry(self):
         
        self.gui_root.update()
    
        w=self.gui_root.winfo_width()
        h=self.gui_root.winfo_height()
        W = self.gui_root.winfo_screenwidth()-self.settings.screen_padding[0]-self.settings.screen_padding[2]
        H = self.gui_root.winfo_screenheight()-self.settings.screen_padding[1]-self.settings.screen_padding[3]
        
        x=(W-w)//2
        y=(H-h)//2
        # y=self.settings.screen_padding[1]
   
        self.gui_root.geometry("+{}+{}".format(x,y))
        print("Root window geometry: {}x{}+{}+{}".format(w,h,x,y))
    # ------------------------------------------------------------------------------------------    

    def set_frame_canvas(self):
        self.frameCanvas = FrameCanvas(self.gui_root)
        self.frameCanvas.grid(row=1,column=0,rowspan=1,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.frameCanvas.grid_propagate(True)
        
    # ------------------------------------------------------------------------------------------
    def set_max_scale(self):
        self.max_width=self.gui_root.winfo_screenwidth()-self.settings.screen_padding[0]-self.settings.screen_padding[2]
        self.max_height=self.gui_root.winfo_screenheight()-self.settings.screen_padding[1]-self.settings.screen_padding[3]
        nz,ny,nx=self.image_generator.volume.shape
        h_window_manager_title=self.settings.wm_title_height
        h_main_menu=self.menuMain.winfo_height()
        h_paddings=self.pady_canvasy[0]+self.pady_canvasy[1]+self.pady_canvasz[0]+self.pady_canvasz[1]
        h_margins=4*self.settings.canvas_image_margin
        h_images=self.max_height-h_window_manager_title-h_main_menu-h_paddings-h_margins
        self.max_scale=h_images/(ny+nz)
        print("Max. scale:",self.max_scale)
        
    # ------------------------------------------------------------------------------------------

    def set_canvases(self):
    
        margin=self.settings.canvas_image_margin

        self.canvasImgX=CanvasImage(self.frameCanvas,margin=margin,cursor_color=self.cursorColorX,image_generator=self.image_generator,axis=0)
        self.canvasImgX.grid(row=0,column=1,padx=self.padx_canvasx,pady=self.pady_canvasx,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvasImgY=CanvasImage(self.frameCanvas,margin=margin,cursor_color=self.cursorColorY,image_generator=self.image_generator,axis=1)
        self.canvasImgY.grid(row=0,column=0,padx=self.padx_canvasy,pady=self.pady_canvasy,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvasImgZ=CanvasImage(self.frameCanvas,margin=margin,cursor_color=self.cursorColorZ,image_generator=self.image_generator,axis=2)
        self.canvasImgZ.grid(row=1,column=0,padx=self.padx_canvasz,pady=self.pady_canvasz,sticky=(tk.N, tk.S, tk.E, tk.W))
        self.canvases=(self.canvasImgX,self.canvasImgY,self.canvasImgZ)
        
        self.canvasImgX["background"]="#d9d9d9"
        self.canvasImgY["background"]="#d9d9d9"
        self.canvasImgZ["background"]="#d9d9d9"

        # self.canvasImgX["background"]="gold"
        # self.canvasImgY["background"]="gold"
        # self.canvasImgZ["background"]="gold"        
        
        self.canvasImgX.frameInfo=self.frameInfo
        self.canvasImgY.frameInfo=self.frameInfo
        self.canvasImgZ.frameInfo=self.frameInfo
        
        self.frameCanvas.update()
        self.frameApp.update()
        
        nz,ny,nx=self.image_generator.volume.shape
        h_main_menu=self.menuMain.winfo_height()
        h_paddings=self.pady_canvasy[0]+self.pady_canvasy[1]+self.pady_canvasz[0]+self.pady_canvasz[1]
        h_margins=4*self.settings.canvas_image_margin
        h_images=int(round((ny+nz)*self.scale))
        h_canvas_frame=h_images+h_margins+h_paddings
        h=h_main_menu+h_canvas_frame+2
        
        w_images=int(round((ny+nx)*self.scale))
        w_margins=4*self.settings.canvas_image_margin
        w_paddings=self.padx_canvasy[0]+self.padx_canvasy[1]+self.padx_canvasx[0]+self.padx_canvasx[1]
        w_canvas_frame=w_images+w_margins+w_paddings
        w_app_frame=self.frameApp.winfo_width()
        w=w_canvas_frame+w_app_frame+3
        
        self.gui_root.geometry("{}x{}".format(w,h))
        
        
    def reset_canvases(self):
        self.canvasImgX.grid_forget()
        self.canvasImgY.grid_forget()
        self.canvasImgZ.grid_forget()
        self.set_canvases()
        
    def set_frame_info(self):
        self.frameInfo=FrameInfo(self.frameApp,volume=self.image_generator.volume,index=self.image_generator.index,origin=self.origin,grid_size=self.grid_size)
        self.frameInfo.grid(row=0,column=0,pady=(6,0))
        self.frameInfo.update_frame(self.image_generator.index)
        
    def reset_frame_info(self):    
        self.frameInfo.grid_forget()
        self.set_frame_info()
        
    def set_frame_processing(self):
        self.frameProcessing=FrameProcessing(self.frameApp,image_generator=self.image_generator,index=self.image_generator.index,canvases=self.canvases)
        self.frameProcessing.grid(row=1,column=0,pady=(4,0),sticky="nswe")
    def reset_frame_processing(self):
        self.frameProcessing.grid_forget()
        self.set_frame_processing()

    def set_cocanvases(self):
         # === Coframes and cocanvases for joint updating ===========
        self.canvasImgX.cocanvases=(self.canvasImgY,self.canvasImgZ)
        self.canvasImgY.cocanvases=(self.canvasImgX,self.canvasImgZ)
        self.canvasImgZ.cocanvases=(self.canvasImgX,self.canvasImgY)
        self.frameProcessing.cocanvases=(self.canvasImgX,self.canvasImgY,self.canvasImgZ)
    def set_coframes(self):
        self.canvasImgX.coframes=(self.frameInfo,)
        self.canvasImgY.coframes=(self.frameInfo,)
        self.canvasImgZ.coframes=(self.frameInfo,)

    # ------------------------------------------------------------------------------------------

    def open(self):
        
        self.menuMain.destroy_menus()
        
        filePath = filedialog.askopenfilename(initialdir=self.settings.current_directory, title="Select a volume data file", filetypes=[("Numpy array", "*.npy"), ("J. Morita volume data", "*.vol"), ("All files", "*.*")])
        if filePath:
            extension=pathlib.Path(filePath).suffix
            stem=pathlib.Path(filePath).stem
            self.nrrdfile=stem+'.nrrd'
            self.settings.current_directory=pathlib.Path(filePath).parent
            
            if extension == '.npy' :
                print("Raw volume data")
                volume=np.load(filePath)
                index=[volume.shape[2]//2,volume.shape[1]//2,volume.shape[0]//2]
                flip=(1,1,-1)       
                
                testVol=TestVolume(volume.dtype)
                testVol.volume=volume
                nz,ny,nx=testVol.volume.shape
                testVol.sizes=(nx,ny,nz)
                testVol.xGridSize=1.0
                testVol.yGridSize=1.0
                testVol.zGridSize=1.0
                testVol.xMin=0
                testVol.yMin=0
                testVol.zMin=0
                
                if testVol.volume.dtype == np.uint8 :
                    self.nrrd=NRRD(3,"uint8",(testVol.volume.shape[2],testVol.volume.shape[1],testVol.volume.shape[0]),"raw")
                else :
                    self.nrrd=NRRD(3,"uint16",(testVol.volume.shape[2],testVol.volume.shape[1],testVol.volume.shape[0]),"raw")
        
                self.nrrd.space="LAS"
                self.nrrd.data=testVol.volume
                self.nrrd.spacedirections=((testVol.xGridSize,0,0),(0,testVol.yGridSize,0),(0,0,testVol.zGridSize))
                self.nrrd.spaceorigin=(testVol.xMin,testVol.yMin,testVol.zMin)
                
                self.origin=(0,-volume.shape[1]+1,0)
                self.grid_size=(1.0, 1.0,1.0)
                
            if extension == '.vol' :
                print("J. Morita volume data")
                jmVol=JmVolume(filePath)
                self.nrrd=jmVol.nrrd
                volume=jmVol.volume
                index=[volume.shape[2]//2,volume.shape[1]//2,volume.shape[0]//2]
                flip=(1,1,-1)
                
                self.origin=(jmVol.xMin,jmVol.yMin,jmVol.zMin)
                self.grid_size=(jmVol.xGridSize,jmVol.yGridSize,jmVol.zGridSize)
                
            scale=1.0
            self.image_generator=ImageGenerator(volume,index,flip,scale)  
            self.set_max_scale() 
            self.scale_ratio=0.7
            self.resize_gui()
        
            
    def create_test_volume(self,test_volume,data_type):
        self.menuMain.destroy_menus()            
 
        if test_volume == 'cone' and data_type == np.uint8 :
            self.nrrdfile='test-volume-cone-8bit.nrrd'
        if test_volume == 'cone' and data_type == np.uint16 :
            self.nrrdfile='test-volume-cone-16bit.nrrd'
        if test_volume == 'wiki' and data_type == np.uint8 :
            self.nrrdfile='test-volume-wiki.nrrd'
 
        testVol=TestVolume(data_type)
        if test_volume=='cone':
            testVol.cone(100)
            index=[100,50,100]
            flip=(1,1,-1)
            volume=testVol.volume
        if test_volume=='wiki':
            testVol.wiki()
            index=[200,200,200]
            flip=(1,1,-1)
            volume=testVol.volume   
            
        np.save("test-volume.npy", testVol.volume, allow_pickle=False) 
        
        if testVol.volume.dtype == np.uint8 :
            self.nrrd=NRRD(3,"uint8",(testVol.volume.shape[2],testVol.volume.shape[1],testVol.volume.shape[0]),"raw")
        else :
            self.nrrd=NRRD(3,"uint16",(testVol.volume.shape[2],testVol.volume.shape[1],testVol.volume.shape[0]),"raw")
            
        self.nrrd.space="LAS"
        self.nrrd.data=testVol.volume
        self.nrrd.spacedirections=((testVol.xGridSize,0,0),(0,testVol.yGridSize,0),(0,0,testVol.zGridSize))
        self.nrrd.spaceorigin=(testVol.xMin,testVol.yMin,testVol.zMin)
   
        self.origin=(testVol.xMin,testVol.yMin,testVol.zMin)
        self.grid_size=(testVol.xGridSize,testVol.yGridSize,testVol.zGridSize)
    
        
        
        scale=1.0
        self.image_generator=ImageGenerator(volume,index,flip,scale)  
        self.set_max_scale() 
        self.scale_ratio=0.7
    
        self.resize_gui()
        
    def export(self):
        self.menuMain.destroy_menus()   
        if self.nrrd != None :
            filePath =  filedialog.asksaveasfilename(initialdir = self.settings.current_directory, initialfile=self.nrrdfile, title = "Select a .nrrd file",filetypes = (("nrrd files","*.nrrd"),("all files","*.*")))
            if filePath:
                print("Volume will be exported as:",filePath) 
                self.settings.current_directory=pathlib.Path(filePath).parent
                print
                self.nrrd.write(filePath)

    def quit(self,event):
        
        self.settings.print()
        self.settings.write(self.settings.file_settings)
        self.gui_root.destroy()
 
 
    # ------------------------------------------------------------------------------------------
    
    def key(self,event):
        global ctrl, shift, ctrl_shift
        k = event.keysym
        #print(event.keycode, event.keysym, event.state)
        
        if ctrl_shift:
            print('Key: <Ctrl>+<Shift>+{}'.format(k))
        if ctrl:
            print('Key: <Ctrl>+{}'.format(k))
        if shift:
            print('Key: <Shift>+{}'.format(k))
        if not ctrl and not shift and not ctrl_shift :
            print("Key: {}".format(k))
            
        if k == 'q' or k == 'Q':
            self.quit(None)
        if k == 'Escape' :
            self.menuMain.destroy_menus()       
            
        if ctrl and k == 'o' :
            self.open()

        if ctrl and k == 's' :
            self.export()

        if ctrl and k == 't' : 
            self.create_test_volume('cone',np.uint8)
            
        if ctrl and k == 'Up':
            print("Scale up")
            self.scale_ratio+=0.1
            if self.scale_ratio>1.0 :
                self.scale_ratio=1.0
            print("Scale ratio:",self.scale_ratio)
            self.resize_gui()
            
        
        if ctrl and k == 'Down':
            print("Scale down")
            self.scale_ratio-=0.1
            if self.scale_ratio<0.5 :
                self.scale_ratio=0.5
            print("Scale ratio:",self.scale_ratio)
            self.resize_gui()
            

        if k == 'c' :
            self.canvasImgX.plot_cursor()
            self.canvasImgY.plot_cursor()
            self.canvasImgZ.plot_cursor()
        if k == 'd' :
            self.canvasImgX.delete_cursor()
            self.canvasImgY.delete_cursor()
            self.canvasImgZ.delete_cursor()   
          
          
# ----------------------------------------------------------------------------------------------         
#---------------------------------------------------------------
testVol=TestVolume(np.uint8)
testVol.cone(100)        
index=[100,50,100]
flip=(1,1,-1)
scale=1.0
volume=testVol.volume
origin=(testVol.xMin,testVol.yMin,testVol.zMin)
grid_size=(testVol.xGridSize,testVol.yGridSize,testVol.zGridSize)
img_generator=ImageGenerator(volume,index,flip,scale)   
#--------------------------------------------------------------- 
volumeView=VolumeView(img_generator,origin,grid_size)
# ---------------------------------------------------------------------------------------------- 

