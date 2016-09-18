#coding=utf-8
from serial import Serial
from PyQt4 import QtCore, QtGui
import time
class my_serial:
	def __init__(self):
		self.com      = 'COM1'
		self.baud     = 250000
		self.byte     = 8
		self.parity   = "N" 
		self.bits     = 1

		self.__isopen__= 0
		#self.serial_open()

	def set_com(self,com):
		self.com = com
	
	def set_baud(self,baud):
		self.baud = baud
	
	def set_byte(self,byte):
		self.baud = byte

	def set_stopbits(self,bit):
		if bit == 1:
			self.bits = 1
		elif bit == 1.5:
			self.bits = 1.5
		elif bit == 2:
			self.bits = 2

	def set_parity(self,flag):
		if flag == 'No':
			self.parity = 'N'
		elif flag == 'Odd':
			self.parity = 'O'
		elif flag == 'Even':
			self.parity = 'E'


	def serial_open(self):
		try:
			self.hand = Serial( self.com,    self.baud,self.byte,
								self.parity, self.bits )
			print 'sucess'
			self.hand.reset_input_buffer()
			self.__isopen__ = 1
			return True
		except Exception, e:
			print e
			return False

	def serial_iswaiting(self):
		return self.hand.inWaiting() #缓冲区数据字节数
	
	def serial_write(self,data):
		self.hand.write(data)


	def serial_read(self):
		if  self.__isopen__==1:
			while self.hand.inWaiting()>0:
				bit = self.hand.inWaiting()
				if bit < 60:
					data = self.hand.read(bit)
					return data
				else:
					data = 20
					data = self.hand.read(bit)
					self.val = data
					return data
			#time.sleep(0.001)
			#print data
		

	def serial_readline(self):
		if  self.__isopen__==1:
			data = self.hand.readline()
			#print data
			self.val = data
			#time.sleep(0.001)
			#print self.serial_iswaiting()
		else:
			data = -1
		return data
	
	def serial_formal_data(self):
		length = self.serial_iswaiting()
		if length > 0:
			data = self.hand.read(length)
			while data[-1] != '\n':
				data += self.hand.read()
				#print data[-1]
		else:
			data = ''
		return data
			
	def serial_clear_buffer(self):
		self.hand.reset_input_buffer()

			




	def serial_close(self):
		self.hand.close()
		self.__isopen__ = 0


