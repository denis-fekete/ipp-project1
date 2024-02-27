from ipp24_module.arg_processing import *
from ipp24_module.utilities import *


def writeInstruction(opcode, file, instOrder):
    """ Starts instruction section in XML file"""
    # increase global counter of instrctions 
    instOrder += 1

    string = "\t" + "<instruction order=\"" +  str(instOrder) + "\" opcode=\"" + opcode + "\">"
    file.append(string)

    return instOrder

#----------------------------------------------------------

def writeEndInstruction(file):
    """ Ends instruction section in XML file"""
    string = "\t" + "</instruction>"
    file.append(string)

#----------------------------------------------------------
    
def writeArg(argType, text, file, argNum):
    """ Writes arguments to the the XML file"""

    # replace problematic characters with XML macros/represenation
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    # increase global counter of arguments
    argNum += 1

    string = "\t\t" + "<arg" + str(argNum) + " type=\"" + argType + "\">" + text + "</arg" + str(argNum) + ">"
    file.append(string)

    return argNum

#----------------------------------------------------------

def keywordProcessing(keyword, argType, args, lineCount):
    """ Processes keyword, sets correct values to "argType" and check syntatic
        errors.
        Returns expected number of arguments for detected keyword. 
    """

    match keyword:
        # ---------- Memory and function calling, working with stack ----------
        case "DEFVAR" : # symb
            checkArgsCount(1, args, lineCount)
            
            if isValidVariable(args[1], lineCount):
                argType.append("var")
        #---------------------------------------
        case "POPS" : # var
            checkArgsCount(1, args, lineCount)
            if isValidVariable(args[1], lineCount):
                argType.append("var")
        #---------------------------------------
        case "CREATEFRAME" | "RETURN" | "BREAK" | "PUSHFRAME" | "POPFRAME": # none
            checkArgsCount(0, args, lineCount)
        #---------------------------------------
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" |
              "LT" |"GT" | "EQ" | "AND" | "OR" |
                "STRI2INT" |
              "CONCAT" | "GETCHAR" | "SETCHAR" |
              "JUMPIFEQ" | "JUMPIFNEQ") : # var symb1 symb2
            checkArgsCount(3, args, lineCount)

            exists = False
            if keyword == "JUMPIFEQ" or keyword == "JUMPIFNEQ":
                exists = isValidLabel(args[1], lineCount)
                argType.append("label")
            else:
                exists = isValidVariable(args[1], lineCount)
                argType.append("var")

            # check if first argument is variable and exists
            if exists:
                #check if arg[2] is valid symbol
                typeT = isValidSymb(args[2], lineCount)
                argType.append(typeT)

                typeT = isValidSymb(args[3], lineCount)
                argType.append(typeT)
            else:
                if keyword == "JUMPIFEQ" or keyword == "JUMPIFNEQ":
                    ErrorHandling(23, "Label '" + args[1] + "'wasn't declared", lineCount)
                else:
                    ErrorHandling(23, "Variable '" + args[1] + "' wasn't declared", lineCount)
        #---------------------------------------
        case "READ": # var type
            checkArgsCount(2, args, lineCount)

            if isValidVariable(args[1], lineCount):
                if isValidType(args[2]):
                    argType.append("var")
                    argType.append("type")
                else:
                    ErrorHandling(23, "Arguemnt: '" + args[2]  + 
                                  "' is not recognized as valid type", lineCount)
        #---------------------------------------
        case "STRLEN" | "TYPE" | "MOVE" | "INT2CHAR" | "NOT" : # var symb
            checkArgsCount(2, args, lineCount)

            if isValidVariable(args[1], lineCount):
                typeT = isValidSymb(args[2], lineCount)
                argType.append("var")
                argType.append(typeT)
        #---------------------------------------
        case "JUMP" | "CALL" | "LABEL" : # label
            checkArgsCount(1, args, lineCount)

            if isValidLabel(args[1], lineCount):
                argType.append("label")
            else:
                ErrorHandling(23, "Label doesn't exist", lineCount)
        #---------------------------------------
        case ("EXIT" | "DPRINT" | "WRITE" | "PUSHS") : # symb
            checkArgsCount(1, args, lineCount)

            typeT = isValidSymb(args[1], lineCount)
            argType.append(typeT)
        #---------------------------------------
        case _ :
            ErrorHandling(22, "Unknown operation code / keyword. Keyword: \"" + str(keyword) + "\"", lineCount)
    # -------- END OF SWITCH --------
            
#----------------------------------------------------------
            
def syntacticControl(args, lineCount, instOrder, file):
    """ Performs syntactic control and fills "file" list"""
    # list for storing types of arguments that will be added in order
    argNum = 0
    argType = []
    keyword = str.upper(args[0])

    # processing based on keyword
    keywordProcessing(keyword, argType, args, lineCount)

    # write new instruction
    instOrder = writeInstruction(keyword, file, instOrder)

    i = 0
    while i < len(argType):
        # if is valid type (literal) cut type and @ from it
        # example: string@hello_world -> string@ hello_world
        if isValidType(argType[i]):
            value = args[i+1]
            ampIdx = value.find("@")
            value = value[ampIdx + 1:]

            argNum = writeArg(argType[i], value, file, argNum)
        else:
            argNum = writeArg(argType[i], args[i+1], file, argNum)
        
        i += 1
    # write end of instruction
    writeEndInstruction(file)

    return instOrder

#----------------------------------------------------------

def main():
    #--------------------------------------------------------------------------
    #   Handling of arguments given to parser
    #--------------------------------------------------------------------------

    # 0th argument is name of script, cut it out
    ParameterHandling(sys.argv)

    #--------------------------------------------------------------------------
    #   Checking head of file
    #--------------------------------------------------------------------------

    lineCount = 1 # line counting

    # filter out newlines and comments before header (.ippcode24)
    while 1:
        # load line from input
        try:
            line = input() # hold information about current line
        except EOFError:
            ErrorHandling(23, "No header found, empty input", -1)

        # split line into arguments and filter out comments
        codeVersion = filterRawLine(line)
        # if first argument of list is not a new line break out 
        if len(codeVersion) > 0:
            break

        lineCount += 1
    # ----------------- END OF WHILE -----------------
    
    # check if first line contains "IPPCODE24" as first argument
    if codeVersion[0].upper() != ".IPPCODE24":
        ErrorHandling(21, "Invalid header", lineCount) # magic constant 
    elif len(codeVersion) > 1: # check if first line is only 
        ErrorHandling(23, "First line must contain only '.IPPCODE24'" +
                      " (case insensitive) and comment.", lineCount)

    #--------------------------------------------------------------------------
    #   Processing input code and syntax control
    #--------------------------------------------------------------------------
    file = [] # stores output string in XML format
    instOrder = 0 # instruction order counter

    # write header to xml
    file.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    file.append("<program language=\"IPPcode24\">")

    # first pass for filling labels into labelList, loop until EOF is found
    while 1:
        try:
            # store whole line from input file into "line" variable  
            line = input()
            # filter argmuents and look for comments
            args = filterRawLine(line)
            lineCount += 1

            # check if line is not empty
            if len(args) > 0 :
                instOrder = syntacticControl(args, lineCount, instOrder, file)
            # store "args" into list of arguments for second pass
        
        # if eof exception is found break from loop
        except EOFError:
            break

    # ----------------- END WHILE ---------------
    #end header for xml
    file.append("</program>")

    #--------------------------------------------------------------------------
    #   Writing generated code interpretation into output file
    #--------------------------------------------------------------------------

    for line in file:
        print(line)

    exit(0)
#----------------------------------------------------------

main()