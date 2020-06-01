r"""Date: 12/3/2020
    Author: Nguyen Quoc Cuong
"""
from tkinter import *
from tkinter_utils import *
import os
from PIL import ImageTk,Image
from Component import Component
from file_utils import *

class Menu(Component):
	BACKGROUND_PATH = 'image/unnamed.jpg'
	HEIGHT = 597
	WIDTH = 805
	FONT_PATH = 'Font/arialbd.ttf'
	TEXT_SIZE = 19
	PLAY_BBOX = (320,140,530,180)
	CUSTOM_BBOX = (320,210,530,250)
	SOLVE_BBOX = (320,280,530,320)
	HELP_BBOX = (320,350,530,390)
	QUIT_BBOX = (320,420,530,460)
	PLAY_POS = (425,160)
	CUSTOM_POS = (421,230)
	SOLVE_POS = (425,300)
	HELP_POS = (425,370)
	QUIT_POS = (425,440)
	BUTTON_BG = "#9caaad"
	CHOSENBUTTON_BG = "#eb073c"
	NORMALBUTTON_BG = "#2c17b3"
 
	def __init__(self,app,master):
		super(Menu,self).__init__(master)
		self.master = master
		self.focus_set()

		self.backgroundimg = ImageTk.PhotoImage(Image.open(Menu.BACKGROUND_PATH).resize((Menu.WIDTH,Menu.HEIGHT),Image.ANTIALIAS))
		self.canvas = Canvas(self, highlightthickness=0,width = Menu.WIDTH,height = Menu.HEIGHT)
		self.canvas.grid(row=0, column=0)
		self.bg = self.canvas.create_image(0, 0, anchor=NW, image=self.backgroundimg)

		self.playbut = Round_rectangle(Menu.PLAY_BBOX,canvas=self.canvas,fill=Menu.BUTTON_BG)
		self.custombut = Round_rectangle(Menu.CUSTOM_BBOX,canvas=self.canvas,fill=Menu.BUTTON_BG)
		self.solvebut = Round_rectangle(Menu.SOLVE_BBOX,canvas=self.canvas,fill=Menu.BUTTON_BG)
		self.helpbut = Round_rectangle(Menu.HELP_BBOX,canvas=self.canvas,fill=Menu.BUTTON_BG)
		self.quitbut = Round_rectangle(Menu.QUIT_BBOX,canvas=self.canvas,fill=Menu.BUTTON_BG)
		self.playtext = self.canvas.create_text(Menu.PLAY_POS[0],Menu.PLAY_POS[1],text="PLAY",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.CHOSENBUTTON_BG)
		self.customtext = self.canvas.create_text(Menu.CUSTOM_POS[0],Menu.CUSTOM_POS[1],text="CUSTOM",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.solvetext = self.canvas.create_text(Menu.SOLVE_POS[0],Menu.SOLVE_POS[1],text="SOLVE",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.helptext = self.canvas.create_text(Menu.HELP_POS[0],Menu.HELP_POS[1],text="HELP",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.quittext = self.canvas.create_text(Menu.QUIT_POS[0],Menu.QUIT_POS[1],text="QUIT",font=(Menu.FONT_PATH,Menu.TEXT_SIZE),fill=Menu.NORMALBUTTON_BG)
		self.chosenid = 0

		self.textmap = {
		    0 : self.playtext,
		    1 : self.customtext,
		    2 : self.solvetext,
		    3 : self.helptext,
		    4 : self.quittext
		}

		self.grid(row=1,column=0,columnspan=3)
		self.bind("<Key>",self.Keypress)
		self.canvas.tag_bind(self.playtext,"<Motion>",lambda event,id=0:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.customtext,"<Motion>",lambda event,id=1:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.solvetext,"<Motion>",lambda event,id=2:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.helptext,"<Motion>",lambda event,id=3:
			                                   self.Mouse_move(id))
		self.canvas.tag_bind(self.quittext,"<Motion>",lambda event,id=4:
			                                   self.Mouse_move(id))

		self.app=app
		self.canvas.tag_bind(self.playtext,"<Button-1>",lambda event:self.Play())
		self.canvas.tag_bind(self.playbut,"<Button-1>",lambda event:self.Play())
		self.canvas.tag_bind(self.customtext,"<Button-1>",lambda event:self.Custom())
		self.canvas.tag_bind(self.custombut,"<Button-1>",lambda event:self.Custom())
		self.canvas.tag_bind(self.quittext,"<Button-1>",lambda event:self.master.quit())
		self.canvas.tag_bind(self.quitbut,"<Button-1>",lambda event:self.master.quit())

	def Play(self):
		self.app.playboard.Enable()
		data = Load_matrix('sample_board/boardstage1.txt')
		self.app.playboard.Create_board_from_data(data)

	def Custom(self):
		self.app.custom_menu.Enable()

	def Reset(self):
		for i in range(5):
			if i==self.chosenid:
				self.canvas.itemconfig(self.textmap[i],fill = Menu.CHOSENBUTTON_BG)
			else:
				self.canvas.itemconfig(self.textmap[i],fill = Menu.NORMALBUTTON_BG)

	def Mouse_move(self,id):
		self.chosenid = id
		for i in range(5):
			self.canvas.itemconfig(self.textmap[i],fill = Menu.NORMALBUTTON_BG)
		self.canvas.itemconfig(self.textmap[id],fill = Menu.CHOSENBUTTON_BG)
			


	def Keypress(self,event):
		if event.keycode == 40:
			self.chosenid = (self.chosenid+1)%5
			self.Reset()
		if event.keycode == 38:
			self.chosenid = self.chosenid - 1 if self.chosenid>0 else 4
			self.Reset()
		if event.keycode == 13:
			if self.chosenid==0:
				self.Play()
			elif self.chosenid==1:
				self.Custom()
			elif self.chosenid==4:
				self.master.quit()