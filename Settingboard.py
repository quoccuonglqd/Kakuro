from __future__ import absolute_import
from Board import Board
from os import listdir
import os.path as osp
from file_utils import *
from tkinter import *
from PIL import ImageTk,Image  
from kaklib.kaksolve import *  

class Settingboard(Board):
	BOARD_SIZE = [(8,8),(10,10),(14,14),(16,16)]
	def __init__(self,app,master):
		super(Settingboard, self).__init__(app,master)

		self.optioncanvas_element = []
		self.entry1.bind('<Key>',self.Update_cell)

		self.button = Button(self.interior,text='Save board',bg='white',command = self.Save,width=30)
		self.button.grid(row=2,column=0,columnspan=3,padx=(10,20),pady=10,sticky=W)
		
		self.app = app
		
		self.log1 = self.discanvas.create_rectangle(570,165,800,380,fill='white',outline='#909692')
		self.log2 = self.discanvas.create_rectangle(570,400,800,545,fill='white',outline='#909692')
		self.discanvas.create_rectangle(570,165,800,190,fill='#918e8e',outline='#909692')
		self.discanvas.create_rectangle(570,400,800,425,fill='#918e8e',outline='#909692')
		self.discanvas.create_text(610,175,text='Check log')
		self.discanvas.create_text(610,410,text='State log')
		

	def Create_inialize_board(self,ind):
		for i in range(len(self.optioncanvas_element)):
			self.discanvas.delete(self.optioncanvas_element[i])

		self.Inialize_board(Settingboard.BOARD_SIZE[ind][0])
		for i in range(self.size):
			for j in range(self.size):
				for element in self.canvaselement[i][j]:
					self.discanvas.tag_bind(element,"<Button-3>",lambda event,i=i,j=j:self.Change_cell_type(event,i,j))

	def Create_existing_board(self,data):
		for i in range(len(self.optioncanvas_element)):
			self.discanvas.delete(self.optioncanvas_element[i])

		self.Create_board_from_data(data)
		for i in range(self.size):
			for j in range(self.size):
				for element in self.canvaselement[i][j]:
					self.discanvas.tag_bind(element,"<Button-3>",lambda event,i=i,j=j:self.Change_cell_type(event,i,j))

	def Update_cell(self,event):
		if event.keycode == 13 and type(self.mat[self.currentpos[0]][self.currentpos[1]])==list:
			value = self.entry1.get()
			if len(value) > 0 and value.isdigit():
				value = int(value)
				if value > 64 or value < 0:
					self.master.attributes("-topmost",False)
					messagebox.showerror(title='Value error', message='Value must be between 0 and 64')
					self.master.attributes("-topmost",True)
					return
				else:
					self.discanvas.itemconfig(self.canvaselement[self.currentpos[0]][self.currentpos[1]][self.currentpos[2]+2],text=str(value))
					self.mat[self.currentpos[0]][self.currentpos[1]][self.currentpos[2]] = value

			else:
				self.master.attributes("-topmost",False)
				messagebox.showerror(title='Value error', message='Value must be integer between 0 and 9')
				self.master.attributes("-topmost",True)
				return
		elif type(self.mat[self.currentpos[0]][self.currentpos[1]])!=list:
			self.master.attributes("-topmost",False)
			messagebox.showerror(title='Action denied', message='Cannot change this cell in this play mode')
			self.master.attributes("-topmost",True)

	def Save(self):
		index = len(listdir('custom_board')) 
		Save_matrix(osp.join('custom_board','board'+str(index)+'.txt'),self.mat)

	def Change_cell_type(self,event,i,j):
		self.Update_info(i,j)
		self.popup_menu = Menu(self, tearoff=0)
		if type(self.mat[i][j])==int:
			self.popup_menu.add_command(label="Split",command=self.Split)
		else:
			self.popup_menu.add_command(label="Merge",command=self.Merge)
		self.popup_menu.add_command(label="Solve",command=self.Solve)

		try:
			self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
		finally:
			self.popup_menu.grab_release()		

	def Split(self):
		size = Board.RECTSIZE_MAP[self.size]
		for i in range(2):
			self.discanvas.delete(self.canvaselement[self.currentpos[0]][self.currentpos[1]][i])
		self.canvaselement[self.currentpos[0]][self.currentpos[1]]=[
            self.discanvas.create_polygon([self.currentpos[1]*size,self.currentpos[0]*size,self.currentpos[1]*size,(self.currentpos[0]+1)*size,(self.currentpos[1]+1)*size,(self.currentpos[0]+1)*size],fill='white',outline='black'),
		    self.discanvas.create_polygon([self.currentpos[1]*size,self.currentpos[0]*size,(self.currentpos[1]+1)*size,self.currentpos[0]*size,(self.currentpos[1]+1)*size,(self.currentpos[0]+1)*size],fill='white',outline='black'),
		    self.discanvas.create_text(self.currentpos[1]*size+Board.TRITEXTPOS_MAP[self.size],(self.currentpos[0]+1)*size-Board.TRITEXTPOS_MAP[self.size],text=str(-1)),
		    self.discanvas.create_text((self.currentpos[1]+1)*size-Board.TRITEXTPOS_MAP[self.size],self.currentpos[0]*size+Board.TRITEXTPOS_MAP[self.size],text=str(-1)) 
		]
		self.mat[self.currentpos[0]][self.currentpos[1]] = [-1,-1]
		self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][0],"<Button-1>",lambda event,i=self.currentpos[0],j=self.currentpos[1]: self.Update_info(i,j,0))
		self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][2],"<Button-1>",lambda event,i=self.currentpos[0],j=self.currentpos[1]: self.Update_info(i,j,0))
		self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][1],"<Button-1>",lambda event,i=self.currentpos[0],j=self.currentpos[1]: self.Update_info(i,j,1))
		self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][3],"<Button-1>",lambda event,i=self.currentpos[0],j=self.currentpos[1]: self.Update_info(i,j,1))
		for i in range(4):
			self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][i],"<Button-3>",lambda event,i=self.currentpos[0],j=self.currentpos[1]:self.Change_cell_type(event,i,j))

	def Merge(self):
		size = Board.RECTSIZE_MAP[self.size]
		for i in range(4):
			self.discanvas.delete(self.canvaselement[self.currentpos[0]][self.currentpos[1]][i])
		self.canvaselement[self.currentpos[0]][self.currentpos[1]]=[
            self.discanvas.create_rectangle(self.currentpos[1]*size,self.currentpos[0]*size,(self.currentpos[1]+1)*size,(self.currentpos[0]+1)*size,fill='white'),
			self.discanvas.create_text(self.currentpos[1]*size+Board.RECTTEXTPOS_MAP[self.size],self.currentpos[0]*size+Board.RECTTEXTPOS_MAP[self.size],text=str(0)) 
		]
		self.mat[self.currentpos[0]][self.currentpos[1]] = 0
		for i in range(2):
			self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][i],"<Button-1>",lambda event,i=self.currentpos[0],j=self.currentpos[1]: self.Update_info(i,j))
			self.discanvas.tag_bind(self.canvaselement[self.currentpos[0]][self.currentpos[1]][i],"<Button-3>",lambda event,i=self.currentpos[0],j=self.currentpos[1]:self.Change_cell_type(event,i,j))

	def Solve(self):
		Change_format(self.mat,'middle_format.txt')
		answer = kaksolve('middle_format.txt')
		for x,y,val in answer:
			self.discanvas.itemconfig(self.canvaselement[x-1][y-1][1],text=str(val))
			self.mat[x-1][y-1] = val