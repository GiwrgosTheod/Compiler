
#DIMITRIOS GOGOS, 5085
#GEORGIOS THEODOROPOULOS, 4967

import sys

def read_cpy_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Classes for Symbol Table 
class Entity:
    def __init__(self, name, entity_type, scope_level):
        self.name = name
        self.entity_type = entity_type
        self.scope_level = scope_level

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, type={self.entity_type}, scope_level={self.scope_level})"

class Variable(Entity):
    def __init__(self, name, datatype, offset, scope_level):
        super().__init__(name, 'Variable', scope_level)
        self.datatype = datatype
        self.offset = offset

    def __repr__(self):
        return f"Variable(name={self.name}, datatype={self.datatype}, offset={self.offset}, scope_level={self.scope_level})"

class FormalParameter(Entity):
    def __init__(self, name, datatype, mode, scope_level):
        super().__init__(name, 'FormalParameter', scope_level)
        self.datatype = datatype
        self.mode = mode

    def __repr__(self):
        return f"FormalParameter(name={self.name}, datatype={self.datatype}, mode={self.mode}, scope_level={self.scope_level})"

class Parameter(FormalParameter):
    def __init__(self, name, datatype, mode, offset, scope_level):
        super().__init__(name, datatype, mode, scope_level)
        self.offset = offset

    def __repr__(self):
        return f"Parameter(name={self.name}, datatype={self.datatype}, mode={self.mode}, offset={self.offset}, scope_level={self.scope_level})"

class Procedure(Entity):
    def __init__(self, name, starting_quad=None, frame_length=None, formal_parameters=None, scope_level=0):
        super().__init__(name, 'Procedure', scope_level)
        self.starting_quad = starting_quad
        self.frame_length = frame_length
        self.formal_parameters = formal_parameters if formal_parameters is not None else []

    def add_formal_parameter(self, parameter):
        self.formal_parameters.append(parameter)

    def __repr__(self):
        return (f"Procedure(name={self.name}, starting_quad={self.starting_quad}, frame_length={self.frame_length}, "
                f"formal_parameters={self.formal_parameters}, scope_level={self.scope_level})")

class Function(Procedure):
    def __init__(self, name, datatype, starting_quad=None, frame_length=None, formal_parameters=None, scope_level=0):
        super().__init__(name, starting_quad, frame_length, formal_parameters, scope_level)
        self.datatype = datatype

    def __repr__(self):
        return (f"Function(name={self.name}, datatype={self.datatype}, starting_quad={self.starting_quad}, "
                f"frame_length={self.frame_length}, formal_parameters={self.formal_parameters}, scope_level={self.scope_level})")

class TemporaryVariable(Variable):
    def __init__(self, name, datatype, offset, scope_level):
        super().__init__(name, datatype, offset, scope_level)

    def __repr__(self):
        return f"TemporaryVariable(name={self.name}, datatype={self.datatype}, offset={self.offset}, scope_level={self.scope_level})"

class SymbolicConstant(Entity):
    def __init__(self, name, datatype, value, scope_level):
        super().__init__(name, 'Constant', scope_level)
        self.datatype = datatype
        self.value = value

    def __repr__(self):
                return f"SymbolicConstant(name={self.name}, datatype={self.datatype}, value={self.value}, scope_level={self.scope_level})"

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Initial scope for the main program
        self.current_scope_level = 0

    def enter_scope(self):
        self.scopes.append({})
        self.current_scope_level += 1
        self.print_symbol_table_to_file("5085_4967.sym", "Entering scope level")

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.current_scope_level -= 1
            self.print_symbol_table_to_file("5085_4967.sym", "Exiting scope level")

    def add_symbol(self, symbol):
        if self.scopes:
            self.scopes[-1][symbol.name] = symbol

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def update_symbol(self, name, **kwargs):
        symbol = self.lookup(name)
        if symbol:
            for key, value in kwargs.items():
                if hasattr(symbol, key):
                    setattr(symbol, key, value)

    def print_symbol_table_to_file(self, filename, message=None):
        with open(filename, 'a') as file:
            if message:
                file.write(message + f" {self.current_scope_level}:\n")
            for level, scope in enumerate(self.scopes):
                file.write(f"Scope Level {level}:\n")
                for name, symbol in scope.items():
                    file.write(f"  {name}: {symbol}\n")
            file.write("\n")

    def __repr__(self):
        return f"SymbolTable(scopes={self.scopes})"

