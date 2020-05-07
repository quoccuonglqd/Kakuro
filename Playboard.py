from __future__ import absolute_import
from Board import Board
from tkinter import *
from tkinter import messagebox

class Playboard(Board):
	def __init__(self,app,master):
		super(Playboard, self).__init__(app,master)
		self.button1 = Button(self.interior,text='Check result',bg='white')
		self.button1.grid(row=2,column=0,columnspan=2,padx=(10,20),pady=10,sticky=W)
		self.button2 = Button(self.interior,text='Next stage',bg='white')
		self.button2.grid(row=2,column=1,pady=10)
		self.app = app
		
		self.entry1.bind('<Key>',self.Update_cell)

	def Update_cell(self,event):
		if event.keycode == 13 and type(self.mat[self.currentpos[0]][self.currentpos[1]])==int:
			value = self.entry1.get()
			if len(value) > 0 and value.isdigit():
				value = int(value)
				if value > 9 or value < 0:
					self.master.attributes("-topmost",False)
					messagebox.showerror(title='Value error', message='Value must be between 0 and 9')
					self.master.attributes("-topmost",True)
					return
				else:
					self.discanvas.itemconfig(self.canvaselement[self.currentpos[0]][self.currentpos[1]][1],text=str(value))
					self.mat[self.currentpos[0]][self.currentpos[1]] = value
			else:
				self.master.attributes("-topmost",False)
				messagebox.showerror(title='Value error', message='Value must be integer between 0 and 9')
				self.master.attributes("-topmost",True)
				return
		elif type(self.mat[self.currentpos[0]][self.currentpos[1]])!=int:
			self.master.attributes("-topmost",False)
			messagebox.showerror(title='Action denied', message='Cannot change this cell in this play mode')
			self.master.attributes("-topmost",True)