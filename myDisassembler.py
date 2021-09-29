"""
Project 1 - Disassembler
ECE 3504, Fall 2021
Nate Doggett

Description: This program disassembles MIPS machines code and coverts
the content into human-readable MIPS assembly
"""


# dictionary of are R_Type and I_Type binary equivalents
r_type = {  '100000':'add',
            '100001':'addu',
            '100100':'and', # may be 0x24
            '100111':'nor',
            '100101':'or',
            '101010':'slt',
            '101011':'sltu',
            '000000':'sll',
            '000010':'srl',
            '100010':'sub',
            '100011':'subu'}
i_type = {  '001000':'addi',
            '001001':'addiu',
            '001100':'addi',
            '000100':'beq',
            '000101':'bne',
            '100100':'lbu',
            '100101':'lhu',
            '100100':'ll',
            '001111':'lui',
            '001101':'ori',
            '001010':'slti',            
            '001011':'sltiu',
            '101000':'sb',
            '111000':'sc',
            '101001':'sh', 
            '101011':'sw'}

file = open('test.txt', 'r')
f = file.readlines()
file.close()

binaryEquiv = []
for line in f:
    str1 = line.strip()
    res = "{0:08b}".format(int(str1, 16)) # converts the hex string into binary
    resFilled = res.zfill(32) # fills the result with any leading zeros
    binaryEquiv.append(resFilled)

for val in binaryEquiv:
    print(val)


def parseRType(line):
    op = line[0:6]
    rs = line[6:11]
    rt = line[11:16]
    rd = line[16:21]
    shamt = line[21:26]
    funct = line[26:32]


def parseIType(line):
    op = line[0:6]
    rs = line[6:11]
    rt = line[11:16]
    immed = line[16:32]

for line in binaryEquiv:
    if line[0:5] == '0000':
        parseRType(line)
    else:
        parseIType(line)


