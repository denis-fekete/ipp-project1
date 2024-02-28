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

def filterBlockedChars(inputString : str):
    """Filters out dangerous (not allowed) characters and returns corrected string"""
    string = inputString.replace("&", "&amp;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt;")

    return string