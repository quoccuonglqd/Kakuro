from __future__ import absolute_import
from tkinter import *
from PIL import ImageTk,Image
from Component import Component

class Board(Component):
	HEIGHT = 597
	WIDTH = 805
	RECTSIZE_MAP = {
	    16:35,
	    8:70,
	    10:56,
	    14:40
	}
	RECTTEXTPOS_MAP = {
	    16:15,
	    8:36,
	    10:30,
	    14:22
	}
	TRITEXTPOS_MAP = {
	    16:11,
	    8:22,
	    10:19,
	    14:13
	}
	def __init__(self,app,master,size):
		super(Board,self).__init__(master)
		self.size = size
		self.currentpos = None

		self.mat = []
		for i in range(self.size):
			row = [0]*self.size
			self.mat.append(row)
		for i in range(self.size):
			self.mat[0][i] = [-1,-1]
			self.mat[i][0] = [-1,-1]

		self.canvaselement = []
		for i in range(self.size):
			x = [None]*self.size
			self.canvaselement.append(x)

		self.discanvas = Canvas(self,bd=0,highlightthickness=0,width = Board.WIDTH,height = Board.HEIGHT)
		self.discanvas.grid(row=0,column=0)
		self.Display()

		self.interior = Frame(self.discanvas)
		self.interior_id = self.discanvas.create_window(565, 0, window=self.interior,
                                           anchor=NW)
		self.label1 = Label(self.interior,text='Grid index: {},{}'.format(0,0),relief=FLAT)
		self.label1.grid(row=0, column=0, columnspan=2,sticky=W,padx=20,pady=20)
		self.label2 = Label(self.interior,text='Value: ',relief=FLAT)
		self.label2.grid(row=1, column=0,padx=(20,0))
		self.entry1= Entry(self.interior,width=29)
		self.entry1.grid(row=1, column=1)

		self.log1 = self.discanvas.create_rectangle(570,140,800,380,fill='white',outline='#909692')
		self.log2 = self.discanvas.create_rectangle(570,400,800,545,fill='white',outline='#909692')
		self.discanvas.create_rectangle(570,140,800,165,fill='#918e8e',outline='#909692')
		self.discanvas.create_rectangle(570,400,800,425,fill='#918e8e',outline='#909692')
		self.discanvas.create_text(610,150,text='Check log')
		self.discanvas.create_text(610,410,text='State log')

		self.grid(row=1,column=0,columnspan=3)

	def Display(self):
		if self.size==0:
			return
		size = Board.RECTSIZE_MAP[self.size]
		for i in range(self.size):
			for j in range(self.size):
				if type(self.mat[i][j])==int:
					self.canvaselement[i][j] = [self.discanvas.create_rectangle(j*size,i*size,(j+1)*size,(i+1)*size,fill='white'),
					self.discanvas.create_text(j*size+Board.RECTTEXTPOS_MAP[self.size],i*size+Board.RECTTEXTPOS_MAP[self.size],text=str(self.mat[i][j]))]
					self.discanvas.tag_bind(self.canvaselement[i][j][0],"<Button-1>",lambda event,i=i,j=j: self.Update_info(i,j))
				else:
					self.canvaselement[i][j]=[self.discanvas.create_polygon([j*size,i*size,j*size,(i+1)*size,(j+1)*size,i*size],fill='white',outline='black'),
					                          self.discanvas.create_polygon([(j+1)*size,(i+1)*size,j*size,(i+1)*size,(j+1)*size,i*size],fill='white',outline='black'),
					                          self.discanvas.create_text(j*size+Board.TRITEXTPOS_MAP[self.size],i*size+Board.TRITEXTPOS_MAP[self.size],text=str(self.mat[i][j][0])),
					                          self.discanvas.create_text((j+1)*size-Board.TRITEXTPOS_MAP[self.size],(i+1)*size-Board.TRITEXTPOS_MAP[self.size],text=str(self.mat[i][j][1]))]
					self.discanvas.tag_bind(self.canvaselement[i][j][0],"<Button-1>",lambda event,i=i,j=j: self.Update_info(i,j,0))
					self.discanvas.tag_bind(self.canvaselement[i][j][1],"<Button-1>",lambda event,i=i,j=j: self.Update_info(i,j,1))
					
					

	def Update_info(self,i,j,*arg):
		self.currentpos = [i,j]
		if len(arg):
			self.currentpos.append(arg[0])
		self.label1.config(text='Grid index: {},{}'.format(i,j))
		self.entry1.delete(0,"end")
		if len(arg)==0:
			self.entry1.insert(0,str(self.mat[i][j]))
		else:
			self.entry1.insert(0,str(self.mat[i][j][arg[0]]))