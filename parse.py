args = []

file = []

instOrder = 0
argNum = 0

labelList = []
varList = []

stackCounter = 0

#----------------------------------------------------------

def dummy():
    1 == 1

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
    if(val[0] > '0' and val[0] < '9'):
        return False
    return True
    

#----------------------------------------------------------

def variableAlreadyExists(val):
    """ Returns is variable "val" already exits in varList
    """
    if isValidVariable(val):
        # TODO: print error
        return False

    global varList

    if val in varList:
        return True
    
    return False
    
#----------------------------------------------------------

def fsm(args, lineCount):
    global labelList
    global varList

    keyword = str.upper(args[0])

    expectedArgs = 0
    argType = []

    match keyword:
        # ---------- Memory and function calling, working with stack ----------
        case "DEFVAR" : # symb
            expectedArgs = 1
            if not variableAlreadyExists(args[1]):
                varList.append(args[1])
                argType.append("var")
            else:
                dummy()
        case "PUSHS" : # symb 
            expectedArgs = 1
            if variableAlreadyExists(args[1]):
                argType.append("var")
            else:
                # TODO: raise exception
                dummy() 
        case "POPS" : # var
            expectedArgs = 1

            if not stackPop():
                # TODO: raise expection, stack underflow
                dummy()

        case "POPFRAME" | "PUSHFRAME" | "CREATEFRAME" | "RETURN" : # none
            expectedArgs = 0
        case "CALL" : # label
            expectedArgs = 1

            if labelAlreadyExists(args[1]):
                argType.append("label")
            else:
                # TODO: error
                dummy()

        # ---------- Arithmetic operations ----------
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" | 
              "LT" |"GT" | "EQ" | "AND" | "OR" | "NOT") : # var symb1 symb2
            expectedArgs = 3
            

        case "INT2CHAR" | "STRI2INT" : # var symb1 symb2
            expectedArgs = 3
        # ---------- Input / output operations ----------
        case "READ": # var type
            expectedArgs = 2
        case "WRITE": # symb
            expectedArgs = 1
        # ---------- Working with strings ----------
        case "CONCAT" | "GETCHAR" | "SETCHAR" : # var symb1 symb2
            expectedArgs = 3
        case "STRLEN" : # var symb
            expectedArgs = 2
        # ---------- Working with types ----------
        case "TYPE": # var symb
            expectedArgs = 2
        # ---------- Program flow control ----------
        case "LABEL" : # symb
            expectedArgs = 1
            argType.append("label")
            labelList.append(args[1]) # add label to label list
        case "JUMP" : # label
            expectedArgs = 1
            numOfArgs = 1
            argType.append("label")
        case "JUMPIFEQ" | "JUMPIFNEQ" : # label symb1 symb2
            expectedArgs = 3
        case "EXIT" : # symb
            expectedArgs = 1
        # ---------- Debugging instructions ----------
        case "DPRINT" : # symb
            expectedArgs = 1
        case "BREAK" : # none
            expectedArgs = 0
        # ---------- Other ----------
        case "#" : # none
            expectedArgs = -1
        case _ :
            #TODO: error unknown symbol
            print("Error, no matching keyword for:", args[0])
    # -------- END OF SWITCH --------

    # check if correct number of arguments were provided
    result = checkArgsCount(expectedArgs, args, lineCount)
    # write new instruction
    writeInstruction(keyword)
    # fill all arguments
    i = 0
    while i < expectedArgs:
        writeArg(argType[i], args[i+1])
        i += 1
    # check for comments
    checkForComments(args)
    # write end of instruction
    writeEndInstruction()

#----------------------------------------------------------

def main():
    # test first line
    line = input()

    if line != ".ippCode24":
        print("Invalid first line")
        SystemExit(1)

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
            line = line.replace("#", "# ")
            # split line into arguments
            args = line.split(" ")
            
            fsm(args, lineCount)
            lineCount += 1

        # if eof exception is found break from loop
        except EOFError:
            break

    #end header for xml
    file.append("</program>")

    print("-----------------------------\nPriting XML representation\n-----------------------------")
    for line in file:
        print(line)

    # filter out characters
    i = 0
    while i < len(file):
        file[i] = file[i].replace("&", "&amp")
        file[i] = file[i].replace("<", "&lt")
        file[i] = file[i].replace(">", "&gt")
        i += 1

#----------------------------------------------------------

main()