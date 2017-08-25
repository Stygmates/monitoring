import jobs
import queue
import table

from PyQt5 import QtCore

class MainWorkerSignals(QtCore.QObject):
	add_row = QtCore.pyqtSignal(object)
	add_filename = QtCore.pyqtSignal(object)
	add_ctf = QtCore.pyqtSignal(object)
	add_mrc = QtCore.pyqtSignal(object)
	add_stats = QtCore.pyqtSignal(object)
	delete_row = QtCore.pyqtSignal(object)
	delete_filename = QtCore.pyqtSignal(object)
	delete_ctf = QtCore.pyqtSignal(object)
	delete_mrc = QtCore.pyqtSignal(object)
	delete_stats = QtCore.pyqtSignal(object)
	start_next = QtCore.pyqtSignal()

class MainWorker(QtCore.QRunnable):
	def __init__(self, path, filename, index):
		super(MainWorker, self).__init__()
		self.signals = MainWorkerSignals()
		self.path = path
		self.filename = filename
		self.index = index

	def run(self):
		self.signals.add_row.emit(self.index)
		filename_item = jobs.load_filename(self.path, self.filename, self.index)
		self.signals.add_filename.emit(filename_item)
		ctf = jobs.load_ctf(self.path, self.filename, self.index)
		self.signals.add_ctf.emit(ctf)
		mrc = jobs.load_mrc(self.path, self.filename, self.index)
		self.signals.add_mrc.emit(mrc)
		stats = jobs.load_stats(self.path, self.filename, self.index)
		self.signals.add_stats.emit(stats)
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
				result = self.parent.update_queue.get(True, 0.5)
				filename = result[0]
				operation = result[1]
				ext = None
				extensions = [table.TIF_EXTENSION, table.CTF_EXTENSION, table.MRC_EXTENSION, table.STATS_EXTENSION]
				for extension in extensions:
					if filename.endswith(extension):
						file = filename[:-(len(extension))]
						ext = extension
				if operation == table.LOADINDEX:
					if ext == table.TIF_EXTENSION:
						if file not in self.parent.filtered_list:
							self.parent.filtered_list.append(file)
							self.parent.filtered_list.sort()
							index = self.parent.filtered_list.index(file)
							self.signals.add_row.emit(index)
							filename_item = jobs.load_filename(self.path, file, index)
							self.signals.add_filename.emit(filename_item)
							ctf = jobs.load_ctf(self.path, file, index)
							self.signals.add_ctf.emit(ctf)
							mrc = jobs.load_mrc(self.path, file, index)
							self.signals.add_mrc.emit(mrc)
							stats = jobs.load_stats(self.path, file, index)
							self.signals.add_stats.emit(stats)
					elif ext == table.CTF_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							ctf = jobs.load_ctf(self.path, file, index)
							self.signals.add_ctf.emit(ctf)
					elif ext == table.MRC_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							mrc = jobs.load_mrc(self.path, file, index)
							self.signals.add_mrc.emit(mrc)
					elif ext == table.STATS_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							stats = jobs.load_stats(self.path, file, index)
							self.signals.add_stats.emit(stats)
				elif operation == table.DELETEINDEX:
					if ext == table.TIF_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							self.parent.filtered_list.remove(file)
							self.signals.delete_row.emit(index)
					elif ext == table.CTF_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							self.signals.delete_ctf.emit(index)
					elif ext == table.MRC_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							self.signals.delete_mrc.emit(index)
					elif ext == table.STATS_EXTENSION:
						if file in self.parent.filtered_list:
							index = self.parent.filtered_list.index(file)
							self.signals.delete_stats.emit(index)
			except queue.Empty:
				pass
			finally:
				self.signals.start_next.emit()
		else:
			pass
