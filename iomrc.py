import mrcfile
from PIL.ImageQt import ImageQt
from PyQt5 import QtGui
from scipy.misc import toimage


#pip install --user mrcfile

def get_pixmap(filename):
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
	except Exception:
		return None
	except RuntimeWarning:
		print("Nope")