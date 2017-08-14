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


class MainWorker(QtCore.QRunnable):
	def __init__(self, path, filename, index):
		super(MainWorker, self).__init__()
		self.signals = MainWorkerSignals()
		self.path = path
		self.filename = filename
		self.index = index

	def load_mrc(self, filename, index):
		mrc_item = QtWidgets.QTableWidgetItem()
		mrc_pixmap_original = iomrc.get_pixmap(self.path + filename + table.MRC_EXTENSION)
		if mrc_pixmap_original is not None:
			mrc_pixmap = mrc_pixmap_original.scaled(WIDGETSIZE, WIDGETSIZE)
			mrc = QtGui.QPixmap(mrc_pixmap)
			mrc_item.setData(Qt.Qt.DecorationRole, mrc)
			mrc_item.setFlags(mrc_item.flags() & ~ Qt.Qt.ItemIsEditable)
			result = [mrc_item, index]
			return result
		else:
			return

	def load_ctf(self, filename, index):
		ctf_item = QtWidgets.QTableWidgetItem()
		ctf_pixmap_original = iomrc.get_pixmap(self.path + filename + table.CTF_EXTENSION)
		if ctf_pixmap_original is not None:
			ctf_pixmap = ctf_pixmap_original.scaled(WIDGETSIZE, WIDGETSIZE)
			ctf = QtGui.QPixmap(ctf_pixmap)
			ctf_item.setData(Qt.Qt.DecorationRole, ctf)
			ctf_item.setFlags(ctf_item.flags() & ~ Qt.Qt.ItemIsEditable)
			result = [ctf_item, index]
			return result
		else:
			return

	def load_stats(self, filename, index):
		statslog = self.path + filename + table.STATS_EXTENSION
		stats = parser.get_stats(self, statslog)
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

	def run(self):
		ctf = self.load_ctf(self.filename, self.index)
		self.signals.main_ctf.emit(ctf)
		mrc = self.load_mrc(self.filename, self.index)
		self.signals.main_mrc.emit(mrc)
		stats = self.load_stats(self.filename, self.index)
		self.signals.main_stats.emit(stats)
		self.signals.start_next.emit()
