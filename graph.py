import parser
import sys, os
import matplotlib.pyplot as plt
path = sys.argv[1]
extension = '_sum-cor_gctf.log'
filenames, phase_shifts = parser.get_phase_shifts(path, extension)
x = range(len(filenames))
plt.plot(phase_shifts, 'ro')
plt.xticks(x, filenames)
plt.show()