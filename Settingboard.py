from __future__ import absolute_import
from Board import Board
from os import listdir
import os.path as osp
from file_utils import *
from tkinter_utils import *
from tkinter import *
from PIL import ImageTk,Image

class Settingboard(Board):
	CREATE_BUTTON_TEXT = ['8x8','10x10','14x14','16x16']
	BOARD_SIZE = [(8,8),(10,10),(14,14),(16,16)]
	GOTO_BUTTON_TEXT = ['Menu','Help']

	def __init__(self,app,master):
		super(Settingboard, self).__init__(app,master)
		self.button1 = Button(self.interior,text='Check result',bg='white')
		self.button1.grid(row=2,column=0,columnspan=2,padx=(10,20),pady=10,sticky=W)
		self.button2 = Button(self.interior,text='Save board',bg='white',command=self.Save)
		self.button2.grid(row=2,column=1,pady=10)

		self.optioncanvas_element = []
		self.entry1.bind('<Key>',self.Update_cell)
		self.Create_option_menu()

	def Resetline(self,id):
		for i in range(3):
			if i==id:
				self.discanvas.itemconfig(self.optioncanvas_element[i],state=HIDDEN)
			else:
				self.discanvas.itemconfig(self.optioncanvas_element[i],state=NORMAL)
		if id==0:
			self.create_interior.lift()
			self.discanvas.tag_raise(self.optioncanvas_element[9])
		elif id==1:
			self.open_interior.lift()
			self.discanvas.tag_raise(self.optioncanvas_element[10])
		elif id==2:
			self.goto_interior.lift()
			self.discanvas.tag_raise(self.optioncanvas_element[11])

	def Create_inialize_board(self,ind):
		for i in range(len(self.optioncanvas_element)):
			self.discanvas.delete(self.optioncanvas_element[i])

		self.Inialize_board(Settingboard.BOARD_SIZE[ind][0])
		for i in range(self.size):
			for j in range(self.size):
				for element in self.canvaselement[i][j]:
					self.discanvas.tag_bind(element,"<Button-3>",lambda event,i=i,j=j:self.Change_cell_type(event,i,j))

	def Create_option_menu(self):
		self.optioncanvas_element.clear()
		self.optioncanvas_element.append(self.discanvas.create_line(190,0,190,187))
		self.optioncanvas_element.append(self.discanvas.create_line(190,187,190,374))
		self.optioncanvas_element.append(self.discanvas.create_line(190,374,190,561))

		self.optioncanvas_element.append(self.discanvas.create_rectangle(0,0,186,187,outline="SystemButtonFace",fill="white",activefill="#60a8db"))
		self.optioncanvas_element.append(self.discanvas.create_rectangle(0,187,186,374,outline="SystemButtonFace",fill="white",activefill="#60a8db"))
		self.optioncanvas_element.append(self.discanvas.create_rectangle(0,374,186,561,outline="SystemButtonFace",fill="white",activefill="#60a8db"))
		self.discanvas.tag_bind(self.optioncanvas_element[3],"<Motion>",lambda event:self.Resetline(0))
		self.discanvas.tag_bind(self.optioncanvas_element[4],"<Motion>",lambda event:self.Resetline(1))
		self.discanvas.tag_bind(self.optioncanvas_element[5],"<Motion>",lambda event:self.Resetline(2))

		self.img1 = ImageTk.PhotoImage(Image.open('image/folder-icon-set-3.png').resize((100,100),Image.ANTIALIAS))
		self.optioncanvas_element.append(self.discanvas.create_image(40,40,image=self.img1,anchor=NW,state=DISABLED))
		self.img2 = ImageTk.PhotoImage(Image.open('image/file-folder-icon-png-2.png').resize((100,100),Image.ANTIALIAS))
		self.optioncanvas_element.append(self.discanvas.create_image(40,230,image=self.img2,anchor=NW,state=DISABLED))
		self.img3 = ImageTk.PhotoImage(Image.open('image/file-document-directory-folio-folder-previous-512.png').resize((100,100),Image.ANTIALIAS))
		self.optioncanvas_element.append(self.discanvas.create_image(40,420,image=self.img3,anchor=NW,state=DISABLED))

		self.optioncanvas_element.append(self.discanvas.create_text(90,170,text='Create',font=('Font/arialbd.ttf',20)))
		self.optioncanvas_element.append(self.discanvas.create_text(90,360,text='Open',font=('Font/arialbd.ttf',20)))
		self.optioncanvas_element.append(self.discanvas.create_text(90,540,text='Go to',font=('Font/arialbd.ttf',20)))

		self.create_interior = VerticalScrolledFrame(self.discanvas)
		self.create_interior.grid(row=0,column=0,columnspan=2)
		self.optioncanvas_element.append(self.discanvas.create_window(192, 0, window=self.create_interior,
                                           anchor=NW,height=565,width=380))
		self.open_interior = VerticalScrolledFrame(self.discanvas)
		self.optioncanvas_element.append(self.discanvas.create_window(192, 0, window=self.open_interior,
                                           anchor=NW,height=565,width=380))
		self.goto_interior = VerticalScrolledFrame(self.discanvas)
		self.optioncanvas_element.append(self.discanvas.create_window(192, 0, window=self.goto_interior,
                                           anchor=NW,height=565,width=380))
		
		self.buttons_create = []
		for i in range(len(Settingboard.CREATE_BUTTON_TEXT)):
			self.buttons_create.append(Button(self.create_interior.interior,text=Settingboard.CREATE_BUTTON_TEXT[i],height=2, width=35, 
			           relief=FLAT,bg="gray99", fg="purple3",font="Dosis",command=lambda i=i:self.Create_inialize_board(i)))
			self.buttons_create[len(self.buttons_create)-1].grid(row=len(self.buttons_create)-1,column=0,pady=10,padx=10)

		self.buttons_goto = []
		for text in Settingboard.GOTO_BUTTON_TEXT:
			self.buttons_goto.append(Button(self.goto_interior.interior,text=text,height=2, width=35, 
			           relief=FLAT,bg="gray99", fg="purple3",font="Dosis"))
			self.buttons_goto[len(self.buttons_goto)-1].grid(row=len(self.buttons_goto)-1,column=0,pady=10,padx=10)

	def Update_cell(self,event):
		if event.keycode == 13 and type(self.mat[self.currentpos[0]][self.currentpos[1]])==list:
			value = self.entry1.get()
			if len(value) > 0 and value.isdigit():
				value = int(value)
				if value > 24 or value < 0:
					self.master.attributes("-topmost",False)
					messagebox.showerror(title='Value error', message='Value must be between 0 and 24')
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