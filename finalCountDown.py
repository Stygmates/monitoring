import sys,os
from PyQt5 import QtWidgets, QtCore
class finalCountDown():
	def __init__(self,parent):
		self.parent = parent
		self.extension = self.parent.extension
		self.path = self.parent.currentPathLineEdit.text()

		self.window = QtWidgets.QWidget()
		self.clock = self.clock()
		self.timeInputLayout = self.timeInputLayout()
		self.timer()
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.mainLayout.addWidget(self.clock)
		self.mainLayout.addLayout(self.timeInputLayout)
		self.initListView()
		layout = QtWidgets.QHBoxLayout()
		self.quitButton = self.quitButton()
		self.backButton = self.backButton()
		self.cancelButton = self.cancelButton()
		self.launchButton = self.launchButton()
		layout.addWidget(self.quitButton)
		layout.addWidget(self.backButton)
		layout.addWidget(self.cancelButton)
		layout.addWidget(self.launchButton)
		self.mainLayout.addLayout(layout)

		self.window.setLayout(self.mainLayout)
		self.window.show()


	#Initialisation de l'affichage
	def clock(self):
		clock = QtWidgets.QLCDNumber()
		clock.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
		clock.display("00:00")
		return clock

	#Initialisation du timer
	def timer(self):
		self.timer = QtCore.QTimer()
		self.timer.setInterval(1000)
		self.timer.timeout.connect(self.affichage)

	#Lancement du timer
	def startTimer(self):
		self.timer.start()

	#Layout contenant les spinbox permettant d'initialiser les heures et minutes du timer
	def timeInputLayout(self):
		labelHours = QtWidgets.QLabel(" hours")
		labelminutes = QtWidgets.QLabel(" minutes")
		self.hours = QtWidgets.QSpinBox()
		self.minutes = QtWidgets.QSpinBox()
		self.minutes.setMaximum(59)

		layout = QtWidgets.QHBoxLayout()
		
		layout.addWidget(self.hours)
		layout.addWidget(labelHours)
		layout.addWidget(self.minutes)
		layout.addWidget(labelminutes)
		return layout

	def launchButton(self):
		okButton = QtWidgets.QPushButton("Launch timer before processing")
		okButton.clicked.connect(self.initTimer)
		self.clock.setStyleSheet("background-color: black;color:green;")
		return okButton

	def cancelButton(self):
		cancelButton = QtWidgets.QPushButton("Cancel")
		cancelButton.setEnabled(False)
		cancelButton.clicked.connect(self.cancelTimer)
		return cancelButton

	def backButton(self):
		backButton = QtWidgets.QPushButton("Back")
		backButton.clicked.connect(self.backFunction)
		return backButton

	def quitButton(self):
		quitButton = QtWidgets.QPushButton("Quit")
		quitButton.clicked.connect(self.quitFunction)
		return quitButton

	def backFunction(self):
		self.window.close()
		self.timer.stop()
		self.parent.window.show()

	def quitFunction(self):
		self.parent.app.quit()

	#Initialise le timer et lance le process fait avant le lancement du timer
	def initTimer(self):

		self.preProcess()

		self.hoursLeft = self.hours.value()
		self.minutesLeft = self.minutes.value()
		self.clock.setStyleSheet("background-color: black;color:red;")
		self.launchButton.setEnabled(False)
		self.cancelButton.setEnabled(True)
		self.startTimer()

	def cancelTimer(self):
		self.timer.stop()
		self.clock.setStyleSheet("background-color: black;color: green;")
		self.launchButton.setEnabled(True)
		self.cancelButton.setEnabled(False)
		self.clock.display("00:00")


	def affichage(self):
		if self.minutesLeft == 0:
			if self.hoursLeft > 0:
				self.minutesLeft = 59
				self.hoursLeft = self.hoursLeft - 1
			else:
				self.postProcess()
				self.timer.stop()
				self.clock.setStyleSheet("background-color: black;color: green;")
				self.launchButton.setEnabled(True)
				self.cancelButton.setEnabled(False)
				self.clock.display("00:00")
		else:
			self.minutesLeft = self.minutesLeft - 1
		time = str(self.hoursLeft) + ":" + str(self.minutesLeft)
		self.clock.display(time)

	#La liste des fichiers dans le dossier
	def initListView(self):
		self.listView = QtWidgets.QListView()

		self.fileList = [f for f in os.listdir(self.path) if f.endswith(self.extension)]

		model = QtCore.QStringListModel(self.fileList)
		self.listView.setModel(model)
		self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		self.nbFiles = len(self.fileList)
		self.nbFilesLabel = QtWidgets.QLabel("Files with the \"" + self.extension + "\" extension: "+ str(self.nbFiles))
		
		self.mainLayout.addWidget(self.nbFilesLabel)
		self.mainLayout.addWidget(self.listView)

	def preProcess(self):
		print("Lancement du pre-process")

	def postProcess(self):
		print("Lancement du post-process")