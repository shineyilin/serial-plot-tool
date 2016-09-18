#coding=utf-8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from math import * 










#grahisc view 步骤
# 1, 建立场景
# 2, 创建直线对象
# 3, 观察


class colorItem(QGraphicsItem):
	n = 0

	def __init__(self):
		super(colorItem, self).__init__()

		self.color = QColor(qrand() % 256,qrand() % 256,qrand() % 256)
		self.setToolTip("QColor(%d, %d, %d)\nClick and drag this color onto the robot!" % 
			( self.color.red(), self.color.green(), self.color.blue() ) )
		self.setCursor(Qt.OpenHandCursor)

	
	def boundingRect(self):
		return QRectF(-15.5, -15.5, 34, 34)

	def paint(self, painter, option, widget):
		painter.setPen(Qt.NoPen)
		painter.setBrush(Qt.darkGray)
		painter.drawEllipse(-12, -12, 30, 30)
		painter.setPen(QPen(Qt.black, 1))
		painter.setBrush(QBrush(self.color))

		for t in range(0,620):
			painter.drawLine(t, -100*sin(t/100.0)-50, 0,0)

	def mousePressEvent(self, event):
		if event.button() != Qt.LeftButton:
			event.ignore()
			return
		self.setCursor(Qt.ClosedHandCursor)

	def mouseReleaseEvent(self, event):
		self.setCursor(Qt.OpenHandCursor)



if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	scene = QGraphicsScene(-40,-400,440,440)
	scene.addLine(0,0,400,0)
	scene.addLine(0,0,0,-400)
	m = colorItem()
	scene.addItem(m)
	view  = QGraphicsView(scene)
	view.show()
	app.exec_()













