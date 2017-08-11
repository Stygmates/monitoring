from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
import os,sys
from inotify_simple import INotify, flags

class mainWorkerSignals(QtCore.QObject):
	stopWatching = QtCore.pyqtSignal()

class watcherWorker(QtCore.QRunnable):
	def __init__(self,window, path):
		super(watcherWorker, self).__init__()
		self.inotify = myInotify(window,path)

	def run(self):
		self.inotify.read()

class myInotify():
	def __init__(self,parent, path):
		self.keepWatching = True
		self.inotify = INotify()
		watch_flags = flags.CREATE | flags.DELETE | flags.MODIFY | flags.DELETE_SELF
		wd = self.inotify.add_watch(path, watch_flags)


	def stopWatching(self):
		self.keepWatching = False


	def read(self):
		while self.keepWatching == True:
			print(self.keepWatching)
			for event in self.inotify.read(timeout=500):
				print(event)
				for flag in flags.from_mask(event.mask):
					print('    ' + str(flag))


class window():
	def __init__(self):
		self.window = QtWidgets.QWidget()
		self.mainLayout = QtWidgets.QGridLayout()
		stopButton = QtWidgets.QPushButton("Stop")
		self.mainLayout.addWidget(stopButton)
		self.window.setLayout(self.mainLayout)
		self.window.show()
		self.threadpool = QtCore.QThreadPool()
		worker = watcherWorker(self,'/home/tandat/test')
		self.threadpool.start(worker)
		stopButton.clicked.connect(worker.inotify.stopWatching)



# if __name__ == '__main__':
# 	app = QtWidgets.QApplication(sys.argv)
# 	window = window()
# 	sys.exit(app.exec_())