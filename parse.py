import sys

args = []

file = []

instOrder = 0
argNum = 0

labelList = []
varList = []

stackVariableCnt = 0
stackFrameCnt = 0

enumerate 
#----------------------------------------------------------
def dummy():
    1 == 1
#----------------------------------------------------------
def ErrorHandling(code, msg, lineCount):
    errorMsg = "Error: " + msg + " (On line: " + str(lineCount) + ")\n"
    sys.stderr.write(errorMsg)
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
    """ Check if "args" contains "expected" number of items, if not
        end program"""
    if expected > len(args) - 1:
        ErrorHandling(23, "Too many arguments given for operation code/keyword: " + args[0]+ " ", lineCount)
    if expected < len(args) - 1:
        ErrorHandling(23, "Not enough arguments given for operation code/keyword: " + args[0] + " ", lineCount)
#----------------------------------------------------------
def stackReset():
    """ Resets "stackCounter"
    """
    global stackVariableCnt
    stackVariableCnt = 0
#----------------------------------------------------------
def stackVarAdd():
    """ Increases variable stack counter "stackVariableCnt" by one"""
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
    """ Check if value "val" is valid label"""
    return True #TODO:
#----------------------------------------------------------
def labelAlreadyExists(val, lineCount):
    """ Checks if label "val" already exists in "labelList"."""

    if not isValidLabel(val):
        ErrorHandling(23, "Label name '" + val + "' is not allowed", lineCount)

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
def variableAlreadyExists(val, lineCount):
    """ Returns is variable "val" already exits in varList"""
    if not isValidVariable(val):
        ErrorHandling(23, val + ": Is not an valid name for variable.", lineCount)
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
def isValidSymbol(val, lineCount):
    """Checks if value "val" is literal or variable, returns "invalid" if neither.
      If "val" is variable returns "var" (also checks if it was declared), if it is literal returns its type.
      Returns "invalid" if "val" is not variable or literal.
    """
    # check if symbol "val" is valid literal
    res = isValidLiteral(val)
    if res != "invalid":
        return res
    # check "val" is valid variable and it exists
    elif variableAlreadyExists(val, lineCount):
        return "var"
    else:
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
    """Replaces '<', '>' and '&' to appropriate macro to work with XML"""
    # filter out characters
    line = line.replace("&", "&amp")
    line = line.replace("<", "&lt")
    line = line.replace(">", "&gt")
    return line
