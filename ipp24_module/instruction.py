from dataclasses import dataclass
import sys
from ipp24_module import argument
 

class Instruction:
    """Class that holds information about instruction"""
    order : int # order of instruction
    opcode : str # opcode / keyword / operation code of instrction
    args : argument.Argument = [] # list holding arguments

    def __init__(self, order : int, opcode : str, args : argument.Argument):
        self.order = order
        self.opcode = opcode
        self.args = args

#------------------------------------------------------------------------------

    def PrintMe(self, prefix : str = "\t", argPrefix : str = "\t\t", addNewLine : bool = True):
        """Prints contains to of argument to standard output"""
        # print start of instuction
        string = prefix + "<instruction order=\"" +  str(self.order) + "\" opcode=\"" + str(self.opcode) + "\">"
        if(addNewLine):
            string += "\n"
        sys.stdout.write(string)

        # print arguments 
        # i + 1 because args need to be counter from 1
        for i in range(len(self.args)):
            self.args[i].PrintMe(argPrefix, i+1, addNewLine)
        
        # print end of instruction
        string = prefix + "</instruction>"
        if(addNewLine):
            string += "\n"

        sys.stdout.write(string)

#------------------------------------------------------------------------------