from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, os, inspect
import tablewatcher
import iomrc
import parser
class table():

	def __init__(self, path, extension):
		self.path = path
		self.extension = extension
		#Widget config
		self.tableWidget = QtWidgets.QTableWidget()
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(0)
		self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.tableWidget.setFixedHeight(600)
		self.tableWidget.setFixedWidth(400)
		#Widget content
		headerList = ["File name","Picture","Parameters"]
		self.tableWidget.setHorizontalHeaderLabels(headerList)
		fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]
		horizontalHeader = self.tableWidget.horizontalHeader();
		verticalHeader = self.tableWidget.verticalHeader();
		horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

		for i in range(0,len(fileList)):
			filenameItem = QtWidgets.QTableWidgetItem(fileList[i])
			#Image
			iconItem = QtWidgets.QTableWidgetItem()
			pixmap = iomrc.getpixmap(self.path+fileList[i])
			image = QtGui.QPixmap(pixmap)
			iconItem.setData(Qt.Qt.DecorationRole, image)

			stats = parser.getStats(fileList[i])
			statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\n Phase shift: " + stats[3])
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setItem(i, 0, filenameItem)
			self.tableWidget.setItem(i, 1, iconItem)
			self.tableWidget.setItem(i, 2, statsItem)
		self.watcher = tablewatcher.watcher(self)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QWidget()
	mainLayout = QtWidgets.QGridLayout()
	table = table('/home/tandat/test2/','cor.mrc')
	mainLayout.addWidget(table.tableWidget)
	window.setLayout(mainLayout)
	window.show()
	sys.exit(app.exec_())