#coding=utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import threading


class draw(QWidget):
	def __init__(self):
		super (draw,self).__init__()
		self.w = 500
		self.h = 250
		self.setPalette( QPalette(Qt.black) )
		self.setAutoFillBackground(True)
		self.setMinimumSize(self.w+10,self.h+20)
		self.pen = QPen(Qt.red,1,Qt.SolidLine,Qt.RoundCap)
		self.brush = QBrush()
		self.pos  = list() 
		self.data = list()
		self.keepdata = list()
		#self.keeptime = list()
		self.qp = QPainter()

		self.color = Qt.red

		self.currenttime = 0
		self.currentvalue = 0

		self.maxvalue = 0
		self.minvalue = 0
		self.updatetime = 0
	#	self.lock = threading.Lock()
		##self.count = 0
		self.xscale = 2 #两个像素表示一个点
		
		self.x1 = 0
		self.x2 = 0
	
	def getwidth(self):
		return self.width()

	def havedata(self):
		if len(self.data) !=0:
			return True
		else:
			return False
	
	def drawPoints(self,qp):
		try:
			if len(self.data) !=0:
				qp.setPen(Qt.blue)
				for pos in self.data:
					qp.drawPoint(pos[0]%self.w, pos[1]*250/1023)

		
		except Exception,e:
			print e


	def drawcurve(self,qp):
		try:
			#self.lock.acquire()
			length = len(self.data)
			if length !=0 and length > 1:
				qp.setPen(self.pen)
				try:
					length = len(self.data)
					for i in range(1,length-1):
						qp.drawLine(i*self.xscale    , self.data[i][0],
									(i-1)*self.xscale, self.data[i-1][0])
						
						
				except Exception, e:
					print e
					print 'dfdf'
					
				qp.setPen(Qt.blue)
				qp.setBrush(Qt.blue)
				#qp.drawLine(self.currenttime, 0, 
				#			self.currenttime, self.h+10)
				#qp.setPen(Qt.red)
		
				qp.drawEllipse(self.currenttime, self.currentvalue,5,5)

		except Exception,e:
			print e
		#self.lock.release()	



	def drawcurve_ex(self,qp):
		try:
			#self.lock.acquire()
			length = len(self.data)
			if length !=0 and length > 1:
				qp.setPen(self.pen)
				try:
					length = len(self.data)
					for i in range(1,length):
						#x1 = self.data[i-1][0]
						#y1 = self.data[i-1][1]
					
						#x2 = self.data[i][0]
						#y2 = self.data[i][1]
						qp.drawLine(self.data[i-1][0]%self.width(),self.data[i-1][1],
									self.data[i][0]%self.width(),self.data[i][1])
						
						
				except Exception, e:
					print e
					
				qp.setPen(Qt.blue)
				qp.drawLine(self.currenttime, 0, 
							self.currenttime, self.h+10)
				#qp.setPen(Qt.red)
		
				#qp.drawEllipse(self.currenttime, self.currentvalue,5,5)

		except Exception,e:
			print e


	def clear_data(self):
		print 'pop data'
		#self.lock.acquire()
		for i in range(0,len(self.data) ):
			self.data.pop(0)
		del self.keepdata[:]
		#for i in range(0,len(self.keepdata) ):
		#	self.keepdata.pop(0)
		
		self.currenttime = 0
		self.currentvalue = 0

		self.x1 = 0
		self.x2 = 0

		print 'pop end'
		self.update()
		#self.lock.release()
	
	def showkeepdata(self,endvalue):
		length = len(self.data)
		self.currenttime = 0
		self.currentvalue = 0
		if endvalue >= length:
			for i in range(0,length):
				l = self.keepdata[endvalue -length+i]
				#print l
				self.data[i] = l 
			print 'on change'
			self.update()

	def drawtimedata(self,qp):
		qp.setPen(Qt.blue)


		qp.drawLine(self.x1,   10,self.x1+5,4 )
		qp.drawLine(self.x1+5, 4,self.x1-5, 4 )
		qp.drawLine(self.x1-5, 4,self.x1,  10 )

		qp.drawLine(self.x1, 10, 
					self.x1, self.h+10)
		
		qp.setPen(Qt.green)
		qp.drawLine(self.x2,   10,self.x2+5,4 )
		qp.drawLine(self.x2+5, 4,self.x2-5, 4 )
		qp.drawLine(self.x2-5, 4,self.x2,  10 )
	
		qp.drawLine(self.x2, 10, 
					self.x2, self.h+10)
	
	def showtimedata(self,x1,x2):
		if x1/ self.xscale >0 and x1/ self.xscale <len(self.data):
			self.x1 = x1
		if x2/ self.xscale >0 and x2/ self.xscale <len(self.data):
			self.x2 = x2



		total = 0
		tim1 = self.data[self.x1/self.xscale][1]
		tim2 = self.data[self.x2/self.xscale][1]
		if tim2 > tim1:
			total = tim2 - tim1
		else:
			total = tim1 - tim2
		#print  self.data[x1][1],self.data[x2][1]
		#print total
		self.update()

		return total



	def adddata(self,data):
		try:
			data[0] = int(data[0])
		except:
			return

		if data[0] > self.maxvalue:
			self.maxvalue = data[0]
		temp = [self.h-data[0]*self.h/self.maxvalue+10,  data[1]]
	
		self.keepdata.append( temp )
		self.data.append    ( temp )

		if len(self.data)*self.xscale >= self.width():
			a = self.data.pop(0)
		
		#if len(self.keepdata) > 200000:
			#self.keepdata.pop(0)
		
		self.currenttime = len(self.data)*2 - 5
		self.currentvalue = temp[0]
		self.update()
		#print data

	def adddata_ex(self,data):
		try:
			data[1] = int(data[1])
		except:
			return

		temp = [data[0], self.h-data[1]*self.h/1024+10,data[2]]
		self.keepdata.append([temp[1],data[2]])


		if data[0] >= self.width():	
			self.data.pop(0)
			self.data.append (temp )
		else:
			self.data.append (temp )
		
		if self.updatetime%60 == 0:
			self.update()
			#self.update()`


	def drawaxis(self,qp):
		qp.setPen(QColor(0,255,255))
		#qp.drawRect(0+1,0+1,self.w-3,self.h-3)
	#	for i in range(1,10):
	#	qp.drawLine(i*self.width()/10, 0,i*self.width()/10,self.height())
		
	#	for i in range(1,5):
	#	qp.drawLine(0, i*self.height()/5,self.width(),i*self.height()/5)
		qp.drawRect(0,0,self.width()-1,self.height()-1)
		qp.drawLine(self.width()/20, 0,self.width()/20,self.height())
		qp.drawLine(0, self.height()/2,self.width(),self.height()/2)
		for i in range(1,20):
			qp.drawLine(self.width()/20*i,self.height()/2-6,self.width()/20*i,self.height()/2)

		qp.setPen(QColor(255,255,255))
		qp.drawText(self.width()/20,self.height(),'Value')
		for i in range(10,0,-1):
			qp.drawText(self.width()/20+4,self.height()-self.height()/10*i,str(self.maxvalue/10*i))
		qp.drawText(self.width()-30,self.height()/2-5,'Time')
		
		
	def drawLines(self,qp,color):
		qp.setPen(color)
		qp.drawLine(0,0,5,0)
		
		

	def paintEvent(self,QPaintEvent):

		self.qp.begin(self)
		self.drawaxis(self.qp)
		self.drawtimedata(self.qp)

		self.qp.setRenderHint(QPainter.Antialiasing,True)
		#self.drawPoints(self.qp)
		self.drawcurve(self.qp)
		#self.drawcurve_ex(self.qp)
	#	print 'call paintEvent'
		self.qp.end()	

	def wheelEvent(self,QmouseEvent):
		print 'call mouse event'
		print QmouseEvent.pos()
		self.update()


