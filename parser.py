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
		for line in tab:
			if "Final Values" in line:
				file.close()
				return line.split()
		file.close()
		return