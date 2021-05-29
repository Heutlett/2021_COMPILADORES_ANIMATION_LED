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
              | list

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
    params  : primitive
            | expression
            | params COMA params
            | empty
    """
    if len(p) == 2:  # Si es solo un parametro
        if type(p[1]) == list:
            if not list_check_type_aux(p.lineno(1), p[1]):
                return
        p[0] = [p[1]]
    else:  # Si son más de dos parametros
        p[0] = p[1] + p[3]


# Expresion para asignacion de variables.
def p_var_assign(p):
    """
    var_assign : ID IGUAL expression
               | ID IGUAL primitive
    """
    # one variable, can only be int, bool or list.

    # ERROR verification (assignment, reassignment)
    if not var_assign_verification_aux(p[1], p[2], p.lineno(1)):
        return

    # If it is a list that does not meet the requirements, the recursion will end up in a string.
    if equalsType(p[2], list) and not list_assign_verification(p.lineno(1), p[2][0], p[1][2][0]):
        return

    # Build our tree
    # Examples:
    # ('=', ('a', 1))
    p[0] = (p[2], (p[1], p[3]))
    print(p[0])


# Expresion para asignar varias variables.
def p_vars_assign(p):
    """
    var_assign : ids IGUAL params
    """
    # If the ID if a list o ids
    # ERROR verification (multiple params)
    if not vars_assign_verification_aux(p[1], p[3], p.lineno(1)):
        return
    # Build our tree
    # Examples
    # ('=', [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])
    p[0] = ('=', vars_assign_tree_aux(p[1], p[3]))


# Expresion para asignar una sublista.
def p_sublist_assign(p):
    """
    var_assign : sublist IGUAL params
    """
    # If the ID if a sublist.
    # If it is a list that does not meet the requirements, the recursion will end up in a string.
    if not list_assign_verification(p.lineno(1), p[3][0], p[1][2][0], p[1][2][1]):
        return

    # Build our tree
    # Examples:
    # Test:  a[0:4]=[1,2,3,4]
    # ( '=' , (('[]', 'a', [0, 4]) , [1, 2, 3, 4]))
    newtuple = ('[]*', p[1][1], p[1][2])
    p[0] = ("=", (newtuple, p[3][0]))
    # NOTA: run() is called in p_operation


# Funcion auxiliar para verificar una reasignacion de la variable.
def var_assign_verification_aux(ID, param, line):
    # If it cannot be declared.
    if not isDefined(ID, line):
        text = "ERROR in line {1}! \"{0}\" is not yet defined.".format(var, line)
        errors.append(text)
        return False

    # If type is already defined.
    elif type(env.get(ID)) != type(param):
        tipo = type(env.get(ID))
        text = "TypeError in line {2}! \"{0}\" type is already {1}.".format(ID, tipo, line)
        errors.append(text)
        return False

    else:
        return True


# Funcion auxiliar para validar los ids y parametros recibidos si son varios ids.
def vars_assign_verification_aux(ids, params, line):
    # Number of params must match the numbers of ids.
    if len(ids) != len(params):
        text = "LenError in line {0}! The number of values does not match the number of IDs.".format(line)
        errors.append(text)
        return False

    # IDs must be unique.
    # All elements type must be the same.
    tipo = type(params[0])
    for ID in ids:

        if ID in env.keys():
            text = "TypeError in line {2}! \"{0}\" is already defined as {1}.".format(ID, env.get(ID), line)
            errors.append(text)
            return False
        if type(ID) != tipo:
            text = "TypeError in line {0}! All values type must be the same.".format(line)
            errors.append(text)
            return False
    return True


# Funcion auxiliar
def vars_assign_tree_aux(ids, params):
    # Build list
    tList = []
    for i in range(len(ids)):
        t = (ids[i], params[i])
        tList.append(t)
    return tList


# Expresion para consultar el tipo de una variable.
def p_var_type(p):
    """
        statement : TYPE PARENTESISIZQ ID PARENTESISDER
    """
    if isDefined(p[3], p.lineno(1)):
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
# listed: enlistado (BOOL,INT,LIST,STRING,...)
def p_list_assign(p):
    '''
    list  : CORCHETEIZQ params CORCHETEDER
    '''
    if p[2][0] is None:
        p[0] = []
    else:
        if equalsType(p[2], list):
            if not list_check_type_aux(p.lineno(1), p[2]):
                return
        p[0] = p[2]


# Expresion para mostrar una lista  o sublista.
def p_callable(p):
    '''
    statement  : sublist
    '''
    p[0] = p[1]
    print(run(p[0]))


# Expresion para obtener una sublista de una lista.
def p_sublist(p):
    '''
    sublist  : ID index
    '''
    # If its not defined
    if not isDefined(p[1], p.lineno(1)):
        return
    # If wrong index range.
    if not list_check_index_range_aux(p.lineno(1), env.get(p[1]), p[2][0], p[2][1]):
        return

    p[0] = ('[]', p[1], p[2])


# Expresion para obtener limite inicial y final de los indices dentro de corchetes.
def p_statemente_dospuntos(p):
    """ index  : CORCHETEIZQ expression CORCHETEDER
               | CORCHETEIZQ expression DOSPUNTOS expression CORCHETEDER
    """
    if len(p) == 4:
        lst = [p[2]] + [None]
    else:
        lst = [p[2]] + [p[4]]
    p[0] = lst


# Expresion para crear lista con range.
def p_statement_list_range(p):
    """
    var_assign : ID IGUAL LIST PARENTESISIZQ RANGE PARENTESISIZQ expression COMA params PARENTESISDER PARENTESISDER
    """
    tmp = []
    for i in range(p[7]):
        tmp.append(p[9][0])

    # Build tree
    # Example
    # ('=', ('a', [1,3,4]))
    p[0] = ('=', (p[1], tmp))


# Expresion para crear lista con range.
def p_statement_list_insert(p):
    """
    statement : ID PUNTO INSERT PARENTESISIZQ expression COMA params PARENTESISDER
    """
    # Build tree
    # Example
    # ('=', ('a', [1,3,4]))
    p[0] = ("INSERT", p[1], p[5], p[7][0])
    print(run(p[0]))


# Funcion general para validar todas las entradas en una lista.
def list_assign_verification(line, lst, index1=None, index2=None):
    if not (list_check_type_aux(line, lst) or list_check_index_range_aux(line, lst, index1) or
            list_check_param_range_concordance_aux(line, lst, index1, index2)):
        return False
    return True


# Función auxiliar para validar que todos los elementos de una lista corresponden al mismo tipo.
def list_check_type_aux(line, lst):
    if not lst:
        return True
    else:
        tipo = type(lst[0])
        for i in lst:
            if not equalsType(i, tipo):
                text = "TypeError in line {1}: \"{0}\" type does not match the type of elements.".format(i, line)
                errors.append(text)
                return False
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
        return False


def equalsType(var, tipo):
    if type(var) == tipo:
        return True
    return False


# Verifica si ID existe en el diccionario.
def isDefined(var, line):
    # Si el valor no es un str.
    if not equalsType(var, str):
        text = "TypeError in line {1}! \"{0}\" needs to be string type.".format(var, line)
        errors.append(text)
        return text
    # Si no existe el ID dentro del diccionario, return false.
    if env.get(var) is None:
        return False
    return True


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


def p_expression_int(p):
    '''
    expression : INT
    '''
    p[0] = p[1]


# Expresiones para expresion negativa.
def p_expression_uminus(p):
    'expression : RESTA expression %prec UMENOS'
    p[0] = -p[2]


# Output to the user that there is an error in the input as it doesn't conform to our grammar.
# p_error is another special Ply function.
def p_error(p):
    print("✘ Syntax error found!", p.type)


# Expresion vacia
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


# Build the parser
parser = yacc.yacc()
# Create the environment upon which we will store and retrieve variables from.
env = {"a": [100, 220, 335, 435, 595], "b": [True, False, False, True, False]}
# Create the dictionary in which we will store and retrieve all errors we get.
errors = []

arithmetic_operators = ['+', '-', '*', '/', '//', '%', '^']


# The run function is our recursive function that 'walks' the tree generated by our parser.
def run(p):
    global env
    global arithmetic_operators
    # print(p)
    if equalsType(p, tuple):

        if p[0] in arithmetic_operators:  # OPERACIONES ARITMETICAS
            return arithmetic_operation(p[0], p[1], p[2])

        elif p[0] == '=':
            var_assign_operation(p[1])
            return ''

        elif p[0] == 'var':  # DEFINIR UNA VARIABLE
            return env[p[1]]

        elif p[0] == 'type':
            return p[1]

        elif p[0] == '[]':
            return list_callable_operation(p[1], p[2])

        elif p[0] == '[]*':
            return list_callable_operation(p[1], p[2], False)

        elif p[0] == 'INSERT':
            return list_insert_operation(p[1], p[2], p[3])

    else:
        return p


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


# Funcion auxiliar para operar la asignacion de las variables.
def var_assign_operation(struct):
    # ('=', (a, 1)) : un elemento, struct = tuple
    # ('=', [(a, 1), (b,2)]) : dos elementos, struct = list
    if type(struct) == tuple:
        assign_operation_aux(run(struct[0]), run(struct[1]))
    else:
        for t in struct:
            var_assign_operation(t)


# Auxiliar para verificar la asignacion de las variables.
def assign_operation_aux(var, value):
    # If variable is a primitive but not a list.
    if not equalsType(var, list):
        env[var] = run(value)
        print(var, ":", env[var])

    # If its an assigment to a sublist.
    else:
        ID = var[0]
        i, j = var[1][0], var[1][1]
        if j is not None:
            env.get(ID)[i:j] = value
        else:
            env.get(ID)[i] = value
        print(ID, ":", env[ID])


def list_callable_operation(ID, indexes, result=True):
    if result:
        if indexes[1] is not None:
            return env.get(ID)[run(indexes[0]):run(indexes[1])]
        return env.get(ID)[run(indexes[0])]
    else:
        return [ID, indexes]


def list_insert_operation(ID, amount, value):
    var = env.get(ID)
   # if not equalsType(var, list):
   #     return
  #  elif equalsType(var, list):
    #    list_check_type_aux()

    var.insert(amount, value)
    return run(("var", ID))

# Create a REPL to provide a way to interface with our calculator.
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)