# Table with tokens
tokens = {
    'ALPHABET': set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"),
    'DIGITS': set("0123456789"),
    'ARITHMETIC_OPERATORS': set("+-*//%"),
    'RELATIONAL_OPERATORS': set("==<><=>=!="),
    'ASSIGNMENT_OPERATOR': set("="),
    'DELIMITERS': set(",:"),
    'GROUPING_SYMBOLS': set("()"),
    'COMMENTS': set("##"),
    'RESERVED_WORDS': set("main def #def #int global if elif else while print return input int and or not".split()),
}

# Lex

def Lex(code):
    # List to store the tokens of the code
    code_tokens = []

    # Resetting variables for lexical analysis
    current_token = ""
    in_comment = False

    # Index for while loop
    index = 0
    while index < len(code):
        char = code[index]

        if in_comment:
            if char == '\n':
                in_comment = False
            index += 1
            continue

        elif char.isspace():
            if current_token:
                if current_token in tokens['RESERVED_WORDS']:
                    code_tokens.append(('RESERVED_WORD', current_token))
                elif current_token.isdigit():
                    code_tokens.append(('DIGIT', current_token))
                else:
                    code_tokens.append(('ALPHABET', current_token))
                current_token = ""
            index += 1
            continue

        elif char in tokens['GROUPING_SYMBOLS']:
            if current_token:
                if current_token in tokens['RESERVED_WORDS']:
                    code_tokens.append(('RESERVED_WORD', current_token))
                elif current_token.isdigit():
                    code_tokens.append(('DIGIT', current_token))
                else:
                    code_tokens.append(('ALPHABET', current_token))
                current_token = ""
            code_tokens.append(('GROUPING_SYMBOL', char))

        elif char == '#':
            if index < len(code) - 1 and code[index + 1] == '#':
                # Handle ## as comment
                in_comment = True
                index += 2  # Move index ahead to skip the second '#' character
                continue

            elif index < len(code) - 3 and code[index + 1:index + 4] == 'def':
                if current_token:
                    if current_token in tokens['RESERVED_WORDS']:
                        code_tokens.append(('RESERVED_WORD', current_token))
                    elif current_token.isdigit():
                        code_tokens.append(('DIGIT', current_token))
                    else:
                        code_tokens.append(('ALPHABET', current_token))
                    current_token = ""
                code_tokens.append(('RESERVED_WORD', '#def'))
                index += 3  # Move index ahead to skip 'def'
                in_comment = False
            elif index < len(code) - 3 and code[index + 1:index + 4] == 'int':
                if current_token:
                    if current_token in tokens['RESERVED_WORDS']:
                        code_tokens.append(('RESERVED_WORD', current_token))
                    elif current_token.isdigit():
                        code_tokens.append(('DIGIT', current_token))
                    else:
                        code_tokens.append(('ALPHABET', current_token))
                    current_token = ""
                code_tokens.append(('RESERVED_WORD', '#int'))
                index += 3  # Move index ahead to skip 'int'
                in_comment = False
            elif index < len(code) - 1 and code[index + 1] == '{':
                if current_token:
                    if current_token in tokens['RESERVED_WORDS']:
                        code_tokens.append(('RESERVED_WORD', current_token))
                    elif current_token.isdigit():
                        code_tokens.append(('DIGIT', current_token))
                    else:
                        code_tokens.append(('ALPHABET', current_token))
                    current_token = ""
                code_tokens.append(('GROUPING_SYMBOL', '#{'))
                index += 1  # Move index ahead to skip the next '{' character
                in_comment = True
            elif index < len(code) - 1 and code[index + 1] == '}':
                if current_token:
                    if current_token in tokens['RESERVED_WORDS']:
                        code_tokens.append(('RESERVED_WORD', current_token))
                    elif current_token.isdigit():
                        code_tokens.append(('DIGIT', current_token))
                    else:
                        code_tokens.append(('ALPHABET', current_token))
                    current_token = ""
                code_tokens.append(('GROUPING_SYMBOL', '#}'))
                index += 1  # Move index ahead to skip the next '}' character
                in_comment = True
            else:
                code_tokens.append(('UNKNOWN', char))  # Treat '#' as unknown if not part of ##

        elif char in tokens['RELATIONAL_OPERATORS']:
            if index < len(code) - 1 and code[index + 1] in tokens['RELATIONAL_OPERATORS']:
                combined_relational_operator = char + code[index + 1]
                if current_token:
                    if current_token in tokens['RESERVED_WORDS']:
                        code_tokens.append(('RESERVED_WORD', current_token))
                    elif current_token.isdigit():
                        code_tokens.append(('DIGIT', current_token))
                    else:
                        code_tokens.append(('ALPHABET', current_token))
                    current_token = ""
                code_tokens.append(('RELATIONAL_OPERATOR', combined_relational_operator))
                index += 1  # Move index ahead to skip the next character
            elif char == '=':
                code_tokens.append(('ASSIGNMENT_OPERATOR', char))  # Treat '=' as assignment operator

            else:
                if current_token:
                    if current_token in tokens['RESERVED_WORDS']:
                        code_tokens.append(('RESERVED_WORD', current_token))
                    elif current_token.isdigit():
                        code_tokens.append(('DIGIT', current_token))
                    else:
                        code_tokens.append(('ALPHABET', current_token))
                    current_token = ""
                code_tokens.append(('RELATIONAL_OPERATOR', char))

        elif char in tokens['DELIMITERS']:
            if current_token:
                if current_token in tokens['RESERVED_WORDS']:
                    code_tokens.append(('RESERVED_WORD', current_token))
                elif current_token.isdigit():
                    code_tokens.append(('DIGIT', current_token))
                else:
                    code_tokens.append(('ALPHABET', current_token))
                current_token = ""
            code_tokens.append(('DELIMITER', char))

        elif char in tokens['ARITHMETIC_OPERATORS']:
            if current_token:
                if current_token in tokens['RESERVED_WORDS']:
                    code_tokens.append(('RESERVED_WORD', current_token))
                elif current_token.isdigit():
                    code_tokens.append(('DIGIT', current_token))
                else:
                    code_tokens.append(('ALPHABET', current_token))
                current_token = ""
            code_tokens.append(('ARITHMETIC_OPERATOR', char))

        else:
            current_token += char

        index += 1

    # Add the last token if it exists
    if current_token:
        if current_token in tokens['RESERVED_WORDS']:
            code_tokens.append(('RESERVED_WORD', current_token))
        elif current_token.isdigit():
            code_tokens.append(('DIGIT', current_token))
        else:
            code_tokens.append(('ALPHABET', current_token))

    return code_tokens

