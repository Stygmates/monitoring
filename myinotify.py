from PyQt5 import QtCore, QtWidgets
from inotify_simple import INotify, flags

class watcherWorkerSignals(QtCore.QObject):
	load_file = QtCore.pyqtSignal(object)
	delete_file = QtCore.pyqtSignal(object)

class watcherWorker(QtCore.QRunnable):
	def __init__(self,window, path):
		super(watcherWorker, self).__init__()
		self.inotify = myInotify(window,path)

	def run(self):
		self.inotify.read()

class myInotify():
	def __init__(self,parent, path):
		self.keep_watching = True
		self.inotify = INotify()
		watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY
		wd = self.inotify.add_watch(path, watch_flags)
		self.signals = watcherWorkerSignals()

	def stop_watching(self):
		self.keep_watching = False


	def read(self):
		while self.keep_watching == True:
			for event in self.inotify.read(timeout=500):
				print(event.name)
				for flag in flags.from_mask(event.mask):
					if flag == flags.DELETE:
						print('Suppression')
						self.signals.deleteFile.emit(event.name)
					elif flag == flags.CREATE:
						print('Creation')
						self.signals.loadFile.emit(event.name)
					elif flag == flags.MODIFY:
						print('Modification')
						self.signals.loadFile.emit(event.name)


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