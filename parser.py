import os
def get_stats(filename):
	try:
		file = open(filename,'r')
	except IOError as e:
		return None
	else:
		line = file.readline()
		tab = []
		while line !="":
			line = file.readline()
			tab.append(line)
		tab.reverse()
		for index, line in enumerate(tab):
			if "Final Values" in line:
				file.close()
				values = line.split()
				parameters = tab[index + 1].split()
				result = []
				for i, parameter in enumerate(parameters):
					if parameter == "Defocus_U":
						result.append(values[i])
					if parameter == "Defocus_V":
						result.append(values[i])
					if parameter == "Phase_shift":
						result.append(values[i])
				return result

		file.close()
		return

def get_phase_shift(filename):
	try:
		file = open(filename, 'r')
	except IOError:
		return
	else:	
		line = file.readline()
		tab = []
		while line !="":
			line = file.readline()
			tab.append(line)
		tab.reverse()
		for index, line in enumerate(tab):
			if 'Final Values' in line:
				file.close()
				values = line.split()
				parameters = tab[index + 1].split()
				result = []
				if 'Phase_shift' in parameters:
					for i, parameter in enumerate(parameters):
						if parameter == 'Phase_shift':
							return values[i]
				else:
					return None


def get_phase_shifts(path, extension):
	logs = []
	for file in os.listdir(path):
		if file.endswith(extension):
			logs.append(file)
	logs.sort()
	phase_shifts = []
	filenames = []
	for element in logs:
		filename = path + element
		if get_phase_shift(filename) is not None:
			phase_shifts.append(get_phase_shift(filename))
			filenames.append(element)
	return filenames, phase_shifts