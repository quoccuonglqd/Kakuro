from __future__ import absolute_import
from tkinter import *
import os
from PIL import ImageTk,Image
from Component import Component
from Titlebar import Titlebar
from Menu import Menu 
from Playboard import Playboard
from Settingboard import Settingboard
from Custom_menu import Custom_menu

class MyMain(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.overrideredirect(1)
        self.attributes("-topmost",True)

    def on_close(self):
        self.master.destroy()


class NewRoot(Tk):    
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        self.mainwindow = MyMain(self)
        
    
class Application(object):
	HEIGHT = 597
	WIDTH = 805

	def __init__(self,master):
		self.master = master
		self.titlebar = Titlebar(self,self.master)
		self.settingboard = Settingboard(self,self.master)
		self.playboard = Playboard(self,self.master)
		self.custom_menu = Custom_menu(self,self.master)
		self.menu = Menu(self,self.master)
		

	def Run(self):
		window_height = Application.HEIGHT
		window_width = Application.WIDTH
		screen_width = self.master.winfo_screenwidth()
		screen_height = self.master.winfo_screenheight()
		x_cordinate = int((screen_width/2) - (window_width/2))
		y_cordinate = int((screen_height/2) - (window_height/2))
		self.master.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
		self.master.mainloop()

	def Close(self):
		self.master.on_close()

	def Transform(self):
		t = Algorithm()
		img = t.Color_space_convert(img=self.image_executer.pq[self.image_executer.it][0], src_cs = 'RGB', dst_cs = 'GRAY')
		self.image_executer.Transform(self.image_executer.pq[self.image_executer.it][0],img,'Gray scale')

rootManager = NewRoot()
app = Application(rootManager.mainwindow)
app.Run()
