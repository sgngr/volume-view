"""
=======================================
Volume View - Volumetric Data Viewer
Application settings module
=======================================
Version:    0.1
Author:     Sinan Güngör
License:    GPL v2
"""

import os

from lxml import etree

class Settings():
    def __init__(self):
        self.file_settings="settings.xml"    
        self.current_directory=None
        self.screen_padding=[10,10,10,50]
        self.canvas_image_margin=10
        self.wm_title_height=28
        
        if os.path.exists(self.file_settings):
            self.read(self.file_settings)
        else :
            self.current_directory=os.getcwd()
            self.write(self.file_settings)
        
    def read (self,file):
        tree=etree.parse(file)
        root=tree.getroot() 
        if root.find('current_directory') == None  :
            self.current_directory=os.getcwd()
        else :
            self.current_directory=root.find('current_directory').text
        if not  os.path.exists(self.current_directory) :
            self.current_directory=os.getcwd()
            
        self.screen_padding[0]=int(root.find('screen_padding_left').text) 
        self.screen_padding[1]=int(root.find('screen_padding_top').text)
        self.screen_padding[2]=int(root.find('screen_padding_right').text) 
        self.screen_padding[3]=int(root.find('screen_padding_bottom').text) 
        self.canvas_image_margin=int(root.find('canvas_image_margin').text) 
        self.wm_title_height=int(root.find('wm_title_height').text) 
        
    def write(self,file):
        root = etree.Element("settings")
        r=etree.SubElement(root,"current_directory").text="{}".format(self.current_directory)
        r=etree.SubElement(root,"screen_padding_left").text="{}".format(self.screen_padding[0])
        r=etree.SubElement(root,"screen_padding_top").text="{}".format(self.screen_padding[1])
        r=etree.SubElement(root,"screen_padding_right").text="{}".format(self.screen_padding[2])
        r=etree.SubElement(root,"screen_padding_bottom").text="{}".format(self.screen_padding[3])
        r=etree.SubElement(root,"canvas_image_margin").text="{}".format(self.canvas_image_margin)
        r=etree.SubElement(root,"wm_title_height").text="{}".format(self.wm_title_height)
        tree = etree.ElementTree(root)
        tree.write(file,encoding="utf-8", xml_declaration=True, pretty_print=True)

    def print(self):
        print("Application Settings:")
        print(" Last directory:",self.current_directory)
        print(" Screen padding:",self.screen_padding)
        print(" Canvas image margin:",self.canvas_image_margin)
        print(" Window manager title height:",self.wm_title_height)
        
if __name__=='__main__':
    settings=Settings()
    settings.print()
    settings.write(settings.file_settings)
