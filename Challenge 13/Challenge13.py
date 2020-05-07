'''
	1/5/2020
	Made by Alejandro Pinel Martinez
    In quarentine
	Tuenti Challenge 10
	Challenge 13 - The Great Toilet Paper Fortress
'''

def GetData(filepath):
	list = []
	f = open(filepath, "r")
	ncases = int(f.readline())
	for i in range(ncases):
		list.append(int(f.readline()))
	f.close()
	return list

class Tower:
	def __init__(self):
		self.n = 0
		self.l = 0
		self.h = 0


def MaximumHeight(toiletpaper):
	height = 3
	l = 5
	used = 43
	needed = 156
	while (needed <= toiletpaper):
		used = needed
		l += 4
		height += 1
		needed = used + l*l + 12*l + 28

	t = Tower()
	t.h = height
	t.l = l
	t.n = used

	return t

def MaximumSize(tower, toiletpaper):
	t = 1
	h = tower.h

	used = tower.n
	central = ((t /2) + 1) * h
	border = 6 + ((20 + 4 * (h - 4)) / 2) * (h - 3)
	needed = used + central + border
	while (needed <= toiletpaper):
		used = needed
		t += 1
		central = ((t /2) + 1) * h
		border = 6 + ((20 + 4 * (h - 4)) / 2) * (h - 3)
		needed = used + central + border
	tower.n = used
	return tower

def GenerateTower(toiletpaper):
	if (toiletpaper < 43):
		return 0
	return MaximumSize(MaximumHeight(toiletpaper), toiletpaper)

if __name__ == "__main__":

	inputfile  = "submitInput"
	outputfile = "submitOutput"

	list = GetData(inputfile)

	msg = ""
	for i in range(len(list)):
		tower = GenerateTower(list[i])
		if (tower == 0):
			string = "Case #" + str(i + 1) + ": " + "IMPOSSIBLE"
		else:
			string = "Case #" + str(i + 1) + ": " + str(tower.h) + " " + str(tower.n)

		msg += string + "\n"
		print (string)

	#Output file
	output = open(outputfile, "w")
	output.write(msg)
	output.close()
