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
    statement : expression PYC
              | callable PYC
              | var_assign
    '''
    print(run(p[1]))



# Expresiones para variables primitivas.
def p_primitive_var(p):
    '''
    primitive : BOOLEAN
              | INT
              | list
              | STRING
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
    params  : empty
            | expression
            | primitive
            | params COMA params
    """
    if len(p) == 2:  # Si es solo un parametro
        if type(p[1]) == list:
            if not matrix_check_type_validation(p.lineno(1), p[1]):
                return
        p[0] = [p[1]]
    else:  # Si son más de dos parametros
        p[0] = p[1] + p[3]


# Expresion para asignacion de variables.
def p_var_assign(p):
    """
    var_assign : ID IGUAL expression PYC
               | ID IGUAL primitive PYC
    """
    # one variable, can only be int, bool, string or list.
    if p[3] is None:
        return
    # ERROR verification (assignment, reassignment)
    if not var_assign_validation(p[1], p[3], p.lineno(1)):
        return

    # If it is a list that does not meet the requirements, the recursion will end up in a string.
    if equalsType(p[2], list) and not list_assign_validation(p.lineno(1), p[2][0], p[1][2][0]):
        return

    # Build our tree
    # Examples:
    # ('=', ('a', 1))
    p[0] = (p[2], (p[1], p[3]))


# Expresion para asignar varias variables.
def p_vars_assign(p):
    """
    var_assign : ids IGUAL params PYC
    """
    # If the ID if a list o ids
    # ERROR verification (multiple params)
    if not vars_assign_validation(p[1], p[3], p.lineno(1)):
        return
    # Build our tree
    # Examples
    # ('=', [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])
    p[0] = ('=', vars_assign_tree_aux(p[1], p[3]))


# Expresion para asignar una sublista.
def p_sublist_assign(p):
    """
    var_assign : sublist IGUAL params PYC
    """
    # If the ID if a sublist.
    # If it is a list that does not meet the requirements, the recursion will end up in a string.
    if not list_assign_validation(p.lineno(1), p[3][0], p[1][2][0], p[1][2][1]):
        return

    # Build our tree
    # Examples:
    # Test:  a[0:4]=[1,2,3,4]
    # ( '=' , (('[]', 'a', [0, 4]) , [1, 2, 3, 4]))
    newtuple = ('[]*', p[1][1], p[1][2])
    p[0] = ("=", (newtuple, p[3][0]))
    # NOTA: run() is called in p_operation


# Funcion auxiliar para verificar una reasignacion de la variable.
def var_assign_validation(ID, param, line):
    # CHECKING PARAM...

    comillas = '"'
    # If param its not a string.
    if equalsType(param, str) and not comillas in param:

        # If ID is a param and it not exist.
        if not isDefined(param, line):
            text = "ERROR in line {1}! \"{0}\" is not yet defined.".format(param, line)
            errors.append(text)
            return False
        return True

    # CHECK ID...

    # If type its already declared.
    if getValue(ID) is not None:
        if type(getValue(ID)) != type(param):
            tipo = var_type(getValue(ID))
            text = "TypeError in line {2}! \"{0}\" type is already {1}.".format(ID, tipo, line)
            errors.append(text)
            return False

    # Return true if its a new variable and
    # param is not and undeclared variable.
    return True


# Funcion auxiliar para validar los ids y parametros recibidos si son varios ids.
def vars_assign_validation(ids, params, line):
    # Number of params must match the numbers of ids.
    if len(ids) != len(params):
        text = "LenError in line {0}! The number of values does not match the number of IDs.".format(line)
        errors.append(text)
        return False

    # All params type must be the same.
    if not matrix_check_type_validation(line, params):
        text = "TypeError in line {0}! All values type must be the same.".format(line)
        errors.append(text)
        return False

    # IDs must be unique.
    for ID in ids:
        if ID in env.keys():
            text = "TypeError in line {2}! \"{0}\" is already defined as {1}.".format(ID, getValue(ID), line)
            errors.append(text)
            return False

    return True


# Funcion auxiliar para definicir varias variables.
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
        statement : TYPE PARENTESISIZQ ID PARENTESISDER PYC
    """
    if isDefined(p[3], p.lineno(1)):
        var = getValue(p[3])
        p[0] = var_type(var)
        print(run(p[0]))


