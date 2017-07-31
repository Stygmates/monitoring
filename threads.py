from PyQt5 import QtCore, QtWidgets, QtGui, Qt
import traceback, sys
import iomrc,parser

CTFINDEX = 1
MRCINDEX = 2
STATSINDEX = 3
class mainWorkerSignals(QtCore.QObject):
	mainCtf = QtCore.pyqtSignal(object)
	mainMrc = QtCore.pyqtSignal(object)
	mainStats = QtCore.pyqtSignal(object)

class mainWorker(QtCore.QRunnable):
	def __init__(self, function, functionType, path, fileList):
		super(mainWorker, self).__init__()
		self.function = function
		self.functionType = functionType
		self.signals = mainWorkerSignals()
		self.path = path
		self.fileList = fileList

	def run(self):
		for i in range(0,len(self.fileList)):
			result = self.function(self.fileList[i], i)
			if self.functionType == CTFINDEX:
				self.signals.mainCtf.emit(result)
			elif self.functionType == MRCINDEX:
				self.signals.mainMrc.emit(result)
			elif self.functionType == STATSINDEX:
				self.signals.mainStats.emit(result)
			else:
				print("Function type not defined")