class draw_line(QWidget):
	def __init__(self,color):
		super (draw_line,self).__init__()
		#self.w = 500
		#self.h = 250
		#self.setPalette( QPalette(Qt.white) )
		#self.setAutoFillBackground(True)
		#self.setMinimumSize(self.w,self.h)
		self.pen = QPen()
		self.brush = QBrush()
		self.data = list()
		self.qp = QPainter()
		self.color = color

	def drawLines(self,qp):
		qp.setPen(self.color)
		qp.drawLine(0,10,80,10)
		

	def paintEvent(self,QPaintEvent):
		self.qp.begin(self)
		self.drawLines(self.qp)
		print 'call paintEvent'
		self.qp.end()	



class layoutUi(QWidget):
	def __init__(self):
		super(layoutUi,self).__init__()

		self.comlist = ['COM1','COM2','COM3','COM4']
		self.baudlist = ['300','600','1200','2400','4800','9600',
						 '19200','38400','43000','56000','57600','115200','250000']
		self.resize(800, 600)
		self.setupUi()
		
	def setupUi(self):
		self.mainlayout = QGridLayout(self)
#################################################################		
		#self.top_1_layout = QGridLayout()
	
		self.label_title = QLabel("<h2>Serial data</h2>")
		self.label_title.setAlignment(Qt.AlignCenter) 
		#self.top_1_layout.addWidget(label_title,0,0)
		self.mainlayout.addWidget(self.label_title,0,0)
		
