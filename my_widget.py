#coding=utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from math import *




class view(QWidget):
	def __init__(self):
		super(view,self).__init__()
		#self.setPalette(QPalette(Qt.black) )
		#self.setAutoFillBackground(True)
		self.view_w = 600
		self.view_h = 250
		self.dx = 50
		self.dy = 30

		self.w = self.view_w + self.dx  #left 40
		self.h = self.view_h + self.dy

		self.setMinimumSize(self.w,self.h)
	
		self.show_data = list()
		self.keep_data = list()

		self.x = self.dx # left 20
		self.y = self.h - self.dy # down 20
		self.step_Volt = 1
		self.step_time = 0.2
		self.qp = QPainter()
		self.xlabel = 'this is a text'
		self.ylabel = 'this is atext' 
		
		self.xscale = 1
		self.yscale = 1

		self.centerx = self.x
		self.centery = self.y

		self.gridpen = QPen(Qt.gray, 1,Qt.DashLine, Qt.RoundCap)
		self.axispen = QPen(Qt.gray, 1,Qt.SolidLine, Qt.RoundCap)

		f = open('data.text','r')
		val = f.readline()
		tim = 0
		while len(val) != 0:
			try:
				#print val
				#val = val.split("\n")
				#val = int(val)
				
				#self.keep_data.append([tim, val])
				tim += 1
				val = f.readline()
			except Exception, e:
				print e
		print 'length:' + str(len(self.keep_data) )
		self.change()

	def change_to_window(self,x,y):
		temp_x = x + self.x
		temp_y = self.y- y
		#print temp_x, temp_y
		return [temp_x, temp_y]
	
	def map(self,x,inmin, inmax, tomin, tomax):
		out = tomin + 1.0*(x - inmin)/(inmax - inmin)*(tomax - tomin)
		return out  

	def change(self):
		
		length = len(self.show_data)
		#print self.keep_data
		print length
		if length > 0:
			for i in range(0,length):
				self.show_data.pop(0)
		index = 0
		while(index < len(self.keep_data) ):
			try:
				x = self.keep_data[index][0] * self.xscale
				y = self.map( self.keep_data[index][1],0,1024,0,self.view_h)

				index += 1
				if x > self.view_w:
					return
				self.show_data.append( self.change_to_window(x,y)) 
				
			except Exception, e:
				print e 

	def draw_range_rect(self,qp):
		qp.setPen( QPen(Qt.white, 1,Qt.SolidLine, Qt.RoundCap) )
		qp.setBrush(Qt.black)
		qp.drawRect(0,0,self.w-1,self.h-1)
		qp.drawRect(self.x,0, self.view_w,self.y)
		
	def draw_axis(self,qp):
		qp.setPen(self.axispen)
		for i in range(1,18):
			qp.drawLine(self.x-5,i*self.view_h/18,self.x,i*self.view_h/18)
			rect =  QRectF(0,i*self.view_h/18,self.x-5,i*self.view_h/18)
			#type(rect)
			#qp.drawText(rect,str(i),Qt.AlignCenter )#,Qt.AlignCenter)
			qp.drawText(rect, Qt.AlignRight,str(i))#| Qt.AlignCenter, str(i))
		for i in range(1,30):
			qp.drawLine(self.x+ i*self.view_w/30, self.y,self.x+ i*self.view_w/30,self.y+5)
			qp.drawText(self.x+ i*self.view_w/30, self.y+18,str(i))#| Qt.AlignCenter, str(i))
	
	def draw_grid(self,qp):
		qp.setPen(self.gridpen)
		for i in range(1,6):
			qp.drawLine(self.x,  i*self.view_h/6, self.w, i*self.view_h/6 )
		for i in range(1,10):
			qp.drawLine(i*self.view_w/10+self.x, 0, i*self.view_w/10+self.x, self.y )

	def draw_curve(self,qp):
		qp.setPen( QPen(Qt.red, 1,Qt.SolidLine, Qt.RoundCap) )
		length = len(self.show_data)
		if length <1: 
			return
		for i in range(1,length):
			qp.drawLine(self.show_data[i][0] , self.show_data[i][1], 
						self.show_data[i-1][0], self.show_data[i-1][1]  )
			#qp.drawEllipse(self.show_data[i][0],self.show_data[i][1],10,10)

	def draw_center(self,qp):
		qp.setPen(QPen(Qt.white, 1,Qt.SolidLine,Qt.RoundCap))
		#qp.drawLine(self.x,self.centery, self.w, self.centery)
		qp.drawLine(self.centerx, 0, self.centerx, self.y)
		qp.drawLine(self.centery, 0, self.centery, self.y)


	def add_data(self,val): #val[0] time val[1] val 
		self.keep_data.append(val)


	def add_to_window(self):
		length = len(self.keep_data)
		for i in range(0,10):
			av_x = sum(self.keep_data[i:i*length/10][0])
	
	def mousePressEvent(self,QmouseEvent):
		print 'call mouse button event'
		if QmouseEvent.button() == Qt.LeftButton:
			self.xscale = 1
			if QmouseEvent.x() > self.x and QmouseEvent.x() < self.w:
				self.centerx = QmouseEvent.x()
				print self.centerx
		self.change()
		self.update()

	def mouseMoveEvent(self,QmouseEvent):
		if QmouseEvent.x() > self.x and QmouseEvent.x() <self.w:
			self.centery = QmouseEvent.x()
		#if QmouseEvent.y() > 0 and QmouseEvent.y() < self.y:
		#	self.centery = QmouseEvent.y()
		self.update()

