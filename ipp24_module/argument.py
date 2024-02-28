from dataclasses import dataclass
import sys
from ipp24_module.arg_processing import validSymbolsForName,  isValidType, filterBlockedChars
from ipp24_module.utilities import ACCEPTED_UNICODE

@dataclass
class Argument:
    """Class that holds information about argument"""

    ttype : str
    text : str

    def __init__(self):
#------------------------------------------------------------------------------
        self.ttype = ""
        self.text = ""

#------------------------------------------------------------------------------

    def CheckIfNotValid(self, arg : str, expected : str):
        """Returns False (0) if argument is valid and if it has expected value\
        Accepted values for exprected are: "symbol", "var", "label" and "literal"\
        where symbols means either var of literal"""
        # decide type based on "arg" parameter and return True if error occured

        if (self.__decideType__(arg) ):
            if (expected == self.ttype):
                return False
            # if expected == symbol, check ttype is variable or literal
            elif (expected == "symbol" and (self.ttype == "var" or isValidType(self.ttype))):
                return False
            # no valid combination, error
            else:
                return True
        else:
            return True

#------------------------------------------------------------------------------

    def PrintMe(self, prefix : str, number : int, addNewLine : bool = True):
        """Prints contains to of argument to standard output"""
        string = prefix + "<arg" + str(number) + " type=\"" + str(self.ttype)
        string += "\">" + str(self.text) + "</arg" + str(number) + ">"

        if(addNewLine):
            string += "\n"
            
        sys.stdout.write(string)
#------------------------------------------------------------------------------

    def SetType(self, ttype):
        """Sets type of argument"""
        self.ttype = ttype

#------------------------------------------------------------------------------

    def SetText(self, text):
        """Sets type of argument"""
        self.text = text

#------------------------------------------------------------------------------
    
    def __decideType__(self, arg : list):
        """Sets type and text of argument, returns True on success"""

        # check if is valid to be variable name
        if self.__isVariable__(arg):
            self.ttype = "var"
            self.text = filterBlockedChars(arg)
            return True
        # if not variable, check if label
        elif self.__isLabel__(arg):
            self.ttype = "label"
            self.text = filterBlockedChars(arg)
            return True
        
        # if neither, check if is literal
        literalType, value =  self.__isLiteral__(arg)
        if(literalType != "invalid"):
            self.ttype = literalType
            self.text = filterBlockedChars(value)
            return True

        return False

#------------------------------------------------------------------------------

    def __isLabel__(self, name : str):
        # name of literal must not start with number
        if name[0].isnumeric():
            return False
        # check rest of the name for literal
        return validSymbolsForName(name)

#------------------------------------------------------------------------------

    def __isVariable__(self, name : str):
        """Returns if prefix of variable name is valid, if yes check other with
        function __isLabel__ (same rules apply to both)"""
        # check if variable has "LF@", "GF@" or "TF@" prefix
        if not (name[0:3] == "LF@" or name[0:3] == "TF@" or name[0:3] == "GF@"):
            return False

        # same rules apply for labels and variables, use same method
        return self.__isLabel__(name[3:]) 

#------------------------------------------------------------------------------

    def __isLiteral__(self, string : str):
        """Check if value "val" is valid literal, if second argmunet "exitIfInvalid"
        is provided and is not "0" or "False" script will end with Error code 23."""
        # find index of "@"
        idx = string.find("@", 1)
        # separate "val" into literal identificator and literal value
        identificator = string[0:idx+1]
        value = string[idx+1:len(string)]

        # ---------------------------------------------------------------------
        if identificator == "string@":
            i = 0
            while i < len(value):
                # if found backslash(\), check if it is accepted in ACCEPTED_UNICODE
                if value[i] == '\\' :
                    if not (value[i + 1 : i + 4] in ACCEPTED_UNICODE):
                        return "invalid", value  
                    i += 3
                i += 1

            return "string", value
        # ---------------------------------------------------------------------
        elif identificator == "int@" and len(value) > 0:
            i = 0
            # check first character, if it is "-" change indexing
            if value[0] == "-" or value[0] == "+":
                i += 1
            
            # check all characters in "value" to be 0-9
            while i < len(value):
                if not (value[i] >= "0" and value[i] <= "9"):
                    return "invalid", value
                
                i += 1

            return "int", value
        # ---------------------------------------------------------------------
        elif identificator == "bool@" and len(value) > 0:
            if value == "true" or value == "false":
                return "bool", value
        # ---------------------------------------------------------------------
        elif identificator == "nil@" and len(value) > 0:
            if value == "nil":
                return "nil", value
        # ---------------------------------------------------------------------
        
        return "invalid", value
