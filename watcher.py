import sys, os, inspect
from PyQt5 import QtWidgets,QtCore


#Permet de surveiller un dossier et de mettre a jour la listView contenant la liste des fichiers du dossier de la classe parent ayant appelee la classe watcher
#Classe fonctionnant seulement lorsque le parent possede les attributs path et listView
class watcher():


	#Fonction permettant de mettre a jour la liste des fichiers presents dans le dossier
	#TODO : modifier la fonction de filtrage pour qu'elle soit plus propre, il y a peut-etre une fonction qui permet de le faire sans utiliser une boucle sur un tableau
	#Entree: Le path du dossier qui est surveille
	def update(self, path):
		fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]
		model = QtCore.QStringListModel(fileList)
		self.parent.listView.setModel(model)
		self.parent.nbFiles = len(fileList)
		self.parent.nbFilesLabel.setText("Files with the \"" + self.extension + "\" extension: "+ str(self.parent.nbFiles))
		if self.parent.launched == True:
			if self.parent.maxValue <= self.parent.nbFiles:
				self.parent.postProcess()
				self.parent.launched = False




	def __init__(self, parent):
		self.parent = parent
		self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.watcher = QtCore.QFileSystemWatcher([self.path])
		self.watcher.directoryChanged.connect(self.update)
		self.extension = self.parent.extension