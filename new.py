import sys, os, inspect
from PyQt5 import QtWidgets,QtCore

class watcher():

	def update(path):
		print("Modification dossier en cours")

	def __init__(self):
		path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		watcher = QtCore.QFileSystemWatcher([path])
		watcher.directoryChanged.connect(self.update)
		print("Atta")

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	watcher = watcher()
	sys.exit(app.exec_())