# Importa el módulo yacc para el compilador
import ply.yacc as yacc
import sys
from lexer.lexer import tokens

# Pretty Printer
import pprint

# Define el archivo del programa

"""
Writing Machine
Parser: Genera el árbol de parseo. Imprime los resultados del parseo.
Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl" 
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python myparser2.py [nombre_archivo].txt" El archivo de lexer.py tiene que estar en la misma carpeta
TODO:
1. Generar los errores para cada error de sintaxis
2. Generar las reglas para todo a partir de las reglas de POS
"""

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
    """ statements : empty
                   | print
                   | primitive
                   | statement
                   | statements statement
    """
    if p[1] is None:
        pass
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
              | funcionreservada
              | procedure

    '''
    # print("BNF:", p[1], " ~ (line 57)")
    run(p[1])
    # print(p[1])
    #print("callable", p[1])
    p[0] = p[1]



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


# Expresion auxiliar para convertir los parametros de input.
def p_params(p):
    """
    params  : input
    """
    # If param is None
    if p[1][0] is None:
        p[0] = None
    # If only one param
    elif len(p[1]) == 1:
        p[0] = p[1][0]
    else:
        p[0] = p[1]


# Expresion para obtener params.
def p_input(p):
    """
    input  : empty
            | expression
            | primitive
            | sublist
            | input COMA input
    """

    # Si es solo un parametro
    if len(p) == 2:
        if type(p[1]) == list:
            if not list_check_type_validation(p.lineno(1), p[1]):
                return None
        p[0] = [p[1]]

    # Si son más de dos input
    else:
        p[0] = p[1] + p[3]


# Expresion para asignacion de variables.
def p_var_assign(p):
    """
    var_assign : ID IGUAL expression PYC
               | ID IGUAL primitive PYC
    """
    # one variable, can only be int, bool, string or list.
    if p[3] is None:
        return None
    # ERROR verification (assignment, reassignment)
    if not var_assign_validation(p[1], p[3], p.lineno(1)):
        return None

    # If it is a list that does not meet the requirements, the recursion will end up in a string.
    if equalsType(p[2], list):
        if not list_check_type_validation(p.lineno(1), p[2]):
            return None

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
        return None
    # Build our tree
    # Examples
    # ('=', [('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])
    p[0] = ('=', vars_assign_tree_aux(p[1], p[3]))


# Expresion para asignar una sublista.
def p_sublist_assign(p):
    """
    var_assign : sublist IGUAL params PYC
    """
    sublist = p[1]
    params = p[3]

    # VALIDATIONS
    # Invalid types.
    if not list_check_type_validation(p.lineno(1), params):
        return None
    # Invalid sublist or params.
    if sublist is None or params is None:
        return None
    if not list_insert_validation(p.lineno(1), sublist[1], params):
        return None

    # Build our tree
    # Examples:
    # Test:  a[0:4]=[1,2,3,4]
    # ( '=' , (('[]', 'a', [0, 4]) , [1, 2, 3, 4]))
    newTuple = (sublist[0] + '*', sublist[1], sublist[2])
    p[0] = ("=", (newTuple, p[3]))

    # NOTA: run() is called in p_operation


# Funcion auxiliar para verificar una reasignacion de la variable.
def var_assign_validation(ID, param, line):
    # CHECKING PARAM...

    comillas = '"'
    # If param its not a string.
    if equalsType(param, str) and not comillas in param:

        # If ID is a param and it does not exist.
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

    # Return true if its a new variable and param is not and undeclared variable.
    return True


# Funcion auxiliar para validar los ids y params recibidos si son varios ids.
def vars_assign_validation(ids, params, line):
    # Number of params must match the numbers of ids.
    print("*ids", ids)
    print("*params", params)

    if len(ids) != len(params):
        text = "LenError in line {0}! The number of values does not match the number of IDs.".format(line)
        errors.append(text)
        return False

    # All params type must be the same.
    if not list_check_type_validation(line, params):
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
    if p[2] is None:
        p[0] = []
    else:
        if equalsType(p[2], list):
            if not list_check_type_validation(p.lineno(1), p[2]):
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
    sublist  : ID multi_index
             | ID CORCHETEIZQ expression COMA expression CORCHETEDER
             | ID CORCHETEIZQ DOSPUNTOS COMA expression CORCHETEDER
    '''

    ID = p[1]

    # If its not defined.
    if not isDefined(ID, p.lineno(1)):
        return None

    lst = getValue(ID)
    # If variable is not a list.
    if not equalsType(lst, list):
        text = "TypeError in line {1}: The type of \"{0}\" must be list.".format(ID, p.lineno(1))
        errors.append(text)
        return None

    # If searching in list. L[0]
    if len(p) == 3:
        indexes = p[2]

    # If searching for column. M[:,0]
    elif p[3] == ":":
        indexes = [":", p[5]]

    # If searching in matrix. M[0][0]
    else:
        indexes = [[p[3], None], [p[5], None]]

    # If searching in list. L[0]
    if len(indexes) == 1:
        if check_index_aux(p.lineno(1), getValue(ID), indexes[0][0], indexes[0][1]):
            # Build tree
            # Example ('[]', a, 1)
            p[0] = ('[]', ID, indexes)

    # If searching for column. M[:,0]
    elif indexes[0] == ":":
        row = getValue(ID)[0]
        if check_index_aux(p.lineno(1), row, indexes[1]):
            # Build tree
            # Example (':', m, 4)
            p[0] = ('[:,]', ID, indexes[1])

    # If searching in matrix. M[0][0]
    else:
        if list_check_index_validation(p.lineno(1), ID, indexes):
            # Build tree
            # Example ('[]', a, [1,2,3])
            p[0] = ('[]', ID, indexes)


