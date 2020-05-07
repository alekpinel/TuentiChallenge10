'''
	30/4/2020
	Made by Alejandro Pinel Martinez
    In quarentine
	Tuenti Challenge 10
	Challenge 9 - Just Another Day on Battlestar Galactica
'''

def hexToDec(hex):
	ascii = int(hex, 16)
	return ascii # hex.decode("hex")

def decToHex(crpt_chr):
	#return printf("%02X\n"% crpt_chr)
	hexnum = hex(crpt_chr).split('x')[-1]
	if (len(hexnum) < 2):
		hexnum = "0" + hexnum
	return hexnum

def getKey(coded, decoded):
	key = ""
	for i in range(len(decoded)):
		cd_str = decoded[i]					#decoded char
		cd_ascii = ord(str(cd_str))
		cc_hex = coded[2*i:2*i+2]			#and two hex chars
		cc_ascii = hexToDec(cc_hex)
		key_part = int(cd_ascii) ^ int(cc_ascii)
		key = str(key_part) + key
	return key

def decrypt(key, code):
	dcrpt_msg = ""
	for i in range(len(key)):
		key_pos = len(key) - 1 - i
		key_char = key[key_pos]					#we take the key
		hx_crpt_chr = code[2*i:2*i+2]			#and two hex chars
		crpt_chr = hexToDec(hx_crpt_chr)
		decrp_chr = int(crpt_chr) ^ int(key_char) #Perform an XOR
		ascii = str(unichr(decrp_chr))
		dcrpt_msg = dcrpt_msg + ascii
	return dcrpt_msg

def encrypt(key, msg):
	crpt_msg = ""
	for i in range(len(msg)):
		c = msg[i]
		asc_chr = ord(str(c))					#We take the ascii value
		key_pos = len(key) - 1 - i
		key_char = key[key_pos]
		crpt_chr = int(asc_chr) ^ int(key_char) #Perform an XOR
		hx_crpt_chr = decToHex(crpt_chr)		#Convert to Hex
		crpt_msg = crpt_msg + str(hx_crpt_chr)
	return crpt_msg

if __name__ == "__main__":

	outputfile = "Output"

	coord = "514;248;980;347;145;332"
	result = "3633363A33353B393038383C363236333635313A353336"

	key = getKey(result, coord)
	coded1 = encrypt(key, coord)
	decoded1 = decrypt(key, result)

	print "\nFirst example we will use to calculate the key"
	print "Coordinates: " + coord
	print "Code: " + result
	print "Key: " + key + " ("+ str(len(key)) + " chars)"
	print "Check Key: Coded: " + coded1 + " ("+ str(len(coded1)) + " chars)"
	print "Check Key: Decoded: " + decoded1 + " ("+ str(len(decoded1)) + " chars)"

	coded2 = "3A3A333A333137393D39313C3C3634333431353A37363D"
	decoded2 = decrypt(key, coded2)

	print "\nSecond example, the real case"
	print "Key: " + key
	print "Code: " + coded2
	print "Coordinates: " + decoded2 + " ("+ str(len(decoded2)) + " chars)"

	output = open(outputfile, "w")
	output.write(decoded2)
	output.close()
