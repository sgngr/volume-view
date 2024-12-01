"""
=======================================
Volume View - Volumetric Data Viewer
NRRD module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""


import numpy as np

class NRRD():
    def __init__(self,dimension,dtype,sizes,encoding):
        self.dimension=dimension
        self.dtype=dtype
        self.encoding=encoding
        self.sizes=sizes
        # ---- Optional specifications 
        # space : "LAS", "RAS", "LPS", "scanner-xyz" 
        # space directions : a tuple value, e.g  ((1.0,0.0,0.0), (0.0,1.0,0.0), (0.0,0.0,1.0))
        # space origin : a tuple value, e.g. (0.0,0.0,0.0)
        self.space=None
        self.spacedirections=None
        self.spaceorigin=None
        self.data=None
            
    def create_test_volume_cone(self,r):
        w=2*r+1
        h=r+1
        nx=w
        ny=h
        listImagesXY=[]
        for i in range(r,-1,-1):
            color = int((1 - i/r)*255 )
            img=np.zeros([ny,nx],dtype=np.uint8)
            center=(r,r//2)
            axesLength=(i,i//2)
            angle=0
            startAngle = 0
            endAngle = 360
            img=cv.ellipse(img, center, axesLength, angle, startAngle, endAngle, color, -1)
            img=cv.rectangle(img,(0,0),(w//5,h),0,-1)
            img=cv.rectangle(img,(0,0),(w,h//5),0,-1)
            listImagesXY.append(img)
            listImagesXY.append(img)
        volume=np.asarray(listImagesXY)
        nz=volume.shape[0]
        self.dimension=3
        self.dtype="uint8"
        self.sizes=(nx,ny,nz)
        self.space="3D-right-handed"
        self.data=volume
        self.spacedirections=((1,0,0),(0,-1,0),(0,0,1))
        self.spaceorigin=(-r,r//2,0)
        
    def write(self,path):
        openedFile=open(path, 'wb')
        openedFile.write(b'NRRD0004\n')  
        openedFile.write(b'# Complete NRRD file format specification at:\n')  
        openedFile.write(b'# http://teem.sourceforge.net/nrrd/format.html\n')  
        
        dimension="dimension: {}\n".format(self.dimension)
        openedFile.write(bytes(dimension,"utf-8"))
        
        sizes="sizes: {} {} {}\n".format(self.sizes[0],self.sizes[1],self.sizes[2])
        openedFile.write(bytes(sizes,"utf-8"))
        
        dtype="type: {}\n".format(self.dtype)
        openedFile.write(bytes(dtype,"utf-8"))
        
        openedFile.write(b'endian: little\n') 
    
        encoding="encoding: {}\n".format(self.encoding)
        openedFile.write(bytes(encoding,"utf-8"))
        
        if self.space:
            space="space: {}\n".format(self.space)
            openedFile.write(bytes(space,"utf-8"))
        
        if self.spacedirections :
            spacedirections="space directions: ({},{},{}) ({},{},{}) ({},{},{})\n".format(self.spacedirections[0][0],self.spacedirections[0][1],self.spacedirections[0][2],self.spacedirections[1][0],self.spacedirections[1][1],self.spacedirections[1][2],self.spacedirections[2][0],self.spacedirections[2][1],self.spacedirections[2][2])
            openedFile.write(bytes(spacedirections,"utf-8"))
                
        if self.spaceorigin :
            spaceorigin="space origin: ({},{},{})\n".format(self.spaceorigin[0],self.spaceorigin[1],self.spaceorigin[2])
            openedFile.write(bytes(spaceorigin,"utf-8"))
        
        openedFile.write(b'kinds: domain domain domain\n') 
        
        if type(self.data) == np.ndarray :
            openedFile.write(b'\n') 
            openedFile.write(self.data.tobytes())
        openedFile.close()
