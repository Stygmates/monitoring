from scipy.misc import toimage
import mrcfile
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL.ImageQt import ImageQt
import sys
#pip install --user mrcfile

def getpixmap(filename):
	try:
		mrc = mrcfile.open(filename, permissive=True)
		if(filename.endswith(".ctf")):
			data2 = mrc.data[0]
		else:
			data2 = mrc.data
		image = toimage(data2)
		qimage = ImageQt(image)
		pix = QtGui.QPixmap.fromImage(qimage)
		mrc.close()
		return pix
	except OSError as e:
		print(e)
		return None