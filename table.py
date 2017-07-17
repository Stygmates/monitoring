from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, os, inspect
import tablewatcher
class table():

	def __init__(self, path, extension):
		self.path = path
		self.extension = extension
		#Widget config
		self.tableWidget = QtWidgets.QTableWidget()
		self.tableWidget.setColumnCount(3)
		self.tableWidget.setRowCount(0)
		self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows);

		#Widget content
		headerList = ["File name","Picture","Parameters"]
		self.tableWidget.setHorizontalHeaderLabels(headerList)
		fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]


		for i in range(0,len(fileList)):
			nameItem = QtWidgets.QTableWidgetItem(fileList[i])
			iconItem = QtWidgets.QTableWidgetItem(fileList[i])
			image = QtGui.QPixmap('/home/tandat/workspace/monitoring/pikachu.jpg')
			icon = QtGui.QIcon(image)
			iconItem.setIcon(icon)
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setItem(i, 0, nameItem)
			self.tableWidget.setItem(i, 1, iconItem)
		self.watcher = tablewatcher.watcher(self)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QWidget()
	mainLayout = QtWidgets.QGridLayout()
	table = table('/home/tandat/workspace/monitoring','.txt')
	mainLayout.addWidget(table.tableWidget)
	window.setLayout(mainLayout)
	window.show()
	sys.exit(app.exec_())