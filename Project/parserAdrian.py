# Importa el módulo yacc para el compilador
import ply.yacc as yacc

# Pretty Printer
import pprint

# Sys para leer argumentos
import sys

# Get the token map from the lexer.  This is required.
from pip._vendor.distlib.compat import raw_input

from lexer.lexer import tokens

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

# Diccionarios
functions = {}  # Lista de funciones almacenadas del programa.
variables = {"a": [1, 2, 3, 4]}  # Las variables almacenadas se guardarán como {ID: valor}.

# Lista de errores del programa.
errors_list = []

# Orden para asignar a las operaciones.
# Se utiliza el %prec para la declaracion de expresiones negativas.
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'DIVISIONENTERA'),
    ('right', 'UMENOS'),
    ('right', 'MODULO'),
    ('right', 'EXPONENTE')
)

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%#################  GRAMMAR RULES %%%%%%%%%%%%%%%%%%%%%%%%%%%%#################'''

'''Cada regla gramatical está definida por una función de Python donde la cadena de documentación 
de esa función contiene la especificación gramatical libre de contexto apropiada.
Los enunciados que componen el cuerpo de la función implementan las acciones semánticas de la regla. 
Cada función acepta un solo argumento p que es una secuencia que contiene los valores de cada 
símbolo gramatical en la regla correspondiente. Los valores de p [i] se asignan a símbolos gramaticales.'''


# The parser grammar rules are defined.
# The rule name does not matter as long as it starts with "p_".


# Expresion que define una recursion entre expresiones.
def p_statements(p):
    """ statements : statements statement
                   | statement
    """
    # NOTA: P[0] corresponde al valor que toma la variable.
    # El conteo de indices para los datos empieza en 1.
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# Definición de posibles expresiones.
def p_statements_expr(p):
    ''' statement : expression
                    | print
                    | funcionreservada
    '''
    p[0] = p[1]


# Definición de if
def p_if(p):
    """ funcionreservada : IF condicion LLAVEIZQ ordenes LLAVEDER PYC
    """
    # Si se cumple la condición, devuelve las ordenes a ejecutar
    if p[2] == True:
        p[0] = ['IF', p[4]]
    else:
        print("No se cumple el if")


# Ordenes (se dan en forma de una lista de listas)
def p_ordenes(p):
    '''ordenes : funcionreservada
                       | statement
                       | ordenes statement
                       | ordenes funcionreservada
   '''
    # Revisa si hay alguna asignación de variable
    for i in p:
       if isinstance(i, list):
          if i[0] != 'DEF' and i[1] not in (variables or variables):
             variables[i[1]] = i[2]
          elif i[0] != 'DEF' and i[1] in (variables or variables):
             errors_list.append("ERROR: Se intentó redefinir la variable {0} ya definida en main".format(i[0]))

   # Si es solo un elemento
    if len(p) == 2:
       p[0] = [p[1]]

   # Si es más de una orden, se concatenan
    else:
       p[0] = p[1] + [p[2]]


#################### CONDICIONES ####################


