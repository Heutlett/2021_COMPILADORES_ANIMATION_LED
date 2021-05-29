# Importa el módulo yacc para el compilador
import ply.yacc as yacc
import sys
from lexer.lexer import tokens

# Ensure our parser understands the correct order of operations.
# The precedence variable is a special Ply variable.
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'DIVISIONENTERA'),
    ('right', 'UMENOS'),
    ('right', 'MODULO'),
    ('right', 'EXPONENTE')
)

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%################# GRAMMAR RULES %%%%%%%%%%%%%%%%%%%%%%%%%%%%################# '''


# Expresion que define una recursion entre expresiones.
def p_statements(p):
    """ statements : statements statement
                   | statement
                   | primitive
                   | empty
                   | print
    """
    # NOTA: p[0] corresponde al valor que toma la variable.
    # El conteo de indices para los datos empieza en 1.
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Define our grammar. We allow expressions, var_assign's and lists.
def p_operation(p):
    '''
    statement : expression
              | var_assign
    '''
    print(run(p[1]))


# Expresiones para variables primitivas.
def p_primitive_var(p):
    '''
    primitive : BOOLEAN
              | INT
              | STRING
              | listed

    '''
    p[0] = p[1]


# Expresion para imprimir las variables presentes.
def p_printVariables(p):
    """
    print : PUNTO
    """
    global env
    global errors
    print(" ▶ variables: ", env)
    print(" ▶ errors: ", errors)


# Expresion para cuando entra un id igual.
def p_equals(p):
    '''
    equals : ID IGUAL
    '''
    # Build our tree
    p[0] = ['=', p[1]]


# Expresion para definir multiples ID o uno solo.
def p_ids(p):
    '''
    ids : ID
        | ids COMA ids
    '''
    if len(p) == 2:  # Si es solo un id
        p[0] = [p[1]]
    else:  # Para más de un id
        p[0] = p[1] + p[3]


# Expresion para obtener parametros.
def p_params(p):
    """
    params  : expression
            | primitive
            | params COMA params
            | empty
    """
    if len(p) == 2:  # Si es solo un parametro
        p[0] = [p[1]]
    else:  # Si son más de dos parametros
        p[0] = p[1] + p[3]


# Expresion para asignacion de variables.
def p_var_assign(p):
    '''
    var_assign : equals expression
               | equals primitive
               | ids IGUAL params
    '''
    # ('=', ('a', 1))
    # ('=', [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])

    if len(p) == 3:  # one variable
        sign = p[1][0]
        id = p[1][1]

        validate = var_assign_verification_aux(id, p[2], p.lineno(1))
        if type(validate) == str:
            p[0] = validate
            return

        # Si es una lista y no cumple con los requisitos, por recursion se obtiene el error en string:
        if type(p[2]) == str:
            p[0] = p[2]
            return

        # Build our tree
        p[0] = (sign, (id, p[2]))

    else:  # more than one variable

        # ERROR verification
        validate = vars_assign_verification_aux(p[1], p[3], p.lineno(1))
        if type(validate) == str:
            p[0] = validate
            return

        p[0] = ('=', vars_assign_tree_aux(p[1], p[3]))
    # NOTA: run() se llama en p_operation


# Funcion auxiliar para verificar una reasignacion de la variable.
def var_assign_verification_aux(id, param, line):
    if env.get(id) is None:
        return True
    elif type(param) == str:
        text = "TypeError in line {1}! \"{0}\" primitive type \"str\" does not exist.".format(id, line)
        errors.append(text)
        return text
    elif (type(env.get(id))) != type(param):
        text = "TypeError in line {2}! \"{0}\" is already {1}.".format(id, type(id), line)
        errors.append(text)
        return text
    else:
        return True


# Funcion auxiliar para validar los ids y parametros recibidos si son varios ids.
def vars_assign_verification_aux(ids, params, line):
    # Number of params must match the numbers of ids.
    if len(ids) != len(params):
        text = "LenError in line {0}! The number of values does not match the number of IDs.".format(line)
        errors.append(text)
        return text

    # IDs must be unique.
    # All elements type must be the same.
    tipo = type(params[0])
    for p in params:
        if p in env.keys():
            text = "ERROR in line {2}! \"{0}\" is already defined as {1}.".format(id, env.get(id), line)
            errors.append(text)
            return text
        if type(p) != tipo:
            text = "TypeError in line {0}! All values type must be the same.".format(line)
            errors.append(text)
            return text
    return True


# Funcion auxiliar
def vars_assign_tree_aux(ids, params):
    # Build list
    tlist = []
    for i in range(len(ids)):
        t = (ids[i], params[i])
        tlist.append(t)
    return tlist


# Expresion para consultar el tipo de una variable.
def p_var_type(p):
    """
        statement : TYPE PARENTESISIZQ ID PARENTESISDER
    """
    if isDefined(p[3]):
        var = env.get(p[3])
        if type(var) == bool:
            p[0] = ('type', bool)
        elif type(var) == int:
            p[0] = ('type', int)
        else:
            print("ERROR in type!")
        print(run(p[0]))


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  LIST  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


# Expresion para crear una lista, ya sea vacia o con parámetros.
def p_list_assign(p):
    '''
    listed  : CORCHETEIZQ params CORCHETEDER
    '''
    if p[2][0] is None:
        p[0] = []
    else:
        p[0] = list_assign_verification(p.lineno(1), p[2])






