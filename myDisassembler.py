"""
Project 1 - Disassembler
ECE 3504, Fall 2021
Nate Doggett

Description: This program disassembles MIPS machines code and coverts
the content into human-readable MIPS assembly
"""
import sys
class RType:
    """ RType instruction type """
    def __init__(self):
        """
        This class is built to handle an R-Type MIPS
        assembly language instruction. The R-Type is
        in the form of an opcode (ALL ZEROS),
        rs, rt, and rd registers, a shift amount,
        and a function encoding
        """
        self.op = None
        self.rs = None
        self.rt = None
        self.rd = None
        self.shamt = None
        self.funct = None

    def parseRType(self, line):
        """ 
        Parses a 32-bit line into the proper
        opcode, registers, and immediate value expected
        from an R-Type instruction

        @param: line    A 32-bit string containing the MIPS
                        instruction in binary
        """
        self.op = "000000"
        self.rs = line[6:11]
        self.rt = line[11:16]
        self.rd = line[16:21]
        self.shamt = line[21:26]
        self.funct = line[26:32]

class IType:
    """ IType instruction type """
    def __init__(self):
        """
        This class is built to handle an I-Type MIPS
        assembly language instruction. The I-Type is
        in the form of an opcode, rs and rt regsiter,
        and an immediate value 
        """
        self.op = None
        self.rs = None
        self.rt = None
        self.immed = None

    def parseIType(self, line):
        """ 
        Parses a 32-bit line into the proper
        opcode, registers, and immediate value expected
        from an I-Type instruction

        @param: line    A 32-bit string containing the MIPS
                        instruction in binary
        """
        self.op = line[0:6]
        self.rs = line[6:11]
        self.rt = line[11:16]
        self.immed = line[16:32]

BYTE_LENGTH = 4

def main(inputStr):
    hasError = False
    # dictionary of are R_Type and I_Type binary equivalents
    r_type_op_codes = { '100000':'add',
                        '100001':'addu',
                        '100100':'and',
                        '100111':'nor',
                        '100101':'or',
                        '101010':'slt',
                        '101011':'sltu',
                        '000000':'sll',
                        '000010':'srl',
                        '100010':'sub',
                        '100011':'subu'}
    i_type_op_codes = { '001000':'addi',
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

    try:
        file = open(inputStr, 'r')
    except:
        print("Cannot dissassemble. File does not exist.")
        return
    f = file.readlines()
    file.close()

    tempOutputList = {}
    addressesThatNeedLabels = []
    programCounter = 0
    lineCounter = 1

    for line in f:
        try:
            str1 = line.strip()

            res = "{0:08b}".format(int(str1, 16)) # converts the hex string into binary
            resFilled = res.zfill(32) # fills the result with any leading zeros

            my_rtype = RType() # reused objects for each pass
            my_itype = IType() # reused objects for each pass
            isRType = False

            if (line[0:6] == '000000'):
                my_rtype.parseRType(resFilled)
                isRType = True
            else:
                my_itype.parseIType(resFilled)
                isRType = False

            if isRType:
                op_str = r_type_op_codes[my_rtype.funct]
                rs_str = register_dict[my_rtype.rs]
                rt_str = register_dict[my_rtype.rt]
                rd_str = register_dict[my_rtype.rd]
                shamt_str = int(my_rtype.shamt,2)

                # only has a different format if a shift amount is given
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

                # if the immed_str should be a negative signed value
                if (immed_str > 50000):
                    immed_str = immed_str-65536

                # format for lw and sw
                if (op_str == "lw" or op_str == "sw"):
                    tempOutputList[programCounter] = "\t" + op_str + " " + rt_str + ", " + str(immed_str) + "(" + rs_str + ")" + "\n"

                # format for beq or bne
                elif (op_str == "beq" or op_str == "bne"):
                    address = BYTE_LENGTH*(programCounter + immed_str + 1)
                    hexAddress = str( hex(address) )
                    hexAddress = hexAddress[2:]
                    addressStr = "Addr_" +  hexAddress.zfill(4)
                    addressesThatNeedLabels.append(programCounter + immed_str + 1)
                    tempOutputList[programCounter] = "\t" + op_str + " " + rt_str + ", " + rs_str + ", " + addressStr + "\n"

                # all other IType formats
                else:
                    tempOutputList[programCounter] = "\t" + op_str + " " + rt_str + ", " + rs_str + ", " + str(immed_str) + "\n"
            programCounter += 1
            lineCounter += 1

        # catches and handles any errors thrown while attmepting to dissassemble
        except:
            output = f[lineCounter-1].strip()
            print(f"Cannot dissasemble {output} at line {lineCounter}")
            hasError = True
            programCounter += 1
            lineCounter += 1

    # if there where no errors, write to <file_name>.s
    if not hasError:
        fileOut = open(file.name[:-4] + ".s", "w") # let the final name be name minus .obj

        for idx in range (0,programCounter):
            if idx in addressesThatNeedLabels:
                address = BYTE_LENGTH*idx
                hexAddress = str( hex(address) )
                hexAddress = hexAddress[2:]
                addressStr = "Addr_" +  hexAddress.zfill(4) + ":\n"
                fileOut.write(addressStr)

            fileOut.write(tempOutputList[idx])
        fileOut.close

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Cannot dissassemble this argument.")
    else:
        main(sys.argv[1])      