#################################################################
		self.top_2_layout = QGridLayout()
		
		#self.top_2_left_layout = QGridLayout()
		self.browser_monitor = QTextBrowser()
	
		self.browser_monitor.setPalette( QPalette(Qt.black) )
		self.browser_monitor.setAutoFillBackground(True)
		self.mainlayout.addWidget(self.browser_monitor,1,0)

		#self.top_2_layout.addLayout(self.top_2_left_layout,0,0)		
#################################################################
		
		self.top_2_right_layout = QGridLayout()
		
		self.label_serial_name = QLabel("Serial name")      
		self.top_2_right_layout.addWidget(self.label_serial_name,0,0)
		
		self.combox_serial_name = QComboBox()
		self.combox_serial_name.addItems( self.comlist )
		#palette1 = QPalette()
	#	palette1.setColor(QPalette.Button, Qt.blue)   # 设置背景颜色
		#palette1.setColor(self.browser_monitor(), QColor(192,253,123))   # 设置背景颜色
		#self.combox_serial_name.setAutoFillBackground(True)
		#self.combox_serial_name.setPalette(palette1)
	
		self.top_2_right_layout.addWidget(self.combox_serial_name,0,1)
		
		self.label_Baud_rate = QLabel("Baud rate")
		self.combox_serial_name.setPalette( QPalette(Qt.green) )
		self.combox_serial_name.setAutoFillBackground(True)
		self.top_2_right_layout.addWidget(self.label_Baud_rate,1,0)
		
		self.combox_baud_rate = QComboBox()
		self.combox_baud_rate.addItems( self.baudlist )
		self.top_2_right_layout.addWidget(self.combox_baud_rate,1,1)
		
		self.label_data_byte = QLabel("Data byte")
		self.top_2_right_layout.addWidget(self.label_data_byte,2,0)
		
		self.combox_data_byte = QComboBox()
		self.combox_data_byte.addItems( ['8','9'] )
		self.top_2_right_layout.addWidget(self.combox_data_byte,2,1)
		
		self.label_odd_even_check = QLabel("Odd Check")
		self.top_2_right_layout.addWidget(self.label_odd_even_check,3,0)
		
		self.combox_dodd_even_check = QComboBox()
		self.combox_dodd_even_check.addItems( ['No','Odd','Even'] )
		self.top_2_right_layout.addWidget(self.combox_dodd_even_check,3,1)
		
		self.label_stop_byte = QLabel("Stop byte")
		self.top_2_right_layout.addWidget(self.label_stop_byte,4,0)
		
		self.combox_stop_byte = QComboBox()
		self.combox_stop_byte.addItems( ['1','1.5','2'] )
		self.top_2_right_layout.addWidget(self.combox_stop_byte,4,1)
		
		self.button_open_serial = QPushButton('Open serial')
		self.top_2_right_layout.addWidget(self.button_open_serial,5,1)

		
		self.button_close_serial = QPushButton('Close serial')
		self.top_2_right_layout.addWidget(self.button_close_serial,6,1)

		self.button_clear_data = QPushButton('Clear data')
		self.top_2_right_layout.addWidget(self.button_clear_data,6,0)

		self.read_ = QCheckBox('Read buff')
		self.top_2_right_layout.addWidget(self.read_,9,0)
	
		self.checkbox_ = QCheckBox('HEX')
		self.top_2_right_layout.addWidget(self.checkbox_,10,0)
		
		self.send_clear = QCheckBox('Send clear')
		self.top_2_right_layout.addWidget(self.send_clear,10,1)
		

		self.top_2_layout.addLayout(self.top_2_right_layout,0,1)	
		self.mainlayout.addLayout(self.top_2_layout,1,1)
		
