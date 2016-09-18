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
		


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w   = pos()
	w.show()
	sys.exit(app.exec_() )