# Condicion
def p_condicion(p):
    """ condicion : expression MAYORQUE expression
                             | expression MENORQUE expression
                             | expression MENORIGUAL expression
                             | expression MAYORIGUAL expression
                             | expression IGUALES expression
                             | value IGUALES value
                             | value  MAYORQUE value
                             | value  MENORQUE value
                             | value  MENORIGUAL value
                             | value  MAYORIGUAL value
    """
    # Variables temporales para la evaluación
    tempX = 0
    tempY = 0

    # Si son variables, las asigna
    variable1 = revisar_variable(p[1])
    variable2 = revisar_variable(p[3])

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
        errors_list.append(
            "ERROR: No se puede comparar con el identificador indefinido {0} en la línea {1}".format(p[1], p.lineno(1)))

    # Si no es número y no existe
    elif not isinstance(p[3], int) and variable2 is False:
        errors_list.append(
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

# Parametros (se dan en forma de una lista)
def p_parametros(p):
    '''parametros : expression
                             | value
                             | parametros COMA expression
                             | parametros COMA value
                             | empty
    '''

    # Si es solo una expresion
    if len(p) == 2:
       p[0] = [p[1]]

    # Si son más de dos
    else:
       p[0] = p[1] + [p[3]]

############################# FUNCIONES RESERVADAS #########################################

def p_list(p):
    '''lista : CORCHETEIZQ CORCHETEDER
             | CORCHETEIZQ parametros CORCHETEDER
    '''

    # Si es solo una expresion
    if len(p) == 3:
       p[0] = "[]"

    # Si son más de dos
    else:
       p[0] = p[2]

"""   
Blink(Dato, Cantidad, RangoTiempo, Estado)
Dato: Indice, Arreglo, etc
Cantidad: Entero
RangoTiempo: "Seg", "Mil", "Min"
Estado: bool
"""

def p_blink(p):
    '''funcionreservada : BLINK PARENTESISIZQ parametros PARENTESISDER PYC

    '''

    if len(p[3]) == 4:

        if p[3][0] == "[]":
            errors_list.append("ERROR in line {0}! The first param cant be a empty list! "
                               "".format(p.lineno(1)))
            return

        if type(p[3][0]) == list or type(p[3][0]) == int:

            if type(p[3][3]) == bool:

                if p[3][2] == "\"Seg\"" or p[3][2] == "\"Mil\"" or p[3][2] == "\"Min\"":

                    if type(p[3][1]) == int:

                        p[0] = ['BLINK', p[3]]

                    else:
                        errors_list.append("ERROR in line {0}! The second param must be a integer! "
                                           "".format(p.lineno(1)))


                else:
                    errors_list.append("ERROR in line {0}! The third param must be a (Seg, Mil, Min)! "
                                       "".format(p.lineno(1)))

            else:
                errors_list.append("ERROR in line {0}! The last param must be a bool! "
                                   "".format(p.lineno(1)))

        else:
            errors_list.append("ERROR in line {0}! The first param must be a list "
                               "".format(p.lineno(1)))
    else:
        errors_list.append("ERROR in line {0}! The number of params must be 4 "
                           "(Dato, Cantidad, RangoTiempo, Estado)".format(p.lineno(1)))

"""   
Delay(Cantidad, RangoTiempo)
Cantidad: Entero
RangoTiempo: "Seg", "Mil", "Min"
"""

def p_delay(p):
    '''funcionreservada : DELAY PARENTESISIZQ parametros PARENTESISDER PYC

    '''

    if len(p[3]) == 2:

        if type(p[3][0]) == int:

            if p[3][1] == "\"Seg\"" or p[3][1] == "\"Mil\"" or p[3][1] == "\"Min\"":

                p[0] = ['DELAY', p[3]]
            else:
                errors_list.append("ERROR in line {0}! The second param must be a (Seg, Mil, Min)! "
                                   "".format(p.lineno(1)))
        else:
            errors_list.append("ERROR in line {0}! The first param must be an integer".format(p.lineno(1)))

    else:
        errors_list.append("ERROR in line {0}! The number of params must be 2 "
                           "(Cantidad, RangoTiempo)".format(p.lineno(1)))


"""   
PrintLed(Col, Row, Valor)
Col: Entero
Row: Entero
Valor: Bool
"""
def p_PrintLed(p):
    '''funcionreservada : PRINTLED PARENTESISIZQ parametros PARENTESISDER PYC

    '''

    if len(p[3]) == 3:

        if type(p[3][0]) == int and type(p[3][1]) == int:

            if type(p[3][2]) == bool:

                p[0] = ['PRINTLED', p[3]]

            else:
                errors_list.append("ERROR in line {0}! The third param must be a boolean".format(p.lineno(1)))

        else:
            errors_list.append("ERROR in line {0}! The first and second param must be integers".format(p.lineno(1)))

    else:
        errors_list.append("ERROR in line {0}! The number of params must be 4 "
                           "(Col, Row, Value)".format(p.lineno(1)))

"""   
PrintLedX(TipoObjeto, Indice, Arreglo)
TipoObjeto: "C", "F", "M"
Indice: Entero
Arreglo: arreglo
"""
def p_PrintLedX(p):
    '''funcionreservada : PRINTLEDX PARENTESISIZQ parametros PARENTESISDER PYC

    '''

    if len(p[3]) == 3:

        if p[3][0] == "\"C\"" or p[3][0] == "\"F\"" or p[3][0] == "\"M\"":

            if type(p[3][1]) == int:
                print(p[3][2])
                if p[3][2] == "[]":
                    errors_list.append("ERROR in line {0}! The last param cant be a empty list! "
                                       "".format(p.lineno(1)))
                    return

                if type(p[3][2]) == list:

                    p[0] = ['PRINTLEDX', p[3]]

                else:
                    errors_list.append("ERROR in line {0}! The last param must be a list! "
                                       "".format(p.lineno(1)))

            else:
                errors_list.append("ERROR in line {0}! The second param must be an integer! "
                                   "".format(p.lineno(1)))

        else:
            errors_list.append("ERROR in line {0}! The first param must be a (Seg, Mil, Min)! "
                               "".format(p.lineno(1)))
    else:
        errors_list.append("ERROR in line {0}! The number of params must be 3 "
                           "(TipoObjeto, Indice, Arreglo)".format(p.lineno(1)))















# Expresion vacia
def p_empty(p):
    """empty :"""
    pass


# Expresion para imprimir las variables presentes.
def p_printVariables(p):
    """
    print : PUNTO
    """
    print(" ▶ variables: ", variables)
    print(" ▶ errors: ", errors_list)


# Expresion para la declaracion de una variable.
def p_statement_assign(p):
    """
        statement : ID IGUAL value
                  | ids IGUAL params
    """

    if isinstance(p[1], str):  # Si es solo un id
        p[0] = assign_aux(p[1], p[3])
    else:  # Para más de un id
        p[0] = multiple_assign_aux(p[1], p[3])
    print(" ▶ variables: ", variables)


# Expresion para definir multiples ID o uno solo.
def p_ids(p):
    """ ids : ID
            | ID COMA ids

    """
    if len(p) == 2:  # Si es solo un id
        p[0] = [p[1]]
    else:  # Para más de un id
        p[0] = [p[1]] + p[3]


# Expresion para obtenr parametros (se dan en forma de una lista)
def p_params(p):
    """
    params  : value
            | params COMA params
    """
    if len(p) == 2:  # Si es solo un parametro
        p[0] = [p[1]]
    else:  # Si son más de dos parametros
        p[0] = p[1] + p[3]


# Funcion auxiliar para declarar multiples variables.
# Hace uso de assign_aux para declarar una sola variable a la vez.
def multiple_assign_aux(ids_list, values_list):
    if len(ids_list) != len(values_list):
        errors_list.append(
            "ERROR in line {0}! The number of values does not match the number of IDs.".format("LINE_NUMBER"))
    var_list = []

    for id in ids_list:
        if id in variables.keys():
            errors_list.append(
                "ERROR in line {2}! \"{0}\" is already defined as {1}.".format(id, variables.get(id), "LINE_NUMBER"))
            return None

    for i in range(len(ids_list)):
        var_list.append(assign_aux(ids_list[i], values_list[i]))
        # print(var_list)
    return var_list


# Funcion auxiliar para declarar una variable.
def assign_aux(id, value):
    if id in variables:
        if equalsType(variables.get(id), value):
            setVariable(id, value)
            return getVariable(id)
        else:
            tipo = type(value)
            if value: tipo = list
            print("ERROR in line {2}! \"{0}\" is already {1}.".format(id, tipo, "LINE_NUMBER"))
    else:
        setVariable(id, value)
        return getVariable(id)


# Valida si una variable es del tipo del segundo parametro de entrada.
def ifType(var1, tipo):
    return type(var1) == tipo


# Valida si dos variables son del mismo tipo.
def equalsType(var1, var2):
    return type(var1) == type(var2)


# Guarda la variable en el diccionario.
def setVariable(id, value):
    if value is not None:
        variables[id] = value


# Get de la variable en el diccionario.
def getVariable(id):
    return variables.get(id, None)  # Retorna none en caso de que no exista el key.


# Expresion para la determinar el valor de una variable.
def p_value(p):
    """ value : INT
              | BOOLEAN
              | ID
              | STRING
              | lista
   """
    if isDeclared(p[1], "LINE_NUMBER"):
        p[0] = variables.get(p[1])
    else:
        p[0] = p[1]


# Expresion para consultar el tipo de una variable.
def p_type(p):
    """
        statement : TYPE PARENTESISIZQ ID PARENTESISDER
    """
    if isDeclared(p[3], "LINE_NUMBER"):
        var = variables.get(p[3])
        if isinstance(var, bool):
            p[0] = bool
        elif isinstance(var, int):
            p[0] = int
        else:
            print("ERROR in type!")


# Verifica si ID existe en el diccionario.
def isDeclared(var, line):
    # Si el valor es una instancia de ID.
    if not isinstance(var, str):
        return False
    # Si no existe el ID dentro del diccionario, return false.
    if variables.get(var) is None:
        errors_list.append("ERROR in line {1}! \"{0}\" is not yet defined.".format(var, line))
        return False
    return True


# # Define una una función
# def p_function_assign(p):
#     """ statement : NAME '(' NAME ')' '=' expression """
#     p[0] = p[1]

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  LISTS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


# Expresion para crear una lista, ya sea vacia o con parámetros.
def p_statement_list_assign(p):
    """ statement  :  ID IGUAL CORCHETEIZQ params CORCHETEDER
                   |  ID IGUAL CORCHETEIZQ empty CORCHETEDER
    """
    if p[4] is None:
        p[0] = assign_aux(p[1], [])
    else:
        if not checkTypeInList_aux("LINE_NUMBER", p[4], type(p[4][0])):  # Si la lista tiene distintos tipos, no se hace nada.
            return
        p[0] = assign_aux(p[1], p[4])


# Expresion para obtener o setear el valor en las posiciones del indice recibido de una lista.
def p_statement_list_index(p):
    """ statement  :  ID index
                   |  ID index IGUAL params
                   |  ID index IGUAL CORCHETEIZQ params CORCHETEDER
    """
    if not isDeclared(p[1], "LINE_NUMBER"):  # Revisar antes si existe la variable.
        return

    id = p[1]
    size = len(p)
    lst = getVariable(id)
    i, j = p[2][0], p[2][1]

    if not checkIndexRange_aux("LINE_NUMBER", lst, i):
        return  # Si el index no es valido, no hace nada.

    if size == 3:
        if j is None:  # Si es la llamada de un indice solo.
            p[0] = lst[i]
        else:  # Si es la llamada de un rango
            p[0] = lst[i:j]

    ## ASIGNACION
    var = getVariable(id)

    if not ifType(var, list):
        errors_list.append("TypeError in line {1}: \'{0}\' is not subscriptable."
                           .format(type(var), "LINE_NUMBER"))

    if size == 5:
        if not checkListValidations_aux("LINE_NUMBER", p[4], var, i):  # validaciones antes del cambio.
            return
        p[0] = var[i] = p[4][0]  # actualizar variable y salida.
    elif size == 7:
        if not checkListValidations_aux("LINE_NUMBER", p[5], var, i, j):  # validaciones antes del cambio.
            return
        p[0] = var[i:j] = p[5]  # actualizar variable y salida.


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


# Funcion auxiliar para realizar varias validaciones a la vez.
def checkListValidations_aux(line, param, var, i, j=None):
    if checkRangeConcordance_aux(line, param, i, j) and \
            checkTypeInList_aux(line, param, type(var[0])) and \
            checkIndexRange_aux(line, var, i, j):
        return True
    return False


# Función auxiliar para validar que todos los elementos de una lista corresponden al mismo tipo.
def checkTypeInList_aux(line, lst, tipo):
    if not lst:
        return True
    else:
        for i in lst:
            if type(i) != tipo:
                errors_list.append("ERROR in line {1}: \"{0}\" type does not match the type of elements in the list."
                                   .format(i, line))
                return False
    return True


# Funcion para verificar que un indice se encuentra dentro del rango indicado.
def checkIndexRange_aux(line, lst, index1, index2=None):
    if index1 >= len(lst):
        errors_list.append("ERROR in line {1}: Index \"{0}\" out of range."
                           .format(index1, line))
        return False
    elif (index2 is not None) and (index2 > len(lst)):
        errors_list.append("ERROR in line {1}: Index \"{0}\" out of range."
                           .format(index2, line))
        return False
    else:
        return True


# Funcion auxiliar para verificar la cantidad de parametros coincide con los indices.
def checkRangeConcordance_aux(line, params, i, j):
    if (j is None) and (len(params) == 1):
        return True
    elif len(params) == (j - i):
        return True
    else:
        errors_list.append("IndexError in line {0}: The number of parameters does not match that of the indexes."
                           .format(line))
        return False


# Expresion para crear lista con range.
def p_statement_list_range(p):
    """ statement : ID IGUAL LIST PARENTESISIZQ RANGE PARENTESISIZQ INT COMA value PARENTESISDER PARENTESISDER """
    tmp = []
    for i in range(p[7]):
        tmp.append(p[9])
    p[0] = assign_aux(p[1], tmp)


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  ARITHMETIC OPERATIONS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


# Expresiones entre paréntesis
def p_expression_op(p):
    """
    expression   : expression RESTA expression
                 | expression SUMA expression
                 | expression DIVISIONENTERA expression
                 | expression DIVISION expression
                 | expression MULTIPLICACION expression
                 | expression MODULO expression
                 | expression EXPONENTE expression
    """
    # Suma
    if p[2] == '+':
        p[0] = p[1] + p[3]

    # Resta
    elif p[2] == '-':
        p[0] = p[1] - p[3]

    # Multiplicación
    elif p[2] == '*':
        p[0] = p[1] * p[3]

    # División
    elif p[2] == '/':
        p[0] = p[1] / p[3]

    # División entera
    elif p[2] == '//':
        p[0] = p[1] // p[3]

    # Modullo
    elif p[2] == '%':
        p[0] = p[1] % p[3]

    # Exponente
    elif p[2] == '^':
        p[0] = pow(p[1], p[3])


# Número negativo
def p_expression_uminus(p):
    'expression : RESTA expression %prec UMENOS'
    p[0] = -p[2]


# Expresiones entre paréntesis
def p_factor_expr(p):
    'expression : PARENTESISIZQ expression PARENTESISDER'
    p[0] = p[2]


# Expresion para definir un término.
def p_expression_num(p):
    'expression : INT'
    p[0] = p[1]


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  ERRORS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


# Error rule for syntax errors.
def p_error(p):
    # print(p)
    print("✘ Syntax error in input", p.type)
    parser.errok()
    # # Reinicia el parser
    # parser.restart()


# Función para revisar si hay una variable
def revisar_variable(a):
    var_local = False
    var_global = False

    # Si la variable ya existe, le cambia el valor
    if a in variables:
        var_global = True

    # Si la variable ya existe, le cambia el valor
    elif a in variables:
        var_local = True

    # Si la variable no existe en ninguna lista
    else:
        return False

    # Si se encontró en la lista de variables globales
    if var_global == True:
        return variables[a]

    # Si se encontró en la lista de variables locales
    if var_local == True:
        return variables[a]



# Build the parser.
parser = yacc.yacc()

while True:
    while True:
        try:
            question = raw_input('>>> ')
        except:
            question = input('>>> ')

        answer = parser.parse(question)
        if answer is not None:
            print("Result: ", answer[0])

    ################################## MAIN #################################



