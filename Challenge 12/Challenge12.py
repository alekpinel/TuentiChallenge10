'''
	1/5/2020
	Made by Alejandro Pinel Martinez
    In quarentine
	Tuenti Challenge 10
	Challenge 12 - Hackerman Origins
'''

# text^e = coded mod n
# text^e - coded = 0 mod n

# test1^e - coded1 = 0 mod n
# test2^e - coded2 = 0 mod n

# So GCD((test1^e - coded1), (test2^e - coded2)) = n
# e is supposed to be 65537 ( the most common)

def StringToInt(string):
	return (int.from_bytes(string, byteorder='big'))

def GCD(a, b):
	resto = 0
	while(b > 0):
		resto = b
		b = a % b
		a = resto

	return a

def GetData(filepath):
	f = open(filepath, "rb")
	bytes = f.read()
	f.close()
	return bytes



def Numb(a, b):
	e = 65537
	return a**65537 - b

def CalculateKeyFermat(a, b, c, d):
	p1 = Numb(a, b)
	p2 = Numb(c, d)
	n = GCD(p1, p2)
	return n

if __name__ == "__main__":

	outputfile = "Output"

	#Get input
	test1coded = StringToInt(GetData("testdata/ciphered/test1.txt"))
	test1decoded = StringToInt(GetData("testdata/plaintexts/test1.txt"))
	test2coded = StringToInt(GetData("testdata/ciphered/test2.txt"))
	test2decoded = StringToInt(GetData("testdata/plaintexts/test2.txt"))



	print (test1coded)
	print (test1decoded)
	print (test2coded)
	print (test2decoded)

	n = CalculateKeyFermat(test1decoded, test1coded, test2decoded, test2coded)

	print ("Public key is: (" + str(65537) + ", " + str(n) +")")