# Funcion general para validar todas las entradas en una lista.
def list_assign_verification(line, lst, index1=None, index2=None):
    validate = list_check_type_aux(line, lst)
    if type(validate) == str:
        return validate

    elif index1 is not None:

        validate = list_check_index_range_aux(line, lst, index1)
        if type(validate) == str:
            return validate

        validate = list_check_param_range_concordance_aux(line, lst, index1, index2)
        if type(validate) == str:
            return validate
    return lst


# Función auxiliar para validar que todos los elementos de una lista corresponden al mismo tipo.
def list_check_type_aux(line, lst):

    if not lst:
        return True
    else:
        tipo = type(lst[0])
        for i in lst:
            if type(i) != tipo:
                text = "TypeError in line {1}: \"{0}\" type does not match the type of elements.".format(i, line)
                errors.append(text)
                return text
    return True


# Funcion para verificar que un indice se encuentra dentro del rango indicado.
def list_check_index_range_aux(line, lst, i, j=None):
    if i >= len(lst):
        text = "LenError in line {1}: Index \"{0}\" out of range.".format(i, line)
        errors.append(text)
        return text
    elif (j is not None) and (j > len(lst)):
        text = "LenError in line {1}: Index \"{0}\" out of range.".format(j, line)
        errors.append(text)
        return text
    else:
        return True


# Funcion auxiliar para verificar la cantidad de parametros coincide con los indices.
def list_check_param_range_concordance_aux(line, params, i, j):
    if (j is None) and (len(params) == 1):
        return True
    elif len(params) == (j - i):
        return True
    else:
        text = "IndexError in line {0}: The number of parameters does not match that of the indexes.".format(line)
        errors.append(text)
        return text


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  ARITHMETIC OPERATIONS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


# Expressions are recursive.
def p_expression(p):
    '''
    expression : expression EXPONENTE expression
               | expression MODULO expression
               | expression MULTIPLICACION expression
               | expression DIVISIONENTERA expression
               | expression DIVISION expression
               | expression SUMA expression
               | expression RESTA expression
    '''
    # Build our tree.
    p[0] = (p[2], p[1], p[3])


# Expresiones entre paréntesis.
def p_expression_parentesis(p):
    'expression : PARENTESISIZQ expression PARENTESISDER'
    p[0] = p[2]


# Expresiones para variable.
def p_expression_var(p):
    '''
    expression : ID
    '''

    # Validation
    if p[1] not in env:
        text = "ERROR in line {1}! \"{0}\" is not yet defined.".format(p[1], p.lineno(1))
        errors.append(text)
        p[0] = text
    else:
        p[0] = ('var', p[1])


# Expresiones para expresion negativa.
def p_expression_uminus(p):
    'expression : RESTA expression %prec UMENOS'
    p[0] = -p[2]


# Output to the user that there is an error in the input as it doesn't conform to our grammar.
# p_error is another special Ply function.
def p_error(p):
    print("✘ Syntax error found!")


# Expresion vacia
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


# Build the parser
parser = yacc.yacc()
# Create the environment upon which we will store and retrieve variables from.
env = {}
# Create the dictionary in which we will store and retrieve all errors we get.
errors = []

arithmetic_operators = ['+', '-', '*', '/', '//', '%', '^']


# The run function is our recursive function that 'walks' the tree generated by our parser.
def run(p):
    global env
    global arithmetic_operators
    # print(p)
    if type(p) == tuple:

        if p[0] in arithmetic_operators:  # OPERACIONES ARITMETICAS
            return arithmetic_operation(p[0], p[1], p[2])

        elif p[0] == '=':
            var_assign_operation(p[1])
            return ''

        elif p[0] == 'var':  # DEFINIR UNA VARIABLE
            return env[p[1]]

        elif p[0] == 'type':
            return p[1]

    else:
        return p


# Funcion auxiliar para operar la asignacion de las variables.
def var_assign_operation(struct):
    # ('var', (a, 1)) : un elemento, struct = tuple
    # ('var', [(a, 1), (b,2)]) : dos elementos, struct = list
    if type(struct) == tuple:
        assign_operation_aux(run(struct[0]), run(struct[1]))
    else:
        for t in struct:
            var_assign_operation(t)


# Auxiliar para verificar la asignacion de las variables.
def assign_operation_aux(var, value):
    env[var] = run(value)  # Definir variable en el diccionario.
    print(var, ":", env[var])


# Funcion auxiliar para operar los calculos aritmeticos por aparte.
def arithmetic_operation(operator, a, b):
    if operator == '+':
        return run(a) + run(b)
    elif operator == '-':
        return run(a) - run(b)
    elif operator == '*':
        return run(a) * run(b)
    elif operator == '/':
        return run(a) / run(b)
    elif operator == '//':
        return run(a) // run(b)
    elif operator == '%':
        return run(a) % run(b)
    elif operator == '^':
        return pow(run(a), run(b))


# Verifica si ID existe en el diccionario.
def isDefined(var):
    # Si el valor es una instancia de ID.
    if type(var) != str:
        return False
    # Si no existe el ID dentro del diccionario, return false.
    if env.get(var) is None:
        errors.append("ERROR in line {1}! \"{0}\" is not yet defined.".format(var, var.lineno))
        return False
    return True


# Create a REPL to provide a way to interface with our calculator.
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)
