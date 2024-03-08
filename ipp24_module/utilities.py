import sys

ACCEPTED_UNICODE = ["000", "001", "002", "003", "004", "005", "006", "007",
"008", "009", "010", "011", "012", "013", "014", "015", "016", "017", "018",
"019", "020", "021", "022", "023", "024", "025", "026", "027", "028", "029", 
"030", "031", "032", "035", "092"]

#------------------------------------------------------------------------------
def ErrorHandling(code, msg, lineCount):
    """Exits script with Error code "code" and prints "msg" to stderr.
    If "lineCount" is negative number don't on which line error occured
    """
    if lineCount >= 0:
        errorMsg = "Error: " + msg + " (On line: " + str(lineCount) + ")\n"
    else:
        errorMsg = "Error: " + msg + "\n"

    sys.stderr.write(errorMsg)
    sys.exit(code)

def PrintUnknownMenu():
    """Prints unknown command messange to the standard output"""

    text = """\
Unknown parameter/'s combination, use --help or -h for help."""
    print(text)

#------------------------------------------------------------------------------

def PrintHelpMenu():
    """Prints help menu to the standard output"""
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

#------------------------------------------------------------------------------

def parameterHandling(input_argv : list):
    # 0th argument is name of script, cut it out
    argv = input_argv[1:] 

    if len(argv) > 1:
            PrintUnknownMenu()
            sys.exit(10)
    elif len(argv) == 1:
        if ("--help" in argv) or ("-h" in argv):
            PrintHelpMenu()
        else:
            PrintUnknownMenu()
            sys.exit(10)

        sys.exit(0) # exit script without problems

#------------------------------------------------------------------------------

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