# Kλήση πίνακα και δημιουργία asm
symbol_table = SymbolTable()

def add_symbol_to_table(symbol):
    global symbol_table
    existing_symbol = symbol_table.lookup(symbol.name)
    if existing_symbol is None or existing_symbol.scope_level < symbol.scope_level:
        symbol_table.add_symbol(symbol)
    elif existing_symbol.scope_level == symbol.scope_level:
        raise ValueError(f"Symbol {symbol.name} already exists in scope level {symbol.scope_level}.")

def gnlvcode(v):
    # Αναζήτηση στον πίνακα συμβόλων για να βρεθεί η μεταβλητή v
    symbol = symbol_table.lookup(v)
    if symbol is None:
        raise ValueError(f"Symbol {v} not found in symbol table.")
    
    level_diff = symbol_table.current_scope_level - symbol.scope_level
    produce(f"lw t0, -4(sp)")  # Ανάγνωση του συνδέσμου προσπέλασης
    
    for _ in range(level_diff - 1):
        produce(f"lw t0, -4(t0)")
    
    produce(f"addi t0, t0, -{symbol.offset}")

def loadvr(v, reg):
    if v.isdigit():
        produce(f"li {reg}, {v}")
    else:
        symbol = symbol_table.lookup(v)
        if symbol is None:
            raise ValueError(f"Symbol {v} not found in symbol table.")
        
        if isinstance(symbol, SymbolicConstant):
            produce(f"li {reg}, {symbol.value}")
        elif symbol.scope_level == 0:
            produce(f"lw {reg}, -{symbol.offset}(gp)")
        elif symbol.scope_level == symbol_table.current_scope_level:
            produce(f"lw {reg}, -{symbol.offset}(sp)")
        else:
            gnlvcode(v)
            produce(f"lw {reg}, (t0)")

