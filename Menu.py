r"""Date: 12/3/2020
    Author: Nguyen Quoc Cuong
"""
from tkinter import *
import os
from PIL import ImageTk,Image
from Component import Component

class Menu(Component):
	BACKGROUND_PATH = 'image/unnamed.jpg'
	HEIGHT = 600
	WIDTH = 805
	FONT_PATH = 'Font/arialbd.ttf'
	TEXT_SIZE = 19
	PLAY_BBOX = (320,140,530,180)
	CUSTOM_BBOX = (320,210,530,250)
	HELP_BBOX = (320,280,530,320)
	QUIT_BBOX = (320,350,530,390)
	PLAY_POS = (425,160)
	CUSTOM_POS = (421,230)
	HELP_POS = (425,300)
	QUIT_POS = (425,370)
	BUTTON_BG = "#9caaad"
	CHOSENBUTTON_BG = "#eb073c"
	NORMALBUTTON_BG = "#2c17b3"
 
	def __init__(self,master):
		super(Menu,self).__init__(master)

		self.backgroundimg = ImageTk.PhotoImage(Image.open(Menu.BACKGROUND_PATH).resize((Menu.WIDTH,Menu.HEIGHT),Image.ANTIALIAS))
		self.canvas = Canvas(self, highlightthickness=0,width = Menu.WIDTH,height = Menu.HEIGHT)
		self.canvas.grid(row=0, column=0)
		self.bg = self.canvas.create_image(0, 0, anchor=NW, image=self.backgroundimg)

		self.playbut = self.Round_rectangle(Menu.PLAY_BBOX)
		self.custombut = self.Round_rectangle(Menu.CUSTOM_BBOX)
		self.helpbut = self.Round_rectangle(Menu.HELP_BBOX)
		self.quitbut = self.Round_rectangle(Menu.QUIT_BBOX)
		self.playtext = self.canvas.create_text(Menu.PLAY_POS[0],Menu.PLAY_POS[1],text="PLAY",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.CHOSENBUTTON_BG)
		self.customtext = self.canvas.create_text(Menu.CUSTOM_POS[0],Menu.CUSTOM_POS[1],text="CUSTOM",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.helptext = self.canvas.create_text(Menu.HELP_POS[0],Menu.HELP_POS[1],text="HELP",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.quittext = self.canvas.create_text(Menu.QUIT_POS[0],Menu.QUIT_POS[1],text="QUIT",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.chosenid = 0

		self.textmap = {
		    0 : self.playtext,
		    1 : self.customtext,
		    2 : self.helptext,
		    3 : self.quittext
		}

		self.grid(row=1,column=0,columnspan=3)
		self.bind_all("<Key>",self.Keypress)
		self.canvas.tag_bind(self.playtext,"<Motion>",lambda event,id=0:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.customtext,"<Motion>",lambda event,id=1:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.helptext,"<Motion>",lambda event,id=2:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.quittext,"<Motion>",lambda event,id=3:
			                                   self.Mouse_move(id))

	def Reset(self):
		for i in range(4):
			if i==self.chosenid:
				self.canvas.itemconfig(self.textmap[i],fill = Menu.CHOSENBUTTON_BG)
			else:
				self.canvas.itemconfig(self.textmap[i],fill = Menu.NORMALBUTTON_BG)

	def Mouse_move(self,id):
		self.chosenid = id
		for i in range(4):
			self.canvas.itemconfig(self.textmap[i],fill = Menu.NORMALBUTTON_BG)
		self.canvas.itemconfig(self.textmap[id],fill = Menu.CHOSENBUTTON_BG)
			


	def Keypress(self,event):
		if event.keycode == 40:
			self.chosenid = (self.chosenid+1)%4
			self.Reset()
		if event.keycode == 38:
			self.chosenid = self.chosenid - 1 if self.chosenid>0 else 3
			self.Reset()
		if event.keycode == 13:
			pass
			
	def Round_rectangle(self, bbox, radius=20, **kwargs):
		x1,y1,x2,y2 = bbox
		points = [x1+radius, y1,
		    x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1]
		return self.canvas.create_polygon(points, **kwargs, smooth=True, fill=Menu.BUTTON_BG)

