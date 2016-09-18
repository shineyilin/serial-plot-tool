from myserial import my_serial


import time 

import re

m = my_serial()
m.serial_open()

data = list()
i = 0
while 1:
	#time.sleep(0.1)
	#i += 1
	#if i %10 == 0:
		data = m.serial_formal_data()
		vals = re.findall( re.compile('(.*?)\n',re.S),data)
		if len(vals) != 0:
			for val in vals:
				val
		print len(vals)
