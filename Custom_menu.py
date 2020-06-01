from __future__ import absolute_import
from tkinter import *
from tkinter_utils import *
from PIL import ImageTk,Image
from Component import Component


class Custom_menu(Component):
	HEIGHT = 597
	WIDTH = 805
	CREATE_BUTTON_TEXT = ['8x8','10x10','14x14','16x16']
	GOTO_BUTTON_TEXT = ['Menu','Help']
	def __init__(self,app,master):
		super(Custom_menu,self).__init__(master)

		self.app = app

		self.discanvas = Canvas(self,bd=0,highlightthickness=0,width = Custom_menu.WIDTH,height = Custom_menu.HEIGHT)
		self.discanvas.grid(row=0,column=0)

		self.optioncanvas_element = []
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
                                           anchor=NW,height=565,width=610))
		self.open_interior = VerticalScrolledFrame(self.discanvas)
		self.optioncanvas_element.append(self.discanvas.create_window(192, 0, window=self.open_interior,
                                           anchor=NW,height=565,width=610))
		self.goto_interior = VerticalScrolledFrame(self.discanvas)
		self.optioncanvas_element.append(self.discanvas.create_window(192, 0, window=self.goto_interior,
                                           anchor=NW,height=565,width=610))
		
		self.buttons_create = []
		for i in range(len(Custom_menu.CREATE_BUTTON_TEXT)):
			self.buttons_create.append(Button(self.create_interior.interior,text=Custom_menu.CREATE_BUTTON_TEXT[i],height=2, width=50, 
			           relief=FLAT,bg="gray99", fg="purple3",font="Dosis",command=lambda i=i:self.Create_inialize_board(i)))
			self.buttons_create[len(self.buttons_create)-1].grid(row=len(self.buttons_create)-1,column=0,pady=10,padx=(65,70))

		self.buttons_goto = []
		for text in Custom_menu.GOTO_BUTTON_TEXT:
			self.buttons_goto.append(Button(self.goto_interior.interior,text=text,height=2, width=50, 
			           relief=FLAT,bg="gray99", fg="purple3",font="Dosis"))
			self.buttons_goto[len(self.buttons_goto)-1].grid(row=len(self.buttons_goto)-1,column=0,pady=10,padx=(65,70))

		self.grid(row=1,column=0,columnspan=3)

	def Create_inialize_board(self,ind):
		self.app.settingboard.Enable()
		self.app.settingboard.Create_inialize_board(ind)

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