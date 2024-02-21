import xml.dom.minidom as md

doc = md.getDOMImplementation().createDocument(None, "hello_tag", None)

root = doc.documentElement()

print(doc.toprettyxml())

keyword = []

def dummy():
    1 == 1

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
    case "ADD" | "SUB" | "MUL" | "DIV" | "IDIV" | "LT" | "GT" | "EQ" | "AND" | "OR" | "NOT": # var symb1 symb2
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

# import xml.etree.ElementTree as ET
# from xml.dom import minidom
# import os

# if not os.path.isfile("file.xml"):
#     open("file.xml", "w").close()

# root = ET.Element("root")

# program = ET.SubElement(root, "program", language="IPPcode24")
# instructions = []
# instructions.append( ET.SubElement(program, "instruction", order="1", opcode="READ") )
# instructions.append( ET.SubElement(program, "instruction", order="2", opcode="WRITE") )
# instructions.append( ET.SubElement(program, "instruction", order="3", opcode="WRITE") )

# reparsed = minidom.parseString(ET.tostring(root, 'utf-8')) 



# reparsed.writexml("repased.xml")