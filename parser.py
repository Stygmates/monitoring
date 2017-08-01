def getStats(self,filename):
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