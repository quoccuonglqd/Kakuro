from __future__ import absolute_import
from Board import Board
from tkinter import *
from tkinter import messagebox
from file_utils import *

class Playboard(Board):
	MAXIMUM_LEVEL = 4
	def __init__(self,app,master):
		super(Playboard, self).__init__(app,master)
		self.button = Button(self.interior,text='Submit',bg='white',command = self.Submit, width=30)
		self.button.grid(row=2,column=0,columnspan=3,padx=(10,20),pady=10,sticky=W)
		self.app = app

		self.log1 = self.discanvas.create_rectangle(570,165,800,380,fill='white',outline='#909692')
		self.log2 = self.discanvas.create_rectangle(570,400,800,545,fill='white',outline='#909692')
		self.discanvas.create_rectangle(570,165,800,190,fill='#918e8e',outline='#909692')
		self.discanvas.create_rectangle(570,400,800,425,fill='#918e8e',outline='#909692')
		self.discanvas.create_text(610,175,text='Check log')
		self.discanvas.create_text(610,410,text='State log')

		self.label1.grid(row=0, column=0, columnspan=2,sticky=W,padx=20,pady=20)
		self.label2.grid(row=1, column=0,padx=(20,0))
		self.entry1.grid(row=1, column=1)
		
		self.entry1.bind('<Key>',self.Update_cell)

		self.ready = True
		self.level = 1

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

	def Submit(self):
		for i in range(self.size):
			for j in range(self.size):
				if type(self.mat[i][j])!=int:
					if self.mat[i][j][0] >0:
						Sum = 0
						for k in range(i+1,self.size):
							if type(self.mat[k][j])!=int:
								break
							Sum += self.mat[k][j] 
						if Sum!=self.mat[i][j][0]:
							self.ready = False
							return
					if self.mat[i][j][1] >0:
						Sum = 0
						for k in range(j+1,self.size):
							if type(self.mat[i][k])!=int:
								break
							Sum += self.mat[i][k] 
						if Sum!=self.mat[i][j][1]:
							self.ready = False
							return
		self.ready = True
		self.Next_level()

	def Next_level(self):
		if self.ready and self.level < Playboard.MAXIMUM_LEVEL:
			self.level += 1
			nextfile = 'test_board/boardstage{}.txt'.format(self.level)
			data = Load_matrix(nextfile)
			self.Create_board_from_data(data)