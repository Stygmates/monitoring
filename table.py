from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, os, inspect
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
		self.extensionLayout = QtWidgets.QHBoxLayout()
		self.extensionLayout.setAlignment(Qt.Qt.AlignLeft)
		self.buttonsLayout = QtWidgets.QHBoxLayout()
		self.buttonsLayout.setAlignment(Qt.Qt.AlignRight)
		#Widget config
		self.applyButton = self.applyButton()
		self.extensionLineEdit = self.extensionLineEdit()
		self.tableWidget = self.tableWidget()
		self.updateList()
		self.quitButton = self.quitButton()
		self.backButton = self.backButton()


		self.buttonsLayout.addWidget(self.quitButton)
		self.buttonsLayout.addWidget(self.backButton)

		self.extensionLayout.addWidget(self.extensionLineEdit)
		self.extensionLayout.addWidget(self.applyButton)

		self.centeredLayout.addLayout(self.extensionLayout)
		self.centeredLayout.addWidget(self.tableWidget)
		self.centeredLayout.addLayout(self.buttonsLayout)

		self.mainLayout.addLayout(self.centeredLayout)

		self.watcher = tablewatcher.watcher(self)

	def tableWidget(self):
		tableWidget = QtWidgets.QTableWidget()
		tableWidget.setColumnCount(3)
		tableWidget.setRowCount(0)
		tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		tableWidget.setFixedHeight(900)
		tableWidget.setFixedWidth(700)
		headerList = ["File name","Picture","Parameters"]
		tableWidget.setHorizontalHeaderLabels(headerList)
		horizontalHeader = tableWidget.horizontalHeader();
		verticalHeader = tableWidget.verticalHeader();
		horizontalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		verticalHeader.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
		return tableWidget

	def updateList(self):
		self.tableWidget.setRowCount(0)
		fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]
		for i in range(0,len(fileList)):
			filenameItem = QtWidgets.QTableWidgetItem(fileList[i])
			#Image
			iconItem = QtWidgets.QTableWidgetItem()
			print(self.path+fileList[i])
			pixmap = iomrc.getpixmap(self.path+fileList[i]).scaled(300,300)
			image = QtGui.QPixmap(pixmap)
			iconItem.setData(Qt.Qt.DecorationRole, image)
			stats = parser.getStats(fileList[i])
			statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\n Phase shift: " + stats[3])
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setItem(i, 0, filenameItem)
			self.tableWidget.setItem(i, 1, iconItem)
			self.tableWidget.setItem(i, 2, statsItem)

	def extensionLineEdit(self):
		extensionLineEdit = QtWidgets.QLineEdit()
		extensionLineEdit.setFixedWidth(400)
		return extensionLineEdit

	def applyButton(self):
		applyButton = QtWidgets.QPushButton("Apply")
		applyButton.clicked.connect(self.applyFunction)
		applyButton.setFixedWidth(200)
		return applyButton

	def applyFunction(self):
		print("Apply Function")

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
	table = table('/home/tandat/test2/','.ctf')
	window.setLayout(table.mainLayout)
	window.show()
	sys.exit(app.exec_())