def getStats(self):
	filename = "test.log"
	file = open(filename,'r')
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