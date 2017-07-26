from PyQt5 import QtCore
import traceback, sys
class workerSignals(QtCore.QObject):
	finished = QtCore.pyqtSignal()
	error = QtCore.pyqtSignal(tuple)
	result = QtCore.pyqtSignal(object)

class Worker(QtCore.QRunnable):
	def __init__(self, function, filename, index):
		super(Worker, self).__init__()
		self.function = function
		self.filename = filename
		self.index = index
		self.signals = workerSignals()


	def run(self):
		try:
			result = self.function(self.filename,self.index)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)  # Return the result of the processing
		finally:
			self.signals.finished.emit()