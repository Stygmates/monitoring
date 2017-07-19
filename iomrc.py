from scipy.misc import toimage
import mrcfile
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL.ImageQt import ImageQt
import sys
#pip install --user mrcfile

def getpixmap(filename):
	print("Ok")
	mrc = mrcfile.open(filename)
	print("What")
	image = toimage(mrc.data)
	qimage = ImageQt(image)
	pix = QtGui.QPixmap.fromImage(qimage)
	mrc.close()
	return pix