from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, os, inspect, re
import tablewatcher
import iomrc
import parser
import threads
class table():

	def __init__(self, parent, path, extension):
		self.parent = parent
		self.window = QtWidgets.QWidget()
		self.threadpool = QtCore.QThreadPool()

		self.widgetsSize = 100
		self.path = path + "/"
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

		self.window.setLayout(self.mainLayout)
		self.window.show()

		self.updateList()


	def tableWidget(self):
		tableWidget = QtWidgets.QTableWidget()
		headerList = ["File name","Ctf","Corresponding mrc","Parameters"]
		tableWidget.setColumnCount(len(headerList))
		tableWidget.setRowCount(0)
		tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		tableWidget.setFixedHeight(len(headerList)*300)
		tableWidget.setFixedWidth(len(headerList)*300)
		tableWidget.setHorizontalHeaderLabels(headerList)
		for i in range(0,len(headerList)):
			tableWidget.setColumnWidth(i,300)
		return tableWidget

	def updateList(self):
		self.tableWidget.setRowCount(0)
		fileList = [f[:-4] for f in os.listdir(self.path) if f.endswith(self.extension)]
		try:
			regex = re.compile(self.filterLineEdit.text())
			filteredList = list(filter(regex.search, fileList))
		except Exception as e:
			filteredList = fileList

		for i in range(0,len(filteredList)):
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setRowHeight(i,300)
			filename = filteredList[i]
			filenameItem = QtWidgets.QTableWidgetItem(filename)
			#Image

			statslog = self.path + filename + "_sum-cor_gctf.log"
			stats = parser.getStats(self,statslog)
			if stats is None:
				statsItem = QtWidgets.QTableWidgetItem("Defocus U:\nDefocus V:\n Phase shift: ")
			else:
				statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\n Phase shift: " + stats[3])
			
			self.tableWidget.setItem(i, 0, filenameItem)
			self.tableWidget.setItem(i, 3, statsItem)

			worker = threads.Worker(self.loadmrc, filename, i)
			worker.signals.result.connect(self.updatemrc)
			self.threadpool.start(worker)
			worker2 = threads.Worker(self.loadctf, filename, i)
			worker2.signals.result.connect(self.updatectf)
			self.threadpool.start(worker2)

		self.tableWidget.sortItems(0)


	def updatemrc(self,result):
		self.tableWidget.setItem(result[1], 2, result[0])

	def updatectf(self,result):
		self.tableWidget.setItem(result[1], 1, result[0])
		
	def loadmrc(self, filename, index):
		mrcItem = QtWidgets.QTableWidgetItem()
		mrcpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.mrc")
		if mrcpixmap is not None:
			mrcpixmap = mrcpixmap.scaled(300,300)
			mrc = QtGui.QPixmap(mrcpixmap)
			mrcItem.setData(Qt.Qt.DecorationRole, mrc)
			return [mrcItem, index]
		else:
			return

	def loadctf(self,filename, index):
		ctfItem = QtWidgets.QTableWidgetItem()
		ctfpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.ctf")
		if ctfpixmap is not None:
			ctfpixmap = ctfpixmap.scaled(300,300)
			ctf = QtGui.QPixmap(ctfpixmap)
			ctfItem.setData(Qt.Qt.DecorationRole, ctf)
			return [ctfItem, index]
		else:
			return

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
		self.window.close()
		self.parent.window.show()

	def quitButton(self):
		quitButton = QtWidgets.QPushButton("Quit")
		quitButton.clicked.connect(self.quitFunction)
		quitButton.setFixedWidth(self.widgetsSize)
		return quitButton

	def quitFunction(self):
		self.parent.app.quit()



# if __name__ == '__main__':
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = QtWidgets.QWidget()
# 	mainLayout = QtWidgets.QGridLayout()
# 	table = table('/home/tandat/test2/','cor.mrc')
# 	window.setLayout(table.mainLayout)
# 	window.show()
# 	sys.exit(app.exec_())