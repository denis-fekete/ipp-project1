import sys

file = []

instOrder = 0
argNum = 0

labelList = []
varList = []

stackVariableCnt = 0
stackFrameCnt = 0

def PrintHelpMenu():
    text = """\
Usage: [PYTHON] parse.py [OPTIONS]

Without OPTIONS parse.py takes text from standard input in 
IPPCode24 language and converts it into an XML file on standard
output.

OPTIONS:
    -h, --help                          Prints (this) help message

PYTHON:
If your system's default python version is not 3.10 use "python3.10"
(when using don't write quotation marks around python command).

Examples:
    python parse.py < path/file         XML representation of code from "file"
                                        will be printed into standard output
"""

    print(text)

#----------------------------------------------------------
def dummy(): # DEBUG:
    1 == 1
#----------------------------------------------------------
def ErrorHandling(code, msg, lineCount):
    """Exits script with Error code "code" and prints "msg" to stderr.
    If "lineCount" is negative number don't on which line error occured
    """
    if lineCount >= 0:
        errorMsg = "Error: " + msg + " (On line: " + str(lineCount) + ")\n"
    else:
        errorMsg = "Error: " + msg + "\n"

    sys.stderr.write(errorMsg)
    exit(code)
#----------------------------------------------------------
def writeInstruction(opcode):
    """ Starts instruction section in XML file"""
    global instOrder
    # increase global counter of instrctions 
    instOrder += 1

    string = "\t" + "<instruction order=\"" +  str(instOrder) + "\" opcode=\"" + opcode + "\">"
    file.append(string)
#----------------------------------------------------------
def writeEndInstruction():
    """ Ends instruction section in XML file"""
    string = "\t" + "</instruction>"
    file.append(string)
    
    global argNum
    argNum = 0 # reset global arguments counter
#----------------------------------------------------------
def writeArg(argType, text):
    """ Writes arguments to the the XML file"""
    global argNum

    # replace problematic characters with XML macros/represenation
    text = text.replace("&", "&amp")
    text = text.replace("<", "&lt")
    text = text.replace(">", "&gt")
    # increase global counter of arguments
    argNum += 1

    string = "\t\t" + "<arg" + str(argNum) + " type=\"" + argType + "\">" + text + "</arg" + str(argNum) + ">"
    file.append(string)
#----------------------------------------------------------
def checkArgsCount(expected, args, lineCount):
    """ Check if "args" contains "expected" number of items, if not end program"""
    # -1 is for KEYWORD that is in args: KEYWORD ARG1 ARG2 etc...
    if expected < len(args) - 1:
        ErrorHandling(23, "Too many arguments given for operation code (or keyword): " + args[0], lineCount)
    if expected > len(args) - 1:
        ErrorHandling(23, "Not enough arguments given for operation code (or keyword): " + args[0], lineCount)
#----------------------------------------------------------
def stackReset():
    """ Resets global "stackCounter" """
    global stackVariableCnt
    stackVariableCnt = 0
#----------------------------------------------------------
def stackVarAdd():
    """ Increases global variable stack counter "stackVariableCnt" by one"""
    global stackVariableCnt
    stackVariableCnt += 1
#----------------------------------------------------------
def stackVarPop():
    """ Returns True if popping from stack of variables was valid"""
    
    global stackVariableCnt
    stackVariableCnt -= 1

    # Check if stackCounter is negative number, if yes return false
    if stackVariableCnt < 0:
        return False

    # Return true if popping was valid and "stackCounter" didn't go to negative
    return True
#----------------------------------------------------------
def stackFrameAdd():
    """ Increases frame stack counter "stackFrameCnt" by one"""
    global stackFrameCnt
    stackFrameCnt += 1
#----------------------------------------------------------
def stackFramePop():
    """ Returns True if popping from stack of frames was valid"""
    global stackFrameCnt
    stackFrameCnt -= 1

    # Check if stackFrameCnt is negative number, if yes return false
    if stackFrameCnt < 0:
        return False

    # Return true if popping was valid and "stackFrameCnt" didn't go to negative
    return True
#----------------------------------------------------------
def isValidLabel(val):
    """ Checks if value "val" is valid label"""
    # label names and variable names follow same rules for naming
    # adding "GF@" makes it valid variable and can be checked by
    # isValidVariable() function
    return isValidVariable("GF@" + val)
#----------------------------------------------------------
def labelAlreadyExists(val, lineCount):
    """ Checks if label "val" already exists in "labelList". 
    Exits with Error code 23 if label name is not valid"""

    if not isValidLabel(val):
        ErrorHandling(23, "Label name '" + val + "' is not allowed", lineCount)

    global labelList

    if val in labelList:
        return True
        
    return False
#----------------------------------------------------------
def isValidVariable(val):
    """ Returns True if variable "val" is valid, False if variable is not valid."""

    identificator = val[0:3]
    if not (identificator == "GF@" or identificator == "LF@" or identificator == "TF@"):
        return False

    i = 4
    while i < len(val):
        if  not (   (val[i] >= '0' and val[i] <= '9') or 
                    (val[i] >= 'a' and val[i] <= 'z') or 
                    (val[i] >= 'A' and val[i] <= 'Z') or
                    val[i] == '_' or val[i] == '-' or 
                    val[i] == '$' or val[i] == '&' or 
                    val[i] == '%' or val[i] == '*' or
                    val[i] == '!' or val[i] == '?'):
                
                return False
        i += 1
        
    return True
