from PyQt5 import QtCore, QtWidgets, QtGui, Qt
import traceback, sys
import iomrc,parser

WIDGETSIZE = 220
class mainWorkerSignals(QtCore.QObject):
	mainCtf = QtCore.pyqtSignal(object)
	mainMrc = QtCore.pyqtSignal(object)
	mainStats = QtCore.pyqtSignal(object)
	startNext = QtCore.pyqtSignal()

class mainWorker(QtCore.QRunnable):
	def __init__(self, path, filename, index):
		super(mainWorker, self).__init__()
		self.signals = mainWorkerSignals()
		self.path = path
		self.filename = filename
		self.index = index


	def loadMrc(self, filename, index):
		mrcItem = QtWidgets.QTableWidgetItem()
		mrcpixmapOriginal = iomrc.getpixmap(self.path + filename + "_sum-cor.mrc")
		if mrcpixmapOriginal is not None:
			mrcpixmap = mrcpixmapOriginal.scaled(WIDGETSIZE,WIDGETSIZE)
			mrc = QtGui.QPixmap(mrcpixmap)
			mrcItem.setData(Qt.Qt.DecorationRole, mrc)
			result = [mrcItem, index, mrcpixmapOriginal]
			return result
		else:
			return

	def loadCtf(self,filename, index):
		ctfItem = QtWidgets.QTableWidgetItem()
		ctfpixmapOriginal = iomrc.getpixmap(self.path + filename + "_sum-cor.ctf")
		if ctfpixmapOriginal is not None:
			ctfpixmap = ctfpixmapOriginal.scaled(WIDGETSIZE,WIDGETSIZE)
			ctf = QtGui.QPixmap(ctfpixmap)
			ctfItem.setData(Qt.Qt.DecorationRole, ctf)
			result = [ctfItem, index, ctfpixmapOriginal]
			return result
		else:
			return

	def loadStats(self,filename,index):
		statslog = self.path + filename + "_sum-cor_gctf.log"
		stats = parser.getStats(self,statslog)
		if stats is None or len(stats) == 0:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U:\nDefocus V:\n Phase shift: ")
		elif len(stats) == 3:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\nPhase shift: " + stats[2])
		else:
			statsItem = QtWidgets.QTableWidgetItem("Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\nPhase shift: None")
		result = [statsItem,index]
		return result

	def run(self):
		ctf = self.loadCtf(self.filename, self.index)
		self.signals.mainCtf.emit(ctf)
		mrc = self.loadMrc(self.filename, self.index)
		self.signals.mainMrc.emit(mrc)
		stats = self.loadStats(self.filename, self.index)
		self.signals.mainStats.emit(stats)
		self.signals.startNext.emit()
