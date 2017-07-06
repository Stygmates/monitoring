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
		self.layout3 = QtWidgets.QVBoxLayout()
		self.verticalLayout = QtWidgets.QVBoxLayout()
		
		#initialisation de tous les widgets
		#Premiere colonne
		self.initListView()
		self.startWatcher()

		#Deuxieme colonne
		self.nbNecessaryFilesSpinBox()
		self.okButton()

		self.mainLayout.addLayout(self.layout)
		self.verticalLayout.addWidget(self.groupBox)
		self.verticalLayout.addLayout(self.layout3)
		self.mainLayout.addLayout(self.verticalLayout)
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

	def nbNecessaryFilesSpinBox(self):
		self.groupBox = QtWidgets.QGroupBox("Limit before processing: ")
		self.nbNecessaryFilesSpinBox = QtWidgets.QSpinBox()
		self.nbNecessaryFilesSpinBox.setMaximum(1000)
		self.layout2.addWidget(self.nbNecessaryFilesSpinBox)
		self.groupBox.setLayout(self.layout2)

	def okButton(self):
		self.okButton = QtWidgets.QPushButton("Ok")
		self.layout3.addWidget(self.okButton)