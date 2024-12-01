"""
=======================================
Volume View - Volumetric Data Viewer
Test volume module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""


import numpy as np
import cv2 as cv
import math

class TestVolume():
    def __init__(self,dtype=np.uint8):
        self.dtype=dtype
        self.volume=None
        
    def cone(self,minor_radius): 
        """Create a tapered eliptical cone."""
        w=4*minor_radius+1
        h=2*minor_radius+1
        nx=w
        ny=h
        listImagesXY=[]
        for i in range(2*minor_radius,-1,-1):
            if self.dtype == np.uint16 :
                color = int((1 - i/(2*minor_radius))*65535)
            else:
                color = int((1 - i/(2*minor_radius))*255)
            img=np.zeros([ny,nx],dtype=self.dtype)
            center=(2*minor_radius,minor_radius)
            axesLength=(i,i//2)
            angle=0
            startAngle = 0
            endAngle = 360
            img=cv.ellipse(img, center, axesLength, angle, startAngle, endAngle, color, -1)
            img=cv.rectangle(img,(0,0),(w//5,h),0,-1)
            # img=cv.rectangle(img,(0,0),(w,h//5),0,-1)
            img=cv.rectangle(img,(0,h-h//5),(w,h),0,-1)
            listImagesXY.append(img)
            listImagesXY.append(img)
        self.volume=np.asarray(listImagesXY)
        nz=self.volume.shape[0]
        self.sizes=(nx,ny,nz)
        self.xGridSize=1.0
        self.yGridSize=1.0
        self.zGridSize=1.0
        
        self.xMin=-(nx-1)//2
        self.xMax=self.xMin+nx-1
        
        self.yMin=-(ny-1)//2
        self.yMax=self.yMin+ny-1
        
        self.zMin=0
        self.zMax=self.zMin+nz-1
    
    def wiki(self):
        nx=401
        ny=401
        nz=401
        listImagesXY=[]
        self.volume=np.zeros([nz,ny,nx],dtype=self.dtype)

        r=65
        r_major=105
        
        # Cylinder - Blue
        xc=310
        yc=90
        center_coordinates=(xc,yc)
        radius=r
        color=171 
        for iz in range(25,401-25):
            img=self.volume[iz,:,:]
            img = cv.circle(img, center_coordinates, radius, color, -1) 
            self.volume[iz,:,:]=img   
        
        # Cone - Green
        xc=90
        yc=90
        center_coordinates=(xc,yc)
        color=86
        for iz in range(25,25+2*r_major+1):
            radius=int(r-r/(2*r_major)*(iz-25))
            img=self.volume[iz,:,:]
            if radius > 0 :
                img = cv.circle(img, center_coordinates, radius, color, -1) 
            self.volume[iz,:,:]=img       
            
         
        # Sphere - Red
        xc=310-r
        yc=310
        center_coordinates=(xc,yc)
        color=255 
        for iz in range(25+r_major-r,25+r_major+r+1):
            rcostheta=(25+r_major-iz)
            radius=int(r*math.sin(math.acos(rcostheta/r)))
            img=self.volume[iz,:,:]
            if radius > 0 :
                img = cv.circle(img, center_coordinates, radius, color, -1) 
            self.volume[iz,:,:]=img 
            
        # Ellipsoid - Yellow
        xc=90
        yc=310
        center_coordinates=(xc,yc)
        color=20
        for iz in range(25,25+r_major+1):
            rmcostheta=(25+r_major-iz)
            radius=int(r*math.sin(math.acos(rmcostheta/r_major)))
            img=self.volume[iz,:,:]
            if radius > 0 :
                img = cv.circle(img, center_coordinates, radius, color, -1) 
            self.volume[iz,:,:]=img 

        # self.volume=self.volume[::-1,:,:]
        # self.volume=np.flip(self.volume,axis=0)

        self.sizes=(nx,ny,nz)
        self.xGridSize=1.0
        self.yGridSize=1.0
        self.zGridSize=1.0
        
        self.xMin=-(nx-1)//2
        self.xMax=self.xMin+nx-1
        
        self.yMin=-(ny-1)//2
        self.yMax=self.yMin+ny-1
        
        self.zMin=0
        self.zMax=self.zMin+nz-1