#	def mouseReleaseEvent(self.QmouseEvent):


	def wheelEvent(self,QwheelEvent):
		print 'call wheel event'
		print QwheelEvent.delta()
		if QwheelEvent.delta()>0 and self.xscale >0:
			self.xscale += 0.1
		if QwheelEvent.delta()<0 and self.xscale >0.1:
			self.xscale -= 0.1		
		self.change()
		self.update()

	def resizeEvent(self,QresizeEvent):
		print "resize event is called"
		self.x = self.dx
		self.y = self.height() - self.dy		
		self.w = self.width()  #left 40
		self.h = self.height()

		self.view_w = self.w - self.dx
		self.view_h = self.h - self.dy
		self.change()
		self.update()

	def paintEvent(self,QPaintEvent):
		
		self.qp.begin(self)
		print 'call pain event'
		
		self.draw_range_rect(self.qp)
		self.draw_axis(self.qp)
				
		self.draw_grid(self.qp)

		self.qp.setRenderHint(QPainter.Antialiasing,True)
		self.draw_curve(self.qp)
		self.qp.setRenderHint(QPainter.Antialiasing,False)
		self.draw_center(self.qp)

		self.qp.end()

class axis(QWidget):
	def __init__(self,param = 'h'):
		super(axis,self).__init__()
		self.setPalette(QPalette(Qt.black) )
		self.setAutoFillBackground(True)
	
		if param == 'h':
			self.w = 600
			self.h = 200
		elif param == 'v':
			self.w = 500
			self.h = 200
		self.setMinimumSize(self.w,self.h)
		
		self.qp = QPainter()

	def map(self,x,inmin, inmax, tomin, tomax):
		out = tomin + 1.0*(x - inmin)/(inmax - inmin)*(tomax - tomin)
		return out  

	def draw_axis(self,qp):
		axispen = QPen(Qt.white, 1,Qt.SolidLine, Qt.RoundCap)
		axisbrush = QBrush(Qt.blue)
		qp.setPen(axispen)
		#qp.setBrush(axisbrush)
		qp.setWindow( 0, -(self.height() - 30),self.width(),self.height() )
		#qp.setViewport(300,300,)

		qp.drawLine( 0, 0, self.width(),0)

	def paintEvent(self,QPaintEvent):
		self.qp.begin(self)
		self.draw_axis(self.qp)

		self.qp.end()









class plot(QWidget):
	def __init__(self):
		super(plot,self).__init__()
		self.layout = QGridLayout()
		self.view = view()
		self.xaxis = axis('h')
		self.yaxis = axis('v')

	#	self.layout.addWidget(self.xaxis,1,1)
		self.layout.addWidget(self.yaxis,0,0)
	#	self.layout.addWidget(self.view,0,1)

		self.setLayout(self.layout)






class main(QWidget):
	def __init__(self):
		super(main,self).__init__()
		
		mainlayout = QGridLayout()
		self.ui = plot()
		self.but = QPushButton()
		mainlayout.addWidget(self.ui,0,0)
		self.setLayout(mainlayout)













import sys 
if __name__ == "__main__":
	app = QApplication(sys.argv)
	w   = main()
	w.show()
	sys.exit(app.exec_() )
