import os

index = 0
noFiles = 0
equality = [">", "<", "="]
operators = ['+', '-', '*', '/']
statements = ['WHILE', 'ENDWHILE', 'FOR', 'NEXT', 'UNTIl', 'REPEAT', 'ELSE', 'REPEAT', 'IF', 'ENDIF', 'PRINT', 'INPUT']


def condition(statement):
    """
    :param statement: The statement to be evaluated
    :return: The evaluated statement
    """
    statement.replace('MOD', '%').replace('DIV', '//').replace('<>', '!=')
    statement.replace('OR', 'or').replace('AND', 'and').replace('NOT', 'not')

    x = len(statement)
    for ch in range(x):
        char = statement[ch]
        if char == "=":
            if statement[ch - 1] not in equality and statement[ch + 1] not in equality:
                statement = statement[:ch] + "=" + statement[ch:]

    return statement


def convertUpperLower(statement):
    temp = statement.lower()

    while 'ucase(' in temp:
        pos = temp.find('ucase(')
        closeBracket = temp[pos:].find(')') + pos

        statement = statement[:pos] + statement[pos + 6:closeBracket] + '.upper()' + statement[closeBracket + 1:]
        temp = statement.lower()

    while 'lcase(' in temp:
        pos = temp.find('lcase(')
        closeBracket = temp[pos:].find(')') + pos

        statement = statement[:pos] + statement[pos + 6:closeBracket] + '.lower()' + statement[closeBracket + 1:]
        temp = statement.lower()

    return statement


def subString(statement):
    """
    :param statement: String
    :return: The string with the substring function
    substring format: substring(string, start, end)
    """
    temp = statement.lower()

    while 'substring(' in temp:
        pos = temp.find('substring(')
        firstComma = temp[pos:].find(',') + pos
        secondComma = temp[firstComma + 1:].find(',') + firstComma + 1
        closeBracket = temp[pos:].find(')') + pos

        start = temp[firstComma + 1:secondComma].strip()
        end = temp[secondComma + 1:closeBracket].strip()

        statement = statement[:pos] + statement[pos + 10:firstComma] + '[' + start + ':' + end + ']' + statement[
                                                                                                       closeBracket + 1:]
        temp = statement.lower()

    return statement


def evaluation(statement):
    statement = statement.replace('MOD', '%').replace('DIV', '//').replace('OR', 'or').replace('AND', 'and').replace(
        'NOT', 'not')
    statement = statement.replace('INT', 'int')
    statement = statement.replace('LENGTH', 'len')
    statement = convertUpperLower(statement)
    statement = subString(statement)
    return statement


def evaluate(line, indentation=0):
    """
    :param line: The line to be evaluated
    :param indentation: The indentation of the line
    :return: The evaluated line
    """
    while '] [' in line:
        line = line.replace('] [', '][')
    if line.upper().find("USERINPUT") == -1:
        return " " * indentation + evaluation(line)
    else:
        var = line.split('=')[0].strip()
        return " " * indentation + var + " = " + "eval(input())"


def PRINT(line, indentation=0):
    line = line[5:].strip()
    output = " " * indentation + "print(" + line + ")"

    return output


def OUTPUT(line, indentation):
    line = line[6:].strip()
    output = " " * indentation + "print(" + line + ")"

    return output


def INPUT(line, indentation=0):
    lst = line.upper().strip().split()
    if "," not in lst:
        output = " " * indentation + line[line.find("INPUT") + 6:].strip() + " = " + "eval(input())"

    return output


def WHILE(line, indentation=0):
    global index
    index += 4
    line = line[5:]
    line_temp = line.upper()
    if line_temp.find("DO") != -1:
        line = line[:line_temp.find("DO")]
    output = " " * indentation + "while" + condition(line) + ":"
    return output


def ENDWHILE():
    global index
    index -= 4


def REPEAT(indentation):
    global index
    index += 4
    return " " * indentation + "while True:"


def UNTIL(line, indentation):
    global index
    index -= 4
    line = line[5:]
    output = " " * indentation + "if" + condition(line) + ":"
    br = " " * (indentation + 4) + "break"
    return [output, br]


def IF(line, indentation):
    global index
    ln = line.upper()
    if ln.find("THEN") != -1:
        line = line[:ln.find("THEN")]
    index += 4
    line = line[2:]
    output = " " * indentation + "if" + condition(line) + ":"
    return output


