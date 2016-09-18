#coding=utf-8

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from windowUi import layoutUi
from myserial import my_serial

import threading
import time
import re
import binascii

def str_hex(val):
	temp = list()
	for v in val:
		temp.append( binascii.b2a_hex(v) ) 
		temp.append(" ")
	return (''.join(temp)).upper()

class Window(QWidget):
	def __init__(self):
		super(Window,self).__init__()
		self.ui = layoutUi()
		self.hand = my_serial()
		self.setLayout(self.ui.mainlayout)
		self.setWindowTitle("Created by SHAN YL")

		icon = QIcon()
		icon.addPixmap(QPixmap("logo.png"),QIcon.Normal, QIcon.Off)
		self.setWindowIcon(icon)
		
		self.connect_signal()
		qpalette = QPalette()
		qpalette.setColor(QPalette.WindowText,Qt.blue)# 前景色
		qpalette.setColor(QPalette.Window,Qt.black)
		self.showMaximized()
        
		self.setPalette( qpalette )
		self.setAutoFillBackground(True)
		#self.setWindowOpacity(1);      
		#self.setWindowFlags(Qt.FramelessWindowHint);      
		#self.setAttribute(Qt.WA_TranslucentBackground);  


		cre = self.frameGeometry() #获取程序窗口大小
		cent = QDesktopWidget().availableGeometry().center() #计算屏幕中心
		cre.moveCenter(cent)  #移动中心到屏幕中心
		self.move(cre.topLeft()) #移动程序到左上角

		self.__isopen__    = False  #串口标志位
		self.__datatype__  = "ASC"
		self.__draw__      = False
		self.__draw_act__  = True 
		self.__tim__       = 0	
		
		self.val           = list()
		self.befval        = 0

		self.lock = threading.Lock()

	
	def __del__(self):
		self.__isopen__ == False

	def connect_signal(self):  #连接信号槽
		self.ui.button_open_serial.clicked.connect(self.onOpenport)		
		self.ui.button_close_serial.clicked.connect(self.closePort)
		self.ui.combox_serial_name.activated.connect(self.setserialname)
		self.ui.combox_baud_rate.activated.connect(self.setserialbaud)
		self.ui.combox_data_byte.activated.connect(self.setserialbyte)
		self.ui.combox_dodd_even_check.activated.connect(self.setoddevencheek)
		self.ui.combox_stop_byte.activated.connect(self.setserialstopbites)
		self.ui.checkbox_.stateChanged.connect(self.outputhex)
		self.ui.button_clear_data.clicked.connect(self.cleardata)
		self.ui.button_send_data.clicked.connect(self.senddata)
		self.ui.button_start_drawing.clicked.connect(self.onstartdrawing)
		self.ui.button_close_drawing.clicked.connect(self.onenddrawing)

		self.ui.button_hold_drawing.clicked.connect(self.onholddrawing)
		self.ui.button_clear_drawing.clicked.connect(self.oncleardrawing)
		self.ui.history_view.valueChanged.connect(self.historyview)

		self.ui.leftmark.valueChanged.connect(self.marktimecount)
		self.ui.rightmark.valueChanged.connect(self.marktimecount)

		#self.connect(self.ui.combox_serial_name, SIGNAL('activated(QString)'), self.setserialname);
		
	def onOpenport(self):  #打开串口
	
		if  self.__isopen__ == False:
			if self.hand.serial_open() == True:
				self.__isopen__ = True
				self.hand.serial_clear_buffer()
				showinterrupt = threading.Thread(target = self.serial_interrupt)				
				showinterrupt.setDaemon(True)
				showinterrupt.start()
			else:
				QMessageBox.critical(self,"Error",'Can not open serial port!')

	

	def closePort(self):  #关闭串口 标志位 __isopen__ 
		if self.__isopen__ == True:
			self.hand.serial_close()
			print 'close port'
			self.__isopen__ = False
			#self.ui.browser_monitor_2.clear_data()
			#self.ui.browser_monitor.clear_data()


	def cleardata(self):
		try:
			self.ui.browser_monitor.clear()
		except Exception,e:
			print e

	def setserialname(self):
		com_name = self.ui.combox_serial_name.currentText()
		print com_name
		self.hand.set_com(str(com_name) )

	def setserialbaud(self):
		baud_rate = self.ui.combox_baud_rate.currentText()
		print baud_rate
		self.hand.set_baud(int(baud_rate) )
	
	def setserialbyte(self):
		byte = self.ui.combox_data_byte.currentText()
		print byte
		self.hand.set_byte(int(byte) )
	
	def setoddevencheek(self):
		cheek = self.ui.combox_dodd_even_check.currentText()
		print cheek
		self.hand.set_parity(str(cheek) )


	def setserialstopbites(self):
		bits = self.ui.combox_stop_byte.currentText()
		print bits
		self.hand.set_stopbits(bits )

	def senddata(self):
		if self.__isopen__ == True:
			val = str(self.ui.browser_send_data.text() )
			self.hand.serial_write(val )
			self.ui.browser_monitor.append("<font color = green >%s</font>" %(val))
		else:
			 QMessageBox.critical(self, "Error", "Please open serial port!" )
		if self.ui.send_clear.isChecked():
			self.ui.browser_send_data.clear()

	def outputhex(self):
		if self.ui.checkbox_.isChecked(): 
			self.__datatype__ = "HEX"
		else: 
			self.__datatype__ = "ASC"

	def onstartdrawing(self):
		if self.__isopen__ ==True:
			self.__draw__ = True
			self.hand.serial_clear_buffer()
			curveinterrupt = threading.Thread(target = self.curve_interrupt)				
			curveinterrupt.setDaemon(True)
			curveinterrupt.start()
		else:
			QMessageBox.critical(self,"Error",'Please open serial port!')

	def onenddrawing(self):
			self.__draw__ = False

	def onholddrawing(self):
		if 	self.__draw_act__ == False:
			self.__draw_act__ = True
		else:
			self.__draw_act__ = False
	
	def oncleardrawing(self):
		self.ui.history_view.setMaximum (0)
		self.ui.history_view.setValue(0)				

		self.ui.browser_monitor_2.clear_data()
		self.__tim__ = 0
	
	def historyview(self):
		val = self.ui.history_view.value()
		if self.__draw__ == False and self.befval != val :
			print 'on call history_view'
			self.befval = val
			self.ui.history_view.setValue(val)				
			print val
			w = self.ui.browser_monitor_2.getwidth()
			self.ui.browser_monitor_2.showkeepdata(val)
			self.ui.leftmark.setMaximum(w)
			self.ui.rightmark.setMaximum(w)

	def marktimecount(self):
		if self.__draw__==False or self.__draw_act__ == False:
			if self.ui.browser_monitor_2.havedata() == True:
				a = self.ui.browser_monitor_2.showtimedata( self.ui.leftmark.value(),
														self.ui.rightmark.value())

				self.ui.timeshow.setValue(a*1000)
	
	def curve_interrupt(self):
		while self.__draw__ == True and self.__isopen__ == True:
			if len(self.val) != 0 and self.__draw_act__ == True: 
				temp = self.val.pop(0)
				try:
					self.ui.browser_monitor_2.adddata([temp[0], temp[1]])
					self.__tim__ += 1
					#if self.__tim__ <= 200000:
					self.ui.history_view.setMaximum (self.__tim__ )
					self.ui.history_view.setValue(self.__tim__    )
	
				except:
					print 'e'

	def serial_interrupt(self):  #打开串口接收线程
		print 'on start'
		#f = open('data.text','w')
		while self.__isopen__ == True:	
			try:
				if self.__draw__ == False:
					if self.ui.read_.isChecked():		
						val = self.hand.serial_read()
					else:
						val = self.hand.serial_readline()
					self.show_data(val)
					time.sleep(0.05)
				
				else:
					time.clock()
					data = self.hand.serial_formal_data()
					self.clock = time.clock()
					
					vals = re.findall( re.compile('(.*?)\n',re.S),data)
					if len(vals) != 0:
						for val in vals:
							self.val.append([val,self.clock])  #获取串口数据
			except Exception,e:
				print e
		
#time.sleep(0.01)

	def show_data(self,val):
		#self.ui.browser_monitor.append('Recv <font color="white">%s</font>' %(time.ctime() ) )	
		if self.__datatype__ == "ASC":
			self.ui.browser_monitor.append('<font color="yellow">%s</font> ' % (val) )
			#self.ui.browser_monitor.append(val)
		else:
			self.ui.browser_monitor.append('<font color="yellow">%s</font><br></br> ' % (str_hex(val) ) )
			#self.ui.browser_monitor.append(str_hex(val) )
		text_move = self.ui.browser_monitor.verticalScrollBar()
		if text_move.value()< text_move.maximum():#如果 数据超出显示范围 移动一行数据
			text_move.setValue( text_move.maximum() )


	
		
				

import sys
if __name__ == "__main__":
	app = QApplication(sys.argv)
	w   = Window()
	w.show()
	sys.exit(app.exec_() ) 
