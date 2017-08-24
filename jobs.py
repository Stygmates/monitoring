import parser
import iomrc
import table
import jobs
from PyQt5 import QtCore, QtWidgets, QtGui, Qt

WIDGETSIZE = 220

def load_filename(path, filename, index):
	filename_item = QtWidgets.QTableWidgetItem(filename)
	filename_item.setFlags(filename_item.flags() & ~ Qt.Qt.ItemIsEditable)
	return [filename_item, index]

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
		return None

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
		return None

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


# def load_row(path, filename, index):
# 	filename_item = load_filename(path, filename, index)
# 	mrc_item = load_mrc(path, filename, index)
# 	ctf_item = load_ctf(path, filename, index)
# 	stats_item = load_stats(path, filename, index)
# 	return [index, filename_item, mrc_item, ctf_item, stats_item]