import sys

f = open(sys.argv[1])
file = f.read()
f.close()
# [name, value]
variables = []
markers = ["_", "+"]


def _get_type(value):
    try:
        int(value)
        return "integer"
    except:
        pass
    if value.startswith("\"") and value.endswith("\""):
        return "string"
def _parse_arguments(args):
    string_started = False
    func_started = False
    final_args = []
    arg = ""
    var = ""
    func_name = ""
    func_a = ""
    func_args = False
    for char in args:
        if char == "\"":
            if not string_started:
                string_started = True
            else:
                string_started = False
                final_args.append(arg)
                arg = ""
        elif string_started:
            arg += char
        elif not string_started and not char == ",":
            var += char
        elif not string_started and char == "," and var != "":
            extra_var = _get_var(var.strip())
            try:
                final_args.append(extra_var[1])

            except: pass
            var = ""
        elif char == "+":
            func_started = True
        if func_started and not char == ":" and not func_args:
            func_name += char
        elif func_started and char ==":" and func_args:
            func_args = True
        elif func_started and func_args:
            if char == ";":
                _function_call(func_name.strip(), _parse_arguments(func_a))
            else: func_a += char
    return final_args

def _get_var(var_name):
    for i in variables:
        if i[0] == var_name:
            return i
    return None
def _function_call(function, args):
    if function == "print":
        print(args[0])
    elif function == "sum":
        total = 0
        for i in args:
            total += int(i)
        return total
    elif function == "sub":
        return int(args[0]) - int(args[1])
    else:
        f = open(function)
        func_file = f.read()
        f.close()
        interpret(func_file)
def _get_statement(f, it, it_pos):
    d_it = 0
    statement = ""
    for i in f.split("\n"):
        d_it_pos = 0
        for char in i:
            if d_it > it or it == d_it and d_it_pos > it_pos - 1:
                if char != ";":
                    statement += char
                else:
                    final_array = [statement[0]]
                    statement = statement[1:]
                    statement_array = statement.strip().split(":")
                    for sect in statement_array:
                        final_array.append(sect.strip())
                    return final_array
            d_it_pos += 1
        d_it += 1
    return None
def _handle_statement(statement):
    # Variables
    if statement[0] == "_":
        it = 0
        new_var = False

        if statement[2].split(" ")[0].strip() == "+":
            f_args = statement[3]
            for i in variables:
                if i[0] == statement[1]:
                    f_args = statement[3]
                    variables[it][1] = str(_function_call(statement[2].split(" ")[1], _parse_arguments(f_args)))
                    new_var = True
                it += 1
            if not new_var:
                variables.append([statement[1], str(_function_call(statement[2].split(" ")[1], _parse_arguments(f_args)))])

        else:
            for i in variables:
                if i[0] == statement[1]:
                    variables[it][1] = _parse_arguments(statement[2])[0]
                    new_var = True
                it += 1
            if not new_var:
                variables.append([statement[1], _parse_arguments(statement[2])[0]])
    # Function exec
    elif statement[0] == "+":
        function = statement[1]
        function_args = _parse_arguments(statement[2])
        _function_call(function, function_args)
def _handle_conditional(statement):
    operators = ["==", "!="]
    new_statement = ""
    for char in statement[0]:
        if char != " ":
            new_statement += char

    statement[0] = new_statement

    statement[1] = statement[1].split(" ")
    new_statement = []
    for i in statement[1]:
        if not i == "":
            if i in operators:
                new_statement.append(i)
            else:
                new_statement.append(_parse_arguments(i+","))
    statement[1] = new_statement

    # if statement
    if statement[0] == "*if" or statement[0] == "*while":
        if statement[1][1] == operators[0]:
            return [statement[0], statement[1][0] == statement[1][2]]
        elif statement[1][1] == operators[1]:
            return [statement[0], statement[1][0] != statement[1][2]]


def interpret(f):
    it = 0
    in_statement = False
    for line in f.split("\n"):
        it_pos = 0
        for char in line:
            if char in markers:
                if not in_statement:
                    in_statement = True
                    _handle_statement(_get_statement(f, it, it_pos))
            elif char == ";" or char == "}":
                in_statement = False
            elif char == "*":
                in_statement = True
                iterator = 0
                statement = ""
                for l in f.split("\n"):
                    iterator_char = 0
                    for c in l:
                        if iterator >= it:
                            if (iterator == it and it_pos <= iterator_char) or iterator > it:
                                statement += c

                        iterator_char += 1
                    iterator += 1
                statement = statement.split(":")
                final = [statement[0], statement[1].split("{")[0]]
                ite = 0
                for i in final:
                    final[ite].strip()
                    ite+=1

                condition = _handle_conditional(final)
                # it = line of statement
                if condition[1]:
                    in_func = []
                    started = False
                    i = 0
                    func = -1
                    for line in f.split("\n"):
                        if i >= it:
                            additional_line = ""
                            if "*" in line:
                                func += 1
                            elif "{" in line:
                                func -= 1
                            for char in line:
                                if func == 0 and (char == "{" or char == "}"):
                                    started = not started
                                elif started:
                                    additional_line += char
                            in_func.append(additional_line)

                        i+=1
                    func_string = ""
                    for i in in_func:
                        if i != "":
                            func_string += i + "\n"
                    if condition[0] == "*if":
                        interpret(func_string)
                    elif condition[0] == "*while":
                        while condition[1]:
                            interpret(func_string)
                            if not _handle_conditional([statement[0], statement[1].split("{")[0]])[1]:
                                break

            it_pos += 1
        it += 1


interpret(file)
# print(variables)