def storerv(reg, v):
    symbol = symbol_table.lookup(v)
    if symbol is None:
        raise ValueError(f"Symbol {v} not found in symbol table.")
    
    if symbol.scope_level == 0:
        produce(f"sw {reg}, -{symbol.offset}(gp)")
    elif symbol.scope_level == symbol_table.current_scope_level:
        produce(f"sw {reg}, -{symbol.offset}(sp)")
    else:
        gnlvcode(v)
        produce(f"sw {reg}, (t0)")

def translate_quad_to_riscv(quad):
    op, arg1, arg2, result = quad[1], quad[2], quad[3], quad[4]
    try:
        if op == '=':
            loadvr(arg1, 't0')
            storerv('t0', result)
        elif op in ['+', '-', '*', '/']:
            loadvr(arg1, 't0')
            loadvr(arg2, 't1')
            if op == '+':
                produce(f'add t2, t0, t1')
            elif op == '-':
                produce(f'sub t2, t0, t1')
            elif op == '*':
                produce(f'mul t2, t0, t1')
            elif op == '/':
                produce(f'div t2, t0, t1')
            storerv('t2', result)
        elif op == 'jump':
            produce(f'j L{result}')
        elif op in ['<', '>', '<=', '>=', '==', '!=']:
            loadvr(arg1, 't0')
            loadvr(arg2, 't1')
            if op == '<':
                produce(f'blt t0, t1, L{result}')
            elif op == '>':
                produce(f'bgt t0, t1, L{result}')
            elif op == '<=':
                produce(f'ble t0, t1, L{result}')
            elif op == '>=':
                produce(f'bge t0, t1, L{result}')
            elif op == '==':
                produce(f'beq t0, t1, L{result}')
            elif op == '!=':
                produce(f'bne t0, t1, L{result}')
        elif op == 'begin_block':
            produce(f'L{result}:')
        elif op == 'end_block':
            produce(f'j end')
        elif op == 'halt':
            produce('li a7, 93')
            produce('ecall')
    except KeyError as e:
        print(f"Error translating quad {quad}: {e}")

def produce(instruction):
    with open('5085_4967.asm', 'a') as file:
        file.write(instruction + '\n')

# Συναρτήσεις για τον ενδιάμεσο κώδικα
quad_list = []
temp_counter = 0

def genQuad(operator, operand1, operand2, operand3):
    global quad_list
    quad_number = len(quad_list) + 1
    quad_list.append((quad_number, operator, operand1, operand2, operand3))
    return quad_number

def nextQuad():
    return len(quad_list) + 1

def newTemp():
    global temp_counter
    temp_counter += 1
    temp_name = f'T_{temp_counter}'
    temp_var = TemporaryVariable(temp_name, 'int', None, symbol_table.current_scope_level)
    add_symbol_to_table(temp_var)
    return temp_name

