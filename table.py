from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys,shutil, os, inspect, re, queue, glob

import tablewatcher
import iomrc
import parser
import threads
ITEM = 0
RESULTINDEX = 1
ORIGINALPIXMAP = 2

CHECKBOXINDEX = 0
FILENAMEINDEX = 1
CTFINDEX = 2
MRCINDEX = 3
STATSINDEX = 4

WIDGETSIZE = 220

NB_WORKERS = 5


class table():

	def __init__(self, parent, path, extension):
		self.parent = parent
		self.parent.app.aboutToQuit.connect(self.quitFunction)
		self.window = QtWidgets.QWidget()
		self.threadpool = QtCore.QThreadPool()
		self.dictionnaireMrc = {}
		self.dictionnaireCtf = {}

		self.path = path + "/"
		self.extension = extension
		self.centeredLayout = QtWidgets.QHBoxLayout()
		self.centeredLayout.setAlignment(Qt.Qt.AlignCenter)
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.setAlignment(Qt.Qt.AlignCenter)
		self.filterLayout = QtWidgets.QVBoxLayout()
		#self.filterLayout.setAlignment(Qt.Qt.AlignLeft)
		self.buttonsLayout = QtWidgets.QGridLayout()
		self.buttonsLayout.setAlignment(Qt.Qt.AlignCenter)
		#Widget config
		self.filterLineEdit = self.filterLineEdit()
		self.tableWidget = self.tableWidget()

		self.clearSelectionButton = self.clearSelectionButton()
		self.uncheckSelectedButton = self.uncheckSelectedButton()
		self.checkSelectedButton = self.checkSelectedButton()
		self.moveButton = self.moveButton()
		self.quitButton = self.quitButton()
		self.backButton = self.backButton()

		self.buttonsLayout.addWidget(self.clearSelectionButton, 0, 0, 1, 2)
		self.buttonsLayout.addWidget(self.uncheckSelectedButton, 1, 0)
		self.buttonsLayout.addWidget(self.checkSelectedButton, 1, 1)
		self.buttonsLayout.addWidget(self.moveButton, 2, 0, 1, 2)
		self.buttonsLayout.addWidget(self.quitButton, 3, 0)
		self.buttonsLayout.addWidget(self.backButton, 3, 1)

		self.filterLayout.addWidget(self.filterLineEdit)

		self.centeredLayout.addWidget(self.tableWidget)
		self.centeredLayout.addLayout(self.buttonsLayout)

		self.mainLayout.addLayout(self.filterLayout)
		self.mainLayout.addLayout(self.centeredLayout)

		self.watcher = tablewatcher.watcher(self)

		self.window.setLayout(self.mainLayout)
		self.window.show()

		self.updateList()



	'''
	Main widget containing the list of all the data
	'''
	def tableWidget(self):
		tableWidget = QtWidgets.QTableWidget()
		headerList = ["","File name","Ctf","Corresponding mrc","Parameters"]
		tableWidget.setColumnCount(len(headerList))
		tableWidget.setRowCount(0)
		tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		tableWidget.setFixedHeight(4 * WIDGETSIZE)
		tableWidget.setFixedWidth((len(headerList)-1) * WIDGETSIZE + 56)
		tableWidget.setHorizontalHeaderLabels(headerList)
		tableWidget.setColumnWidth(0,25)
		tableWidget.cellDoubleClicked.connect(self.displayImage)
		for i in range(1,len(headerList)):
			tableWidget.setColumnWidth(i,WIDGETSIZE)
		return tableWidget


	'''
	Function that updates the table with all of the data
	'''
	def updateList(self):
		self.tableWidget.setRowCount(0)
		fileList = [f[:-4] for f in os.listdir(self.path) if f.endswith(self.extension)]
		try:
			regex = re.compile(self.filterLineEdit.text())
			filteredList = list(filter(regex.search, fileList))
		except Exception as e:
			filteredList = fileList

		self.filequeue = queue.Queue(0)
		for i, filename in enumerate(filteredList):
			self.tableWidget.insertRow(self.tableWidget.rowCount())
			self.tableWidget.setRowHeight(i, WIDGETSIZE)
			filenameItem = QtWidgets.QTableWidgetItem(filename)
			self.tableWidget.setItem(i, FILENAMEINDEX, filenameItem)
			checkBoxItem = QtWidgets.QTableWidgetItem()
			checkBoxItem.setCheckState(Qt.Qt.Unchecked)
			self.tableWidget.setItem(i,CHECKBOXINDEX,checkBoxItem)
			self.filequeue.put([i,filename])

		for thread in range(NB_WORKERS):
			if self.filequeue.empty() == False:
				element = self.filequeue.get()
				worker = threads.mainWorker(self.path, element[1], element[0])
				worker.signals.mainCtf.connect(self.updateCtf)
				worker.signals.mainMrc.connect(self.updateMrc)
				worker.signals.mainStats.connect(self.updateStats)
				worker.signals.startNext.connect(self.startNext)
				self.threadpool.start(worker)
		self.tableWidget.sortItems(0)

	'''
	Function called that starts a new job once the last one is done, this is to keep the number of threads workers equal to NB_WORKERS
	'''
	def startNext(self):
		if self.filequeue.empty() == False:
			element = self.filequeue.get()
			worker = threads.mainWorker(self.path, element[1], element[0])
			worker.signals.mainCtf.connect(self.updateCtf)
			worker.signals.mainMrc.connect(self.updateMrc)
			worker.signals.mainStats.connect(self.updateStats)
			worker.signals.startNext.connect(self.startNext)
			self.threadpool.start(worker)

	'''
	Function that updates the filename column on the table with the result given by one of the threads
	'''
	def updateFilename(self, result):
		self.tableWidget.setItem(result[RESULTINDEX], FILENAMEINDEX, result[ITEM])

	'''
	Function that updates the stats column on the table with the result given by one of the threads
	'''
	def updateStats(self, result):
		self.tableWidget.setItem(result[RESULTINDEX], STATSINDEX, result[ITEM])

	'''
	Function that updates the mrc column on the table with the result given by one of the threads
	'''
	def updateMrc(self,result):
		if result is not None:
			self.tableWidget.setItem(result[RESULTINDEX], MRCINDEX, result[ITEM])
			self.dictionnaireMrc[result[RESULTINDEX]] = result[ORIGINALPIXMAP]

	'''
	Function that updates the ctf column on the table with the result given by one of the threads
	'''
	def updateCtf(self,result):
		if result is not None:
			self.tableWidget.setItem(result[RESULTINDEX], CTFINDEX, result[ITEM])
			self.dictionnaireCtf[result[RESULTINDEX]] = result[ORIGINALPIXMAP]

	'''
	Function that creates the popup image when double clicking on an image
	'''
	def displayImage(self, row, column):
		if column == CTFINDEX or MRCINDEX:
			dialog = QtWidgets.QDialog()
			
			image = QtWidgets.QLabel()
			if column == CTFINDEX:
				try:
					pixmap = self.dictionnaireCtf[row].scaled(1000,1000)
				except KeyError:
					return
			else:
				try:
					pixmap = self.dictionnaireMrc[row].scaled(1000,1000)
				except KeyError:
					return
			image.setPixmap(pixmap)
			layout = QtWidgets.QVBoxLayout()
			layout.addWidget(image)
			dialog.setLayout(layout)
			dialog.show()
			dialog.exec_()

	'''
	'''
	'''Widgets definition
	'''
	'''
	'''
	def filterLineEdit(self):
		filterLineEdit = QtWidgets.QLineEdit()
		filterLineEdit.setFixedWidth(400)
		filterLineEdit.setPlaceholderText("Filter")
		filterLineEdit.textChanged.connect(self.updateList)
		return filterLineEdit

	def clearSelectionButton(self):
		clearSelectionButton = QtWidgets.QPushButton("Clear selection")
		clearSelectionButton.clicked.connect(self.clearSelectionFunction)
		return clearSelectionButton

	def checkSelectedButton(self):
		checkSelectedButton = QtWidgets.QPushButton("Check selected rows")
		checkSelectedButton.clicked.connect(self.checkSelectedFunction)
		return checkSelectedButton
	
	def uncheckSelectedButton(self):
		checkSelectedButton = QtWidgets.QPushButton("Uncheck selected rows")
		checkSelectedButton.clicked.connect(self.uncheckSelectedFunction)
		return checkSelectedButton

	def moveButton(self):
		moveButton = QtWidgets.QPushButton("Move to trash")
		moveButton.clicked.connect(self.moveFunction)
		return moveButton

	def backButton(self):
		backButton = QtWidgets.QPushButton("Back")
		backButton.clicked.connect(self.backFunction)
		#backButton.setFixedWidth(self.buttonsSize)
		return backButton

	def quitButton(self):
		quitButton = QtWidgets.QPushButton("Quit")
		quitButton.clicked.connect(self.quitFunction)
		#quitButton.setFixedWidth(self.buttonsSize)
		return quitButton

	'''
	'''
	'''Functions called by corresponding buttons
	'''
	'''
	'''

	def clearSelectionFunction(self):
		self.tableWidget.clearSelection()

	def checkSelectedFunction(self):
		selectedRows = self.tableWidget.selectionModel().selectedRows()
		for index in selectedRows:
			self.tableWidget.item(index.row(), CHECKBOXINDEX).setCheckState(Qt.Qt.Checked)

	def uncheckSelectedFunction(self):
		selectedRows = self.tableWidget.selectionModel().selectedRows()
		for index in selectedRows:
			self.tableWidget.item(index.row(), CHECKBOXINDEX).setCheckState(Qt.Qt.Unchecked)

	def moveFunction(self):
		trashPath = self.path + "Trash/"
		try:
			os.mkdir(trashPath)
		except OSError:
			pass
		for i in range(self.tableWidget.rowCount()):
			checkbox = self.tableWidget.item(i, CHECKBOXINDEX)
			if checkbox.checkState() == Qt.Qt.Checked:
				filename = self.tableWidget.item(i, FILENAMEINDEX).text()
				for file in glob.glob(self.path + filename + "*"):
					shutil.move(file, trashPath + os.path.basename(file))
	
	def backFunction(self):
		self.window.close()
		self.parent.window.show()

	def quitFunction(self):
		self.threadpool.clear()
		self.threadpool.waitForDone()
		self.parent.app.quit()



# if __name__ == '__main__':
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = QtWidgets.QWidget()
# 	mainLayout = QtWidgets.QGridLayout()
# 	table = table('/home/tandat/test2/','cor.mrc')
# 	window.setLayout(table.mainLayout)
# 	window.show()
# 	sys.exit(app.exec_())