#################################################################	
		self.middlelayout = QGridLayout()
		
		self.browser_send_data = QLineEdit()
		palette1 = QPalette()
		#palette1.setColor(QPalette.Button, Qt.blue)   # 设置背景颜色
		#palette1.setColor(QPalette.Window, Qt.black)   # 设置背景颜色
		self.browser_send_data.setAutoFillBackground(True)
		self.browser_send_data.setPalette( QPalette(Qt.black) )
		
		self.mainlayout.addWidget(self.browser_send_data,2,0)
	
		self.button_send_data = QPushButton('Send data')
		self.mainlayout.addWidget(self.button_send_data,2,1)
		
		#self.mainlayout.addLayout(self.middlelayout,2,0)
			
#################################################################
	
		self.label_real_time_curve = QLabel("<h2>Real time curve</h2>")
		self.label_real_time_curve.setAlignment(Qt.AlignCenter) 

		self.mainlayout.addWidget(self.label_real_time_curve,3,0)

#################################################################
	
		self.downlayout = QGridLayout()
		#self.down_left_layout = QGridLayout()
		
		self.browser_monitor_2 = draw()
		self.mainlayout.addWidget(self.browser_monitor_2,4,0)
		
		self.history_view = QScrollBar(Qt.Horizontal)#,self.bottomRightGroupBox)
		self.history_view.setMaximum (0)
						
		self.mainlayout.addWidget(self.history_view,5,0)
	
	
	

		#self.downlayout.addLayout(self.down_left_layout,0,0)
		
#################################################################		
		
		
		self.down_right_layout = QGridLayout()
		
		self.label_data_channel = QLabel("Begin channel")
		self.down_right_layout.addWidget(self.label_data_channel,0,0)
		
		self.combox_data_channel = QComboBox()
		self.combox_data_channel.addItems( ['1','2','3'] )
		self.down_right_layout.addWidget(self.combox_data_channel,0,1)
		
		self.button_hold_drawing = QPushButton('hold drawing')
		self.down_right_layout.addWidget(self.button_hold_drawing,1,0)

		self.button_clear_drawing = QPushButton('clear drawing')
		self.down_right_layout.addWidget(self.button_clear_drawing,2,0)


		self.button_start_drawing = QPushButton('Start drawing')
		self.down_right_layout.addWidget(self.button_start_drawing,1,1)
		
		self.button_close_drawing = QPushButton('Close drawing')
		self.down_right_layout.addWidget(self.button_close_drawing,2,1)
		
		self.label_channel_1 = QLabel("CH1")
		self.down_right_layout.addWidget(self.label_channel_1,3,0)
		
#		self.label_channel_line = QFrame()
#		self.label_channel_line.setFrameShape(QFrame.HLine)
#		self.label_channel_line.setStyleSheet("QFrame{ background-color: solid red ; border: 1px solid red;   }") 
		self.label_channel_line_1 = draw_line(Qt.red)

		self.down_right_layout.addWidget(self.label_channel_line_1,3,1)

		self.label_channel_2 = QLabel("CH2")
		self.down_right_layout.addWidget(self.label_channel_2,4,0)
		self.label_channel_line_2 = draw_line(QColor(0,0,255))
		self.down_right_layout.addWidget(self.label_channel_line_2,4,1)


		self.label_channel_3 = QLabel("CH3")
		self.down_right_layout.addWidget(self.label_channel_3,5,0)
		self.label_channel_line_3 = draw_line(QColor(0,255,0))
		self.down_right_layout.addWidget(self.label_channel_line_3,5,1)


