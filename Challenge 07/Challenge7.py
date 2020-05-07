'''
	28/4/2020
	Made by Alejandro Pinel Martinez
    In quarentine
	Tuenti Challenge 10
	Challenge 7 - Encrypted lines
'''

def AddToDictionary(dict, word, translation):
    length = len(word)
    for i in range(length):
        dict[word[i]] = translation[i]

def ApplyDictionary(dict, text):
    length = len(text)
    newtext = ""
    for i in range(length):
        if (text[i] <> '\n'):
            if (text[i] in dict):
                newtext += dict[text[i]]
            else:
                newtext += text[i]
    return newtext

if __name__ == "__main__":

    lines = []
    nlines = 0

    inputfile = "submitInput"
    outputfile = "Output"

    #Get input
    f = open(inputfile, "r")
    nlines = int(f.readline())
    for i in range(nlines):
        lines.append(f.readline())
    f.close()

    dict = {}

    #I found the music to be composed by Antonin Dvorak
    #Translate Dvorak keyboard to qwerty

    AddToDictionary(dict, "',.pyfgcrl/=", "qwertyuiop[]")
    AddToDictionary(dict, "aoeuidhtns-", "asdfghjkl;'#")
    AddToDictionary(dict, ";qjkxbmwvz", "zxcvbnm,./")

    print "Dictionary: " + str(len(dict))
    print dict
    keys = []
    trans = []
    for i in dict:
        keys.append(i)
        trans.append(dict[i])
    trans.sort()
    print "Known keys: "
    print keys
    print "Known letters: "
    print trans

    correctedtext = []

    for i in lines:
        correctedtext.append(ApplyDictionary(dict, i))

    output = open(outputfile, "w")
    for i in range(nlines):
        string = "Case #" + str(i + 1) + ": " + correctedtext[i]
        print string
        output.write(string + '\n')
    output.close()
