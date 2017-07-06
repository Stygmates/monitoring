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
		self.window.setWindowTitle("Select a directory")
		mainGrid = QVBoxLayout()

		self.invalidPathLabel()
		mainGrid.addWidget(self.invalidPathLabel)

		grid = QHBoxLayout()
		self.currentPathLineEdit()
		self.selectDirectoryButton()
		grid.addWidget(self.currentPathLineEdit)
		grid.addWidget(self.selectDirectoryButton)

		#Deuxieme ligne avec les radiobuttons

		#Groupbox = seulement le visuel
		self.groupBox = QGroupBox("Launch process depending on")
		self.timeRadioButton = QRadioButton("Time")
		self.nbFilesRadioButton = QRadioButton("Number of files")

		grid2 = QHBoxLayout()
		grid2.addWidget(self.timeRadioButton)
		grid2.addWidget(self.nbFilesRadioButton)
		grid2.setAlignment(Qt.AlignLeft)
		self.groupBox.setLayout(grid2)

		#ButtonGroup pour regrouper les radiobox en un group

		self.buttonGroup = QButtonGroup()
		self.buttonGroup.addButton(self.timeRadioButton)
		self.buttonGroup.addButton(self.nbFilesRadioButton)
		self.buttonGroup.buttonClicked.connect(self.activateOk)

		#Troisieme ligne avec les boutons ok et quitter
		grid3 = QHBoxLayout()
		self.quitButton()
		self.okButton()
		grid3.addWidget(self.quitButton)
		grid3.addWidget(self.okButton)

		mainGrid.addLayout(grid)
		mainGrid.addWidget(self.groupBox)
		mainGrid.addLayout(grid3)
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
		self.currentPathLineEdit.setToolTip("Path of the directory")
		self.currentPathLineEdit.setPlaceholderText("Path to the directory to monitor")


	#Bouton permettant d'ouvrir une popup afin de selectionner le dossier dans l'arborescence
	def selectDirectoryButton(self):
		self.selectDirectoryButton = QPushButton("Select a directory")
		self.selectDirectoryButton.setFixedWidth(buttonSize)
		self.selectDirectoryButton.clicked.connect(self.folderChooser)


	def okButton(self):
		self.okButton = QPushButton("Ok")
		self.okButton.setFixedWidth(buttonSize)
		self.okButton.clicked.connect(self.monitor)
		self.okButton.setEnabled(False)

	def quitButton(self):
		self.quitButton = QPushButton("Quit")
		self.quitButton.setFixedWidth(buttonSize)
		self.quitButton.clicked.connect(self.closeChooser)

	#Message d'erreur lorsqu'un path non valide est present dans le currentPathLineEdit
	def invalidPathLabel(self):
		self.invalidPathLabel = QLabel("Invalid path")
		self.invalidPathLabel.setStyleSheet("QLabel { color : red; }")
		self.invalidPathLabel.setVisible(False)

	def activateOk(self):
		self.okButton.setEnabled(True)


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

