'''
	1/5/2020
	Made by Alejandro Pinel Martinez
    In quarentine
	Tuenti Challenge 10
	Challenge 11 - All the Possibilities
'''



def AllPossibilities(Obj, Forbbiden):
	#print "Searching for " + str(Obj) + " Rorbidden: "
	#print Forbbiden

	table = [[0 for x in range(Obj)] for y in range(Obj)]

	for i in range(Obj):
		for j in range(Obj):
			table[i][j] = -1


	def PossToLimit(Actual, Limit):
		InitialActual = Actual
		if (table[Actual][Limit] <> -1):
			return table[Actual][Limit]

		Actual += Limit
		pos = -1

		if (Actual == Obj):
			pos = 1
		elif (Actual > Obj):
			pos = 0
		elif (Limit == 1):
			if (1 not in Forbbiden):
				pos = 1
			else:
				pos = 0

		if (pos == -1):
			pos = 0
			for i in range(1, Limit + 1):
				if (i not in Forbbiden):
					pos += PossToLimit(Actual, i)

		table[InitialActual][Limit] = pos
		return pos

	AllPos = 0
	for i in range(1, Obj):
		if (i not in Forbbiden):
			AllPos += PossToLimit(0, i)

	return AllPos


if __name__ == "__main__":

	inputfile = "submitInput"
	outputfile = "submitOutput"

	#Get input
	f = open(inputfile, "r")
	nlines = int(f.readline())
	lines = []
	for i in range(nlines):
		lines.append(f.readline())
	f.close()

	Possibilities = []
	for i in range(nlines):
		line = lines[i].split()

		Obj = int(line[0])
		Forbbiden = []
		for number in line[1:]:
			Forbbiden.append(int(number))

		poss = AllPossibilities(Obj, Forbbiden)

		Possibilities.append(poss)
		print "Case #" + str(i + 1) + ": " + str(poss)


	#Output file
	output = open(outputfile, "w")
	for i in range(nlines):
		string = "Case #" + str(i + 1) + ": " + str(Possibilities[i])
		output.write(string + '\n')
	output.close()
