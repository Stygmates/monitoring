import os

from PyQt5 import QtWidgets, QtCore


class FinalCountDown:
	def __init__(self, parent):
		self.parent = parent
		self.extension = self.parent.extension
		self.path = self.parent.current_path_lineedit.text()

		self.window = QtWidgets.QWidget()
		self.clock = self.clock()
		self.time_input_layout = self.time_input_layout()
		self.timer = self.timer()
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addWidget(self.clock)
		self.main_layout.addLayout(self.time_input_layout)
		self.init_listview()
		layout = QtWidgets.QHBoxLayout()
		self.quit_button = self.quit_button()
		self.back_button = self.back_button()
		self.cancel_button = self.cancel_button()
		self.launch_button = self.launch_button()
		layout.addWidget(self.quit_button)
		layout.addWidget(self.back_button)
		layout.addWidget(self.cancel_button)
		layout.addWidget(self.launch_button)
		self.main_layout.addLayout(layout)

		self.window.setLayout(self.main_layout)
		self.window.show()


	#Initialisation de l'affichage
	def clock(self):
		clock = QtWidgets.QLCDNumber()
		clock.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
		clock.display("00:00")
		return clock

	#Initialisation du timer
	def timer(self):
		timer = QtCore.QTimer()
		timer.setInterval(1000)
		timer.timeout.connect(self.affichage)
		return timer

	#Lancement du timer
	def start_timer(self):
		self.timer.start()

	#Layout contenant les spinbox permettant d'initialiser les heures et minutes du timer
	def time_input_layout(self):
		label_hours = QtWidgets.QLabel(" hours")
		label_minutes = QtWidgets.QLabel(" minutes")
		self.hours = QtWidgets.QSpinBox()
		self.minutes = QtWidgets.QSpinBox()
		self.minutes.setMaximum(59)

		layout = QtWidgets.QHBoxLayout()
		
		layout.addWidget(self.hours)
		layout.addWidget(label_hours)
		layout.addWidget(self.minutes)
		layout.addWidget(label_minutes)
		return layout

	def launch_button(self):
		ok_button = QtWidgets.QPushButton("Launch timer before processing")
		ok_button.clicked.connect(self.init_timer)
		self.clock.setStyleSheet("background-color: black;color:green;")
		return ok_button

	def cancel_button(self):
		cancel_button = QtWidgets.QPushButton("Cancel")
		cancel_button.setEnabled(False)
		cancel_button.clicked.connect(self.cancel_timer)
		return cancel_button

	def back_button(self):
		back_button = QtWidgets.QPushButton("Back")
		back_button.clicked.connect(self.back_function)
		return back_button

	def quit_button(self):
		quit_button = QtWidgets.QPushButton("Quit")
		quit_button.clicked.connect(self.quit_function)
		return quit_button

	def back_function(self):
		self.window.close()
		self.timer.stop()
		self.parent.window.show()

	def quit_function(self):
		self.parent.app.quit()

	#Initialise le timer et lance le process fait avant le lancement du timer
	def init_timer(self):

		self.pre_process()

		self.hours_left = self.hours.value()
		self.minutes_left = self.minutes.value()
		self.clock.setStyleSheet("background-color: black;color:red;")
		self.launch_button.setEnabled(False)
		self.cancel_button.setEnabled(True)
		self.start_timer()

	def cancel_timer(self):
		self.timer.stop()
		self.clock.setStyleSheet("background-color: black;color: green;")
		self.launch_button.setEnabled(True)
		self.cancel_button.setEnabled(False)
		self.clock.display("00:00")


	def affichage(self):
		if self.minutes_left == 0:
			if self.hours_left > 0:
				self.minutes_left = 59
				self.hours_left = self.hours_left - 1
			else:
				self.post_process()
				self.timer.stop()
				self.clock.setStyleSheet("background-color: black;color: green;")
				self.launch_button.setEnabled(True)
				self.cancel_button.setEnabled(False)
				self.clock.display("00:00")
		else:
			self.minutes_left = self.minutes_left - 1
		time = str(self.hours_left) + ":" + str(self.minutes_left)
		self.clock.display(time)

	#La liste des fichiers dans le dossier
	def init_listview(self):
		self.listiew = QtWidgets.QListView()

		self.file_list = [f for f in os.listdir(self.path) if f.endswith(self.extension)]

		model = QtCore.QStringListModel(self.file_list)
		self.listView.setModel(model)
		self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		self.nb_files = len(self.file_list)
		self.nb_files_label = QtWidgets.QLabel("Files with the \"" + self.extension + "\" extension: "+ str(self.nb_files))

		self.main_layout.addWidget(self.nb_files_label)
		self.main_layout.addWidget(self.list_view)

	def pre_process(self):
		print("Lancement du pre-process")

	def post_process(self):
		print("Lancement du post-process")