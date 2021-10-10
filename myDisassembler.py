"""
Project 1 - Disassembler
ECE 3504, Fall 2021
Nate Doggett

Description: This program disassembles MIPS machines code and coverts
the content into human-readable MIPS assembly
"""
class RType:
    """ RType instruction type """
    def __init__(self):
        self.op = None
        self.rs = None
        self.rt = None
        self.rd = None
        self.shamt = None
        self.funct = None

    def parseRType(self, line):
        self.op = "000000"
        self.rs = line[6:11]
        self.rt = line[11:16]
        self.rd = line[16:21]
        self.shamt = line[21:26]
        self.funct = line[26:32]

class IType:
    """ IType instruction type """
    def __init__(self):
        self.op = None
        self.rs = None
        self.rt = None
        self.immed = None

    def parseIType(self, line):
        self.op = line[0:6]
        self.rs = line[6:11]
        self.rt = line[11:16]
        self.immed = line[16:32]

def main(inputStr):
    # dictionary of are R_Type and I_Type binary equivalents
    r_type_op_codes = {  '100000':'add',
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
    i_type_op_codes = {  '001000':'addi',
                '001001':'addiu',
                '001100':'addi',
                '000100':'beq',
                '000101':'bne',
                '100100':'lbu',
                '100101':'lhu',
                '100100':'ll',
                '001111':'lui',
                '100011':'lw',
                '001101':'ori',
                '001010':'slti',            
                '001011':'sltiu',
                '101000':'sb',
                '111000':'sc',
                '101001':'sh', 
                '101011':'sw'}
    register_dict = {   '00000':'$zero',
                        '00001':'$at',
                        '00010':'$v0',
                        '00011':'$v1',
                        '00100':'$a0',
                        '00101':'$a1',
                        '00110':'$a2',
                        '00111':'$a3',
                        '01000':'$t0',
                        '01001':'$t1',
                        '01010':'$t2',
                        '01011':'$t3',
                        '01100':'$t4',
                        '01101':'$t5',
                        '01110':'$t6',
                        '01111':'$t7',
                        '10000':'$s0',
                        '10001':'$s1',
                        '10010':'$s2',
                        '10011':'$s3',
                        '10100':'$s4',
                        '10101':'$s5',
                        '10110':'$s6',
                        '10111':'$s7',
                        '11000':'$t8',
                        '11001':'$t9',
                        '11010':'$k0',
                        '11011':'$k1',
                        '11100':'$gp',
                        '11101':'$sp',
                        '11110':'$fp',
                        '11111':'$ra'}


    file = open(inputStr, 'r')
    f = file.readlines()
    file.close()

    binaryEquiv = []
    tempOutputList = {}
    addressesThatNeedLabels = []
    programCounter = 0
    lineCounter = 1

    for line in f:
        str1 = line.strip()
        if (len(str1) != 8):
            print("Cannot dissassemble " + str1 + " at line " + str(lineCounter) + " due to invalid length.")
        else:
            res = "{0:08b}".format(int(str1, 16)) # converts the hex string into binary
            resFilled = res.zfill(32) # fills the result with any leading zeros
            binaryEquiv.append(resFilled)
            lineCounter += 1

    my_rtype = RType()
    my_itype = IType()
    isRType = False
    lineCounter = 1

    for line in binaryEquiv:
        if (line[0:6] == '000000'):
            my_rtype.parseRType(line)
            isRType = True
        else:
            my_itype.parseIType(line)
            isRType = False

        if isRType:

            op_str = r_type_op_codes[my_rtype.funct]
            rs_str = register_dict[my_rtype.rs]
            rt_str = register_dict[my_rtype.rt]
            rd_str = register_dict[my_rtype.rd]
            shamt_str = int(my_rtype.shamt,2)
            
            temp_int = int(my_rtype.funct,2)
            funct_str = hex(temp_int)

            if (shamt_str == 0):
                tempOutputList[programCounter] = "\t" + op_str + " " + rd_str + ", " + rs_str + ", " + rt_str  + "\n"
            else:
                tempOutputList[programCounter] = "\t" + op_str + " " + rd_str + ", " + rt_str + ", " + str(shamt_str) + "\n"

        # IType case
        else: 
            op_str = i_type_op_codes[my_itype.op]
            rs_str = register_dict[my_itype.rs]
            rt_str = register_dict[my_itype.rt]
            immed_str = int(my_itype.immed,2)
            if (immed_str > 60000):
                immed_str = immed_str-65536

            if (op_str == "lw" or op_str == "sw"):
                tempOutputList[programCounter] = "\t" + op_str + " " + rt_str + ", " + str(immed_str) + "(" + rs_str + ")" + "\n"
            elif (op_str == "beq" or op_str == "bne"):
                address = str( 4*(programCounter + immed_str + 1) )
                addressStr = "Addr_" +  address.zfill(4)
                addressesThatNeedLabels.append(programCounter + immed_str + 1)
                tempOutputList[programCounter] = "\t" + op_str + " " + rt_str + ", " + rs_str + ", " + addressStr + "\n"
            else:
                tempOutputList[programCounter] = "\t" + op_str + " " + rt_str + ", " + rs_str + ", " + str(immed_str) + "\n"
        programCounter += 1


    fileOut = open(file.name[:-4] + ".s", "w")

    for i in range (0,programCounter):
        if i in addressesThatNeedLabels:
            address = str(i*4)
            addressStr = "Addr_" +  address.zfill(4) + ":\n"
            fileOut.write(addressStr)

        fileOut.write(tempOutputList[i])

    fileOut.close

if __name__ == "__main__":
    #inputStr = input("Please input a textfile: ")
    inputStr = "test.obj"
    main(inputStr)      