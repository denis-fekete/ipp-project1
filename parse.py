args = []

file = []

instOrder = 0
argNum = 0

#----------------------------------------------------------

def writeInstruction(opcode):
    global instOrder
    instOrder += 1

    string = "\t" + "<instruction order=\"" +  str(instOrder) + "\" opcode=\"" + opcode + "\">"
    file.append(string)

#----------------------------------------------------------
    
def writeEndInstruction():
    string = "\t" + "</instruction>"
    file.append(string)
    
    global argNum
    argNum = 0

#----------------------------------------------------------

def writeArg(argType, text):
    global argNum
    argNum += 1
    string = "\t\t" + "<arg" + str(argNum) + " type=\"" + argType + "\">" + text + "</arg" + str(argNum) + ">"
    file.append(string)

#----------------------------------------------------------

def checkArgsCount(expected, args, lineCount):
    argCount = len(args);
    if argCount < expected:
            #TODO: change to error print
            print("Syntax error on line", lineCount, "not enough arguments")
            print("Line:", args)

#----------------------------------------------------------

def checkForComments(args):
    dummy()

#----------------------------------------------------------

def fsm(args, lineCount):

    keyword = str.upper(args[0])

    expectedArgs = 0
    numOfArgs = 0
    argType = []

    match keyword:
        # Memory and function calling, working with stack
        case "DEFVAR" | "PUSHS" : # symb 
            dummy()
        case "POPS" : # var
            dummy()
        case "POPFRAME" | "PUSHFRAME" | "CREATEFRAME" | "RETURM" : # none
            dummy()
        case "CALL" : # label
            dummy()
        # Arithmetic operations
        case ("ADD" | "SUB" | "MUL" | "DIV" | "IDIV" | 
              "LT" |"GT" | "EQ" | "AND" | "OR" | "NOT") : # var symb1 symb2
            dummy()
        case "INT2CHAR" | "STRI2INT" : # var symb1 symb2
            dummy()
        # Input / output operations
        case "READ": # var type
            dummy()
        case "WRITE": # symb
            dummy()
        # Working with strings
        case "CONCAT" | "GETCHAR" | "SETCHAR" : # var symb1 symb2
            dummy()
        case "STRLEN" : # var symb
            dummy()
        # Working with types
        case "TYPE": # var symb
            dummy()
        # Program flow control
        case "LABEL" | "JUMP" : # label
            dummy()
        case "JUMPIFEQ" | "JUMPIFNEQ" : # label symb1 symb2
            dummy()
        case "EXIT" : # symb
            dummy()
        case "#" : # none
            dummy()
        case _ :
            #TODO: error unknown symbol
            print("Error, no matching keyword for:", args[0])
    # -------- END OF SWITCH --------

    # check if correct number of arguments were provided
    checkArgsCount(expectedArgs, args, lineCount)
    # write new instruction
    writeInstruction(keyword)
    # fill all arguments
    i = 1
    while i <= argNum:
        writeArg(argType[i], args[i])
        i += 1
    # check for comments
    checkForComments(args)
    # write end of instruction
    writeEndInstruction()


#----------------------------------------------------------

def dummy():
    1 == 1

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