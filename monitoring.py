import watcher

from PyQt5 import QtCore, QtGui, QtWidgets
import os

#Fenetre permettant l'affichage de la liste de fichiers se trouvant dans le dossier selectionne, le parent doit posseder un attribut currentPathLineEdit
class monitoring():
	def __init__(self, parent):
		self.parent = parent
		self.window = QtWidgets.QWidget()
		self.path = self.parent.currentPathLineEdit.text()

		#Creation des layouts
		self.mainLayout = QtWidgets.QHBoxLayout()
		self.layout = QtWidgets.QVBoxLayout()
		self.layout2 = QtWidgets.QVBoxLayout()
		
		#initialisation de tous les widgets
		#Premiere colonne
		self.initListView()
		self.startWatcher()

		#Deuxieme colonne
		self.nbNecessaryFilesLineEdit()
		self.okButton()
		self.mainLayout.addLayout(self.layout)
		self.mainLayout.addLayout(self.layout2)
		self.window.setLayout(self.mainLayout)
		self.window.show()


	def initListView(self):
		self.listView = QtWidgets.QListView()

		self.fileList = [f for f in os.listdir(self.path) if f.endswith('.txt')]

		model = QtCore.QStringListModel(self.fileList)
		self.listView.setModel(model)
		self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		self.nbFiles = len(self.fileList)
		self.nbFilesLabel = QtWidgets.QLabel("Number of files with the correct extension inside the directory: " + str(self.nbFiles))
		
		self.layout.addWidget(self.nbFilesLabel)
		self.layout.addWidget(self.listView)


	def startWatcher(self):
		self.watcher = watcher.watcher(self)

	def nbNecessaryFilesLineEdit(self):
		self.nbNecessaryFilesLabel = QtWidgets.QLabel("Limit before processing: ")
		self.nbNecessaryFilesLineEdit = QtWidgets.QLineEdit()

		self.layout2.addWidget(self.nbNecessaryFilesLabel)
		self.layout2.addWidget(self.nbNecessaryFilesLineEdit)

	def okButton(self):
		self.okButton = QtWidgets.QPushButton("Ok")
		self.layout2.addWidget(self.okButton)