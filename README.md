**Implementační dokumentace k 1. úloze do IPP 2023/2024**<br>
**Jméno a příjmení: Denis Fekete**<br>
**Login: xfeket01**

### Quick Summary
IPP project 1 is an lexical code analyzer of IPPcode24 language. Script in 
python takes IPPcode24 code as an input and converts it into an XML file in 
correct format and controls lexical errors.

### 1. Handling of parameters
The Script takes either *one* or *zero* parameters. If the parameter is *--help* a help menu will be printed to to the standard output (from now on *stdout*). Any other combination of parameters will result in an unknown command menu printed to *stdout* and exiting with exit code *10*.
### 2. Checking head of file
Lines are stripped of unimportant characters, this process is repeated until a line that does contain header or operation code (comments, white spaces, tabulators and just a newline characters will be filtered out by the function *filterRawLine()*). The first found line is then transformed to uppercase and compared to constant a *.IPPCODE24*. If the first line is not matching the script ends with error code *21*. If another word/s was found on the line with the header script ends with error code *23* (comments excluded).
### 3. Processing input code and syntactic control
Lines of input code are processed by a function *filterRawLine()* that returns a list of arguments. The function *keywordProcessing()*. In function, a first argument is compared with constants (operation codes/keywords). If no match is found script exits with error code *22*. The number and type of argument/s are checked based on the first argument, if no error is found an argument object is created.

A new argument object is then checked for its type by the function *CheckIfValid()* with parameters arguments and expected data type. A private method *decideType()* is called and sets the type and the text of the argument object. If the expected value is the same value that was decided by the internal method *false* is returned, otherwise *true* is returned.

After the argument object/s are checked to be valid they are put in the list. Operation code (alias keyword) and list of arguments are then passed as parameters to the Instruction object, which is returned by the function *keywordProcessing()*. Instruction objects are then put into a list.
### 4. Outputing generated XML representation
After all lines have been processed a variable *program* (list of instructions) is printed to the *stdout* by Program method *PrintMe()*.`
