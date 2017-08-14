import inspect
import os
import sys

import table
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

buttonSize = 200

#Classe de l'interface qui s'occupe de choisir le dossier qui sera surveille
class folderchooser():

	def init_layout(self, path):
		self.window = QWidget()
		self.window.setWindowTitle("Select a directory")
		main_grid = QVBoxLayout()

		self.invalid_path_label = self.invalid_path_label()
		main_grid.addWidget(self.invalid_path_label)

		grid = QHBoxLayout()
		self.current_path_lineedit = self.current_path_lineedit(path)
		self.select_directory_button = self.select_directory_button()
		grid.addWidget(self.current_path_lineedit)
		grid.addWidget(self.select_directory_button)

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
		self.quit_button = self.quit_button()
		self.ok_button = self.ok_button()
		grid3.addWidget(self.quit_button)
		grid3.addWidget(self.ok_button)

		main_grid.addLayout(grid)
		# mainGrid.addWidget(self.groupBox)
		# mainGrid.addLayout(extensionLayout)
		main_grid.addLayout(grid3)
		self.window.setLayout(main_grid)


	def __init__(self, path, value):
		self.app = QApplication(sys.argv)
		self.init_layout(path)
		self.window.show()
		if value:
			self.monitor()
		sys.exit(self.app.exec_())



	#Le lineedit qui contient le chemin du dossier que l'on a choisi
	def current_path_lineedit(self,path):
		currentfolder = path
		current_path_lineedit = QLineEdit(currentfolder)
		current_path_lineedit.setToolTip("Path of the directory")
		current_path_lineedit.setPlaceholderText("Path to the directory to monitor")
		current_path_lineedit.returnPressed.connect(self.monitor)
		return current_path_lineedit


	#Bouton permettant d'ouvrir une popup afin de selectionner le dossier dans l'arborescence
	def select_directory_button(self):
		select_directory_button = QPushButton("Select a directory")
		select_directory_button.setFixedWidth(buttonSize)
		select_directory_button.clicked.connect(self.folder_chooser)
		return select_directory_button

	def extension_lineedit(self):
		extension_lineedit = QLineEdit('.tif')
		extension_lineedit.setToolTip("File extension of the files to watch out")
		extension_lineedit.setPlaceholderText("Extension")
		return extension_lineedit


	def ok_button(self):
		ok_button = QPushButton("Ok")
		ok_button.setFixedWidth(buttonSize)
		ok_button.clicked.connect(self.monitor)
		ok_button.setAutoDefault(True)
		#okButton.setEnabled(False)
		return ok_button

	def quit_button(self):
		quit_button = QPushButton("Quit")
		quit_button.setFixedWidth(buttonSize)
		quit_button.clicked.connect(self.close_chooser)
		return quit_button

	#Message d'erreur lorsqu'un path non valide est present dans le currentPathLineEdit
	def invalid_path_label(self):
		invalid_path_label = QLabel("Invalid path")
		invalid_path_label.setStyleSheet("QLabel { color : red; }")
		invalid_path_label.setVisible(False)
		return invalid_path_label

	def activate_ok(self):
		self.ok_button.setEnabled(True)


	#Boite de dialogue ouverte lorsque l'on appuie sur le bouton selectDirectoryButton
	def folder_chooser(self):
		currentfolder = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		dir = QFileDialog.getExistingDirectory(None, 'Select a folder:', currentfolder, QFileDialog.ShowDirsOnly)
		if len(dir) > 0:
			self.current_path_lineedit.setText(dir)

	def close_chooser(self):
		self.app.quit()

	def monitor(self):
		#self.extension = self.extensionLineEdit.text()
		if os.path.lexists(self.current_path_lineedit.text()):
			self.window.hide()
			# if self.buttonGroup.checkedId() == 1:
			# 	self.Monitor = finalCountDown.finalCountDown(self)
			# elif self.buttonGroup.checkedId() == 2:
			# 	self.Monitor = monitoring.monitoring(self)
			# else:
			# 	print("Fenetre invalide " + str(self.buttonGroup.checkedId()))
			self.table = table.table(self, self.current_path_lineedit.text(),'tif')
		else:
			self.invalid_path_label.setVisible(True)