# Expresion para varios parámetros de index. Clausula de Klean.
def p_multiple_index(p):
    """
    multi_index : index
                | index multi_index
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


# Expresion para obtener limite inicial y final de los indices dentro de corchetes.
def p_index_dospuntos(p):
    """
    index  : CORCHETEIZQ expression CORCHETEDER
           | CORCHETEIZQ expression DOSPUNTOS expression CORCHETEDER
    """
    if len(p) == 4:
        lst = [p[2]] + [None]
    else:
        lst = [p[2]] + [p[4]]
    p[0] = lst


# # Expresion para poder llamar a las matrices como M[1,1].
# def p_matrix_column(p):
#     '''
#     sublist   :    ID CORCHETEIZQ PUNTO COMA expression CORCHETEDER
#     '''
#
#     ID = p[1]
#     indexes = [[p[5], None]]
#
#     # If its not defined.
#     if not isDefined(ID, p.lineno(1)):
#         return None
#
#     lst = getValue(ID)
#     # If variable is not a list.
#     if not equalsType(lst, list):
#         text = "TypeError in line {1}: The type of \"{0}\" must be list.".format(ID, p.lineno(1))
#         errors.append(text)
#         return None
#
#
#
#     print(p[1], p[3], p[5])


# Expresion para crear lista con range.
def p_statement_list_range(p):
    """
    var_assign : ID IGUAL LIST PARENTESISIZQ RANGE PARENTESISIZQ expression COMA params PARENTESISDER PARENTESISDER PYC
    """
    tmp = []
    for i in range(p[7]):
        tmp.append(p[9])

    # Build tree
    # Example ('=', ('a', [1,3,4]))
    p[0] = ('=', (p[1], tmp))


# Expresion para crear lista con range.
def p_statement_list_insert(p):
    """
    statement : ID PUNTO INSERT PARENTESISIZQ expression COMA params PARENTESISDER PYC
    """
    line = p.lineno(1)
    ID = p[1]
    num = p[5]
    params = p[7]

    # If its not defined
    if not isDefined(ID, p.lineno(1)):
        return None
    # Validation
    if not list_insert_validation(line, ID, params):
        return None

    # Build tree
    # Example
    # ('INSERT', 'a', [True,False,True], 0, None) => a = [[True,False,True], [False, True], ...]
    p[0] = ("INSERT", ID, num, params)
    # print("BNF:", p[0])
    # print(run(p[0]))
    # print(p[0])


# Expresion para crear lista con range.
def p_statement_list_del(p):
    """
    statement : ID PUNTO DEL PARENTESISIZQ expression PARENTESISDER PYC
    """
    line = p.lineno(1)
    ID = p[1]
    i = p[5]

    # If its not defined.
    if not isDefined(ID, line):
        return None
    # If wrong index range.
    if not check_index_aux(line, getValue(ID), i):
        return None

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


def p_neg(p):
    """
    statement : sublist PUNTO NEG PYC
              | sublist PUNTO T PYC
              | sublist PUNTO F PYC
    """
    sublist = p[1]
    newTuple = (sublist[0] + '*', sublist[1], sublist[2])
    p[0] = (p[3].upper(), newTuple)

    # Build tree
    # Example  ('NEG', ('[]', 'b', [[0, 2]]))
    # Example  ('T', ('[]*', 'b', [[0, 2]]))
    # Example  ('F', ('[]', 'b', [[0, 2]]))
    # print("BNF:", p[0])
    # print(run(p[0]))
    # print(p[0])


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


# Expresion vacia
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  UTIL FUNCTIONS & VALIDATIONS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''

' ###### Variable functions  ###### '


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


# Función para revisar si hay una variable
def revisar_variable(a):
    var_local = False
    var_global = False

    # Si la variable ya existe, le cambia el valor
    if a in env:
        var_global = True

    # Si la variable ya existe, le cambia el valor
    elif a in env:
        var_local = True

    # Si la variable no existe en ninguna lista
    else:
        return False

    # Si se encontró en la lista de variables globales
    if var_global:
        return env[a]

    # Si se encontró en la lista de variables locales
    if var_local:
        return env[a]


' ###### Validation of insertion in a list ###### '


# Función auxiliar para comparar si un elemento nuevo puede ser insertado en una lista.
def list_insert_validation(line, ID, value):
    var = getValue(ID)  # get variable

    # If ID is not list and value is list.
    if not equalsType(var, list) and equalsType(value, list):
        text = "TypeError in line {2}: \"{1}\" does not match the type of \"{0}\"." \
            .format(ID, value, line)
        errors.append(text)
        return False

    # If ID is list and value is not.
    elif equalsType(var, list) and not equalsType(value, list):
        if type(var[0]) != type(value):
            text = "TypeError in line {2}: \"{1}\" does not match the type of \"{0}\"." \
                .format(ID, value, line)
            errors.append(text)
            return False

    elif not (equalsType(var, list) and equalsType(value, list)):
        if type(var) != type(value):
            text = "TypeError in line {2}: \"{1}\" does not match the type of \"{0}\"." \
                .format(ID, value, line)
            errors.append(text)
            return False

    # If both are lists.
    else:
        typeID = get_list_type(var)  # get first element types.
        typeValue = get_list_type(value)  # get first element types.
        if typeID != typeValue:
            text = "TypeError in line {2}: The type of \"{1}\" does not match the type of elements in \"{0}\"." \
                .format(ID, value[0], line)
            errors.append(text)
            return False

    # Then its a valid insertion.
    return True


' ###### Type validation of elements in a list ###### '


# Función para validar que todos los elementos de una lista corresponden al mismo tipo.
def list_check_type_validation(line, lst):
    # If not a list or list is empty.
    if not equalsType(lst, list) or not lst:
        return True

    # If its not a list of lists.
    if not equalsType(lst[0], list):
        return check_type_aux(line, lst)

    # If its a list of lists.
    else:
        # Get the type that all items in the list are supposed to be.
        supposedType = get_list_type(lst)
        return multi_check_type_aux(line, lst, supposedType)


# Funcion auxiliar para obtener el primer elemento de una lista que no sea una sublista.
def get_list_type(lst):
    if equalsType(lst, list):
        return get_list_type(lst[0])
    return type(lst)


# Función para validar que todos los elementos de una lista de listas corresponde al mismo tipo.
def multi_check_type_aux(line, lst, supposedType):
    for i in range(len(lst)):
        sublist = lst[i]

        # If its a sublist.
        if equalsType(sublist, list):
            # If all elements are type list.
            if check_type_aux(line, sublist):
                if not multi_check_type_aux(line, sublist, supposedType):
                    return False

        # If its an int or bool.
        else:
            # If all elements are the same type.
            if check_type_aux(line, lst):
                return True
            return False
    return True


# Función para validar que todos los elementos de una lista corresponden al mismo tipo.
def check_type_aux(line, lst, supposedType=None):
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


''' ###### List index validation ###### '''


# Funcion global para verificar que un indice se encuentra dentro del rango indicado dentro de una lista
# de elementos o una lista de listas.
def list_check_index_validation(line, ID, indexes):
    lst = getValue(ID)

    # If variable is not a list.
    if not equalsType(lst, list):
        text = "TypeError in line {1}: The type of \"{0}\" must be list.".format(ID, line)
        errors.append(text)
        return False
    return check_index(line, lst, indexes)


def check_index(line, lst, indexes):
    # Indexes variables.
    i = indexes[0][0]
    j = indexes[0][1]

    # Stop condition: last inner list.
    if len(indexes) == 1:
        return check_index_aux(line, lst, i, j)

    # If there are internal lists.
    else:

        # Validate index for outer list
        if not check_index_aux(line, lst, i, j):
            return False

        # Validate index for inner list
        sublist = lst[i]
        if j is not None:
            sublist = lst[i:j]

        # Then all indexes are valid.
        return check_index(line, sublist, indexes[1:])


# Funcion para verificar que un indice se encuentra dentro del rango indicado de una sola lista.
def check_index_aux(line, lst, i, j=None):
    # If its not a list. Then False
    if not equalsType(lst, list):
        text = "TypeError in line {1}: {0} object is not subscriptable.".format(var_type(lst), line)
        errors.append(text)
        return False

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


''' ###### List index range validation ###### '''


# Funcion para verificar la cantidad de parametros coincide con los indices insertados.
def list_check_param_and_range_concordance_validation(line, params, i, j):
    if (j is None) and (len(params) == 1):
        return True
    elif len(params) == (j - i):
        return True
    else:
        text = "IndexError in line {0}: The number of parameters does not match that of the indexes.".format(line)
        errors.append(text)
        return False


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  FUNCTIONS GRAMMARS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''

# Condicion
def p_condicion(p):
    """ condicion : expression IGUALES valorIf
                             | expression  MAYORQUE valorIf
                             | expression  MENORQUE valorIf
                             | expression  MENORIGUAL valorIf
                             | expression  MAYORIGUAL valorIf
    """

    # Mayorque
    if p[2] == '>':
        p[0] = [p[1], '>', p[3]]

    # MayorOIgual
    elif p[2] == '>=':
        p[0] = [p[1], '>=', p[3]]

    # MenorQue
    elif p[2] == '<':
        p[0] = [p[1], '<', p[3]]

    # MenorOIgual
    elif p[2] == '<=':
        p[0] = [p[1], '<=', p[3]]

    # Igual
    elif p[2] == '==':
        p[0] = [p[1], '==', p[3]]


    """
    # Variables temporales para la evaluación
    tempX = 0
    tempY = 0

    variable1 = 0

    # Si son variables, las asigna
    if isDefined(p[1][1],1):
        variable1 = env[p[1][1]]

    variable2 = p[3]

    # Error
    error = False

    # Asigna los valores dependiendo si es ID o un int
    if variable1 is not False and variable2 is not False:
        tempX = variable1
        tempY = variable2

    # Revisa si la primera entrada es una variable y la segunda número
    elif variable1 is not False and isinstance(p[3], int):
        tempX = variable1
        tempY = p[3]

    # Revisa si la primera entrada es un número y la segunda variable
    elif variable2 is not False and isinstance(p[1], int):
        tempX = p[1]
        tempY = variable2

    # Revisa si la primera entrada es un número y la segunda número
    elif isinstance(p[1], int) and isinstance(p[3], int):
        tempX = p[1]
        tempY = p[3]

    # Si no es número y no existe
    elif not isinstance(p[1], int) and variable1 is False:
        errors.append(
            "ERROR: No se puede comparar con el identificador indefinido {0} en la línea {1}".format(p[1], p.lineno(1)))

    # Si no es número y no existe
    elif not isinstance(p[3], int) and variable2 is False:
        errors.append(
            "ERROR: No se puede comparar con el identificador indefinido {0} en la línea {1}".format(p[3], p.lineno(3)))

    # Mayorque
    if p[2] == '>':
        p[0] = (tempX > tempY)

    # MayorOIgual
    elif p[2] == '>=':
        p[0] = tempX >= tempY

    # MenorQue
    elif p[2] == '<':
        p[0] = tempX < tempY

    # MenorOIgual
    elif p[2] == '<=':
        p[0] = tempX <= tempY

    # Igual
    elif p[2] == '==':
        p[0] = tempX == tempY
    """


def p_valorIf(p):
    """ valorIf : BOOLEAN
              | INT
    """
    p[0] = p[1]


# Definición de if
def p_if(p):
   """ funcionreservada : IF PARENTESISIZQ condicion PARENTESISDER LLAVEIZQ ordenes LLAVEDER
   """
   # Si se cumple la condición, devuelve las ordenes a ejecutar

   #if p[3] == True:
   #     p[0] = ['IF', p[6]]
   p[0] = ['IF', p[3] ,p[6]]


def p_procedure(p):
    '''
    procedure : PROCEDURE ID PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC
                | PROCEDURE MAIN PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC
    '''

    p[0] = ['PROCEDURE', p[2], p[4], p[7]]


def p_call(p):
    '''
    funcionreservada : CALL ID PARENTESISIZQ params PARENTESISDER PYC
    '''

    p[0] = ['CALL', p[2], p[4]]


def p_for(p):
    '''
    funcionreservada : FOR expression IN INT LLAVEIZQ ordenes LLAVEDER
                        | FOR expression IN expression LLAVEIZQ ordenes LLAVEDER
    '''

    p[0] = ['FOR', p[2], p[4], p[6]]


# Ordenes (se dan en forma de una lista de listas)
def p_ordenes(p):
    '''
    ordenes : statement
                       | ordenes statement
                       | ordenes funcionreservada
                       | funcionreservada

   '''

    """    # Revisa si hay alguna asignación de variable
    for i in p:
        if isinstance(i, list):
            if i[0] != 'DEF' and i[1] not in (env or env):
                env[i[1]] = i[2]
            elif i[0] != 'DEF' and i[1] in (env or env):
                errors.append("ERROR: Se intentó redefinir la variable {0} ya definida en main".format(i[0]))"""

    # Si es solo un elemento
    if len(p) == 2:
        p[0] = [p[1]]

    # Si es más de una orden, se concatenan
    else:
        p[0] = p[1] + [p[2]]


"""   
Blink(Dato, Cantidad, RangoTiempo, Estado)
Dato: Indice, Arreglo, etc
Cantidad: Entero
RangoTiempo: "Seg", "Mil", "Min"
Estado: bool
"""


def p_blink(p):
    '''
    funcionreservada : BLINK PARENTESISIZQ params PARENTESISDER PYC
    '''
    print(p[3])

    if len(p[3]) == 4:

        if p[3][0] == "[]":
            errors.append("ERROR in line {0}! The first param cant be a empty list! "
                          "".format(p.lineno(1)))
            return

        if type(p[3][0]) == list or type(p[3][0]) == int:

            if type(p[3][3]) == bool:

                if p[3][2] == "\"Seg\"" or p[3][2] == "\"Mil\"" or p[3][2] == "\"Min\"":

                    if type(p[3][1]) == int:

                        p[0] = ['BLINK', p[3]]
                        #print(run(p[0]))

                    else:
                        errors.append("ERROR in line {0}! The second param must be a integer! "
                                      "".format(p.lineno(1)))


                else:
                    errors.append("ERROR in line {0}! The third param must be a (Seg, Mil, Min)! "
                                  "".format(p.lineno(1)))

            else:
                errors.append("ERROR in line {0}! The last param must be a bool! "
                              "".format(p.lineno(1)))

        else:
            errors.append("ERROR in line {0}! The first param must be a list "
                          "".format(p.lineno(1)))
    else:
        errors.append("ERROR in line {0}! The number of params must be 4 "
                      "(Dato, Cantidad, RangoTiempo, Estado)".format(p.lineno(1)))


"""   
Delay(Cantidad, RangoTiempo)
Cantidad: Entero
RangoTiempo: "Seg", "Mil", "Min"
"""


def p_delay(p):
    '''
    funcionreservada : DELAY PARENTESISIZQ params PARENTESISDER PYC
    '''

    if len(p[3]) == 2:

        if type(p[3][0]) == int:

            if p[3][1] == "\"Seg\"" or p[3][1] == "\"Mil\"" or p[3][1] == "\"Min\"":
                p[0] = ['DELAY', p[3]]

            else:
                errors.append("ERROR in line {0}! The second param must be a (Seg, Mil, Min)! "
                              "".format(p.lineno(1)))
        else:
            errors.append("ERROR in line {0}! The first param must be an integer".format(p.lineno(1)))

    else:
        errors.append("ERROR in line {0}! The number of params must be 2 "
                      "(Cantidad, RangoTiempo)".format(p.lineno(1)))


"""   
PrintLed(Col, Row, Valor)
Col: Entero
Row: Entero
Valor: Bool
"""


def p_PrintLed(p):
    '''
    funcionreservada : PRINTLED PARENTESISIZQ params PARENTESISDER PYC
    '''

    if len(p[3]) == 3:

        if type(p[3][0]) == int and type(p[3][1]) == int:
            print(p[3])
            if type(p[3][2]) == bool:
                p[0] = ['PRINTLED', p[3]]

            else:
                errors.append("ERROR in line {0}! The third param must be a boolean".format(p.lineno(1)))

        else:
            errors.append("ERROR in line {0}! The first and second param must be integers".format(p.lineno(1)))

    else:
        errors.append("ERROR in line {0}! The number of params must be 4 "
                      "(Col, Row, Value)".format(p.lineno(1)))


"""   
PrintLedX(TipoObjeto, Indice, Arreglo)
TipoObjeto: "C", "F", "M"
Indice: Entero
Arreglo: arreglo
"""


def p_PrintLedX(p):
    '''
    funcionreservada : PRINTLEDX PARENTESISIZQ params PARENTESISDER PYC
    '''

    if len(p[3]) == 3:

        if p[3][0] == "\"C\"" or p[3][0] == "\"F\"" or p[3][0] == "\"M\"":

            if type(p[3][1]) == int:

                if p[3][2] == "[]":
                    errors.append("ERROR in line {0}! The last param cant be a empty list! "
                                  "".format(p.lineno(1)))
                    return

                val = getValue(p[3][2][1])
                if type(val) == list:
                    p[0] = ['PRINTLEDX', p[3]]

                else:
                    errors.append("ERROR in line {0}! The last param must be a list! "
                                  "".format(p.lineno(1)))

            else:
                errors.append("ERROR in line {0}! The second param must be an integer! "
                              "".format(p.lineno(1)))

        else:
            errors.append("ERROR in line {0}! The first param must be a (Seg, Mil, Min)! "
                          "".format(p.lineno(1)))
    else:
        errors.append("ERROR in line {0}! The number of params must be 3 "
                      "(TipoObjeto, Indice, Arreglo)".format(p.lineno(1)))


# Output to the user that there is an error in the input as it doesn't conform to our grammar.
# p_error is another special Ply function.
def p_error(p):
    print("✘ Syntax error found!", p)


# Build the parser
parser = yacc.yacc()
# Create the environment upon which we will store and retrieve variables from.
env = {}
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

        elif p[0] == '[:,]':
            return matrix_column_operation(p[1], p[2])

        elif p[0] == '[:,]*':
            return matrix_column_operation(p[1], p[2], False)

        elif p[0] == 'INSERT':
            return list_insert_operation(p[1], p[2], p[3])

        elif p[0] == 'DEL':
            return list_delete_operation(p[1], p[2])

        elif p[0] == 'LEN':
            return list_len_operation(p[1])

        elif p[0] == "NEG":
            return neg_operation(p[1])

        elif p[0] == "T":
            return t_operation(p[1])

        elif p[0] == "F":
            return f_operation(p[1])

        elif p[0] == 'BLINK':
            return p[1]

        elif p[0] == 'DELAY':
            return p[1]

        elif p[0] == 'PRINTLED':
            return p[1]

        elif p[0] == 'PRINTLEDX':
            return p[1]


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
    # print ("Struct:", struct)
    if type(struct) == tuple:
        var_assign_operation_aux(run(struct[0]), run(struct[1]))
    else:
        for t in struct:
            var_assign_operation(t)


# Auxiliar para verificar la asignacion de las variables.
def var_assign_operation_aux(var, value):
    #print(var)
    # If variable is a primitive but not a list.
    if not equalsType(var, list):
        env[var] = run(value)
        #print(var, ":", env[var])

    # If its an assignment to a column.
    elif var[0] == ':':
        ID = var[1]
        env[ID] = matrix_column_assign(getValue(ID), var[2], value)

    # If its an assignment to a sublist.
    else:
        ID = var[0]
        i, j = var[1][0][0], var[1][0][1]
        if j is not None:
            getValue(ID)[i:j] = value
        else:
            getValue(ID)[i] = value
        #print(ID, ":", env[ID])


# Funcion para leer y realizar la funcion del arbol de la llamada a una sublista.
def list_callable_operation(ID, indexes, result=True):
    if result:
        lst = getValue(ID)
        return sublist_recursive_call(lst, indexes)

    else:
        return [ID, indexes]


# Funcion para recorrer recursivamente la llamada de varios indices en una lista.
def sublist_recursive_call(lst, indexes):
    # Indexes variables.
    i = indexes[0][0]
    j = indexes[0][1]

    # Stop condition: last index list.
    if len(indexes) == 1:
        sublist = lst[run(i)]
        if j is not None:
            sublist = lst[run(i):run(j)]
        return sublist

    # If there are inner index list.
    else:
        sublist = lst[run(i)]
        if j is not None:
            sublist = lst[run(i):run(j)]

        # Then all indexes are valid.
        return sublist_recursive_call(sublist, indexes[1:])


# Funcion para leer y realizar la funcion del arbol de la insercion a una lista.
def list_insert_operation(ID, amount, value):
    var = getValue(ID)
    var.insert(run(amount), value)
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


# Funcion que hace switch del valor booleano de una lista, matriz o rango de las mismas.
def neg_operation(param):
    return bool_operation_aux("N", run(param))


# Funcion que cambia el valor booleano a True de una lista, matriz o rango de las mismas.
def t_operation(param):
    return bool_operation_aux("T", run(param))


# Funcion que cambia el valor booleano a False de una lista, matriz o rango de las mismas.
def f_operation(param):
    return bool_operation_aux("F", run(param))


def bool_operation_aux(order, value):
    # If value is not a list.
    #print(order)
    run()
    #print(value)

    # if not equalsType(value, list):

    # if (equalsType(param))


# Funcion para leer y realizar la funcion del arbol de mostrar la columna de una matriz.
def matrix_column_operation(ID, col, result=True):
    var = getValue(ID)
    if not result:
        return [":", ID, col]
    return matrix_column_aux(var, col)


def matrix_column_aux(var, col):
    tmp = []
    for row in var:
        tmp.append(row[col])
    return tmp


# Funcion que asigna los valores de columna de una matriz a otra.
def matrix_column_assign(var, col, new_val_list):
    # print(var, col, new_val_list)
    for r in range(len(var)):
        # print(var[r][col], "|", new_val_list[r])
        var[r][col] = new_val_list[r]
    return var


# # Create a REPL to provide a way to interface with our calculator.
# while True:
#     try:
#         s = input('>> ')
#     except EOFError:
#         break
#     parser.parse(s)

# Create a REPL to provide a way to interface with our calculator.
print("\n--------- RESULTS ---------")

# Crea el printer para poder imprimir tanto en el Shell de Python como en CMD
pp = pprint.PrettyPrinter(indent=2)

# Implementación para leer un archivo que será el insumo del parser
with open(program_file, 'r') as file:
    insumo = file.read()
    result = parser.parse(insumo)
    pp.pprint(result)
    print(env)

    print("\nErrores:")
    pp.pprint(errors)
