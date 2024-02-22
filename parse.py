args = []

file = []

instOrder = 0
argNum = 0

labelList = []
varList = []

stackCounter = 0

enumerate 
#----------------------------------------------------------
def dummy():
    1 == 1
#----------------------------------------------------------
def ErrorHandling(code):
    #TODO:print error message
    print("Error:", code)
    exit(code)
#----------------------------------------------------------
def writeInstruction(opcode):
    """ Starts instruction section in XML file"""
    global instOrder
    instOrder += 1

    string = "\t" + "<instruction order=\"" +  str(instOrder) + "\" opcode=\"" + opcode + "\">"
    file.append(string)
#----------------------------------------------------------
def writeEndInstruction():
    """ Ends instruction section in XML file"""
    string = "\t" + "</instruction>"
    file.append(string)
    
    global argNum
    argNum = 0
#----------------------------------------------------------
def writeArg(argType, text):
    """ Writes arguments to the the XML file"""
    global argNum

    text = filterProblematicChars(text)
    
    argNum += 1
    string = "\t\t" + "<arg" + str(argNum) + " type=\"" + argType + "\">" + text + "</arg" + str(argNum) + ">"
    file.append(string)
#----------------------------------------------------------
def checkArgsCount(expected, args, lineCount):
    """ Returns "False" or "0" if less than expected agruments are stored in "args".
        Returns "True" if expected amount was found. "-1" means more than enough were given
        possible comment found. "-1" means that given arguments is same value as expected.
    """
    # if comment was found
    if expected == -1:
        return 1

    argCount = len(args);
    if argCount < expected:
            #TODO: change to error print
            print("Syntax error on line", lineCount, "not enough arguments")
            print("Line:", args)
            return 0
    # check if no excesive arguments were given
    elif argCount == expected:
        return 1
    # if more than expected other will probably be comments
    else:
        return -1
#----------------------------------------------------------
def checkForComments(args, idx):
    """ Check if arguments in "args" after index "idx" are comments 
    """
    return True
#----------------------------------------------------------
def stackReset():
    """ Resets "stackCounter"
    """
    global stackCounter
    stackCounter = 0
#----------------------------------------------------------
def stackAdd():
    """ Increases "stackCounter" by one
    """
    global stackCounter
    stackCounter += 1
#----------------------------------------------------------
def stackPop():
    """ Returns True if popping from stack was valid
    """
    global stackCounter
    stackCounter -= 1

    # Check if stackCounter is negative number, if yes return false
    if stackCounter < 0:
        return False

    # Return true if popping was valid and "stackCounter" didn't go to negative
    return True
#----------------------------------------------------------
def isValidLabel(val):
    """ Check if value "val" is valid label"""
    if(val[0] > '0' and val[0] < '9'):
        return False
    return True
#----------------------------------------------------------
def labelAlreadyExists(val):
    """ Checks if label "val" already exists in "labelList"."""

    if isValidLabel(val):
        #TODO: print error
        return False

    global labelList

    if val in varList:
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
        if  not ((val[i] > '0' and val[i] < '9') or (val[i] > 'a' and val[i] < 'z') or (val[i] > 'A' and val[i] < 'Z')):
            return False
        if not (val[i] != '_' or val[i] != '$' or val[i] != '&' or val[i] != '%' or val[i] != '*' or val[i] != '!' or val[i] != '?' ):
            return False
        i += 1
        
    return True
#----------------------------------------------------------
def variableAlreadyExists(val):
    """ Returns is variable "val" already exits in varList"""
    if not isValidVariable(val):
        # TODO: print error
        return False

    global varList

    if val in varList:
        return True
    
    return False
#----------------------------------------------------------
def isValidLiteral(val):
    """Check is value "val" is valid literal"""
    #TODO:
    
    idx = val.find("@")
    identificator = val[0:idx+1]
    value = val[idx+1:len(val)]

    if identificator == "string@":
        return "string"
    elif identificator == "int@":
        return "int" # TODO:
    elif identificator == "bool@":
        if value == "true" or value == "false":
            return "bool"
    elif identificator == "nil":
        if value == "nil":
            return "nil"
    
    return "invalid"
#----------------------------------------------------------
def isValidSymbol(val):
    """Checks if value "val" is Literal or Variable"""
    if variableAlreadyExists(val):
        return "var"
    else:
        res = isValidLiteral(val)
        if res != "invalid":
            return res
    return "invalid"
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
def filterProblematicChars(line):
    # filter out characters
    line = line.replace("&", "&amp")
    line = line.replace("<", "&lt")
    line = line.replace(">", "&gt")
    return line
