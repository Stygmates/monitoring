import parser
import sys, os
import matplotlib.pyplot as plt
path = sys.argv[1]
extension = '_sum-cor_gctf.log'
filenames, phase_shifts = parser.get_phase_shifts(path, extension)
plt.plot(phase_shifts, 'ro')
plt.axhline(y = 180, color = 'k')
plt.axhline(y = 35, color = 'k', linestyle = '--')
plt.axhline(y = 145, color = 'k', linestyle = '--')
plt.axhline(color = 'k')
plt.show()
