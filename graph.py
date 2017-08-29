import parser
import sys, os
import matplotlib.pyplot as plt
import mpld3
path = sys.argv[1]
graph = sys.argv[2]
extension = '_sum-cor_gctf.log'
if graph == 'phase_shift':
	filenames, phase_shifts = parser.get_phase_shifts(path, extension)
	fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
	ax.grid(color='white', linestyle='solid')
	ax.set_title('Phase shift graph')
	if len(filenames) > 0:
		mylist = [i for i in range(len(filenames))]
		scatters = ax.scatter(phase_shifts, mylist, c = 'r')
	ax.axhline(y = 180, color = 'k')
	ax.axhline(y = 35, color = 'k', linestyle = '--')
	ax.axhline(y = 90, color = 'k', linestyle = '-')
	ax.axhline(y = 145, color = 'k', linestyle = '--')
	ax.axhline(color = 'k')
elif graph == 'defocus':
	filenames, defocus_u, defocus_v = parser.get_defocus(path, extension)
	fig, ax = plt.subplots(subplot_kw=dict(axisbg='#EEEEEE'))
	if len(filenames) > 0:
		scatters = ax.scatter(defocus_u, defocus_v, c = 'r')
		ax.grid(color='white', linestyle='solid')
		ax.set_title('Defocus graph')
tooltip = mpld3.plugins.PointLabelTooltip(scatters, labels=filenames)
mpld3.plugins.connect(fig, tooltip)
mpld3.show()
