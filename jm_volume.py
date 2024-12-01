"""
=======================================
Volume View - Volumetric Data Viewer
J. Morita volume data module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v3
"""

import os.path
import numpy as np
import math
import cv2 as cv
from lxml import etree


from nrrd import *

#------------------------------------------------------------------

class JmVolume():
    def __init__(self,path):
        if os.path.isfile(path):
            self.exists=True
            self.path=path
        
            openedFile=open(self.path, 'rb')
            allBytes=openedFile.read()
            openedFile.close()
            
            b=allBytes.find(b'<?xml')
            e=allBytes.find(b'</JmVolume>')+11
        
            self.headerBytes=allBytes[b:e]
            self.headerXml=etree.fromstring(self.headerBytes)
                        
            b=allBytes.find(b'Array3D')+7
            limits=np.frombuffer(allBytes[b:b+24],dtype=np.dtype('int32')).tolist()
            self.xmin=limits[0]
            self.xmax=limits[1]
            self.ymin=limits[2]
            self.ymax=limits[3]
            self.zmin=limits[4]
            self.zmax=limits[5]
            self.sizes=(self.xmax-self.xmin+1,self.ymax-self.ymin+1,self.zmax-self.zmin+1)
            
            b=allBytes.find(b'Array3D')+7+24
            self.volumeBytes=allBytes[b:]
            self.volume=np.frombuffer(allBytes[b:],dtype=np.dtype('uint16')).reshape(self.sizes)
            
            self.volume=self.volume.swapaxes(0,2)
            
            self.parse_header()
            
            self.convert_nrrd()
            
        else:
            self.exists=False

    def print_header(self):
        xml = etree.tostring(self.headerXml, pretty_print=True)
        print(xml.decode(), end='')
    
    def parse_header(self):
        attribute=self.headerXml.find('Attribute')
        self.xGridSize=float(attribute.find('tfXGridSize').values()[0])
        self.yGridSize=float(attribute.find('tfYGridSize').values()[0])
        self.zGridSize=float(attribute.find('tfZGridSize').values()[0])
        self.xCenter=int(attribute.find('tfXCenter').values()[0])
        self.yCenter=int(attribute.find('tfYCenter').values()[0])
        self.zCenter=int(attribute.find('tfZCenter').values()[0])
        
        fyi=self.headerXml.find('FYI')
        self.xMin=int(fyi.find('XMin').values()[0])
        self.yMin=int(fyi.find('YMin').values()[0])
        self.zMin=int(fyi.find('ZMin').values()[0])
        self.xMax=int(fyi.find('XMax').values()[0])
        self.yMax=int(fyi.find('YMax').values()[0])
        self.zMax=int(fyi.find('ZMax').values()[0])
        
    
    def rotate_image(self,image,center,angle,size,color):
        """Rotate image using padding."""
        rotate_matrix = cv.getRotationMatrix2D(center=center, angle=angle, scale=1)    
        return cv.warpAffine(src=image, M=rotate_matrix, dsize=size, borderMode=cv.BORDER_CONSTANT, borderValue=color)
    
    def rotate(self,angle):
        """Rotate volume along the longitudinal axis."""   
        listHorizontalImages=[]
        h,w = self.volume.shape[1:] 
        # Odd numbers are expected
        center=(w//2,h//2)
        size=(w,h)
        
        for iz in range(self.volume.shape[0]):
            imgHorizontal=self.volume[iz,:,:]
            color=int(imgHorizontal[0,0])
            imgHorizontal_rotated=self.rotate_image(imgHorizontal,center,angle,size,color)
            listHorizontalImages.append(imgHorizontal_rotated)
        self.volume=np.asarray(listHorizontalImages)
        self.convert_nrrd()
    
    def cut(self,axis,index0,index1):
        """Cut out volume parts which are  outside a range)"""
        if index0 < 0 :
            index0 = 0
        if index1 > self.sizes[axis]:
            index1 = self.sizes[axis]    
            
        if index1-index0 > 1 :
            if axis == 0:
                self.volume=self.volume[:,:,index0:index1]
                self.xmin=self.xmin+index0
                self.xmax=self.xmin+index1-index0-1
            if axis == 1:
                self.volume=self.volume[:,index0:index1,:]
                self.ymin=self.ymin+index0
                self.ymax=self.ymin+index1-index0-1
            if axis == 2:
                self.volume=self.volume[index0:index1,:,:]
                self.zmin=self.zmin+index0
                self.zmax=self.zmin+index1-index0-1
                
        self.convert_nrrd()
    
    def convert_nrrd(self):
        self.nrrd=NRRD(3,"uint16",(self.volume.shape[2],self.volume.shape[1],self.volume.shape[0]),"raw")
        self.nrrd.space="LAS"
        self.nrrd.data=self.volume
        self.nrrd.spacedirections=((self.xGridSize,0,0),(0,self.yGridSize,0),(0,0,self.zGridSize))
        self.nrrd.spaceorigin=(self.xmin*self.xGridSize, self.ymin*self.yGridSize, self.zmin*self.zGridSize)
   
        
if __name__=='__main__':
    jmVolume=JmVolume("CT_0.vol")
    if jmVolume.exists:
        print("Jm Volume path:",jmVolume.path)
        print("Sizes:",jmVolume.sizes)
        print("Shape of volume data array:",jmVolume.volume.shape)
        # jmVolume.print_header()
        jmVolume.rotate(-45.88)
        jmVolume.cut(2,0,141)
        np.save("jm-volume.npy", jmVolume.volume, allow_pickle=False) 
        jmVolume.nrrd.write("jm-volume.nrrd")
        print("NRRD shape:", jmVolume.nrrd.data.shape)


