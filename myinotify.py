import table
from PyQt5 import QtCore, QtWidgets
from inotify_simple import INotify, flags, masks


class watcherWorkerSignals(QtCore.QObject):
	reload_file = QtCore.pyqtSignal(object)
	load_file = QtCore.pyqtSignal(object)
	delete_file = QtCore.pyqtSignal(object)

class watcherWorker(QtCore.QRunnable):
	def __init__(self,window, path):
		super(watcherWorker, self).__init__()
		self.inotify = myInotify(path)

	def run(self):
		self.inotify.read()

class myInotify():
	def __init__(self, path):
		self.keep_watching = True
		self.inotify = INotify()
		watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY| masks.MOVE
		wd = self.inotify.add_watch(path, watch_flags)
		self.signals = watcherWorkerSignals()

	def stop_watching(self):
		self.keep_watching = False


	def read(self):
		while self.keep_watching:
			for event in self.inotify.read(timeout=500):
				print("Watching")
				print(event)
				for flag in flags.from_mask(event.mask):
					if flag == flags.DELETE or flag == flags.MOVED_FROM:
						print('Suppression')
						self.signals.delete_file.emit(event.name)
					elif flag == flags.CREATE or flag == flags.MOVED_TO:
						print('Creation')
						self.signals.load_file.emit(event.name)
					elif flag == flags.MODIFY:
						print('Modification')
						if event.name.endswith(table.MRC_EXTENSION):
							filename = event.name[:-(len(table.MRC_EXTENSION))]
							self.signals.reload_file.emit(filename)
						elif event.name.endswith(table.CTF_EXTENSION):
							filename = event.name[:-(len(table.CTF_EXTENSION))]
							self.signals.reload_file.emit(filename)
						elif event.name.endswith(table.STATS_EXTENSION):
							filename = event.name[:-(len(table.STATS_EXTENSION))]
							self.signals.reload_file.emit(filename)


class window():
	def __init__(self):
		self.window = QtWidgets.QWidget()
		self.main_layout = QtWidgets.QGridLayout()
		stop_button = QtWidgets.QPushButton("Stop")
		self.main_layout.addWidget(stop_button)
		self.window.setLayout(self.main_layout)
		self.window.show()
		self.threadpool = QtCore.QThreadPool()
		worker = watcherWorker(self,'/home/tandat/test')
		self.threadpool.start(worker)
		stop_button.clicked.connect(worker.inotify.stop_watching)



# if __name__ == '__main__':
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = window()
# 	sys.exit(app.exec_())