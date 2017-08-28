import parser
import sys
import matplotlib.pyplot as plt

path = sys.argv[1]
#path = '/home/tandat/test2/'
extension = '_sum-cor_gctf.log'
filenames, phase_shifts = parser.get_phase_shifts(path, extension)
x = range(len(filenames))
plt.plot(phase_shifts, 'ro')
plt.xticks(x, filenames)
plt.show()