def emptyList():
    return []

def makeList(label):
    return [label]

def mergeList(list1, list2):
    return list1 + list2

def backpatch(list, label):
    global quad_list
    for i in list:
        quad = quad_list[i-1]
        quad_list[i-1] = (quad[0], quad[1], quad[2], quad[3], label)

def printQuads():
    global quad_list
    with open('5085_4967.int', 'w') as f:
        for quad in quad_list:
            f.write(f'{quad[0]}: {quad[1]}, {quad[2]}, {quad[3]}, {quad[4]}\n')
    # Translate quadruples to RISC-V assembly
    for quad in quad_list:
        try:
            translate_quad_to_riscv(quad)
        except ValueError as e:
            print(f"Error translating quad {quad}: {e}")


# Yacc
def Yacc(code_tokens):
    global index
    index = 0

    def match(expected_type, expected_value=None):
        global index
        nonlocal code_tokens
        if index < len(code_tokens):
            token = code_tokens[index]
            if token[0] == expected_type and (expected_value is None or token[1] == expected_value):
                index += 1
            else:
                error(f"Expected token type '{expected_type}' with value '{expected_value}', but found '{token[0]}' with value '{token[1]}'")
        else:
            error("Unexpected end of input")

    def program():
        global_variables1()
        functions()
        main_function()

    def global_variables1():
        while index < len(code_tokens) and code_tokens[index][1] == '#int':
            match('RESERVED_WORD', '#int')
            var_name = code_tokens[index][1]
            match('ALPHABET')
            variable = Variable(var_name, 'int', None, symbol_table.current_scope_level)
            add_symbol_to_table(variable)
            while index < len(code_tokens) and code_tokens[index][1] == ',':
                match('DELIMITER', ',')
                var_name = code_tokens[index][1]
                match('ALPHABET')
                variable = Variable(var_name, 'int', None, symbol_table.current_scope_level)
                add_symbol_to_table(variable)

    def global_variables2():
        while index < len(code_tokens) and code_tokens[index][1] == 'global':
            match('RESERVED_WORD', 'global')
            var_name = code_tokens[index][1]
            match('ALPHABET')
            variable = Variable(var_name, 'int', None, symbol_table.current_scope_level)
            add_symbol_to_table(variable)

    def functions():
        while index < len(code_tokens) and code_tokens[index][1] == 'def':
            match('RESERVED_WORD', 'def')
            func_name = code_tokens[index][1]
            match('ALPHABET')
            params = formal_pars()
            match('DELIMITER', ':')
            proc = Procedure(func_name, scope_level=symbol_table.current_scope_level)
            add_symbol_to_table(proc)
            genQuad('begin_block', func_name, '_', '_')
            for param in params:
                genQuad('par', param.name, param.mode, '_')
                add_symbol_to_table(param)
            match('GROUPING_SYMBOL', '#{')
            symbol_table.enter_scope()
            block()
            match('GROUPING_SYMBOL', '#}')
            symbol_table.exit_scope()
            genQuad('end_block', func_name, '_', '_')

    def formal_pars():
        match('GROUPING_SYMBOL', '(')
        params = []
        if index < len(code_tokens) and code_tokens[index][1] != ')':
            while True:
                param_name = code_tokens[index][1]
                match('ALPHABET')
                param = Parameter(param_name, 'int', 'cv', None, symbol_table.current_scope_level)
                params.append(param)
                if index < len(code_tokens) and code_tokens[index][1] == ',':
                    match('DELIMITER', ',')
                    continue
                elif index < len(code_tokens) and code_tokens[index][1] == ')':
                    break
                elif index < len(code_tokens) and code_tokens[index][0] == 'DIGIT':
                    match('DIGIT')
                    if index < len(code_tokens) and code_tokens[index][1] == ',':
                        match('DELIMITER', ',')
                        continue
                    elif index < len(code_tokens) and code_tokens[index][1] == ')':
                        break
                    else:
                        error("Invalid token after digit in formal parameters")
                else:
                    error("Invalid token in formal parameters")
        match('GROUPING_SYMBOL', ')')
        return params

    def declarations():
        while index < len(code_tokens) and code_tokens[index][1] == '#int':
            match('RESERVED_WORD', '#int')
            var_name = code_tokens[index][1]
            match('ALPHABET')
            variable = Variable(var_name, 'int', None, symbol_table.current_scope_level)
            add_symbol_to_table(variable)
            while index < len(code_tokens) and code_tokens[index][1] == ',':
                match('DELIMITER', ',')
                var_name = code_tokens[index][1]
                match('ALPHABET')
                variable = Variable(var_name, 'int', None, symbol_table.current_scope_level)
                add_symbol_to_table(variable)

    def statement():
        if index < len(code_tokens) and code_tokens[index][1] == 'if':
            if_statement()
        elif index < len(code_tokens) and code_tokens[index][1] == 'while':
            while_statement()
        elif index < len(code_tokens) and code_tokens[index][1] == 'def':
            functions()
        elif index < len(code_tokens) and code_tokens[index][1] == 'return':
            return_statement()
        elif index < len(code_tokens) and code_tokens[index][1] == 'print':
            print_statement()
        elif index < len(code_tokens) and code_tokens[index][0] == 'ALPHABET':
            assignment_statement()
        else:
            error("Invalid statement")

    def if_statement():
        match('RESERVED_WORD', 'if')
        B()
        B_true = nextQuad()
        genQuad('jump', '_', '_', '_')
        B_false = nextQuad()
        match('DELIMITER', ':')
        statement()
        while index < len(code_tokens) and code_tokens[index][1] == 'elif':
            backpatch([B_false], nextQuad())
            match('RESERVED_WORD', 'elif')
            B()
            B_true = nextQuad()
            genQuad('jump', '_', '_', '_')
            B_false = nextQuad()
            match('DELIMITER', ':')
            statement()
        if index < len(code_tokens) and code_tokens[index][1] == 'else':
            backpatch([B_false], nextQuad())
            match('RESERVED_WORD', 'else')
            match('DELIMITER', ':')
            statement()
        backpatch([B_true], nextQuad())

    def while_statement():
        match('RESERVED_WORD', 'while')
        B_true = nextQuad()
        B()
        B_false = nextQuad()
        match('DELIMITER', ':')
        match('GROUPING_SYMBOL', '#{')
        symbol_table.enter_scope()
        block()
        match('GROUPING_SYMBOL', '#}')
        symbol_table.exit_scope()
        genQuad('jump', '_', '_', B_true)
        backpatch([B_false], nextQuad())

    def block():
        declarations()
        global_variables2()
        while index < len(code_tokens) and code_tokens[index][1] != '#}':
            statement()

    def return_statement():
        match('RESERVED_WORD', 'return')
        expression()
        genQuad('ret', expression.place, '_', '_')

    def print_statement():
        match('RESERVED_WORD', 'print')
        expression()
        genQuad('out', expression.place, '_', '_')

    def input_statement():
        match('RESERVED_WORD', 'int')
        match('GROUPING_SYMBOL', '(')
        match('RESERVED_WORD', 'input')
        match('GROUPING_SYMBOL', '(')
        var_name = code_tokens[index][1]
        match('GROUPING_SYMBOL', ')')
        match('GROUPING_SYMBOL', ')')
        genQuad('in', var_name, '_', '_')

    def assignment_statement():
        id = code_tokens[index][1]
        match('ALPHABET')
        match('ASSIGNMENT_OPERATOR', '=')
        if index < len(code_tokens) and code_tokens[index][1] == 'int':
            input_statement()
        else:
            expression()
            genQuad('=', expression.place, '_', id)

    def term():
        factor()
        term.place = factor.place
        while index < len(code_tokens) and code_tokens[index][1] in ['*', '/', '%']:
            op = code_tokens[index][1]
            match('ARITHMETIC_OPERATOR')
            factor()
            w = newTemp()
            genQuad(op, term.place, factor.place, w)
            term.place = w

    def factor():
        if index < len(code_tokens) and code_tokens[index][1] == '(':
            match('GROUPING_SYMBOL', '(')
            expression()
            match('GROUPING_SYMBOL', ')')
            factor.place = expression.place
        elif index < len(code_tokens) and code_tokens[index][0] == 'ALPHABET':
            factor.place = code_tokens[index][1]
            match('ALPHABET')
        elif index < len(code_tokens) and code_tokens[index][0] == 'DIGIT':
            factor.place = code_tokens[index][1]
            match('DIGIT')
        else:
            error("Invalid factor")

    def B():
        Q()
        B.true = Q.true
        B.false = Q.false
        while index < len(code_tokens) and code_tokens[index][1] == 'or':
            backpatch(B.false, nextQuad())
            match('RESERVED_WORD', 'or')
            Q()
            B.true = mergeList(B.true, Q.true)
            B.false = Q.false

    def Q():
        R()
        Q.true = R.true
        Q.false = R.false
        while index < len(code_tokens) and code_tokens[index][1] == 'and':
            backpatch(Q.true, nextQuad())
            match('RESERVED_WORD', 'and')
            R()
            Q.false = mergeList(Q.false, R.false)
            Q.true = R.true

    def R():
        if index < len(code_tokens) and code_tokens[index][1] == '(':
            match('GROUPING_SYMBOL', '(')
            B()
            match('GROUPING_SYMBOL', ')')
            R.true = B.true
            R.false = B.false
        elif index < len(code_tokens) and code_tokens[index][0] == 'ALPHABET':
            E1()
            if index < len(code_tokens) and code_tokens[index][1] in ['>', '<', '<=', '>=', '==', '!=']:
                relop = code_tokens[index][1]
                match('RELATIONAL_OPERATOR', relop)
                E2()
                R.true = makeList(nextQuad())
                genQuad(relop, E1.place, E2.place, "_")
                R.false = makeList(nextQuad())
                genQuad("jump", "_", "_", "_")
            else:
                error("Relational operator expected")
        else:
            error("Invalid factor in R")

    def expression():
        term()
        expression.place = term.place
        while index < len(code_tokens) and code_tokens[index][1] in ['+', '-']:
            op = code_tokens[index][1]
            match('ARITHMETIC_OPERATOR', op)
            term()
            w = newTemp()
            genQuad(op, expression.place, term.place, w)
            expression.place = w

    def E1():
        expression()
        E1.place = expression.place

    def E2():
        expression()
        E2.place = expression.place

    def main_function():
        match('RESERVED_WORD', '#def')
        match('RESERVED_WORD', 'main')
        genQuad('begin_block', 'main', '_', '_')
        global_variables1()
        statement()
        genQuad('halt', '_', '_', '_')
        genQuad('end_block', 'main', '_', '_')

    def error(msg):
        raise SyntaxError(msg)

    program()

def main():
    # If there's a command-line parameter for the .cpy file name
    if len(sys.argv) > 1:
        # Store the file name from the command-line parameter
        cpy_file_path = sys.argv[1]

        # Read the content of the .cpy file
        code = read_cpy_file(cpy_file_path)

        # Parse the code using the syntax analyzer
        try:
            # Tokenizing the code
            code_tokens = Lex(code)

            # Printing the tokens
            for token_type, token_value in code_tokens:
                print(f'Type: {token_type}, Value: {token_value}')

            # Parsing the code using syntax analyzer
            Yacc(code_tokens)
            print("Parsing successful.")
            printQuads()  # Print the quadruples after parsing
        except SyntaxError as e:
            print(f"SyntaxError: {str(e)}")
    else:
        print("Please specify the name of a .cpy file as a command-line parameter.")

if __name__ == "__main__":
    main()
