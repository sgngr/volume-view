"""
=======================================
Volume View - Volumetric Data Viewer
Image generator module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v2
"""


from PIL import Image, ImageTk

from test_volume import *
                
class ImageGenerator():
    def __init__(self,volume,index,flip,scale):
        self.volume=volume 
        self.index=index
        self.flip=flip
        self.scale=scale
        
        print("Volume shape (nz,ny,nx):",self.volume.shape)
        self.size=(self.volume.shape[2],self.volume.shape[1],self.volume.shape[0])
        
        self.axis=0
        self.image=None
        self.images=[None,None,None]
        
        self.minValue=np.min(self.volume)
        self.maxValue=np.max(self.volume)
        
        if self.volume.dtype == np.uint16 :
            self.normalize=True
        else :
            self.normalize=False
            
        self.equalize_histogram=False

        self.create_image(self.index,self.axis)
    
    def create_image(self,index,axis):
        self.index=index
        if axis == 0 :
            arrImage=self.volume[:,:,self.index[0]]
            wh=(int(self.size[1]*self.scale),int(self.size[2]*self.scale))
        if axis == 1 :
            arrImage=self.volume[:,self.index[1],:]
            wh=(int(self.size[0]*self.scale),int(self.size[2]*self.scale))
        if axis == 2 :
            arrImage=self.volume[self.index[2],:,:]
            wh=(int(self.size[0]*self.scale),int(self.size[1]*self.scale))
                
        arrImage=cv.resize(arrImage, wh)
                
        if self.flip[axis] == 0 :
            arrImage=np.fliplr(arrImage)
        if self.flip[axis] == 1 :
            arrImage=np.flipud(arrImage)
    
        # == Image proccessing ===============================
            
        if self.normalize:
            
            print("Image proccessing: Normalize (NORM_MINMAX)")
            normalizedImg = np.zeros(arrImage.shape)
            arrImage_normalized=cv.normalize(arrImage, normalizedImg, 0, 255, cv.NORM_MINMAX)
            arrImage=arrImage_normalized
            # arrImage=np.asarray(arrImage//256,dtype=np.uint8)

        if self.equalize_histogram :
            
            print("Image proccessing: Histogram equalization")
            if arrImage.dtype == 'uint16' :
                if self.normalize == False :
                    arrImage=np.asarray(arrImage//256,dtype=np.uint8)
                arrImage = cv.equalizeHist(np.asarray(arrImage,dtype=np.uint8))
            else:
                
                arrImage = cv.equalizeHist(arrImage)
            
        self.image=Image.fromarray(arrImage)
    
    def create_images(self,index):
        
        for axis in range(3):
            if axis == 0 :
                arrImage=self.volume[:,:,self.index[0]]
                wh=(int(self.size[1]*self.scale),int(self.size[2]*self.scale))
            if axis == 1 :
                arrImage=self.volume[:,self.index[1],:]
                wh=(int(self.size[0]*self.scale),int(self.size[2]*self.scale))
            if axis == 2 :
                arrImage=self.volume[self.index[2],:,:]
                wh=(int(self.size[0]*self.scale),int(self.size[1]*self.scale))
                
            arrImage=cv.resize(arrImage, wh)
                
            if self.flip[axis] == 0 :
                arrImage=np.fliplr(arrImage)
            if self.flip[axis] == 1 :
                arrImage=np.flipud(arrImage)
            
            # == Image proccessing ===============================
            
            if self.normalize:
                normalizedImg = np.zeros(arrImage.shape)
                arrImage_normalized=cv.normalize(arrImage, normalizedImg, 0, 255, cv.NORM_MINMAX)
                arrImage=arrImage_normalized
                # arrImage=np.asarray(arrImage//256,dtype=np.uint8)

            if self.equalize_histogram :
                if arrImage.dtype == 'uint16' :
                    if self.normalize == False :
                        arrImage=np.asarray(arrImage//256,dtype=np.uint8)
                    arrImage = cv.equalizeHist(np.asarray(arrImage,dtype=np.uint8))
                else:
                    arrImage = cv.equalizeHist(arrImage)
            
            image=Image.fromarray(arrImage)
            self.images[axis]=image

if __name__ == "__main__":
    
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

    imageGenerator=ImageGenerator(volume,index,flip,scale)
    
    # ===  Generate images ==========
    axis=0
    imageGenerator.create_image(index,axis)
    imageX=imageGenerator.image
    
    axis=1
    imageGenerator.create_image(index,axis)
    imageY=imageGenerator.image
    
    axis=2
    imageGenerator.create_image(index,axis)
    imageZ=imageGenerator.image
    
    

    
    # ===  Display images ==========

    import tkinter as tk
    
#     def handle_key(event):
#                 
#         i,j,k=index
#         nz,ny,nx=volume.shape
#         
#         ks = event.keysym
#         print("Key: {k}".format(k=ks))
#         if ks == 'q' or ks == 'Q':
#             quit()    
    
    axis=0
    i,j,k=index
    nz,ny,nx=volume.shape
    
    
    def key(event):
        
        global axis
        global index
        global i
        global j
        global k
        
        ks=event.keysym
        print("Key:",ks)
        if ks == 'q':
            root.destroy()

        if ks ==  'Left' :
            axis-=1
            if axis < 0 :
                axis=2
            print("Axis:",axis)
        if ks ==  'Right' :
            axis+=1
            if axis > 2 :
                axis=0
            print("Axis:",axis)

        if ks == 'Up' :
            if axis == 0 :
                if i < nx -1 :
                    i+=1
            
            if axis == 1 :
                if j < ny -1 :
                    j+=1
                    
            if axis == 2 :
                if k < nz-1 :
                    k+=1
    
            index=[i,j,k]
            print("Index:",i,j,k)
    
            update_images()
            
        
        if ks == 'Down' :
            if axis == 0 :
                if i > 1 :
                    i-=1
            
            if axis == 1 :
                if j > 1 :
                    j-=1
                    
            if axis == 2 :
                if k > 1 :
                    k-=1

            index=[i,j,k]
            print("Index:",i,j,k)
            
            update_images()
              
    
    def update_images():
        
        imageGenerator.create_image(index,0)
        imageX=imageGenerator.image
        root.imageX=ImageTk.PhotoImage(image=imageX)
        
        imageGenerator.create_image(index,1)
        imageY=imageGenerator.image
        root.imageY=ImageTk.PhotoImage(image=imageY)
        
        imageGenerator.create_image(index,2)
        imageZ=imageGenerator.image
        root.imageZ=ImageTk.PhotoImage(image=imageZ)
    
    
        labelImageX["image"]=root.imageX
        labelImageY["image"]=root.imageY
        labelImageZ["image"]=root.imageZ
    
    root = tk.Tk()
    root.title("Image generator")
    root.bind('<Key>', key)
 

    
    # PhotoImage     
    root.imageX=ImageTk.PhotoImage(image=imageX)
    root.imageY=ImageTk.PhotoImage(image=imageY)
    root.imageZ=ImageTk.PhotoImage(image=imageZ)
    
    labelImageX=tk.Label(root,image=root.imageX)
    labelImageY=tk.Label(root,image=root.imageY)
    labelImageZ=tk.Label(root,image=root.imageZ)
        
    labelImageX.grid(row=0,column=0)
    labelImageY.grid(row=0,column=1)
    labelImageZ.grid(row=0,column=2)
    
    root.mainloop()
