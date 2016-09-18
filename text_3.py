#coding=utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *


import sys 
import random 

import time




class plot_area(QWidget):
	def __init__(self):
		super(plot_area, self).__init__()
		self.w = 600
		self.h = 600
		self.setPalette( QPalette(Qt.black) )
		self.setAutoFillBackground(True)
		self.setMinimumSize(self.w, self.h)
		self.painter = QPainter()
		self.pen     = QPen(Qt.blue, 1, Qt.SolidLine)

		
		self.i = 20
		self.j = 20
		self.w = self.width()/self.i 
		self.h = self.height()/self.j
		self.map = list()
		self.init_bar()
		self.alllength = 65536
		self.lengthto = 65536
		self.lengend = 0
		
	def init_bar(self):
		self.map = list()

		for i in range(0,self.i):
			self.map.append([])
			for j in range(0,self.j):
				self.map[i].append(0)
				#self.map[i].append(random.randint(0,1))
				#print self.map
	
		self.x1 = 1
		self.y1 = 15

		self.join = list()
		self.join.append([self.x1, self.y1])
		self.x2 = 18
		self.y2 = 10

		self.map[self.x1][self.y1] = 2
		self.map[self.x2][self.y2] = 3
			
	def solve(self, i = 1, j = 15):
		#print 'on solve'
		length = list()
		if self.map[i][j] == 0 or self.map[i][j] == 2 or self.map[i][j] == 4:
			for di in [-1,0,1]:
				for dj in [-1,0,1]:
					ci = i + di
					cj = j + dj

					if self.map[ci][cj] == 1 or self.map[ci][cj] == 4:

						continue
					else:
						#print self.map[ci][cj]

						length.append( [(self.x2-ci)**2 + (self.y2-cj)**2,di,dj] )
			l = length[0]
			print len(length)
			if len(length) == 0:
				self.map[i][j] = 4
			for dl in length:
				if dl[0] < l[0]:
					l = dl
			i = i + l[1]
			j = j + l[2]
			#print i,j
			
			if self.map[i][j] == 3:
				print 'end'
				return 0
			self.map[i][j] = 4
			self.update()
			#time.sleep(0.5)
			self.solve(i,j)

	def solve_ex(self,i = 1,j = 15):
		length = list()
		for di in [-1,0,1]:
			for dj in [-1,0,1]:
				ci = i + di
				cj = j + dj
				if ci<0 or ci >self.i-1 or cj<0 or cj >self.j-1:
					print 'out range'
					continue

				if self.map[ci][cj] == 3:
					print 'the end'
					return
				if self.map[ci][cj] == 1:
					print 'on wall'
					continue
				if [ci, cj] in self.join:
					print 'on back'
					continue
				if self.map[ci][cj] == 0:
					length.append( [(self.x2-ci)**2 + (self.y2-cj)**2,di,dj] )
			
		if len(length) == 0:
			self.join.pop()
			solve_ex(self.join[-1][0],self.join[-1][1] )
			print 'no result'
			return
		for dl in length:
			if dl[0] < length[0]:
				l = dl
		del length
		i = i + l[1]
		j = j + l[2]
		self.map[i][j] = 4
		self.join.append([i,j])

		self.solve_ex(i,j)
	

		
			
	def clear(self):
		self.join = list()
		self.join.append([self.x1, self.y1])
			
		for i in range(0,self.i):
			for j in range(0,self.j):
				if self.map[i][j] == 4:
					self.map[i][j] = 0
				



	def draw_bar(self, data):
		self.painter.setPen(self.pen)
			
		for i in range(0, self.i):
			for j in range(0, self.j):
				x = self.w * i
				y = self.h * j
				if self.map[i][j] == 1:
					self.painter.setBrush(Qt.white)	
				elif self.map[i][j] == 2:
					self.painter.setBrush(Qt.red)
				elif self.map[i][j] == 3:
					self.painter.setBrush(Qt.green)
				elif self.map[i][j] == 4:
					self.painter.setBrush(Qt.blue)
				else:
					self.painter.setBrush(Qt.black)	
				self.painter.drawRect(x, y, x+ self.w, y +self.h )
				
	def draw_cureve(self):
		print 'on draw cureve'
		self.draw_bar(self.map)
		self.painter.setPen(self.pen)
		


	def paintEvent(self, painevent):
		print 'on call paint event'
		self.painter.begin(self)
		##########################################################
		self.draw_cureve()
		
		self.painter.setRenderHint(QPainter.Antialiasing,True)

		
		##########################################################
		self.painter.end()

	def resizeEvent(self, resizeevent):
		print 'on call resize event'
		self.w = self.width()/self.i
		self.h = self.height()/self.j
	
	def mousePressEvent(self, mousepressevent):

		i = mousepressevent.x()/(self.width()/self.i  )
		j = mousepressevent.y()/(self.height()/self.j )	
		if mousepressevent.button() == Qt.LeftButton:
			self.map[i][j] = 1
			self.types = 1
			self.update()
		else:
			self.types = 2
			self.map[i][j] = 0 
			self.update()	
	def mouseReleaseEvent(self,mousereleaseevent):
		self.types = 0
	def mouseMoveEvent(self, mousemoveevent):
		i = mousemoveevent.x()/( self.width()/self.i  ) 
		j = mousemoveevent.y()/( self.height()/self.j )
		
		if self.types == 1:
			self.map[i][j] = 1
		elif self.types == 2:            #mousemoveevent.button() == Qt.RightButton:
			self.map[i][j] = 0
		self.update()
	def wheelEvent(self, wheelevent):
		print "start wheel event"
		self.clear()

		#print self.map
		self.update()
		self.solve_ex()
		self.update()
	






class pos(QDialog):
	def __init__(self):
		super(pos,self).__init__()
		self.setWindowTitle("Geogramy")
		self.setGeometry(100,100,400,400)
		#label_1 = QLabel('x0:')
		plot    = plot_area() 
		layout  = QGridLayout()

		#layout.addWidget(label_1,0,0)
		layout.addWidget(plot, 1, 0)
		self.setLayout(layout)
	
	def moveEvent(self,event):
		self.update()
	
		


if __name__ == "__main__":
	app = QApplication(sys.argv)
	w   = pos()
	w.show()
	sys.exit(app.exec_() )
