**Implementační dokumentace k 1. úloze do IPP 2023/2024**<br>
**Jméno a příjmení: Denis Fekete**<br>
**Login: xfeket01**

### 1. Handling of parameters
The behavior of the script is based on the number of provided parameters:<br>
* if **2** or **more** parameters are provided script ends with error code *10* and the error message is printed to the standout error output (from now on *stderr*).<br>
* if exactly **1** parameter is provided and it is either *--help* or *-h* a help menu will be printed to the standard output (from now on *stdout*) and the script exits with error code *0*. If any other parameter is provided unknown parameter message will appear and the script will exit with error code *0*.<br>
* if *no* parameters were provided script will attempt to parse characters from standard input (from now on *stdin*) into an XML format while also making syntactic control.
### 2. Checking head of file
The input sequence of characters is being processed line by line by function *filterRawLine()*. Lines are stripped of unimportant characters, and this process is repeated until the first line that doesn't contain comments, blank characters (white spaces and tabulators) or just newline characters. The first found word is then transformed to uppercase and compared to *IPPCODE24*. If the first word is not valid the script ends with error code *21*. If another word was found on the line with the header script ends with error code *23*.
### 3. Processing input code and syntactic control
The process of generating representation in XML is the is similar to **2nd step** separating lines one by one into a list of words (without unimportant data like line spacing or comments). The first word is always compared (case insensitive) to the list of **keywords** or **operation codes**. If no match is found script ends with error code *23*. If the keyword matches, other arguments are checked for further syntactic control. Based on specific keywords arguments are checked for:
* number of arguments given
* type of argument (variable, literal or label)

For example, keyword *ADD* checks if there are exactly 3 arguments, of which 1st must be variable and the 2nd and 3rd must be symbols (variable or literal).

**Variables** and **Labels** are checked to contain only alphanumeric characters and special allowed characters as well as prefixes, also they mustn't start with numbers.
**Literals** are checked by their type, strings can contain any Unicode characters and escape sequences that are stored in a global constant variable. Storing escape character sequences in a variable allows further easier implementation of other characters accepted by the script.

Any errors such as an invalid variable name, or the incorrect number of arguments leads to exiting the script with error code *23*. If the error is detected appropriate argument type is stored in a list of arguments that is then added to the XML representation.

There is also an internal line counter to make error messages more informative for users. 
### 4. Outputing generated XML representation
The output of the script is being handled by the standard library function *print()* into a *stdout*. Correct numbering of instructions and arguments is being handled by internal counters. Output to *stdout* is being done at the end of the script, so in case of an error, no characters will be printed.

