from __future__ import absolute_import
from Board import Board
from tkinter import *

class Settingboard(Board):
	def __init__(self,app,master):
		super(Settingboard, self).__init__(app,master,0)
		self.button1 = Button(self.interior,text='Check result',bg='white')
		self.button1.grid(row=2,column=0,columnspan=2,padx=(10,20),pady=10,sticky=W)
		self.button2 = Button(self.interior,text='Save board',bg='white')
		self.button2.grid(row=2,column=1,pady=10)