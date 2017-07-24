import monitoring,finalCountDown

import sys,os,inspect
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import table

buttonSize = 200

#Classe de l'interface qui s'occupe de choisir le dossier qui sera surveille
class folderchooser():

	def initLayout(self):
		self.window = QWidget()
		self.window.setWindowTitle("Select a directory")
		mainGrid = QVBoxLayout()

		self.invalidPathLabel = self.invalidPathLabel()
		mainGrid.addWidget(self.invalidPathLabel)

		grid = QHBoxLayout()
		self.currentPathLineEdit = self.currentPathLineEdit()
		self.selectDirectoryButton = self.selectDirectoryButton()
		grid.addWidget(self.currentPathLineEdit)
		grid.addWidget(self.selectDirectoryButton)

		#Deuxieme ligne avec les radiobuttons

		#Groupbox = seulement le visuel
		# self.groupBox = QGroupBox("Start process depending on")
		# self.timeRadioButton = QRadioButton("Time")
		# self.nbFilesRadioButton = QRadioButton("Number of files")

		# grid2 = QHBoxLayout()
		# grid2.addWidget(self.timeRadioButton)
		# grid2.addWidget(self.nbFilesRadioButton)
		# grid2.setAlignment(Qt.AlignLeft)
		# self.groupBox.setLayout(grid2)

		#ButtonGroup pour regrouper les radiobox en un group

		# self.buttonGroup = QButtonGroup()
		# self.buttonGroup.addButton(self.timeRadioButton,1)
		# self.buttonGroup.addButton(self.nbFilesRadioButton,2)
		# self.buttonGroup.buttonClicked.connect(self.activateOk)

		# extensionLabel = QLabel("Extension to monitor")
		# self.extensionLineEdit = self.extensionLineEdit()
		# extensionLayout = QVBoxLayout()
		# extensionLayout.addWidget(extensionLabel)
		# extensionLayout.addWidget(self.extensionLineEdit)


		#Troisieme ligne avec les boutons ok et quitter
		grid3 = QHBoxLayout()
		self.quitButton = self.quitButton()
		self.okButton = self.okButton()
		grid3.addWidget(self.quitButton)
		grid3.addWidget(self.okButton)

		mainGrid.addLayout(grid)
		# mainGrid.addWidget(self.groupBox)
		# mainGrid.addLayout(extensionLayout)
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
		currentPathLineEdit = QLineEdit(currentfolder)
		currentPathLineEdit.setToolTip("Path of the directory")
		currentPathLineEdit.setPlaceholderText("Path to the directory to monitor")
		return currentPathLineEdit


	#Bouton permettant d'ouvrir une popup afin de selectionner le dossier dans l'arborescence
	def selectDirectoryButton(self):
		selectDirectoryButton = QPushButton("Select a directory")
		selectDirectoryButton.setFixedWidth(buttonSize)
		selectDirectoryButton.clicked.connect(self.folderChooser)
		return selectDirectoryButton

	def extensionLineEdit(self):
		extensionLineEdit = QLineEdit('.tif')
		extensionLineEdit.setToolTip("File extension of the files to watch out")
		extensionLineEdit.setPlaceholderText("Extension")
		return extensionLineEdit


	def okButton(self):
		okButton = QPushButton("Ok")
		okButton.setFixedWidth(buttonSize)
		okButton.clicked.connect(self.monitor)
		#okButton.setEnabled(False)
		return okButton

	def quitButton(self):
		quitButton = QPushButton("Quit")
		quitButton.setFixedWidth(buttonSize)
		quitButton.clicked.connect(self.closeChooser)
		return quitButton

	#Message d'erreur lorsqu'un path non valide est present dans le currentPathLineEdit
	def invalidPathLabel(self):
		invalidPathLabel = QLabel("Invalid path")
		invalidPathLabel.setStyleSheet("QLabel { color : red; }")
		invalidPathLabel.setVisible(False)
		return invalidPathLabel

	def activateOk(self):
		self.okButton.setEnabled(True)


	#Boite de dialogue ouverte lorsque l'on appuie sur le bouton selectDirectoryButton
	def folderChooser(self):
		currentfolder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', currentfolder, QFileDialog.ShowDirsOnly)
		if len(dir) > 0:
			self.currentPathLineEdit.setText(dir)

	def closeChooser(self):
		self.app.quit()

	def monitor(self):
		#self.extension = self.extensionLineEdit.text()
		if os.path.lexists(self.currentPathLineEdit.text()):
			self.window.hide()
			# if self.buttonGroup.checkedId() == 1:
			# 	self.Monitor = finalCountDown.finalCountDown(self)
			# elif self.buttonGroup.checkedId() == 2:
			# 	self.Monitor = monitoring.monitoring(self)
			# else:
			# 	print("Fenetre invalide " + str(self.buttonGroup.checkedId()))
			self.table = table.table(self, self.currentPathLineEdit.text(),'cor.mrc')
		else:
			self.invalidPathLabel.setVisible(True)

