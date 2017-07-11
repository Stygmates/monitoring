import watcher

from PyQt5 import QtCore, QtGui, QtWidgets
import os

#Fenetre permettant l'affichage de la liste de fichiers se trouvant dans le dossier selectionne, le parent doit posseder un attribut currentPathLineEdit
class monitoring():
	def __init__(self, parent):
		self.parent = parent
		self.window = QtWidgets.QWidget()
		self.path = self.parent.currentPathLineEdit.text()
		self.extension = self.parent.extension

		#Variable servant a verifier si le watcher est lance pour le dossier 
		self.launched = False

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
		self.cancelButton()
		self.backButton()
		self.quitButton()

		self.mainLayout.addLayout(self.layout)
		self.verticalLayout.addWidget(self.groupBox)
		self.verticalLayout.addLayout(self.layout3)
		self.mainLayout.addLayout(self.verticalLayout)
		self.window.setLayout(self.mainLayout)
		self.window.show()


	#La liste des fichiers dans le dossier
	def initListView(self):
		self.listView = QtWidgets.QListView()

		self.fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]

		model = QtCore.QStringListModel(self.fileList)
		self.listView.setModel(model)
		self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		self.nbFiles = len(self.fileList)
		self.nbFilesLabel = QtWidgets.QLabel("Files with the \"" + self.extension + "\" extension: "+ str(self.nbFiles))
		
		self.layout.addWidget(self.nbFilesLabel)
		self.layout.addWidget(self.listView)


	#Le watcher qui affiche la liste des fichiers et qui lance egalement le postprocessing lorsque le nombre de fichiers necessaire est atteint dans le dossier
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
		self.okButton.clicked.connect(self.okFunction)
		self.layout3.addWidget(self.okButton)

	def cancelButton(self):
		self.cancelButton = QtWidgets.QPushButton("Cancel")
		self.cancelButton.setEnabled(False)
		self.cancelButton.clicked.connect(self.cancelFunction)
		self.layout3.addWidget(self.cancelButton)

	def backButton(self):
		self.backButton = QtWidgets.QPushButton("Back")
		self.backButton.clicked.connect(self.backFunction)
		self.layout3.addWidget(self.backButton)

	def quitButton(self):
		self.quitButton = QtWidgets.QPushButton("Quit")
		self.quitButton.clicked.connect(self.quitFunction)
		self.layout3.addWidget(self.quitButton)

	def okFunction(self):
		self.preProcess()
		self.okButton.setEnabled(False)
		self.cancelButton.setEnabled(True)
		self.launched = True
		self.maxValue = self.nbNecessaryFilesSpinBox.value()
		if self.maxValue < self.nbFiles:
			self.postProcess()

	def cancelFunction(self):
		self.okButton.setEnabled(True)
		self.cancelButton.setEnabled(False)
		self.launched = False

	def backFunction(self):
		self.window.close()
		self.parent.window.show()

	def quitFunction(self):
		self.parent.app.quit()


	#Fonction lancee avant l'attente du nombre de fichiers requis dans le repertoire
	def preProcess(self):
		print("Lancement du pre-processing")


	#Process lance une fois que la limite du nombre de fichiers est atteint
	def postProcess(self):
		print("Lancement du post-processing")
		#TODO : Reactiver le bouton ok, desactiver le bouton cancel et remettre variable launched a False