#----------------------------------------------------------
def variableAlreadyExists(val, lineCount, exitIfInvalidName=True):
    """ Returns is variable "val" already exits in varList.
     If "exitIfInvalidName" parameter is False script will not exit with error code."""
    # check if variable "val" has valid name
    res = isValidVariable(val)

    # if "val" is not valid name for a variable
    if not res:
        # if "exit if invalid name" is true, print error and exit
        if exitIfInvalidName:
            ErrorHandling(23, val + ": Is not an valid name for variable.", lineCount)
        else: # return false
            return False
        
    global varList
    # check if val is in global variable list
    if val in varList:
        return True
    
    return False
#----------------------------------------------------------
def isValidLiteral(val, exitIfInvalid = 0):
    """Check if value "val" is valid literal, if second argmunet "exitIfInvalid"
      is provided and is not "0" or "False" script will end with Error code 23."""
    # find index of "@"
    idx = val.find("@")
    # separate "val" into literal identificator and literal value
    identificator = val[0:idx+1]
    value = val[idx+1:len(val)]

    if identificator == "string@":
        return "string"
    elif identificator == "int@":
        # check first character, if it is "-" change indexing
        if value[0] == "-":
            i = 1
        else:
            i = 0
        
        # check all characters in "value" to be 0-9
        while i < len(value):
            if not (value[i] >= "0" and value[i] <= "9"):
                if exitIfInvalid:
                    ErrorHandling(23, str(val) + " is not an valid literal", exitIfInvalid)
                else:
                    return "invalid"
            i +=1
            
        return "int"
    elif identificator == "bool@":
        if value == "true" or value == "false":
            return "bool"
    elif identificator == "nil":
        if value == "nil":
            return "nil"
    
    return "invalid"
#----------------------------------------------------------
def isValidSymb(val, lineCount):
    """Checks if value "val" is literal or variable, if neither ends script with code 23.
      If "val" is variable returns "var" (also checks if it was declared), if it is literal returns its type.
    """
    # check if symbol "val" is valid literal
    res = isValidLiteral(val, lineCount)
    if res != "invalid":
        return res
    # check "val" is valid variable and it exists
    elif variableAlreadyExists(val, lineCount, False):
        return "var"
    else:
        ErrorHandling(23, "Argument '" + str(val) +"' is not a valid symbol (variable or literal)", lineCount)
#----------------------------------------------------------
def isValidType(val):
    """Checks if value "val" is valid type, return True if yes"""
    match val:
        case "int":
            return True
        case "string":
            return True
        case "bool":
            return True
        case "nil":
            return True
        case _:
            return False
#----------------------------------------------------------
def keywordProcessing(keyword, argType, args, lineCount):
    """ Processes keyword, sets correct values to "argType" and check syntatic
        errors.
        Returns expected number of arguments for detected keyword. 
    """
    global labelList
    global varList

    match keyword:
        # ---------- Memory and function calling, working with stack ----------
        case "DEFVAR" : # symb
            checkArgsCount(1, args, lineCount)
            
            if not variableAlreadyExists(args[1], lineCount):
                varList.append(args[1])
                argType.append("var")
            else:
                ErrorHandling(23, "Duplicate variable declaration.", lineCount)
        #---------------------------------------
        case "POPS" : # var
            checkArgsCount(1, args, lineCount)

            # check if stack is not already empty
            if not stackVarPop():
                ErrorHandling(23, "Invalid popping from stack of variables, stack was empty.", lineCount)
            # check if provided argument is existing variable
            if not variableAlreadyExists(args[1], lineCount):
                ErrorHandling(23, "Provided variable is not declared", lineCount)
        #---------------------------------------
        case "CREATEFRAME" | "RETURN" | "BREAK" | "PUSHFRAME" | "POPFRAME": # none
            #TODO: check if cannot be joined with PUSHFRAME
            checkArgsCount(0, args, lineCount)
            if keyword == "PUSHFRAME":
                stackFrameAdd()
            if keyword == "POPFRAME":
                # check if stack is not already empty
                if not stackFramePop():
                    ErrorHandling(23, "Invalid popping from stack of frames, stack was empty.", lineCount)
        #---------------------------------------
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" | 
              "LT" |"GT" | "EQ" | "AND" | "OR" | "NOT" |
              "INT2CHAR" | "STRI2INT" |
              "CONCAT" | "GETCHAR" | "SETCHAR" |
              "JUMPIFEQ" | "JUMPIFNEQ") : # var symb1 symb2
            checkArgsCount(3, args, lineCount)

            exists = False
            if keyword == "JUMPIFEQ" or keyword == "JUMPIFNEQ":
                exists = labelAlreadyExists(args[1], lineCount)
            else:
                exists = variableAlreadyExists(args[1], lineCount)

            # check if first argument is variable and exists
            if exists:
                argType.append("var")
                
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

            if variableAlreadyExists(args[1], lineCount):
                if isValidType(args[2]):
                    argType.append("var")
                    argType.append("type")
                else:
                    ErrorHandling(23, "Arguemnt: '" + args[2]  + 
                                  "' is not recognized as valid type", lineCount)
            else:
                ErrorHandling(23, "Variable '" + args[1] + "' wasn't declared", lineCount)
        #---------------------------------------
        case "STRLEN" | "TYPE" | "MOVE" : # var symb
            checkArgsCount(2, args, lineCount)

            if variableAlreadyExists(args[1], lineCount):
                typeT = isValidSymb(args[2], lineCount)
                argType.append("var")
                argType.append(typeT)
            else:
                ErrorHandling(23, "Variable '" + args[1] + "' wasn't declared", lineCount)
        #---------------------------------------
        case "JUMP" | "CALL" | "LABEL" : # label
            checkArgsCount(1, args, lineCount)

            if labelAlreadyExists(args[1], lineCount):
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
            ErrorHandling(22, "Unknown operation code / keyword. Keyword: \"" + str(keyword) + "\"")
    # -------- END OF SWITCH --------
