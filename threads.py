from PyQt5 import QtCore, QtWidgets, QtGui, Qt
import traceback, sys
import iomrc,parser

WIDGETSIZE = 220
class mainWorkerSignals(QtCore.QObject):
	mainCtf = QtCore.pyqtSignal(object)
	mainMrc = QtCore.pyqtSignal(object)
	mainStats = QtCore.pyqtSignal(object)

class mainWorker(QtCore.QRunnable):
	def __init__(self, path, filename, index):
		super(mainWorker, self).__init__()
		self.signals = mainWorkerSignals()
		self.path = path
		self.filename = filename
		self.index = index


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

	def run(self):
		ctf = self.loadCtf(self.filename, self.index)
		self.signals.mainCtf.emit(ctf)
		mrc = self.loadMrc(self.filename, self.index)
		self.signals.mainMrc.emit(mrc)
		stats = self.loadStats(self.filename, self.index)
		self.signals.mainStats.emit(stats)
