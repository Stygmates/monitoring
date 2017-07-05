import monitoring

import sys,os,inspect
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

buttonSize = 200

#Classe de l'interface qui s'occupe de choisir le dossier qui sera surveille
class filechooser():

	def initLayout(self):
		self.window = QWidget()
		self.window.setWindowTitle("Choix du dossier")
		mainGrid = QVBoxLayout()

		self.invalidPathLabel()
		mainGrid.addWidget(self.invalidPathLabel)

		grid = QHBoxLayout()

		self.currentPathLineEdit()
		self.selectDirectoryButton()

		grid.addWidget(self.currentPathLineEdit)
		grid.addWidget(self.selectDirectoryButton)

		grid2 = QHBoxLayout()

		self.quitButton()
		self.okButton()

		grid2.addWidget(self.quitButton)
		grid2.addWidget(self.okButton)

		mainGrid.addLayout(grid)
		mainGrid.addLayout(grid2)
		self.window.setLayout(mainGrid)


	def __init__(self):
		self.app = QApplication(sys.argv)

		self.initLayout()
		self.window.show()
		sys.exit(self.app.exec_())


	#Le lineedit qui contient le chemin du dossier que l'on a choisi
	def currentPathLineEdit(self):
		currentfolder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.currentPathLineEdit = QLineEdit(currentfolder)
		self.currentPathLineEdit.setToolTip("Chemin du dossier")
		self.currentPathLineEdit.setPlaceholderText("Chemin vers le dossier a surveiller")


	#Bouton permettant d'ouvrir une popup afin de selectionner le dossier dans l'arborescence
	def selectDirectoryButton(self):
		self.selectDirectoryButton = QPushButton("Selectionnez le dossier")
		self.selectDirectoryButton.setFixedWidth(buttonSize)
		self.selectDirectoryButton.clicked.connect(self.folderChooser)


	def okButton(self):
		self.okButton = QPushButton("Valider")
		self.okButton.setFixedWidth(buttonSize)
		self.okButton.clicked.connect(self.monitor)

	def quitButton(self):
		self.quitButton = QPushButton("Quitter")
		self.quitButton.setFixedWidth(buttonSize)
		self.quitButton.clicked.connect(self.closeChooser)
		

	#Message d'erreur lorsqu'un path non valide est present dans le currentPathLineEdit
	def invalidPathLabel(self):
		self.invalidPathLabel = QLabel("Chemin de dossier non valide")
		self.invalidPathLabel.setStyleSheet("QLabel { color : red; }")
		self.invalidPathLabel.setVisible(False)


	#Boite de dialogue ouverte lorsque l'on appuie sur le bouton selectDirectoryButton
	def folderChooser(self):
		currentfolder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', currentfolder, QFileDialog.ShowDirsOnly)
		self.currentPathLineEdit.setText(dir)

	def closeChooser(self):
		self.app.quit()

	def monitor(self):
		if os.path.lexists(self.currentPathLineEdit.text()):
			self.window.hide()
			self.Monitor = monitoring.monitoring(self)
		else:
			self.invalidPathLabel.setVisible(True)

