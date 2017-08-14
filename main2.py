import inspect
import os
import sys

import folderchooser2

if __name__ == '__main__':
    if len(sys.argv) == 2:
        Chooser = folderchooser2.folderchooser(sys.argv[1], True)
        Chooser.display()
        Chooser.monitor()
    else:
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        Chooser = folderchooser2.folderchooser(path, False)
        Chooser.display()
