import jobs

from PyQt5 import QtCore

class MainWorkerSignals(QtCore.QObject):
	main_add_row = QtCore.pyqtSignal(object)
	main_filename = QtCore.pyqtSignal(object)
	main_ctf = QtCore.pyqtSignal(object)
	main_mrc = QtCore.pyqtSignal(object)
	main_stats = QtCore.pyqtSignal(object)
	start_next = QtCore.pyqtSignal()

class MainWorker(QtCore.QRunnable):
	def __init__(self, path, filename, index):
		super(MainWorker, self).__init__()
		self.signals = MainWorkerSignals()
		self.path = path
		self.filename = filename
		self.index = index

	def run(self):
		self.signals.main_add_row.emit(self.index)
		filename_item = jobs.load_filename(self.path, self.filename, self.index)
		self.signals.main_filename.emit(filename_item)
		ctf = jobs.load_ctf(self.path, self.filename, self.index)
		self.signals.main_ctf.emit(ctf)
		mrc = jobs.load_mrc(self.path, self.filename, self.index)
		self.signals.main_mrc.emit(mrc)
		stats = jobs.load_stats(self.path, self.filename, self.index)
		self.signals.main_stats.emit(stats)
		self.signals.start_next.emit()

class UpdaterWorker(QtCore.QRunnable):
	def __init__(self, parent):
		super(UpdaterWorker,self).__init__()
		self.signals = MainWorkerSignals()
		self.path = parent.path
		self.parent = parent

	def run(self):
		if not self.parent.stop_loading:
			try:
				result = self.parent.update_queue.get(True, 500)
				filename = result[0]
				index = result[1]
				ctf = load_ctf(self.path, filename, index)
				self.signals.main_ctf.emit(ctf)
				mrc = load_mrc(self.path, filename, index)
				self.signals.main_mrc.emit(mrc)
				stats = load_stats(self.path, filename, index)
				self.signals.main_stats.emit(stats)
			finally:
				self.signals.start_next.emit()
