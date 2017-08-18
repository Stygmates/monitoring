import parser

import iomrc
import table
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

WIDGETSIZE = 220


class MainWorkerSignals(QtCore.QObject):
	main_ctf = QtCore.pyqtSignal(object)
	main_mrc = QtCore.pyqtSignal(object)
	main_stats = QtCore.pyqtSignal(object)
	start_next = QtCore.pyqtSignal()

def load_mrc(path, filename, index):
	mrc_item = QtWidgets.QTableWidgetItem()
	mrc_pixmap_original = iomrc.get_pixmap(path + filename + table.MRC_EXTENSION)
	if mrc_pixmap_original is not None:
		mrc_pixmap = mrc_pixmap_original.scaled(WIDGETSIZE, WIDGETSIZE)
		mrc = QtGui.QPixmap(mrc_pixmap)
		mrc_item.setData(Qt.Qt.DecorationRole, mrc)
		mrc_item.setFlags(mrc_item.flags() & ~ Qt.Qt.ItemIsEditable)
		result = [mrc_item, index]
		return result
	else:
		return

def load_ctf(path, filename, index):
	ctf_item = QtWidgets.QTableWidgetItem()
	ctf_pixmap_original = iomrc.get_pixmap(path + filename + table.CTF_EXTENSION)
	if ctf_pixmap_original is not None:
		ctf_pixmap = ctf_pixmap_original.scaled(WIDGETSIZE, WIDGETSIZE)
		ctf = QtGui.QPixmap(ctf_pixmap)
		ctf_item.setData(Qt.Qt.DecorationRole, ctf)
		ctf_item.setFlags(ctf_item.flags() & ~ Qt.Qt.ItemIsEditable)
		result = [ctf_item, index]
		return result
	else:
		return

def load_stats(path, filename, index):
	statslog = path + filename + table.STATS_EXTENSION
	stats = parser.get_stats(statslog)
	if stats is None or len(stats) == 0:
		stats_item = QtWidgets.QTableWidgetItem("Defocus U:\nDefocus V:\n Phase shift: ")
	elif len(stats) == 3:
		stats_item = QtWidgets.QTableWidgetItem(
			"Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\nPhase shift: " + stats[2])
	else:
		stats_item = QtWidgets.QTableWidgetItem(
			"Defocus U: " + stats[0] + "\nDefocus V: " + stats[1] + "\nPhase shift: None")
		stats_item.setFlags(stats_item.flags() & ~ Qt.Qt.ItemIsEditable)
	result = [stats_item, index]
	return result

class MainWorker(QtCore.QRunnable):
	def __init__(self, path, filename, index):
		super(MainWorker, self).__init__()
		self.signals = MainWorkerSignals()
		self.path = path
		self.filename = filename
		self.index = index

	def run(self):
		ctf = load_ctf(self.path, self.filename, self.index)
		self.signals.main_ctf.emit(ctf)
		mrc = load_mrc(self.path, self.filename, self.index)
		self.signals.main_mrc.emit(mrc)
		stats = load_stats(self.path, self.filename, self.index)
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
