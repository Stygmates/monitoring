from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, os, inspect, re
import tablewatcher
import iomrc
import parser
class table():

	def __init__(self, path, extension):
		self.widgetsSize = 100
		self.path = path
		self.extension = extension
		self.centeredLayout = QtWidgets.QVBoxLayout()
		self.centeredLayout.setAlignment(Qt.Qt.AlignCenter)
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.setAlignment(Qt.Qt.AlignCenter)
		self.filterLayout = QtWidgets.QHBoxLayout()
		self.filterLayout.setAlignment(Qt.Qt.AlignLeft)
		self.buttonsLayout = QtWidgets.QHBoxLayout()
		self.buttonsLayout.setAlignment(Qt.Qt.AlignRight)
		#Widget config
		self.filterLineEdit = self.filterLineEdit()
		self.tableWidget = self.tableWidget()
		self.updateList()
		self.quitButton = self.quitButton()
		self.backButton = self.backButton()


		self.buttonsLayout.addWidget(self.quitButton)
		self.buttonsLayout.addWidget(self.backButton)

		self.filterLayout.addWidget(self.filterLineEdit)

		self.centeredLayout.addLayout(self.filterLayout)
		self.centeredLayout.addWidget(self.tableWidget)
		self.centeredLayout.addLayout(self.buttonsLayout)

		self.mainLayout.addLayout(self.centeredLayout)

		self.watcher = tablewatcher.watcher(self)

	def tableWidget(self):
		tableWidget = QtWidgets.QTableWidget()
		headerList = ["File name","Ctf","Corresponding mrc","Parameters"]
		tableWidget.setColumnCount(len(headerList))
		tableWidget.setRowCount(0)
		tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		tableWidget.setFixedHeight(900)
		tableWidget.setFixedWidth(1000)
		tableWidget.setHorizontalHeaderLabels(headerList)
		horizontalHeader = tableWidget.horizontalHeader();
		verticalHeader = tableWidget.verticalHeader();
		horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		return tableWidget

	def updateList(self):
		self.tableWidget.setRowCount(0)
		fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]
		regex = re.compile(self.filterLineEdit.text())
		filteredList = list(filter(regex.search, fileList))
		for i in range(0,len(filteredList)):
			filename = filteredList[i][:-12]
			filenameItem = QtWidgets.QTableWidgetItem(filename)
			#Image
			ctfItem = QtWidgets.QTableWidgetItem()
			ctfpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.ctf").scaled(300, 300)
			ctf = QtGui.QPixmap(ctfpixmap)
			ctfItem.setData(Qt.Qt.DecorationRole, ctf)

			mrcItem = QtWidgets.QTableWidgetItem()
			mrcpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.mrc").scaled(300, 300)
			mrc = QtGui.QPixmap(mrcpixmap)
			mrcItem.setData(Qt.Qt.DecorationRole, mrc)

			statslog = self.path + filename + "_sum-cor_gctf.log"
			stats = parser.getStats(self,statslog)
			if stats is None:
				statsItem = QtWidgets.QTableWidgetItem("Defocus U:\nDefocus V:\n Phase shift: ")
			else:
				statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\n Phase shift: " + stats[3])
			
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setItem(i, 0, filenameItem)
			self.tableWidget.setItem(i, 1, ctfItem)
			self.tableWidget.setItem(i, 2, mrcItem)
			self.tableWidget.setItem(i, 3, statsItem)

	def filterLineEdit(self):
		filterLineEdit = QtWidgets.QLineEdit()
		filterLineEdit.setFixedWidth(400)
		filterLineEdit.setPlaceholderText("Filter")
		filterLineEdit.textChanged.connect(self.updateList)
		return filterLineEdit

	def backButton(self):
		backButton = QtWidgets.QPushButton("Back")
		backButton.clicked.connect(self.backFunction)
		backButton.setFixedWidth(self.widgetsSize)
		return backButton

	def backFunction(self):
		print("Back Function")

	def quitButton(self):
		quitButton = QtWidgets.QPushButton("Quit")
		quitButton.clicked.connect(self.quitFunction)
		quitButton.setFixedWidth(self.widgetsSize)
		return quitButton

	def quitFunction(self):
		print("Quit Function")



if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	window = QtWidgets.QWidget()
	mainLayout = QtWidgets.QGridLayout()
	table = table('/home/tandat/test2/','cor.mrc')
	window.setLayout(table.mainLayout)
	window.show()
	sys.exit(app.exec_())