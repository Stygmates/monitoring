import glob
import os
import queue
import re
import shutil

import iomrc
import myinotify
import threads
from PyQt5 import QtCore, QtWidgets, Qt

ITEM = 0
RESULTINDEX = 1


TIF_EXTENSION = '.tif'
MRC_EXTENSION = '_sum-cor.mrc'
CTF_EXTENSION = '_sum-cor.ctf'
STATS_EXTENSION ='_sum-cor_gctf.log'

CHECKBOXINDEX = 0
FILENAMEINDEX = 1
CTFINDEX = 2
MRCINDEX = 3
STATSINDEX = 4

LOADINDEX = 0
DELETEINDEX = 1

WIDGETSIZE = 220

NB_WORKERS = 5


class table():

	def __init__(self, parent, path, extension):
		self.parent = parent
		self.window = QtWidgets.QWidget()
		self.threadpool = QtCore.QThreadPool()
		self.stop_loading = False
		self.path = path + '/'
		self.extension = extension
		self.update_queue = queue.Queue(0)
		self.watcher = myinotify.watcherWorker(self,self.path)
		self.watcher.inotify.signals.load_file.connect(self.load_file)
		self.watcher.inotify.signals.delete_file.connect(self.delete_file)
		self.threadpool.start(self.watcher)

		self.parent.app.aboutToQuit.connect(self.watcher.inotify.stop_watching)
		self.parent.app.aboutToQuit.connect(self.quit_function)

		self.centered_layout = QtWidgets.QHBoxLayout()
		self.centered_layout.setAlignment(Qt.Qt.AlignCenter)
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.setAlignment(Qt.Qt.AlignCenter)
		self.filter_layout = QtWidgets.QVBoxLayout()
		#self.filterLayout.setAlignment(Qt.Qt.AlignLeft)
		self.buttons_layout = QtWidgets.QGridLayout()
		self.buttons_layout.setAlignment(Qt.Qt.AlignCenter)
		#Widget config
		self.path_label = self.path_label()
		self.filter_lineedit = self.filter_lineedit()
		self.table_widget = self.table_widget()

		self.check_all_button = self.check_all_button()
		self.clear_selection_button = self.clear_selection_button()
		self.uncheck_selected_button = self.uncheck_selected_button()
		self.check_selected_button = self.check_selected_button()
		self.move_button = self.move_button()
		self.quit_button = self.quit_button()
		self.back_button = self.back_button()

		self.buttons_layout.addWidget(self.check_all_button, 0, 0, 1, 2)
		self.buttons_layout.addWidget(self.clear_selection_button, 1, 0, 1, 2)
		self.buttons_layout.addWidget(self.uncheck_selected_button, 2, 0)
		self.buttons_layout.addWidget(self.check_selected_button, 2, 1)
		self.buttons_layout.addWidget(self.move_button, 3, 0, 1, 2)
		self.buttons_layout.addWidget(self.quit_button, 4, 0)
		self.buttons_layout.addWidget(self.back_button, 4, 1)

		self.filter_layout.addWidget(self.path_label)
		self.filter_layout.addWidget(self.filter_lineedit)

		self.centered_layout.addWidget(self.table_widget)
		self.centered_layout.addLayout(self.buttons_layout)

		self.main_layout.addLayout(self.filter_layout)
		self.main_layout.addLayout(self.centered_layout)

		self.window.setLayout(self.main_layout)
		self.window.show()

		self.load_list()

	def load_file(self, filename):
		if filename.endswith((TIF_EXTENSION, MRC_EXTENSION, CTF_EXTENSION, STATS_EXTENSION)):
			if filename.endswith(MRC_EXTENSION):
				file = filename[:-(len(MRC_EXTENSION))]
			elif filename.endswith(CTF_EXTENSION):
				file = filename[:-(len(CTF_EXTENSION))]
			elif filename.endswith(STATS_EXTENSION):
				file = filename[:-(len(STATS_EXTENSION))]
			try:
				index = self.filtered_list.index(file)
			except ValueError:
				index = -1
			result = [filename, index]
			self.update_queue.put(result)

	def delete_file(self, filename):
		print('Suppression ' + filename)

	'''
	Main widget containing the list of all the data
	'''

	def table_widget(self):
		table_widget = QtWidgets.QTableWidget()
		header_list = ["", "File name", "Ctf", "Corresponding mrc", "Parameters"]
		table_widget.setColumnCount(len(header_list))
		table_widget.setRowCount(0)
		table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		table_widget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
		table_widget.setFixedHeight(4 * WIDGETSIZE)
		table_widget.setFixedWidth((len(header_list) - 1) * WIDGETSIZE + 56)
		table_widget.setHorizontalHeaderLabels(header_list)
		table_widget.setColumnWidth(0, 25)
		table_widget.cellDoubleClicked.connect(self.display_image)
		for i in range(1, len(header_list)):
			table_widget.setColumnWidth(i, WIDGETSIZE)
		return table_widget


	'''
	Function that updates the table with all of the data
	'''

	def load_list(self):
		self.table_widget.setRowCount(0)
		file_list = [f[:-4] for f in os.listdir(self.path) if f.endswith(self.extension)]
		try:
			regex = re.compile(self.filter_lineedit.text())
			self.filtered_list = list(filter(regex.search, file_list))
		except Exception as e:
			self.filtered_list = file_list

		self.filequeue = queue.Queue(0)
		for i, filename in enumerate(self.filtered_list):
			self.filequeue.put([i,filename])

		for thread in range(NB_WORKERS):
			if not self.filequeue.empty():
				element = self.filequeue.get()
				worker = threads.MainWorker(self.path, element[1], element[0])
				worker.signals.main_add_row.connect(self.add_row)
				worker.signals.main_filename.connect(self.update_filename)
				worker.signals.main_ctf.connect(self.update_ctf)
				worker.signals.main_mrc.connect(self.update_mrc)
				worker.signals.main_stats.connect(self.update_stats)
				worker.signals.start_next.connect(self.start_next)
				self.threadpool.start(worker)
		#self.table_widget.sortItems(0)
		'''
		updater = threads.UpdaterWorker(self)
		updater.signals.main_add_row.connect(self.insert_row)
		updater.signals.main_ctf.connect(self.update_ctf)
		updater.signals.main_mrc.connect(self.update_mrc)
		updater.signals.main_stats.connect(self.update_stats)
		self.threadpool.start(updater)
		'''

	'''
	Function called that starts a new job once the last one is done, this is to keep the number of threads workers equal to NB_WORKERS
	'''

	def start_next(self):
		if not self.stop_loading:
			if not self.filequeue.empty():
				element = self.filequeue.get()
				worker = threads.MainWorker(self.path, element[1], element[0])
				worker.signals.main_add_row.connect(self.add_row)
				worker.signals.main_filename.connect(self.update_filename)
				worker.signals.main_ctf.connect(self.update_ctf)
				worker.signals.main_mrc.connect(self.update_mrc)
				worker.signals.main_stats.connect(self.update_stats)
				worker.signals.start_next.connect(self.start_next)
				self.threadpool.start(worker)

	def start_next_update(self):
		if not self.stop_loading:
			updater = threads.UpdaterWorker(self)
			updater.signals.main_add_row.connect(self.insert_row)
			updater.signals.main_ctf.connect(self.update_ctf)
			updater.signals.main_mrc.connect(self.update_mrc)
			updater.signals.main_stats.connect(self.update_stats)
			updater.signals.start_next.connect(self.start_next_update)
			self.threadpool.start(updater)


	def add_row(self, index):
		self.table_widget.insertRow(index)
		self.table_widget.setRowHeight(index, WIDGETSIZE)
		checkbox_item = QtWidgets.QTableWidgetItem()
		checkbox_item.setCheckState(Qt.Qt.Unchecked)
		self.table_widget.setItem(index, CHECKBOXINDEX, checkbox_item)
	'''
	Function that updates the filename column on the table with the result given by one of the threads
	'''

	def update_filename(self, result):
		index = result[RESULTINDEX]
		self.table_widget.setItem(index, FILENAMEINDEX, result[ITEM])

	'''
	Function that updates the stats column on the table with the result given by one of the threads
	'''

	def update_stats(self, result):
		index = result[RESULTINDEX]
		self.table_widget.setItem(index, STATSINDEX, result[ITEM])

	'''
	Function that updates the mrc column on the table with the result given by one of the threads
	'''

	def update_mrc(self, result):
		if result is not None:
			index = result[RESULTINDEX]
			self.table_widget.setItem(index, MRCINDEX, result[ITEM])

	'''
	Function that updates the ctf column on the table with the result given by one of the threads
	'''

	def update_ctf(self, result):
		if result is not None:
			index = result[RESULTINDEX]
			self.table_widget.setItem(index, CTFINDEX, result[ITEM])

	'''
	Function that creates the popup image when double clicking on an image
	'''

	def display_image(self, row, column):
		filename = self.table_widget.item(row, FILENAMEINDEX).text()
		if column == CTFINDEX or column == MRCINDEX:	
			if column == CTFINDEX:
				pixmap = iomrc.get_pixmap(self.path + filename + CTF_EXTENSION)
				window_title = filename + CTF_EXTENSION
			elif column == MRCINDEX:
				pixmap = iomrc.get_pixmap(self.path + filename + MRC_EXTENSION)
				window_title = filename + MRC_EXTENSION
			if pixmap is not None:
				dialog = QtWidgets.QDialog()
				image = QtWidgets.QLabel()
				dialog.setWindowTitle(window_title)
				final_pixmap = pixmap.scaled(1000, 1000)
				image.setPixmap(final_pixmap)
				layout = QtWidgets.QVBoxLayout()
				layout.addWidget(image)
				dialog.setLayout(layout)
				dialog.show()
				dialog.exec_()

	'''
	'''
	'''Widgets definition
	'''
	'''
	'''

	def path_label(self):
		label = QtWidgets.QLabel(self.path)
		return label

	def filter_lineedit(self):
		filter_lineedit = QtWidgets.QLineEdit()
		filter_lineedit.setFixedWidth(400)
		filter_lineedit.setPlaceholderText("Filter")
		filter_lineedit.textChanged.connect(self.load_list)
		return filter_lineedit

	def check_all_button(self):
		check_all_button = QtWidgets.QCheckBox("Check/Uncheck all")
		check_all_button.stateChanged.connect(self.check_all_function)
		return check_all_button

	def clear_selection_button(self):
		clear_selection_button = QtWidgets.QPushButton("Clear selection")
		clear_selection_button.clicked.connect(self.clear_selection_function)
		return clear_selection_button

	def check_selected_button(self):
		check_selected_button = QtWidgets.QPushButton("Check selected rows")
		check_selected_button.clicked.connect(self.check_selected_function)
		return check_selected_button

	def uncheck_selected_button(self):
		check_selected_button = QtWidgets.QPushButton("Uncheck selected rows")
		check_selected_button.clicked.connect(self.uncheck_selected_function)
		return check_selected_button

	def move_button(self):
		move_button = QtWidgets.QPushButton("Move to trash")
		move_button.clicked.connect(self.move_function)
		return move_button

	def back_button(self):
		back_button = QtWidgets.QPushButton("Back")
		back_button.clicked.connect(self.watcher.inotify.stop_watching)
		back_button.clicked.connect(self.back_function)
		#backButton.setFixedWidth(self.buttonsSize)
		return back_button

	def quit_button(self):
		quit_button = QtWidgets.QPushButton("Quit")
		quit_button.clicked.connect(self.watcher.inotify.stop_watching)
		quit_button.clicked.connect(self.quit_function)
		#quitButton.setFixedWidth(self.buttonsSize)
		return quit_button

	'''
	'''
	'''Functions called by corresponding buttons
	'''
	'''
	'''

	def check_all_function(self):
		state = self.check_all_button.checkState()
		for index in range(self.table_widget.rowCount()):
			checkbox_item = self.table_widget.item(index, CHECKBOXINDEX)
			if state == Qt.Qt.Checked:
				checkbox_item.setCheckState(Qt.Qt.Checked)
			elif state == Qt.Qt.Unchecked:
				checkbox_item.setCheckState(Qt.Qt.Unchecked)

	def clear_selection_function(self):
		self.table_widget.clearSelection()

	def check_selected_function(self):
		selected_rows = self.table_widget.selectionModel().selectedRows()
		for index in selected_rows:
			self.table_widget.item(index.row(), CHECKBOXINDEX).setCheckState(Qt.Qt.Checked)

	def uncheck_selected_function(self):
		selected_rows = self.table_widget.selectionModel().selectedRows()
		for index in selected_rows:
			self.table_widget.item(index.row(), CHECKBOXINDEX).setCheckState(Qt.Qt.Unchecked)

	def move_function(self):
		trash_path = self.path + "Trash/"
		try:
			os.mkdir(trash_path)
		except OSError:
			pass
		for i in range(self.table_widget.rowCount()):
			checkbox = self.table_widget.item(i, CHECKBOXINDEX)
			if checkbox.checkState() == Qt.Qt.Checked:
				filename = self.table_widget.item(i, FILENAMEINDEX).text()
				for file in glob.glob(self.path + filename + "*"):
					shutil.move(file, trash_path + os.path.basename(file))

	def back_function(self):
		self.stop_loading = True
		self.threadpool.clear()
		self.threadpool.waitForDone()
		self.window.close()
		self.parent.window.show()

	def quit_function(self):
		self.stop_loading = True
		self.threadpool.clear()
		self.threadpool.waitForDone()
		self.parent.app.quit()



# if __name__ == '__main__':
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = QtWidgets.QWidget()
# 	mainLayout = QtWidgets.QGridLayout()
# 	table = table('/home/tandat/test2/','cor.mrc')
# 	window.setLayout(table.mainLayout)
# 	window.show()
# 	sys.exit(app.exec_())