#		self.label_channel_4 = QLabel("CH4")
#		self.down_right_layout.addWidget(self.label_channel_4,6,0)
#		self.label_channel_line_4 = draw_line(QColor(155,155,0))
#		self.down_right_layout.addWidget(self.label_channel_line_4,6,1)

#		self.label_channel_5 = QLabel("CH5")
#		self.down_right_layout.addWidget(self.label_channel_5,7,0)
#		self.label_channel_line_5 = draw_line(QColor(255,255,0))
#		self.down_right_layout.addWidget(self.label_channel_line_5,7,1)

#		self.label_channel_6 = QLabel("CH6")
#		self.down_right_layout.addWidget(self.label_channel_6,8,0)
#		self.label_channel_line_6 = draw_line(QColor(255,0,255))
#		self.down_right_layout.addWidget(self.label_channel_line_6,8,1)

#		self.label_channel_7 = QLabel("CH7")
#		self.down_right_layout.addWidget(self.label_channel_7,9,0)
#		self.label_channel_line_7 = draw_line(QColor(0,255,255))
#		self.down_right_layout.addWidget(self.label_channel_line_7,9,1)

#		self.label_channel_8 = QLabel("CH8")
#		self.down_right_layout.addWidget(self.label_channel_8,10,0)
#		self.label_channel_line_8 = draw_line(QColor(0,155,144))
#		self.down_right_layout.addWidget(self.label_channel_line_8,10,1)
		
		self.leftmark = QDial()#QSlider(Qt.Horizontal)
		#self.leftmark.setMaximum(1023)
		#self.leftmark.setSingleStep(1)
		#self.leftmark.setOrientation(QtCore.Qt.Horizontal)
		self.down_right_layout.addWidget(self.leftmark,6,0)
		
		self.rightmark = QDial()#QSlider(Qt.Horizontal)
		#self.leftmark.setMaximum(1023)
		#self.rightmark.setSingleStep(1)
		#self.leftmark.setOrientation(QtCore.Qt.Horizontal)
		self.down_right_layout.addWidget(self.rightmark,6,1)
		
		self.timelabel = QLabel('time /ms')
		self.timelabel.setAlignment(Qt.AlignCenter) 
		self.down_right_layout.addWidget(self.timelabel,7,0)
	
		self.timeshow = QDoubleSpinBox()
		self.timeshow.setAlignment(Qt.AlignCenter) 
		self.down_right_layout.addWidget(self.timeshow,7,1)
			

		self.downlayout.addLayout(self.down_right_layout,0,1)
		self.mainlayout.addLayout(self.downlayout,4,1)
		

######################################################		
		#self.setLayout(self.mainlayout)
		

 



class move_bar(QWidget):
	def __init__(self):
		super(move_bar,self).__init__()
		
		self.w = 10
		self.h = 250
		self.setPalette( QPalette(Qt.black) )
		self.setAutoFillBackground(True)
		self.pen = QPen(Qt.red,1,Qt.SolidLine,Qt.RoundCap)
		







class plot(QWidget):
	def __init__(self):
		super (draw,self).__init__()
		self.w = 500
		self.h = 250
		self.setPalette( QPalette(Qt.black) )
		self.setAutoFillBackground(True)
		self.setMinimumSize(self.w+10,self.h+20)
		self.pen = QPen(Qt.red,1,Qt.SolidLine,Qt.RoundCap)
		self.brush = QBrush()
		self.buff  = list()
		self.keepdata = list()

		self.qp = QPainter()
		self.color = Qt.red

		self.base_px = self.width() - 20
		self.base_py = self.height() - 20


	def corrdchange(self,x,y):
		return 

	def getwidth(self):
		return self.width()

	def havedata(self):
		if len(self.data) !=0:
			return True
		else:
			return False
	

	def drawcurve(self,qp):
		length = len(self.buff)
		if length > 1:
			qp.setPen(self.pen)
			try:
				length = len(self.data)
				for i in range(1,length):
					qp.drawLine(0,0,10,1)
			except Exception, e:
				print e

	def paintEvent(self,QPaintEvent):
		self.qp.begin(self)
		self.qp.setRenderHint(QPainter.Antialiasing,True)
		self.drawcurve(self.qp)
		self.qp.end()	


