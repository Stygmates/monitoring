import folderchooser
import sys, os, inspect

if __name__ == '__main__':
	if len(sys.argv) == 2:
		Chooser = folderchooser.folderchooser(sys.argv[1],True)
		Chooser.display()
		Chooser.monitor()
	else:
		path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		Chooser = folderchooser.folderchooser(path, False)
		Chooser.display()