# Funcion auxiliar para obtener el tipo de una variable en string.
def var_type(var):
    if equalsType(var, bool):
        return 'bool'
    elif equalsType(var, int):
        return 'int'
    elif equalsType(var, list):
        return 'list'
    elif equalsType(var, str):
        return 'str'
    else:
        print("ERROR in type!")


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
            if not matrix_check_type_validation(p.lineno(1), p[2]):
                return
        p[0] = p[2]


# Expresion para mostrar una lista  o sublista.
def p_callable(p):
    '''
    callable  : sublist
    '''
    p[0] = p[1]


# Expresion para obtener una sublista de una lista.
def p_sublist(p):
    '''
    sublist  : ID index
    '''
    if check_variable_and_index(p.lineno(1), p[1], p[2][0], p[2][1]):
        # Build tree
        # Example ('[]', a, 1)
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
    var_assign : ID IGUAL LIST PARENTESISIZQ RANGE PARENTESISIZQ expression COMA params PARENTESISDER PARENTESISDER PYC
    """
    tmp = []
    for i in range(p[7]):
        tmp.append(p[9][0])

    # Build tree
    # Example ('=', ('a', [1,3,4]))
    p[0] = ('=', (p[1], tmp))


# Expresion para crear lista con range.
def p_statement_list_insert(p):
    """
    statement : ID PUNTO INSERT PARENTESISIZQ expression COMA params PARENTESISDER PYC
    """
    # If its not defined
    if not isDefined(p[1], p.lineno(1)):
        return
    # Validation
    if not list_insert_validation(p.lineno(1), p[1], p[7]): return

    # Build tree
    # Example
    # ('INSERT', 'a', [True,False,True], 0, None) => a = [[True,False,True], [False, True], ...]
    p[0] = ("INSERT", p[1], p[5], p[7][0])
    print(run(p[0]))


# Expresion para crear lista con range.
def p_statement_list_del(p):
    """
    statement : ID PUNTO DEL PARENTESISIZQ expression PARENTESISDER PYC
    """
    if check_variable_and_index(p.lineno(1), p[1], p[5]):
        # Build tree
        # Example ('DEL', 'a', 2)
        p[0] = ("DEL", p[1], p[5])
        print(run(p[0]))


# Expresion para crear lista con range.
def p_statement_list_len(p):
    """
    statement : LEN PARENTESISIZQ ID PARENTESISDER PYC
              | LEN PARENTESISIZQ list PARENTESISDER PYC
    """
    # if its a list.
    if equalsType(p[3], list) or isDefined(p[3], p.lineno(1)):
        # Build tree
        # Example ('LEN', [1,2,3])
        # Example ('LEN', 'a')
        p[0] = ("LEN", p[3])
        print(run(p[0]))

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  UTIL FUNCTIONS & VALIDATIONS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


# Funcion para obtener una de las variables del dictionario con el ID
def getValue(key):
    return env.get(key)


# Funcion auxiliar para comparar una variable con un tipo primitivo.
def equalsType(var, tipo):
    if type(var) == tipo:
        return True
    return False


# Verifica si ID existe en el diccionario.
def isDefined(var, line):
    # Si existe el ID dentro del diccionario, return true.
    if getValue(var) is None:
        return False
    return True


# Funcion auxiliar para revisar la existencia de la variable y si el indice es valido.
def check_variable_and_index(line, ID, i, j=None):
    # If its not defined.
    if not isDefined(ID, line):
        return False
    # If wrong index range.
    if not list_check_index_validation(line, ID, i, j):
        return False
    return True


# Función auxiliar para comparar si un elemento nuevo puede ser insertado en una lista.
def list_insert_validation(line, ID, value):
    var = getValue(ID)  # get variable
    typeID = get_list_type(var)  # get first element types.
    typeValue = get_list_type(value)  # get first element types.

    # If the value if a list ,verify is all values are the same type.
    if not matrix_check_type_validation(line, value):
        return False

    # If var is and empty list.
    if equalsType(typeID, None):
        return True

    # If both lists type is not the same.
    if typeID != typeValue:
        text = "TypeError in line {2}: The type of \"{1}\" does not match the type of elements in \"{0}\"." \
            .format(ID, value[0], line)
        errors.append(text)
        return False
    return True


# Funcion general para validar todas las entradas en una lista.
def list_assign_validation(line, lst, index1=None, index2=None):
    if not (matrix_check_type_validation(line, lst) or list_check_index_validation(line, lst, index1) or
            list_check_param_and_range_concordance_validation(line, lst, index1, index2)):
        return False
    return True


# Función para validar que todos los elementos de una matriz corresponden al mismo tipo.
def matrix_check_type_validation(line, lst):
    # If not a list or list is empty.
    if not equalsType(lst, list) or not lst:
        return True
    # Get the type that all items in the list are supposed to be.
    supposedType = get_list_type(lst)

    # If its not a matrix
    if not equalsType(lst[0], list):
        return list_check_type_validation(line, lst, supposedType)

    for i in lst:
        if not (list_check_type_validation(line, i, supposedType)):
            return False
    return True


# Función para validar que todos los elementos de una matriz corresponden al mismo tipo.
def list_check_type_validation(line, lst, supposedType=None):
    # If not a list or list is empty.
    if not equalsType(lst, list) or not lst:
        return True

    # Get the type that all items in the list are supposed to be.
    if supposedType is None:
        supposedType = type(lst[0])

    for i in lst:
        if not equalsType(i, supposedType):
            text = "TypeError in line {1}: \"{0}\" type does not match the type of elements.".format(i, line)
            errors.append(text)
            return False
    return True


# Funcion auxiliar para obtener el primer elemento de una lista que no sea una sublista.
def get_list_type(lst):
    if equalsType(lst, list):
        return get_list_type(lst[0])
    return type(lst)


# Funcion para verificar que un indice se encuentra dentro del rango indicado.
def list_check_index_validation(line, ID, i, j=None):
    lst = env.get(ID)
    if i >= len(lst):
        text = "LenError in line {1}: Index \"{0}\" out of range.".format(i, line)
        errors.append(text)
        return False
    elif (j is not None) and (j > len(lst)):
        text = "LenError in line {1}: Index \"{0}\" out of range.".format(j, line)
        errors.append(text)
        return False
    else:
        return True


# Funcion auxiliar para verificar la cantidad de parametros coincide con los indices.
def list_check_param_and_range_concordance_validation(line, params, i, j):
    if (j is None) and (len(params) == 1):
        return True
    elif len(params) == (j - i):
        return True
    else:
        text = "IndexError in line {0}: The number of parameters does not match that of the indexes.".format(line)
        errors.append(text)
        return False


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
    print("✘ Syntax error found!", p)


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

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  READING TREE OPERATIONS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


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

        elif p[0] == 'DEL':
            return list_delete_operation(p[1], p[2])

        elif p[0] == 'LEN':
            return list_len_operation(p[1])

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


# Funcion para operar la asignacion de las variables.
def var_assign_operation(struct):
    # ('=', (a, 1)) : un elemento, struct = tuple
    # ('=', [(a, 1), (b,2)]) : dos elementos, struct = list
    if type(struct) == tuple:
        var_assign_operation_aux(run(struct[0]), run(struct[1]))
    else:
        for t in struct:
            var_assign_operation(t)


# Auxiliar para verificar la asignacion de las variables.
def var_assign_operation_aux(var, value):
    # If variable is a primitive but not a list.
    if not equalsType(var, list):
        env[var] = run(value)
        print(var, ":", env[var])

    # If its an assigment to a sublist.
    else:
        ID = var[0]
        i, j = var[1][0], var[1][1]
        if j is not None:
            getValue(ID)[i:j] = value
        else:
            getValue(ID)[i] = value
        print(ID, ":", env[ID])


# Funcion para leer y realizar la funcion del arbol de la llamada a una sublista.
def list_callable_operation(ID, indexes, result=True):
    if result:
        if indexes[1] is not None:
            return getValue(ID)[run(indexes[0]):run(indexes[1])]
        return getValue(ID)[run(indexes[0])]
    else:
        return [ID, indexes]


# Funcion para leer y realizar la funcion del arbol de la insercion a una lista.
def list_insert_operation(ID, amount, value):
    var = getValue(ID)
    var.insert(amount, value)
    return run(("var", ID))


# Funcion para leer y realizar la funcion del arbol de eliminar un elemento de una lista.
def list_delete_operation(ID, index):
    var = getValue(ID)
    var.pop(index)
    return var


# Funcion para leer y realizar la funcion del arbol de mostrar el tamaño de una lista.
def list_len_operation(param):
    if equalsType(param, str):
        return len(getValue(param))
    return len(param)


# Create a REPL to provide a way to interface with our calculator.
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)
