import parser
import sys, os
import matplotlib.pyplot as plt
path = sys.argv[1]
extension = '_sum-cor_gctf.log'
filenames, phase_shifts = parser.get_phase_shifts(path, extension)
for index, value in enumerate(phase_shifts):
	if value > 180 or < 0:
		plt.plot(index, value, 'ro')
	elif value > 35 and < 145:
		plt.plot(index, value, 'go')
	else 
		plt.plot(index, value, 'yo')

plt.axhline(y = 180, color = 'k')
plt.axhline(y = 35, color = 'k', linestyle = '--')
plt.axhline(y = 145, color = 'k', linestyle = '--')
plt.axhline(color = 'k')
plt.show()
