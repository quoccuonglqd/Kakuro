from __future__ import absolute_import
from Board import Board
from tkinter import *
from tkinter import messagebox

class Playboard(Board):
	def __init__(self,app,master):
		super(Playboard, self).__init__(app,master)
		self.button1 = Button(self.interior,text='Check result',bg='white',command = self.chekc)
		self.button1.grid(row=2,column=0,columnspan=2,padx=(10,20),pady=10,sticky=W)
		self.button2 = Button(self.interior,text='Next stage',bg='white')
		self.button2.grid(row=2,column=1,pady=10)
		self.app = app

		self.log1 = self.discanvas.create_rectangle(570,140,800,380,fill='white',outline='#909692')
		self.log2 = self.discanvas.create_rectangle(570,400,800,545,fill='white',outline='#909692')
		self.discanvas.create_rectangle(570,140,800,165,fill='#918e8e',outline='#909692')
		self.discanvas.create_rectangle(570,400,800,425,fill='#918e8e',outline='#909692')
		self.discanvas.create_text(610,150,text='Check log')
		self.discanvas.create_text(610,410,text='State log')

		self.label1.grid(row=0, column=0, columnspan=2,sticky=W,padx=20,pady=20)
		self.label2.grid(row=1, column=0,padx=(20,0))
		self.entry1.grid(row=1, column=1)
		
		self.entry1.bind('<Key>',self.Update_cell)

		self.ready = False

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

	def Check(self):
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
							return
					if self.mat[i][j][1] >0:
						Sum = 0
						for k in range(j+1,self.size):
							if type(self.mat[i][k])!=int:
								break
							Sum += self.mat[i][k] 
						if Sum!=self.mat[i][j][1]:
							return
		self.ready = True
		return

	def chekc(self):
		self.Check()
		print(self.ready)