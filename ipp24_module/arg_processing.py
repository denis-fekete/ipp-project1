from ipp24_module.utilities import ErrorHandling, ACCEPTED_UNICODE

#------------------------------------------------------------------------------
def checkArgsCount(expected, args, lineCount, keyword):
    """ Check if "args" contains "expected" number of items, if not end program"""
    # -1 is for KEYWORD that is in args: KEYWORD ARG1 ARG2 etc...
    if expected < len(args):
        ErrorHandling(23, "Too many arguments given for operation code (or keyword): " + keyword, lineCount)
    if expected > len(args):
        ErrorHandling(23, "Not enough arguments given for operation code (or keyword): " + keyword, lineCount)

#------------------------------------------------------------------------------

def validSymbolsForName(word : str):
    """Returns True if name/word is valid"""
    for i in range(len(word)):
        # if not valid, return false
        if not validSymbol(word[i]):
            return False

    return True

#------------------------------------------------------------------------------

def validSymbol(char : str):
    """Returns if character is valid for a name"""
    if char.isnumeric():
        return True
    elif ((char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z') or
        char == '_' or char == '-' or char == '$' or char == '&' or 
        char == '%' or char == '*' or char == '!' or char == '?'):
        return True
    else:
        return False

#------------------------------------------------------------------------------

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
        
#------------------------------------------------------------------------------

def filterDangerousChars(inputString : str):
    """Filters out dangerous (not allowed) characters and returns corrected string"""
    string = inputString.replace("&", "&amp;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")

    return string

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