def FOR(line, indentation):
    global index
    index += 4
    line = line[3:].strip()
    variable = line[:line.find('=')].strip()
    line = line.upper()
    start = line[line.find('=') + 1:line.find('TO')].strip()
    end = line[line.find('TO') + 2:].strip()
    output = " " * indentation + "for " + variable + " in range(" + start + "," + end + "):"

    return output


def DECLARE():
    pass


def NEXT():
    global index
    index -= 4


def ENDIF():
    global index
    index -= 4


def ELSE(indentation):
    global index
    return " " * (indentation - 4) + "else:"


def initialize_lists_dict(lines):
    global index
    out = []
    lists = []
    for line in lines:
        l = line.strip()
        if l.find('[') != -1:
            bef_br = l[:l.find('[')].upper()

            flag = False
            for op in (statements + operators):
                if bef_br.find(op) != -1:
                    flag = True
            if flag:
                continue
            name = l[:l.find('[')]
            if name not in lists:
                lists.append(name)
                out.append(name + '={}')

    return out


def initialize_lists_list(lines):
    global index
    out = []
    lists = []
    for line in lines:
        l = line.strip()
        if l.find('[') != -1:
            bef_br = l[:l.find('[')].upper()

            flag = False
            for op in (statements + operators):
                if bef_br.find(op) != -1:
                    flag = True
            if flag:
                continue
            name = l[:l.find('[')]
            if name not in lists:
                if line.find("][") == -1 and line.find("] [") == -1:
                    lists.append(name)
                    out.append(name + '=[0 for i in range(1000)]')
                else:
                    lists.append(name)
                    out.append(name + '=[[0 for i in range(1000)] for f in range(1000)]')
    return out


def OPEN(line, indentation):
    # Format of OPEN statement: OPEN filename FOR Read/Write FOR filename
    global index
    index += 4
    temp = line.upper()
    readMode = 'w+' if temp.find('WRITE') != -1 else 'r'
    filename = line.strip().split()[1]

    output = "with open(" + filename + ",'" + readMode + f"') as {filename}:"

    return output


def WRITEFILE(line, indentation):
    # Format: WRITEFILE filename, <variable>
    output = " " * indentation + "f.write(" + line[line.find(',') + 1:].strip() + ")"

    return output


def READFILE(line, indentation):
    # Format: READFILE filename, <variable>
    filename = line.strip().split()[1].replace(',', '')
    output = " " * indentation + line[line.find(',') + 1:].strip() + f" = {filename}.readline()"

    return output


def CLOSEFILE():
    # Format: CLOSEFILE filename
    global index
    index -= 4


def FUNCTION(line, indentation):
    global index
    index += 4
    line = line[9:]
    c = line.count(':')
    for _ in range(c-1):
        line = line[:line.find(':')] + line[line.find(','):]
    line = line[:line.find(':')] + line[line.find(')'):line.find(')')+1]
    output = " " * indentation + "def " + line[:line.find(')')+1] + ":"
    return output

def ENDFUNCTION():
    global index
    index -= 4

def RETURN(line, indentation):
    output = " " * indentation + "return " + line[6:].strip()
    return output

def CALL(line, indentation):
    output = " " * indentation + line[4:].strip()
    return output

def PROCEDURE(line, indentation):  # Same as FUNCTION
    global index
    index += 4
    line = line[9:]
    c = line.count(':')
    for _ in range(c-1):
        line = line[:line.find(':')] + line[line.find(','):]
    line = line[:line.find(':')] + line[line.find(')'):line.find(')')+1]
    output = " " * indentation + "def " + line[:line.find(')')+1] + ":"
    return output

def ENDPROCEDURE():
    global index
    index -= 4


input_list = []
output_list = []


