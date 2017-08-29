import parser
import sys, os
import matplotlib.pyplot as plt
path = sys.argv[1]
print(path)
graph = sys.argv[2]
extension = '_sum-cor_gctf.log'
if graph == 'phase_shift':
	filenames, phase_shifts = parser.get_phase_shifts(path, extension)
	plt.figure('Phase shifts graph')
	if len(filenames) > 0:
		plt.plot(phase_shifts, 'ro')
	plt.axhline(y = 180, color = 'k')
	plt.axhline(y = 35, color = 'k', linestyle = '--')
	plt.axhline(y = 90, color = 'k', linestyle = '-')
	plt.axhline(y = 145, color = 'k', linestyle = '--')
	plt.axhline(color = 'k')
elif graph == 'defocus':
	filenames, defocus_u, defocus_v = parser.get_defocus(path, extension)
	plt.figure('Defocus graph')
	if len(filenames) > 0:
		plt.plot(defocus_u,defocus_v, 'ro')
plt.show()
