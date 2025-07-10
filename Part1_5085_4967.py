#DIMITRIOS GOGOS, 5085
#GEORGIOS THEODOROPOULOS, 4967

import sys

# Function to read the content from a .cpy file from cmd with command python Part1_5085_4967.py test.cpy
def read_cpy_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

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
            match('ALPHABET')
            while index < len(code_tokens) and code_tokens[index][1] == ',':
                match('DELIMITER', ',')
                match('ALPHABET')

    def global_variables2():
        while index < len(code_tokens) and code_tokens[index][1] == 'global':
            match('RESERVED_WORD', 'global')
            match('ALPHABET')

    def block():
        while index < len(code_tokens) and code_tokens[index][1] != '#}':
            declarations()
            global_variables2()
            statement()
            

    def functions():
        while index < len(code_tokens) and code_tokens[index][1] == 'def':
            match('RESERVED_WORD', 'def')
            match('ALPHABET')
            formal_pars()
            match('DELIMITER', ':')
            match('GROUPING_SYMBOL', '#{')
            block()
            match('GROUPING_SYMBOL', '#}')# End of block
            

    def formal_pars():
        match('GROUPING_SYMBOL', '(')
        if index < len(code_tokens) and code_tokens[index][1] != ')':
            while True:
                match('ALPHABET')  # Accept alphabets
                if index < len(code_tokens) and code_tokens[index][1] == ',':
                    match('DELIMITER', ',')
                    continue
                elif index < len(code_tokens) and code_tokens[index][1] == ')':
                    break
                elif index < len(code_tokens) and code_tokens[index][0] == 'DIGIT':
                    match('DIGIT')  # Accept digits
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


    def declarations():
        while index < len(code_tokens) and code_tokens[index][1] == '#int':
            match('RESERVED_WORD', '#int')
            match('ALPHABET')
            while index < len(code_tokens) and code_tokens[index][1] == ',':
                match('DELIMITER', ',')
                match('ALPHABET')

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
        expression()
        condition()
        
        match('DELIMITER', ':')
        statement()
        while index < len(code_tokens) and code_tokens[index][1] == 'elif':
            match('RESERVED_WORD', 'elif')
            expression()
            condition()
            
            match('DELIMITER', ':')
            statement()
        if index < len(code_tokens) and code_tokens[index][1] == 'else':
            match('RESERVED_WORD', 'else')
            match('DELIMITER', ':')
            statement()

    def while_statement():
        match('RESERVED_WORD', 'while')
        match('ALPHABET')
        condition()
        match('DELIMITER', ':')
        block()
        match('GROUPING_SYMBOL', '#}')  # End of block
        

    def return_statement():
        match('RESERVED_WORD', 'return')
        expression()

    def print_statement():
        match('RESERVED_WORD', 'print')
        expression()

    def assignment_statement():
        match('ALPHABET')
        match('ASSIGNMENT_OPERATOR', '=')
        expression()

    def expression():
        term()
        while index < len(code_tokens) and code_tokens[index][1] in ['+', '-']:
            match('ARITHMETIC_OPERATOR')
            term()

    def term():
        factor()
        while index < len(code_tokens) and code_tokens[index][1] in ['*', '//', '%']:
            match('ARITHMETIC_OPERATOR')
            factor()

    def bool_term():
        if index < len(code_tokens) and code_tokens[index][1] == 'not':
            match('RESERVED_WORD', 'not')
            condition()

    def relational_operator():
        if index < len(code_tokens) and code_tokens[index][1] in ['>', '<', '<=', '>=', '==', '!=']:
            match('RELATIONAL_OPERATOR')
            if index < len(code_tokens) and code_tokens[index][0] == 'ALPHABET':
                match('ALPHABET')
            else: 
                match('DIGIT')
        else:
            error("Relational operator expected")

    def condition():
        bool_term()
        relational_operator()
        while index < len(code_tokens) and code_tokens[index][1] in ['and', 'or']:
            match('RESERVED_WORD')
            match('ALPHABET')
            condition()


    def factor():
        if index < len(code_tokens) and code_tokens[index][0] == 'ALPHABET':
            match('ALPHABET')
        elif index < len(code_tokens) and code_tokens[index][0] == 'DIGIT':
            match('DIGIT')
        elif index < len(code_tokens) and code_tokens[index][1] == '(':
            match('GROUPING_SYMBOL', '(')
            expression()
            match('GROUPING_SYMBOL', ')')
        else:
            error("Invalid factor")
            statement()
    

    def main_function():
        match('RESERVED_WORD', '#def')
        match('RESERVED_WORD', 'main')
        global_variables1()
        statement()
        
        

    def error(msg):
        raise SyntaxError(msg)

    program()




# Main function
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
        except SyntaxError as e:
            print(f"SyntaxError: {str(e)}")
    else:
        print("Please specify the name of a .cpy file as a command-line parameter.")

if __name__ == "__main__":
    main()