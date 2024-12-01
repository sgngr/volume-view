"""
=======================================
Volume View - Volumetric Data Viewer
Canvas module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import tkinter as tk
import numpy as np
import cv2 as cv

import platform

from PIL import ImageTk


class CanvasImage(tk.Canvas):

    def __init__(self, *args, **kwargs):
        self.margin=kwargs["margin"]
        self.cursor_color=kwargs["cursor_color"]
        self.image_generator=kwargs["image_generator"]
        self.axis=kwargs["axis"]
        
        self.index=self.image_generator.index
        self.scale=self.image_generator.scale
        self.volume=self.image_generator.volume
        self.flip=self.image_generator.flip
        
        self.size=self.image_generator.size
        
        self.cursor=[0,0]
        
        # === Cowidgets / Coframes ============

        self.cocanvases=()
        self.coframes=()

        # === Determine size and init canvsas ==========
        self.get_image()
        self.width=self.image.width+2*self.margin
        self.height=self.image.height+2*self.margin
        super().__init__(*args,width=self.width,height=self.height,bd=0,highlightthickness=0,relief="flat")
        # print("Canvas size: {}x{}".format(self.width,self.height))
        # --- Draw canvas border and image area markers
        
        self.create_line(0,0,self.width,0,tags="hmin",fill="white")
        self.create_line(0,self.height-1,self.width,self.height-1,tags="hmax",fill="white")       
        self.create_line(0,0,0,self.height-1,tags="vmin",fill="white")
        self.create_line(self.width-1,0,self.width-1,self.height,tags="vmax",fill="white")
    
        self.create_line(0,self.margin,self.margin//2,self.margin,fill="white")
        self.create_line(0,self.height-self.margin-1,self.margin//2,self.height-self.margin-1,fill="white")
        self.create_line(self.width-self.margin//2-1,self.margin,self.width,self.margin,fill="white")
        self.create_line(self.width-self.margin//2-1,self.height-self.margin-1,self.width,self.height-self.margin-1,fill="white")
        
        self.create_line(self.margin,0,self.margin,self.margin//2,fill="white")
        self.create_line(self.margin,self.height-self.margin//2-1,self.margin,self.height ,fill="white")        
        self.create_line(self.width-self.margin-1,0,self.width-self.margin-1,self.margin//2,fill="white")
        self.create_line(self.width-self.margin-1,self.height-self.margin//2-1,self.width-self.margin-1,self.height ,fill="white")
        
        # --- Update canvas 
        self.index_to_cursor()
        self.update_cursor()
        self.update_canvas(self.index,dragging=False,joint_update=True)

        # --- Bindings 
        self.bindings()

    def bindings(self):
        self.tag_bind("cursor_h", "<Enter>", self.h_enter)
        self.tag_bind("cursor_h", "<Leave>", self.h_leave)

        self.tag_bind("cursor_v", "<Enter>", self.v_enter)
        self.tag_bind("cursor_v", "<Leave>", self.v_leave)       
  
        self.tag_bind("cursor_h","<Button-1>", self.drag_start)
        self.tag_bind("cursor_h", "<B1-Motion>", self.drag_motion_h)
        self.tag_bind("cursor_h","<ButtonRelease-1>", self.drag_stop)
        
        self.tag_bind("cursor_v","<Button-1>", self.drag_start)
        self.tag_bind("cursor_v", "<B1-Motion>", self.drag_motion_v)
        self.tag_bind("cursor_v","<ButtonRelease-1>", self.drag_stop)
        
        #linux scroll
        self.bind("<Button-4>", self.roll_forward)
        self.bind("<Button-5>", self.roll_backward)
        #windows scroll
        self.bind("<MouseWheel>", self.roll)  
  
        self.bind('<Double Button-1>',self.set_index)

    # === Update function ============== 
    def update_canvas(self,index,dragging=False,joint_update=False):
        self.index=index
        self.show_image()
        if dragging==False:
            self.plot_cursor() 
        if joint_update == True :
            for canvas in self.cocanvases:
                canvas.update_canvas(self.index)
            for frame in self.coframes:
                frame.update_frame(self.index)
    # === Functions ====================
    def get_image(self):
        self.image_generator.create_image(self.index,self.axis)
        self.image=self.image_generator.image
        
    def show_image(self):
        self.get_image()
        self.imgTk = ImageTk.PhotoImage(image=self.image) 
        self.create_image(self.margin,self.margin,tags="image",anchor=tk.NW,image=self.imgTk)

    def index_to_cursor(self):
        i,j,k=self.index
        nx,ny,nz=self.size
                
        if self.axis == 0 :
            if self.flip[0] == 0 :
                x=(1-j/ny)*self.image.width
            else:
                x=j/ny*self.image.width
            if self.flip[0] == 1 :
                y=(1-k/nz)*self.image.height
            else :
                y=k/nz*self.image.height
                
        if self.axis == 1 :
            if self.flip[1] == 0 :
                x=(1-i/nx)*self.image.width
            else :
                x=i/nx*self.image.width
            if self.flip[1] == 1 :
                y=(1-k/nz)*self.image.height
            else :
                y=k/nz*self.image.height   
                
        if self.axis == 2 :
            if self.flip[2] == 0 :
                x=(1-i/nx)*self.image.width
            else :
                x=i/nx*self.image.width
            if self.flip[2] == 1 :   
                y=(1-j/ny)*self.image.height
            else :
                y=j/ny*self.image.height
                
        self.cursor=[int(round(x)),int(round(y))]
    
        
    def cursor_to_index(self):
        i,j,k=self.index
        nx,ny,nz=self.size
    
        x=self.cursor[0]
        y=self.cursor[1]
        scale=self.scale
    
        if self.axis == 0 :
            if self.flip[0]==0 :
                j=int(ny-x/scale)
            else :
                j=int(x/scale)
            if self.flip[0]==1 :
                k=int(nz-y/scale)
            else :
                k=int(y/scale)
            
        if self.axis == 1 :
            if self.flip[1]==0 :
                i=int(nx-x/scale)
            else :
                i=int(x/scale)
            if self.flip[1]==1 :
                k=int(nz-y/scale)
            else :
                k=int(y/scale) 
            
        if self.axis == 2 :
            if self.flip[2]==0 :
                i=int(nx-x/scale)
            else :
                i=int(x/scale)
            if self.flip[2]==1 :
                j=int(ny-y/scale)
            else :
                j=int(y/scale)  
        
        if i <  0 :
            i=0
        if j <  0 :
            j=0 
        if k <  0 :
            k=0    
    
        if i > nx -1 :
            i=nx-1
        if j > ny -1 :
            j=ny-1
        if k > nz -1 :
            k=nz-1

        self.index=[i,j,k]
        
    
    def delete_cursor(self):
        self.delete('cursor_h')
        self.delete('cursor_v')
        
    def update_cursor(self):
        cursor0=self.cursor
        self.index_to_cursor()
        dx=self.cursor[0]-cursor0[0]
        dy=self.cursor[1]-cursor0[1]
        self.move(self.find_withtag("cursor_v"),0,dx)
        self.move(self.find_withtag("cursor_h"),0,dy)
    
   
    def plot_cursor(self):
        self.delete_cursor()        
        self.index_to_cursor()
                
        x=self.cursor[0]
        y=self.cursor[1]
 
        xq=1
        yq=1
        if platform.system()=="Linux" :
            xq=2
            yq=2
        x1=1
        y1=y+self.margin
        x2=self.width-xq
        y2=y+self.margin
        self.create_line(x1,y1,x2,y2,tags="cursor_h",fill=self.cursor_color[1])
            
        x1=x+self.margin
        y1=1       
        x2=x+self.margin
        y2=self.height-yq
        self.create_line(x1,y1,x2,y2,tags="cursor_v",fill=self.cursor_color[0]) 

    # === Handler functions
    
    def set_index(self,event):
        
        on_image=True
        if (event.x < self.margin+1 ) or (event.x > self.margin+self.image.width) :
            on_image = False
            
        if (event.y < self.margin+1 ) or (event.y > self.margin+self.image.height) :
            on_image = False
    
        if on_image :
            self.x=event.x-self.margin
            self.y=event.y-self.margin
            self.cursor=[self.x,self.y]    
            self.cursor_to_index()
            self.update_canvas(self.index,joint_update=True)

    def roll(self,event):
        if (event.delta > 0):
            self.roll_forward(event)
        elif (event.delta < 0):
            self.roll_backward(event)

    def roll_forward(self,event):
        if self.axis==0:
            self.index[0]+=1
            if self.index[0] >= self.size[0] :
                self.index[0]=self.size[0]-1 
        if self.axis==1:
            self.index[1]+=1
            if self.index[1] >= self.size[1] :
                self.index[1]=self.size[1]-1         
        if self.axis==2:
            self.index[2]+=1
            if self.index[2] >= self.size[2] :
                self.index[2]=self.size[2]-1 

        self.update_canvas(self.index,joint_update=True)
        


    def roll_backward(self,event):
        if self.axis==0:
            self.index[0]-=1
            if self.index[0] < 0 :
                self.index[0]=0
        if self.axis==1:
            self.index[1]-=1
            if self.index[1] < 0 :
                self.index[1]=0
        if self.axis==2:
            self.index[2]-=1
            if self.index[2] < 0 :
                self.index[2]=0
                
        self.update_canvas(self.index,joint_update=True)
       
        
    def h_enter(self,event):
        self.config(cursor="sb_v_double_arrow")
    def h_leave(self,event):
        self.config(cursor="")
    def v_enter(self,event):
        self.config(cursor="sb_h_double_arrow")
    def v_leave(self,event):
        self.config(cursor="")
    
    def drag_start(self,event):
        self.lastmouse=[event.x,event.y]
        self.dragging=True
    
    def drag_stop(self,event):
        self.plot_cursor()


    def drag_motion_h(self,event):
        dx=event.x-self.lastmouse[0]
        dy=event.y-self.lastmouse[1]
        
        if (event.y < self.margin+1 ) or (event.y > self.margin+self.image.height) :
            self.dragging = False
            
        if self.dragging :
            self.lastmouse=[event.x,event.y]
            self.cursor[1]+=dy
            self.move(self.find_withtag("cursor_h"),0,dy)
            self.cursor_to_index()
            self.update_canvas(self.index,dragging=True,joint_update=True)
            self.tag_raise("cursor_h")
            self.tag_raise("cursor_v")
            
        
    def drag_motion_v(self,event):
        dx=event.x-self.lastmouse[0]
        dy=event.y-self.lastmouse[1]
        
        if (event.x < self.margin+1 ) or (event.x > self.margin+self.image.width) :
            self.dragging = False
        if self.dragging :
            self.lastmouse=[event.x,event.y]  
            self.cursor[0]+=dx
            self.move(self.find_withtag("cursor_v"),dx,0)
            self.cursor_to_index()
            self.update_canvas(self.index,dragging=True,joint_update=True)
            self.tag_raise("cursor_h")
            self.tag_raise("cursor_v")


if __name__ == "__main__":
    
    from tkinter import ttk
    
    from test_volume import *
    from image_generator import *
    
    class FrameInfo(ttk.Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
            
            self['relief'] = 'raised'
            self['padding'] = (5,5,5,5)
            self.columnconfigure(0,weight=1) # fill horizontally
            
            self.volume=kwargs["volume"]
            self.index=kwargs["index"]
            
            self.labelIndex=tk.Label(self,text="Index: ")
            self.labelIndex.grid()   
            self.labelIntensity=tk.Label(self,text="Intensity: ")
            self.labelIntensity.grid()
            
            self.update_frame(self.index)
            
        def update_frame(self,index,joint_update=False): 
            self.index=index
            self.intensity=self.volume[self.index[2],self.index[1],self.index[0]]
            self.labelIndex["text"]="Index: {}  {}  {}".format(self.index[0],self.index[1],self.index[2])
            self.labelIntensity["text"]="Intensity: {} ".format(self.intensity)
           
   
    class FrameScale(ttk.Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
        
            self.columnconfigure(0, weight=1) # fill horizontally
            
            self.axis=0
            if 'axis' in kwargs.keys() :
                self.axis=kwargs["axis"]
            self.index=[0,0,0]
            if 'index' in kwargs.keys() :
                self.index=kwargs["index"]
            
            # === Cowidgets / Coframes ============

            self.coconvases=[]
            self.coframes=[]
            
            # === Scale ============
            self.var_min=0
            if 'value_min' in kwargs.keys() :
                self.value_min=kwargs["value_min"]
            
            self.value_max=100
            if 'value_max' in kwargs.keys() :
                self.value_max=kwargs["value_max"]
            
            self.variable=tk.IntVar()
            self.variable.set(50)
            if 'value' in kwargs.keys() :
                self.variable.set(int(kwargs["value"]))
        
            self.scale=ttk.Scale(self, variable = self.variable, from_ = self.value_min, to = self.value_max)
            self.scale.grid(row=0,column=0,padx=(0,0),sticky=tk.EW)
            self.scale["command"]=self.set_variable
            
        def set_variable(self,variable):
            self.index[self.axis]=self.variable.get()
            self.update_frame(self.index,joint_update=True)
            
        def update_frame(self,index,joint_update=False):
            self.index=index
            self.variable.set(self.index[self.axis])
            if joint_update == True:
                for frame in self.coframes :
                    frame.update_frame(self.index)
                for canvas in self.cocanvases :
                    canvas.update_canvas(self.index)
   
    class FrameMain(ttk.Frame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
            index=kwargs["index"]
            self.update_frame(index)
        def update_frame(self,index,joint_update=False):    
            self.index=index
            self.i=index[0]
            self.j=index[1]
            self.k=index[2]
            
    def handle_key(event):
        
        global axis_selected
        global index
        
        i,j,k=index
        nz,ny,nx=volume.shape
        
        ks = event.keysym
        print("Key: {k}".format(k=ks))
        if ks == 'q' or ks == 'Q':
            quit()
        if ks == 'c' :
            for canvas in canvases:
                if canvas != None:
                    canvas.plot_cursor()

        if ks == 'd' :
            for canvas in canvases:
                if canvas != None:
                    canvas.delete_cursor()

  

    #  === Create test volume ==================================
    # Create 8bit test volume 
    testVol=TestVolume(np.uint8)
    testVol.cone(100)
    # testVol.wiki()
    
    np.save("test-volume.npy", testVol.volume, allow_pickle=False) 
    volume=np.load("test-volume.npy")
        
    
    index=[100,100,100]
    intensity=volume[index[2],index[1],index[0]]
    flip=(1,1,1)
    scale=1.0
    img_generator=ImageGenerator(volume,index,flip,scale)
    
    
    # === Root window ==========================================

    root = tk.Tk()
    root.title("Volume View")
    root.bind('<Key>', handle_key)
    
    
    # ==== Frames and Canvas ===================================
    
    
    frameMain=FrameMain(root,index=index)
    frameInfo=FrameInfo(frameMain,index=index,volume=volume)  
    
    margin=10
    cursor_color=("green","red")
    canvasImgX=CanvasImage(frameMain,margin=margin,cursor_color=cursor_color,image_generator=img_generator,axis=0)
    cursor_color=("blue","red")
    canvasImgY=CanvasImage(frameMain,margin=margin,cursor_color=cursor_color,image_generator=img_generator,axis=1)
    cursor_color=("blue","green")
    canvasImgZ=CanvasImage(frameMain,margin=margin,cursor_color=cursor_color,image_generator=img_generator,axis=2)
      
    # canvasImgX["background"]="gold"
    # canvasImgY["background"]="gold"
    # canvasImgZ["background"]="gold"
   
    nz,ny,nx=volume.shape
    i,j,k=index
    frameScaleX=FrameScale(frameMain,axis=0,value_min=0,value_max=nx-1,value=i,index=index)
    frameScaleY=FrameScale(frameMain,axis=1,value_min=0,value_max=ny-1,value=j,index=index)
    frameScaleZ=FrameScale(frameMain,axis=2,value_min=0,value_max=nz-1,value=k,index=index)
   
    # === Sytle and Layout =====================================
    style=ttk.Style()
    style.theme_use('clam')
    
    frameMain.grid()
    frameInfo.grid(row=0,column=0,columnspan=3,padx=(10,10),pady=(10,5),sticky=(tk.NW,tk.SE))
    canvasImgX.grid(row=1,column=0,padx=(10,5),pady=(5,5))
    canvasImgY.grid(row=1,column=1,padx=(5,5),pady=(5,5))
    canvasImgZ.grid(row=1,column=2,padx=(5,10),pady=(5,5))
    
    frameScaleX.grid(row=2,column=0,padx=(10,5),pady=(0,10),sticky=tk.EW)
    frameScaleY.grid(row=2,column=1,padx=(5,5),pady=(0,10),sticky=tk.EW)
    frameScaleZ.grid(row=2,column=2,padx=(5,10),pady=(0,10),sticky=tk.EW)
    
    # === Coframes and cocanvases for joint updating ===========
    
    canvasImgX.cocanvases=(canvasImgY,canvasImgZ)
    canvasImgY.cocanvases=(canvasImgX,canvasImgZ)
    canvasImgZ.cocanvases=(canvasImgX,canvasImgY)
    canvasImgX.coframes=(frameMain,frameInfo,frameScaleX,frameScaleY,frameScaleZ)
    canvasImgY.coframes=(frameMain,frameInfo,frameScaleX,frameScaleY,frameScaleZ)
    canvasImgZ.coframes=(frameMain,frameInfo,frameScaleX,frameScaleY,frameScaleZ)
   
    frameScaleX.coframes=(frameInfo,)
    frameScaleY.coframes=(frameInfo,)
    frameScaleZ.coframes=(frameInfo,)
    frameScaleX.cocanvases=(canvasImgX,canvasImgY,canvasImgZ)
    frameScaleY.cocanvases=(canvasImgX,canvasImgY,canvasImgZ)
    frameScaleZ.cocanvases=(canvasImgX,canvasImgY,canvasImgZ)
    
    # === Canvases =============================================
    
    canvases=(canvasImgX,canvasImgY,canvasImgZ)
   
    # === Run ==================================================
    root.mainloop()
    