#----------------------------------------------------------
def fillLabels(args, lineCount):
    global labelList

    # check if argument is LABEL, if not skip
    if args[0].upper() == "LABEL":
        checkArgsCount(1, args, lineCount)            
        
        # check if label has valid name
        if isValidLabel(args[1]):
            labelList.append(args[1]) # add label to label list
        else:
            ErrorHandling(23, "Not a valid name for label", lineCount)
#----------------------------------------------------------
def filterRawLine(inputLine):
    """Separates line into operation code/keyword and arguments, 
        removes unnecesary whitespaces and comments if found.
        Returns list of separated arguments.
    """
    # find first "#" in the line
    commentIdx = inputLine.find("#")
    # if "#" was found, separate "line" and "comment" into separate variables
    if commentIdx != -1:
        line = inputLine[0:commentIdx]
    else:
        line = inputLine

    # replace all '\t' with ' ', also replace multiple whitespaces '    ' with just one ' '
    line = line.replace('\t', ' ')
    # split line into arguments
    args = line.split(" ")
    
    # clear '' values from args list
    i = 0
    while i < len(args):
        if len(args[i]) <= 0:
            del args[i]
        else: # if not found, increment
            i += 1

    return args
#----------------------------------------------------------
def syntacticControl(args, lineCount):
    """ Performs syntactic control and fills "file" list"""
    # list for storing types of arguments that will be added in order
    argType = []
    keyword = str.upper(args[0])

    # processing based on keyword
    keywordProcessing(keyword, argType, args, lineCount)

    # write new instruction
    writeInstruction(keyword)

    i = 0
    while i < len(argType):
        # if is valid type (literal) cut type and @ from it
        # example: string@hello_world -> string@ hello_world
        if isValidType(argType[i]):
            value = args[i+1]
            ampIdx = value.find("@")
            value = value[ampIdx + 1:]

            writeArg(argType[i], value)
        else:
            writeArg(argType[i], args[i+1])
        
        i += 1
    # write end of instruction
    writeEndInstruction()
#----------------------------------------------------------
def main():
    #--------------------------------------------------------------------------
    #   Handling of arguments given to parser
    #--------------------------------------------------------------------------

    # 0th argument is name of script, cut it out
    argv = sys.argv[1:] 

    if len(argv) > 1:
        ErrorHandling(10, "Too many arguements, parse.py takes only one argument (--help or -h)", -1)

    if ("--help" in argv) or ("-h" in argv):
        PrintHelpMenu()
        exit(0) # exit script without problems

    #--------------------------------------------------------------------------
    #   Checking head of file
    #--------------------------------------------------------------------------

    lineCount = 1 # line counting
    lines = [] # list of arguments representing each line

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
    #   First pass, filling list of Labels
    #--------------------------------------------------------------------------

    # first pass for filling labels into labelList, loop until EOF is found
    while 1:
        try:
            # store whole line from input file into "line" variable  
            line = input()
            # filter argmuents and look for comments
            args = filterRawLine(line)

            # check if line is not empty
            if len(args) > 0 :
                fillLabels(args, lineCount)
                lineCount += 1
            # store "args" into list of arguments for second pass
            lines.append(args)
        
        # if eof exception is found break from loop
        except EOFError:
            break

    #--------------------------------------------------------------------------
    #   Second pass, creating code and checking syntax
    #--------------------------------------------------------------------------
        
    # write header to xml
    file.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    file.append("<program language=\"IPPcode24\">")

    # reset line counter
    lineCount = 1
    # second pass
    for line in lines:
        lineCount += 1
        if len(line) > 0:
            syntacticControl(line, lineCount)
        
    #end header for xml
    file.append("</program>")

    #--------------------------------------------------------------------------
    #   Writing generated code interpretation into output file
    #--------------------------------------------------------------------------

    for line in file:
        print(line)

#----------------------------------------------------------

main()