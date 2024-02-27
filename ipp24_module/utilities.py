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
    exit(code)

def PrintUnknownMenu():
    """Prints unknown command messange to the standard output"""

    text = """\
Unknown parameter, use --help or -h for help."""
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
    argv = input_argv[1:] 

    if len(argv) > 1:
        ErrorHandling(10, "Too many arguements, parse.py takes only one argument (--help or -h)", -1)
    elif len(argv) == 1:
        if ("--help" in argv) or ("-h" in argv):
            PrintHelpMenu()
        else:
            PrintUnknownMenu()

        exit(0) # exit script without problems