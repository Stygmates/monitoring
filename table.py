from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys, os, inspect, re
import tablewatcher
import iomrc
import parser
import threads
ITEM = 0
RESULTINDEX = 1

FILENAMEINDEX = 0
CTFINDEX = 1
MRCINDEX = 2
STATSINDEX = 3

WIDGETSIZE = 220
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
		tableWidget.setFixedHeight(4 * WIDGETSIZE)
		tableWidget.setFixedWidth(len(headerList) * WIDGETSIZE + 31)
		tableWidget.setHorizontalHeaderLabels(headerList)
		for i in range(0,len(headerList)):
			tableWidget.setColumnWidth(i,WIDGETSIZE)
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
			self.tableWidget.setRowHeight(i, WIDGETSIZE)
			filename = filteredList[i]
			filenameItem = QtWidgets.QTableWidgetItem(filename)
			self.tableWidget.setItem(i, 0, filenameItem)

			workerCtf = threads.mainWorker(self.loadCtf, CTFINDEX, self.path, filteredList[i], i)
			workerCtf.signals.mainCtf.connect(self.updateCtf)
			self.threadpool.start(workerCtf)

			workerMrc = threads.mainWorker(self.loadMrc, MRCINDEX, self.path,filteredList[i], i)
			workerMrc.signals.mainMrc.connect(self.updateMrc)
			self.threadpool.start(workerMrc)

			workerStats = threads.mainWorker(self.loadStats, STATSINDEX, self.path, filteredList[i], i)
			workerStats.signals.mainStats.connect(self.updateStats)
			self.threadpool.start(workerStats)

		self.tableWidget.sortItems(0)

	def loadMrc(self, filename, index):
		mrcItem = QtWidgets.QTableWidgetItem()
		mrcpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.mrc")
		if mrcpixmap is not None:
			mrcpixmap = mrcpixmap.scaled(WIDGETSIZE,WIDGETSIZE)
			mrc = QtGui.QPixmap(mrcpixmap)
			mrcItem.setData(Qt.Qt.DecorationRole, mrc)
			result = [mrcItem,index]
			return result
		else:
			return

	def loadCtf(self,filename, index):
		ctfItem = QtWidgets.QTableWidgetItem()
		ctfpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.ctf")
		if ctfpixmap is not None:
			ctfpixmap = ctfpixmap.scaled(WIDGETSIZE,WIDGETSIZE)
			ctf = QtGui.QPixmap(ctfpixmap)
			ctfItem.setData(Qt.Qt.DecorationRole, ctf)
			result = [ctfItem,index]
			return result
		else:
			return

	def loadStats(self,filename,index):
		statslog = self.path + filename + "_sum-cor_gctf.log"
		stats = parser.getStats(self,statslog)
		if stats is None:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U:\nDefocus V:\n Phase shift: ")
		else:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\nPhase shift: " + stats[3])
		result = [statsItem,index]
		return result

	def updateFilename(self, result):
		self.tableWidget.setItem(result[RESULTINDEX], FILENAMEINDEX, result[ITEM])

	def updateStats(self, result):
		self.tableWidget.setItem(result[RESULTINDEX], STATSINDEX, result[ITEM])

	def updateMrc(self,result):
		if result is not None:
			self.tableWidget.setItem(result[RESULTINDEX], MRCINDEX, result[ITEM])

	def updateCtf(self,result):
		if result is not None:
			self.tableWidget.setItem(result[RESULTINDEX], CTFINDEX, result[ITEM])

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