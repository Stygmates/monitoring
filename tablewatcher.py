import sys, os, inspect
from PyQt5 import QtWidgets,QtCore


#Permet de surveiller un dossier et de mettre a jour la listView contenant la liste des fichiers du dossier de la classe parent ayant appelee la classe watcher
#Classe fonctionnant seulement lorsque le parent possede les attributs path et listView
class watcher():


	#Fonction permettant de mettre a jour la liste des fichiers presents dans le dossier
	#TODO : modifier la fonction de filtrage pour qu'elle soit plus propre, il y a peut-etre une fonction qui permet de le faire sans utiliser une boucle sur un tableau
	#Entree: Le path du dossier qui est surveille
	def update(self):
		fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]
		self.parent.tableWidget.setRowCount(0)
		for i in range(0,len(fileList)):
			tableWidgetItem = QtWidgets.QTableWidgetItem(fileList[i])
			self.parent.tableWidget.insertRow(self.parent.tableWidget.rowCount())
			self.parent.tableWidget.setItem(i,0,tableWidgetItem)




	def __init__(self, parent):
		self.parent = parent
		self.path = parent.path
		self.extension = self.parent.extension
		self.watcher = QtCore.QFileSystemWatcher([self.path])
		self.watcher.directoryChanged.connect(self.update)