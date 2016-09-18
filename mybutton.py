#coding=utf-8

from PyQt4.QtGui import *
from PyQt4.QtGui import *


import sys 

class pos(QDialog):
	def __init__(self):
		super(pos,self).__init__()
		self.setWindowTitle("Geogramy")
		label_1 = QLabel('x0:')
		label_2 = QLabel('y0:')
		layout  = QGridLayout()
		layout.addWidget(label_1,0,0)
		layout.addWidget(label_2,1,0)
		self.setLayout(layout)
	def moveEvent(self,event):
		self.update()	


class my_button(QWidget):
	def __init__(self):
		super(my_button,self).__init__()

	def loadPixmap(self,pic_name):
		serf.picmap = QPixmap(pic_name)


class window():
	def __init__(self):
		super(window,self)__init__()
		
		self.setWindowTitle("Created by SHAN YL")  #±ÍÃ‚
		
		icon = QIcon()  #Õº±Í
		icon.addPixmap(QPixmap("logo.png"),QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)



if __name__ == "__main__":
	app = QApplication(sys.argv)
	w   = pos()
	w.show()
	sys.exit(app.exec_() )