#----------------------------------------------------------
def keywordProcessing(keyword, argType, args, lineCount):
    """ Processes keyword, sets correct values to "argType" and check syntatic
        errors.
        Returns expected number of arguments for detected keyword. 
    """
    global labelList
    global varList

    expectedArgs = 0

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
        case "PUSHS" : # symb 
            checkArgsCount(1, args, lineCount)

            res = isValidSymbol(args[1], lineCount)
            if res != "invalid":
                argType.append(res)
            else:
                ErrorHandling(23, "Provided symbol is not variable or literal", lineCount)
        #---------------------------------------
        case "POPS" : # var
            checkArgsCount(1, args, lineCount)

            # check if stack is not already empty
            if not stackVarPop():
                # TODO: raise expection, stack underflow
                ErrorHandling(23) # TODO:
            # check if provided argument is existing variable
            if not variableAlreadyExists(args[1], lineCount):
                ErrorHandling(23, "Provided variable is not declared", lineCount)
        #---------------------------------------
        case "POPFRAME": # none
            checkArgsCount(0, args, lineCount)

            # check if stack is not already empty
            if not stackFramePop():
                ErrorHandling(23, "Invalid popping from stack, stack was empty.", lineCount)
        #---------------------------------------
        case "PUSHFRAME": # none
            checkArgsCount(0, args, lineCount)
            stackFrameAdd()
        #---------------------------------------
        case "CREATEFRAME" | "RETURN" | "BREAK": # none
            #TODO: check if cannot be joined with PUSHFRAME
            checkArgsCount(0, args, lineCount)
        #---------------------------------------
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" | 
              "LT" |"GT" | "EQ" | "AND" | "OR" | "NOT" |
              "INT2CHAR" | "STRI2INT" |
              "CONCAT" | "GETCHAR" | "SETCHAR") : # var symb1 symb2
            checkArgsCount(3, args, lineCount)

            # check if first argument is variable and exists
            if variableAlreadyExists(args[1], lineCount):
                argType.append("var")
                
                #check if arg[2] is valid symbol
                res = isValidSymbol(args[2], lineCount)
                if res == "invalid":
                    ErrorHandling(23) #TODO:
                else:
                    argType.append(res)

                res = isValidSymbol(args[3], lineCount)
                if res == "invalid":
                    ErrorHandling(23) #TODO:
                else:
                    argType.append(res)
            else:
                ErrorHandling(23) #TODO:

        #---------------------------------------
        case "READ": # var type
            checkArgsCount(2, args, lineCount)

            if variableAlreadyExists(args[1], lineCount):
                if isValidType(args[2]):
                    argType.append("var")
                    argType.append("type")
                else:
                    ErrorHandling(23) # TODO:
            else:
                ErrorHandling(23) # TODO:
        #---------------------------------------
        case "WRITE": # symb
            checkArgsCount(1, args, lineCount)

            res = isValidSymbol(args[1], lineCount)
            if res != "invalid":
                argType.append(res)
            else:
                ErrorHandling(23) # TODO:
        #---------------------------------------
        case "STRLEN" | "TYPE" | "MOVE" : # var symb
            checkArgsCount(2, args, lineCount)

            if variableAlreadyExists(args[1], lineCount):
                res = isValidSymbol(args[2], lineCount)
                if res != "invalid":
                    argType.append("var")
                    argType.append(res)
                else:
                    ErrorHandling(23, "Variable doesn't exist", lineCount)
            else:
                ErrorHandling(23, "Variable doesn't exist", lineCount) # TODO:
        #---------------------------------------
        case "LABEL" : # label
            checkArgsCount(1, args, lineCount)            

            if isValidLabel(args[1]):
                argType.append("label")
                labelList.append(args[1]) # add label to label list
            else:
                ErrorHandling(23, "Not a valid name for label", lineCount)
        #---------------------------------------
        case "JUMP" | "CALL" : # label
            checkArgsCount(1, args, lineCount)

            if labelAlreadyExists(args[1], lineCount):
                argType.append("label")
            else:
                ErrorHandling(23, "Label doesn't exist", lineCount)
        #---------------------------------------
        case "JUMPIFEQ" | "JUMPIFNEQ" : # label symb1 symb2
            checkArgsCount(3, args, lineCount)
            
            if isValidLabel(args[1]):
                argType.append("label")

                res = isValidSymbol(args[2], lineCount)
                if res == "invalid":
                    ErrorHandling(23) #TODO:
                else:
                    argType.append(res)

                res = isValidSymbol(args[3], lineCount)
                if res == "invalid":
                    ErrorHandling(23) #TODO:
                else:
                    argType.append(res)
        #---------------------------------------
        case ("EXIT" | "DPRINT") : # symb
            checkArgsCount(1, args, lineCount)

            res = isValidSymbol(args[1], lineCount)
            if res != "invalid":
                argType.append(res)
            else:
                ErrorHandling(23) #TODO:
        #---------------------------------------
        case _ :
            #TODO: error unknown symbol
            ErrorHandling(22, "Unknown operation code / keyword. Keyword: \"" + str(keyword) + "\"")
    # -------- END OF SWITCH --------
    
    return expectedArgs
#----------------------------------------------------------
def filterRawLine(inputLine):
    """Separates line into operation code/keyword and arguments, 
        removes unnecesary whitespaces and separates comment if detected
    """
    # find first "#" in the line
    commentIdx = inputLine.find("#")
    # if "#" was found, separate "line" and "comment" into separate variables
    comment = ""
    if commentIdx != -1:
        comment = inputLine[commentIdx:len(inputLine)]
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

    return comment, args
#----------------------------------------------------------
def fsm(args, lineCount):
    #TODO: add comment
    """
    """
    print(args)
    argType = []
    keyword = str.upper(args[0])

    # processing based on keyword
    expectedArgs = keywordProcessing(keyword, argType, args, lineCount)

    # write new instruction
    writeInstruction(keyword)

    i = 0
    while i < len(argType):
        writeArg(argType[i], args[i+1])
        i += 1
    # write end of instruction
    writeEndInstruction()

#----------------------------------------------------------

def main():
    # test first line
    line = input()
    
    # find #comment if there is some
    commentIdx = line.find("#")

    # check if there is and comment on header line 
    if(commentIdx > 0):
        codeVersion = line[0:commentIdx]
    else: # if not store whole line
        codeVersion = line

    # delete tabulators '\t' and whitespaces ' '
    codeVersion = codeVersion.replace("\t", " ").split(" ")
    #TODO: checking if there is invalid code after ippCode24 or comments
    if codeVersion[0].upper() != ".IPPCODE24":
        ErrorHandling(21, "Nonexisting / invalid header")

    # write header to xml
    file.append("<? xml version=\"1.0\" encoding=\"UTF-8\"?>")
    file.append("<program language=\"IPPcode24\">")
    
    # line counting
    lineCount = 1

    # loop until EOF is found
    while 1:
        try:
            # store whole line from input file into "line" variable  
            line = input()
            # filter argmuents and look for comments            
            comment, args = filterRawLine(line)

            # check if line is not empty
            if len(args) > 0 :
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