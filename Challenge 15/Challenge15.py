'''
	3/5/2020
	Made by Alejandro Pinel Martinez
    In quarentine
	Tuenti Challenge 10
	Challenge 15 - The internsheep
'''

import binascii, os
import tarfile
import zlib

class Experiment:
    def __init__(self, animalname):
        self.name = animalname
        self.alterations = []
        self.results = []

    def AddAlteration(self, pos, byte):
        byte = int(byte).to_bytes(1, 'big')
        self.alterations.append([int(pos), byte])

    def Print(self):
        print(self.name)
        print(self.alterations)

    def GetCRC(self):

        animalsfile = "animals"
        tar = tarfile.open(animalsfile + ".tar.gz", encoding='utf-8')

        file = tar.extractfile(animalsfile + "/./" + self.name)

        file.seek(0, os.SEEK_END)
        nbytes = file.tell()
        #print('Size of file is', nbytes, 'bytes')

        dna = []

        if (nbytes > 0):
            dna = [[nbytes - 1, b'\x00']]
        crc32 = CRCDispersed(dna)
        self.results.append(crc32)

        #print ("List: ",dna)
        #print("Crc32: ", hex(crc32))


        for alt in self.alterations:
            ChangeDispersedMap(dna, alt)
            #print ("List: ",dna)

            crc32 = CRCDispersed(dna)
            self.results.append(crc32)
            #print("Crc32: ", hex(crc32))

    def GetResults(self):
        msg = ""
        for i in range(len(self.results)):
            result = self.name + " " + str(i) + ": " + "{:08x}".format(self.results[i]) +"\n"
            msg += result
        return msg

def ChangeDispersedMap(map, alteration):
    if (len(map) == 0):
        map.append(alteration)
        return map
    added = False
    for i in range(len(map) - 1, -1, -1):
        alt = map[i]
        index = alt[0]
        if (index >= alteration[0]):
            map[i][0] += 1
        else:
            break
        #if (index <= alteration[0]):
        #    map.insert(i, alteration)
        #    return map
    map.append(alteration)
    map.sort()


def Crc32(data, previouscrc):
    #previouscrc = 0
    Polynomial = 0xEDB88320;
    crc = previouscrc ^ 0xFFFFFFFF

    for byte in data:
        current = byte#int.from_bytes(byte, byteorder='big')
        crc = crc ^ current
        for i in range(8):
            crc = (crc >> 1) ^ (-int(crc & 1) & Polynomial)
    return crc ^ 0xFFFFFFFF


# Thanks to Gfy to post this implementation because the zlib does not work well for me
def Crc32Combine(crc1, crc2, len2):
    """Explanation algorithm: https://stackoverflow.com/a/23126768/654160
    crc32(crc32(0, seq1, len1), seq2, len2) == crc32_combine(
        crc32(0, seq1, len1), crc32(0, seq2, len2), len2)"""
    # degenerate case (also disallow negative lengths)
    if len2 <= 0:
        return crc1

    # put operator for one zero bit in odd
    # CRC-32 polynomial, 1, 2, 4, 8, ..., 1073741824
    odd = [0xedb88320] + [1 << i for i in range(0, 31)]
    even = [0] * 32

    def matrix_times(matrix, vector):
        number_sum = 0
        matrix_index = 0
        while vector != 0:
            if vector & 1:
                number_sum ^= matrix[matrix_index]
            vector = vector >> 1 & 0x7FFFFFFF
            matrix_index += 1
        return number_sum

    # put operator for two zero bits in even - gf2_matrix_square(even, odd)
    even[:] = [matrix_times(odd, odd[n]) for n in range(0, 32)]

    # put operator for four zero bits in odd
    odd[:] = [matrix_times(even, even[n]) for n in range(0, 32)]

    # apply len2 zeros to crc1 (first square will put the operator for one
    # zero byte, eight zero bits, in even)
    while len2 != 0:
        # apply zeros operator for this bit of len2
        even[:] = [matrix_times(odd, odd[n]) for n in range(0, 32)]
        if len2 & 1:
            crc1 = matrix_times(even, crc1)
        len2 >>= 1

        # if no more bits set, then done
        if len2 == 0:
            break

        # another iteration of the loop with odd and even swapped
        odd[:] = [matrix_times(even, even[n]) for n in range(0, 32)]
        if len2 & 1:
            crc1 = matrix_times(odd, crc1)
        len2 >>= 1

        # if no more bits set, then done
        # return combined crc
    crc1 ^= crc2
    return crc1

def GetData(filepath):
    list = []
    f = open(filepath, "r")
    line = f.readline()
    while (line):
        info = line.split()
        exp = Experiment(info[0])
        nadds = int(info[1])
        for i in range(nadds):
            alt = f.readline().split()
            exp.AddAlteration(alt[0], alt[1])
        list.append(exp)
        line = f.readline()
    f.close()
    return list

ZEROCRC = []

def CreateTableZeros(SIZE):
    zero = b'\x00'
    ZEROCRC.append(Crc32(zero, 0))
    for i in range(SIZE):
        ZEROCRC.append(Crc32Combine(ZEROCRC[i], ZEROCRC[i], 2**i))

def CreateCRCZeros(Nceros):
    crc = 0
    i = 0
    while (Nceros > 0):
        if (Nceros & 1 == 1):
            crc = Crc32Combine(crc, ZEROCRC[i], 2**i)
        Nceros = Nceros >> 1
        i += 1
    return crc

def CRCDispersed(dispersedlist):
    crc = 0
    lastpart = -1
    for part in dispersedlist:
        nzeros = part[0] - lastpart - 1
        crc = Crc32Combine(crc, CreateCRCZeros(nzeros), nzeros)
        crc = Crc32(part[1], crc)
        lastpart = part[0]
    return crc


def GetAnimalData(animalname):
    animalsfile = "animals"
    tar = tarfile.open(animalsfile + ".tar.gz", encoding='utf-8')

    #for member in tar.getnames():
    #    print (member)

    file = tar.extractfile(animalsfile + "/./" + animalname)

    #data = file.read()

    byte = file.read(1)
    while (byte):
        print(byte)
        byte = file.read(1)

    tar.close()

if __name__ == "__main__":

    inputfile  = "submitInput"
    outputfile = "submitOutput"

    CreateTableZeros(64)

    experiments = GetData(inputfile)

    for e in experiments:
        e.Print()
        e.GetCRC()
        print(e.GetResults())

    print("RESULTS: ")

    #Output file
    output = open(outputfile, "w")
    for e in experiments:
        msg = e.GetResults()
        print(msg)
        output.write(msg)
    output.close()