def Main(lines):
    global index, output_list
    output_list += initialize_lists_list(lines)
    for line in lines:
        if line[:5].upper() == "WHILE":
            output_list.append(WHILE(line, index))
        elif line[:6].upper() == "REPEAT":
            output_list.append(REPEAT(index))
        elif line[:2].upper() == "IF":
            output_list.append(IF(line, index))
        elif line[:5].upper() == "PRINT":
            output_list.append(PRINT(line, index))
        elif line[:5].upper() == "OUTPUT":
            output_list.append(OUTPUT(line, index))
        elif line[:5].upper() == "UNTIL":
            output_list.extend(UNTIL(line, index))
        elif line[:8].upper() == "ENDWHILE":
            ENDWHILE()
        elif line[:3].upper() == "FOR":
            output_list.append(FOR(line, index))
        elif line[:4].upper() == "NEXT":
            NEXT()
        elif line[:5].upper() == "ENDIF":
            ENDIF()
        elif line[:5].upper() == "ELSE":
            output_list.append(ELSE(index))
        elif line[:5].upper() == "INPUT":
            output_list.append(INPUT(line, index))
        elif line[:7].upper() == "DECLARE":
            DECLARE()
        elif line[:2].upper() == "//":
            continue
        elif line[:4].upper() == "OPEN":
            output_list.append(OPEN(line, index))
        elif line[:9].upper() == "WRITEFILE":
            output_list.append(WRITEFILE(line, index))
        elif line[:8].upper() == "READFILE":
            output_list.append(READFILE(line, index))
        elif line[:9].upper() == "CLOSEFILE":
            CLOSEFILE(index)
        elif line[:8].upper() == "FUNCTION":
            output_list.append(FUNCTION(line, index))
        elif line[:11].upper() == "ENDFUNCTION":
            ENDFUNCTION()
        elif line[:6].upper() == "RETURN":
            output_list.append(RETURN(line, index))
        elif line[:4].upper() == "CALL":
            output_list.append(CALL(line, index))
        elif line[:9].upper() == "PROCEDURE":
            output_list.append(PROCEDURE(line, index))
        elif line[:12].upper() == "ENDPROCEDURE":
            ENDPROCEDURE()
        else:
            if "=" in line:
                output_list.append(evaluate(line, index))


errors = {}


def add_error(error_name, line_no="NA"):
    global errors
    error_no = len(errors)
    meta = f"Error #{str(error_no)} on line #{str(line_no)}:"
    errors[meta] = error_name


def detect_errors(lines):
    variables = []

    for l in range(len(lines)):
        line = lines[l]
        line = line.upper()
        if line[-1] in operators:
            add_error("Missing Variable/Number", l)

        for ch in range(len(line)):
            if line[ch] == ',':
                try:
                    if line[ch - 1] != " ":
                        line = line[:ch] + " " + line[ch:]
                    if line[ch + 1] != " ":
                        line = line[:ch + 1] + " " + line[ch + 1:]
                except IndexError:
                    if ch == 0:
                        add_error("Comma in the beginning of line", ch)
                    else:
                        add_error("Comma in the end of line", ch)

    op_counts = {
        "WHILE": sum('WHILE' in s for s in lines),
        "FOR": sum('FOR' in s for s in lines),
        "REPEAT": sum('REPEAT' in s for s in lines),
        "IF": sum('IF' in s for s in lines),
    }
    Closers_counts = {
        "ENDWHILE": sum('ENDWHILE' in s for s in lines),
        "NEXT": sum('NEXT' in s for s in lines),
        "UNTIL": sum('UNTIL' in s for s in lines),
        "ENDIF": sum('ENDIF' in s for s in lines),
    }

    if op_counts['WHILE'] > Closers_counts["ENDWHILE"]:
        add_error("Unclosed WHILE Loop")
    if op_counts['REPEAT'] > Closers_counts["UNTIL"]:
        add_error("Unclosed REPEAT Loop")
    if op_counts['IF'] > Closers_counts["ENDIF"]:
        add_error("Unclosed IF statement")
    if op_counts['FOR'] > Closers_counts["NEXT"]:
        add_error("Unclosed FOR Loop")


path = os.path.dirname(__file__)
path.replace("\\", "/")
pseudocode = path + "/input.txt"
pythonCode = path + "/output.py"

Main(input_list)

with open(pseudocode, "r") as file:
    line_List = list(file)

for i in range(len(line_List)):
    line_List[i] = line_List[i].strip()

Main(line_List)
output_list.append("input(\"Press enter to exit \")")

with open(pythonCode, "w") as file:
    for item in output_list:
        file.write("%s\n" % item)

code_to_execute = compile("\n".join(output_list), "<string>", "exec")
exec(code_to_execute)