def keywordProcessing(keyword, argType, args):
    global labelList
    global varList

    expectedArgs = 0

    match keyword:
        # ---------- Memory and function calling, working with stack ----------
        case "DEFVAR" : # symb
            expectedArgs = 1
            if not variableAlreadyExists(args[1]):
                varList.append(args[1])
                argType.append("var")
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "PUSHS" : # symb 
            expectedArgs = 1
            if variableAlreadyExists(args[1]):
                argType.append("var")
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "POPS" : # var
            expectedArgs = 1

            if not stackPop():
                # TODO: raise expection, stack underflow
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "POPFRAME" | "PUSHFRAME" | "CREATEFRAME" | "RETURN" : # none
            expectedArgs = 0
        #---------------------------------------
        case "CALL" : # label
            expectedArgs = 1

            if labelAlreadyExists(args[1]):
                argType.append("label")
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" | 
              "LT" |"GT" | "EQ" | "AND" | "OR" | "NOT" |
              "INT2CHAR" | "STRI2INT" |
              "CONCAT" | "GETCHAR" | "SETCHAR") : # var symb1 symb2
            expectedArgs = 3
            if variableAlreadyExists(args[1]):
                argType.append("var")

                res = isValidSymbol(args[2])
                if res == "invalid":
                    ErrorHandling(0) #TODO:
                else:
                    argType.append(res)

                res = isValidSymbol(args[3])
                if res == "invalid":
                    ErrorHandling(0) #TODO:
                else:
                    argType.append(res)
            else:
                ErrorHandling(0) #TODO:

        #---------------------------------------
        case "READ": # var type
            expectedArgs = 2
            if variableAlreadyExists(args[1]):
                if isValidType(args[2]):
                    argType.append("var")
                    argType.append("type")
                else:
                    ErrorHandling(0) # TODO:
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "WRITE": # symb
            expectedArgs = 1
            res = isValidSymbol(args[1])
            if res != "invalid":
                argType.append(res)
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "STRLEN" | "TYPE" | "MOVE" : # var symb
            expectedArgs = 2

            if variableAlreadyExists(args[1]):
                res = isValidSymbol(args[2])
                if res != "invalid":
                    argType.append("var")
                    argType.append(res)
                else:
                    ErrorHandling(0) # TODO:
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "LABEL" : # label
            expectedArgs = 1
            if isValidLabel(args[1]):
                argType.append("label")
                labelList.append(args[1]) # add label to label list
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "JUMP" : # label
            expectedArgs = 1
            if isValidLabel(args[1]):
                argType.append("label")
            else:
                ErrorHandling(0) # TODO:
        #---------------------------------------
        case "JUMPIFEQ" | "JUMPIFNEQ" : # label symb1 symb2
            expectedArgs = 3
            if isValidLabel(args[1]):
                argType.append("label")

                res = isValidSymbol(args[2])
                if res == "invalid":
                    ErrorHandling(0) #TODO:
                else:
                    argType.append(res)

                res = isValidSymbol(args[3])
                if res == "invalid":
                    ErrorHandling(0) #TODO:
                else:
                    argType.append(res)
        #---------------------------------------
        case ("EXIT" | "DPRINT") : # symb
            expectedArgs = 1
            res = isValidSymbol(args[1])
            if res != "invalid":
                argType.append(res)
            else:
                ErrorHandling(0) #TODO:
        #---------------------------------------
        case "BREAK" : # none
            expectedArgs = 0
        #---------------------------------------
        case "#" : # none
            expectedArgs = -1
        #---------------------------------------
        case _ :
            #TODO: error unknown symbol
            print(args)
            print("Error, no matching keyword for:", args[0])
            ErrorHandling(1) #TODO:
    # -------- END OF SWITCH --------
    
    return expectedArgs
#----------------------------------------------------------
def fsm(args, lineCount):
    global labelList
    global varList

    keyword = str.upper(args[0])
    argType = []

    # processing based on keyword
    expectedArgs = keywordProcessing(keyword, argType, args)

    # check if correct number of arguments were provided
    result = checkArgsCount(expectedArgs, args, lineCount)
    # write new instruction
    writeInstruction(keyword)
    # fill all arguments

    # append empty dummy characters to argType
    argType.append(" ")
    argType.append(" ")
    argType.append(" ")

    i = 0
    while i < expectedArgs:
        writeArg(argType[i], args[i+1])
        i += 1
    # check for comments
    checkForComments(args, expectedArgs)
    # write end of instruction
    writeEndInstruction()

#----------------------------------------------------------

def main():
    # test first line
    line = input()
    
    # find #comment if there is some
    commentIdx = line.find("#")
    codeVersion = line[0:commentIdx]
    # delete tabulators '\t' and whitespaces ' '
    codeVersion = codeVersion.replace("\t", "").replace(" ", "")

    if codeVersion.upper() != ".IPPCODE24":
        
        ErrorHandling(21)
    # write header to xml
    file.append("<? xml version=\"1.0\" encoding=\"UTF-8\"?>")
    file.append("<program language=\"IPPcode24\">")
    
    # line counting
    lineCount = 1

    # loop until EOF is found
    while 1:
        try:
            # store whole line into  
            line = input()
            # replace all '\t' with ' ', also replace multiple whitespaces '    ' with just one ' '
            line = line.replace('\t', ' ')
            # add space after #
            line = line.replace("#", " #")
            # split line into arguments
            args = line.split(" ")
            
            emptyLineSkip = line.replace(" ", "").replace("\t", "")
            if len(emptyLineSkip) != 0:
                fsm(args, lineCount)
                lineCount += 1

        # if eof exception is found break from loop
        except EOFError:
            break

    #end header for xml
    file.append("</program>")

    for line in file:
        print(line)

#----------------------------------------------------------

main()