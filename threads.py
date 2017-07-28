from PyQt5 import QtCore, QtWidgets, QtGui, Qt
import traceback, sys
import iomrc,parser

class mainWorkerSignals(QtCore.QObject):
	mainctf = QtCore.pyqtSignal(object)
	mainmrc = QtCore.pyqtSignal(object)
	mainstats = QtCore.pyqtSignal(object)
	wtf = QtCore.pyqtSignal()

class mainWorker(QtCore.QRunnable):
	def __init__(self,path, filteredList):
		super(mainWorker, self).__init__()
		self.signals = mainWorkerSignals()
		self.threadpool = QtCore.QThreadPool()
		self.filteredList = filteredList
		self.path = path

	def loadmrc(self, filename, index):
		mrcItem = QtWidgets.QTableWidgetItem()
		mrcpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.mrc")
		if mrcpixmap is not None:
			mrcpixmap = mrcpixmap.scaled(300,300)
			mrc = QtGui.QPixmap(mrcpixmap)
			mrcItem.setData(Qt.Qt.DecorationRole, mrc)
			return [mrcItem,index]
		else:
			return

	def loadctf(self,filename, index):
		ctfItem = QtWidgets.QTableWidgetItem()
		ctfpixmap = iomrc.getpixmap(self.path + filename + "_sum-cor.ctf")
		if ctfpixmap is not None:
			ctfpixmap = ctfpixmap.scaled(300,300)
			ctf = QtGui.QPixmap(ctfpixmap)
			ctfItem.setData(Qt.Qt.DecorationRole, ctf)
			return [ctfItem,index]
		else:
			return

	def loadstats(self,filename,index):
		statslog = self.path + filename + "_sum-cor_gctf.log"
		stats = parser.getStats(self,statslog)
		if stats is None:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U:\nDefocus V:\n Phase shift: ")
		else:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\nPhase shift: " + stats[3])
		return [statsItem,index]

	def printwtf(self,result):
		print("WTF")

	def run(self):
		for i in range(0,len(self.filteredList)):
			mrc = self.loadmrc(self.filteredList[i], i)
			self.signals.mainmrc.emit(mrc)
			ctf = self.loadctf(self.filteredList[i], i)
			self.signals.mainctf.emit(ctf)
			stats = self.loadstats(self.filteredList[i], i)
			self.signals.mainstats.emit(stats)
