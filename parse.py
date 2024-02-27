from ipp24_module.arg_processing import *
from ipp24_module.utilities import *
from ipp24_module.instruction import *
from ipp24_module.argument import * 


#----------------------------------------------------------

def keywordProcessing(keyword, args, lineCount):
    """ Processes keyword, sets correct values to "argType" and check syntatic
        errors.
        Returns expected number of arguments for detected keyword. 
    """
    argList : Argument = []
    match keyword:
        # ---------- Memory and function calling, working with stack ----------
        case "DEFVAR" | "POPS": # symb
            checkArgsCount(1, args, lineCount, keyword)
            
            argList.append(Argument())
        
            if argList[0].CheckIfNotValid(args[0], "var") :
                ErrorHandling(23, args[1] + " is not a valid variable name", lineCount)
        #---------------------------------------
        case "CREATEFRAME" | "RETURN" | "BREAK" | "PUSHFRAME" | "POPFRAME": # none
            checkArgsCount(0, args, lineCount, keyword)
        #---------------------------------------
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" |
              "LT" |"GT" | "EQ" | "AND" | "OR" |
                "STRI2INT" |
              "CONCAT" | "GETCHAR" | "SETCHAR" |
              "JUMPIFEQ" | "JUMPIFNEQ") : # var symb1 symb2
            checkArgsCount(3, args, lineCount, keyword)

            # based on keyword check first argument to be label or variable
            if keyword == "JUMPIFEQ" or keyword == "JUMPIFNEQ":
                argList.append(Argument())

                if argList[0].CheckIfNotValid(args[0], "label") :
                    ErrorHandling(23, args[1] + " is not a valid label name", lineCount)
            else:
                argList.append(Argument())

                if argList[0].CheckIfNotValid(args[0], "var") :
                    ErrorHandling(23, args[1] + " is not a valid variable name", lineCount)

            # check second parameter to be symbol
            argList.append(Argument())

            if argList[1].CheckIfNotValid(args[1], "symbol") :
                ErrorHandling(23, args[1] + " is not a valid symbol", lineCount)
            
            # check third parameter to be symbol
            argList.append(Argument())

            if argList[2].CheckIfNotValid(args[2], "symbol") :
                ErrorHandling(23, args[1] + " is not a valid symbol", lineCount)
        #---------------------------------------
        case "READ": # var type
            checkArgsCount(2, args, lineCount, keyword)

            argList.append(Argument())

            if argList[0].CheckIfNotValid(args[0], "var") :
                ErrorHandling(23, args[0] + " is not a valid variable name", lineCount)

            if isValidType(args[1]):
                argList.append(Argument())
                argList[1].SetType("type")
                argList[1].SetText(args[1])
            else:
                ErrorHandling(23, "Argument: '" + args[1]  + "' is not recognized as valid type", lineCount)
        #---------------------------------------
        case "STRLEN" | "TYPE" | "MOVE" | "INT2CHAR" | "NOT" : # var symb
            checkArgsCount(2, args, lineCount, keyword)

            argList.append(Argument())

            if argList[0].CheckIfNotValid(args[0], "var") :
                ErrorHandling(23, args[0] + " is not a valid variable name", lineCount)
            argList.append(Argument())

            if argList[1].CheckIfNotValid(args[1], "symbol") :
                ErrorHandling(23, args[1] + " is not a valid symbol", lineCount)
        #---------------------------------------
        case "JUMP" | "CALL" | "LABEL" : # label
            checkArgsCount(1, args, lineCount, keyword)

            argList.append(Argument())

            if argList[0].CheckIfNotValid(args[0], "label") :
                ErrorHandling(23, args[0] + " is not a valid label name", lineCount)
        #---------------------------------------
        case ("EXIT" | "DPRINT" | "WRITE" | "PUSHS") : # symb
            checkArgsCount(1, args, lineCount, keyword)

            argList.append(Argument())

            if argList[0].CheckIfNotValid(args[0], "symbol") :
                ErrorHandling(23, args[0] + " is not a valid symbol", lineCount)
        #---------------------------------------
        case _ :
            ErrorHandling(22, "Unknown operation code / keyword. Keyword: \"" + str(keyword) + "\"", lineCount)
    # -------- END OF SWITCH --------
            
    return argList

#----------------------------------------------------------

def main():
    #--------------------------------------------------------------------------
    #   Handling of arguments given to parser
    #--------------------------------------------------------------------------

    # 0th argument is name of script, cut it out
    parameterHandling(sys.argv)

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
    instOrder = 1 # instruction order counter

    program : Instruction = []

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
                # turn first argument on line into uppercase
                keyword = str.upper(args[0])
                # processing based on keyword
                argList = keywordProcessing(keyword, args[1:], lineCount)
                # create instruction with arguemnts
                inst = Instruction(instOrder, keyword, argList)
                # append instruction into program
                program.append(inst)

                instOrder += 1
            # store "args" into list of arguments for second pass
        
        # if eof exception is found break from loop
        except EOFError:
            break

    # ----------------- END WHILE ---------------

    #--------------------------------------------------------------------------
    #   Writing generated code interpretation into output file
    #--------------------------------------------------------------------------
        
    # write header to xml
    sys.stdout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>"+"\n")
    sys.stdout.write("<program language=\"IPPcode24\">"+"\n")

    for instruction in program:
        instruction.PrintMe("\t", "\t\t", True)

    #end header for xml
    sys.stdout.write("</program>"+"\n")

    exit(0)
#----------------------------------------------------------

main()