# from Syntax_Analysis import result
# from Syntax_Analysis import errors

from Syntax_Analysis import run_syntax_analysis
import copy
import pprint
import ast

# Lista de arboles sintacticos generados en el analisis sintactico
sintacticList = []

# Errores generados en el analisis sintactico
errorList = []

# Codigo main
main_code = []

# Lista de variables globales
global_variables = {}

# Diccionario de diccionarios de variables locales
local_variables = {}

# Lista de blinks activos
blink_list = []

# Lista de procedimientos secundarios
procedures_list = []

# Diccionario para acciones con dict
accionesConDict = ['=', '[]', '[]*']

# Matriz actual
matriz = [[False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False]]

# Lista de instrucciones que ejecutara el arduino
instrucciones = []

# Pretty print para impresiones mas claras
pp = pprint.PrettyPrinter(indent=1, width=150)


# Funcion para obtener una de las variables del dictionario recibido
def getVariable(key, procedure):
    '''
    Funcion que retorna el valor de un key en el diccionario recibido, si no se encuentra en
    el diccionario recibido se busca en el diccionario global.
    :param key: key de la variable en el diccionario
    :param procedure: diccionario en donde se debe buscar
    :return: Value del key correspondiente, si no se encuentra retorna None.
    '''

    # print("Procedure", procedure)

    if procedure.lower() == "main":
        if key in global_variables.keys():
            return global_variables.get(key)
    else:
        print("Key", key)
        print("Procedure", procedure)
        if key in local_variables[procedure].keys():
            return local_variables[procedure].get(key)
        elif key in global_variables.keys():
            return global_variables.get(key)

    return None


# Funcion para asignar a una variables del dictionario recibido
def setVariable(procedure, key, value):
    if procedure.lower() == "main":
        global_variables[key] = value
    else:
        local_variables[procedure][key] = value


# Verifica si ID existe en el diccionario.
def isGlobalDeclared(var, variables_dic):
    # Si existe el ID dentro del diccionario, return true.
    if getVariable(var, variables_dic) is None:
        return False
    return True


# Funcion auxiliar para comparar una variable con un tipo primitivo.
def equalsType(var, tipo):
    if type(var) == tipo:
        return True
    return False


arithmetic_operators = ['+', '-', '*', '/', '//', '%', '^']
sublist_operators = ['row', 'row,col', 'col', 'sublist']


def get_var(line, var, varDict):
    val = getVariable(var, varDict)
    if val is None:
        errorList.append("ERROR in line {0}! \"{1}\" is not yet defined.".format(line, var))
    # print("Val", val)
    return val


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●      OPERACIONES ARITMETICAS        ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def arithmetic_operation(line, operator, a, b, procedure):
    '''
    Funcion auxiliar para operar los calculos aritmeticos por aparte.
    Funciona como switch case para la operacion que se debe realizar.
    :param line: linea en donde se encuentra el lector.
    :param operator: operacion que se debe realizar
    :param a: expresion uno
    :param b: expresion dos
    :return: el resultado de aplicar el operando a ambas expresiones recibididas.
    '''

    # Si es una variable.
    tmpa = a
    tmpb = b

    if type(a) == str:
        tmpa = [line, 'var', a]
    a = tmpa

    if type(b) == str:
        tmpb = [line, 'var', b]
    b = tmpb


    a = exe_orden(a, procedure)
    b = exe_orden(b, procedure)

    if a is None or b is None:
        return None



    # print("Este es a:", a)
    # print("Este es b:", b)

    if operator == '+':
        return a + b

    elif operator == '-':
        return a - b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b
    elif operator == '//':
        return a // b
    elif operator == '%':
        return a % b
    elif operator == '^':
        return pow(a, b)
    else:
        errorList.append("ArithmeticError in line {0}!".format(line))
        return "Error aritmetico"


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●      ASIGNACION DE VARIABLES        ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def var_assign_operation(line, procedure, ID, value):
    '''
    Funcion que asigna una variable y realiza las verificaciones necesarias.
    :param line: linea en donde se encuentra el lector.
    :param ID:  lista de los ids o ID individual
    :param value:  lista de los valores o valor individual.
    :param procedure: diccionario en donde se está trabajando la asignación.
    :return: asignacion de la variable deseada en el diccionario deseado.
    '''
    # Si es más de una variable.
    if type(ID) == list and type(value) == list:
        return var_assign_operation_aux(line, procedure, ID, value)
    print("▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ", ID, value)

    # Si es una sola variable.
    tmp = individual_assign_validation(line, procedure, ID, value)
    print("▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ", tmp)
    if tmp is None:
        return None

    # Asignación
    print("SALIDA is:", tmp)

    if type(tmp[0]) == str:
        key = tmp[0]
        val = tmp[1]
        setVariable(procedure, key, val)
        return getVariable(ID, procedure)
    else:
        return None


# Funcion para operar la asignacion de las variables.
def var_assign_operation_aux(line, procedure, ID, value):
    # print("id: " + ID)

    # Si es más de una variable.
    # [line, '=', [ID1,ID2,..., IDn], [val1,val2,..., valn], dict]
    if type(ID) == list and type(value) == list:

        # Validaciones.
        if not multi_assign_validation(line, procedure, ID, value):
            # Error se agrega en la funcion anterior.
            return False

        # Asignacion en cascada.
        for i in range(len(ID)):
            tmp = var_assign_operation(line, procedure, ID[i], value[i])
            if tmp is None:
                return None
        return True

    # Si es solo una variable.
    # [line, ID, value, dict]
    else:
        return individual_assign_validation(line, procedure, ID, value)


def individual_assign_validation(line, procedure, ID, value):
    '''
    Funcion para verificar la asignacion de las variables individualmente.
    :param line: linea en donde se encuentra el lector.
    :param ID:  lista de los ids o ID individual
    :param value:  lista de los valores o valor individual.
    :param procedure: diccionario en donde se está trabajando la asignación.
    :return: lista con ID y value si se cumplen todas las verificaciones, False en caso contrario.
    '''

    # A = None
    #     # A = B
    #     # A = 1
    #     # A = [1]
    #     # A = B[2] -> (B, [1,2,3...])
    #     # A[2] =  B[2] -> (B, [1,2,3...])

    # Si es una asignacion a una sublista.
    if type(ID) == list:
        return sublist_assign(ID, procedure, exe_orden(value, procedure))

    # Si la variable es una lista, obtener el valor si es una operacion.
    if type(value) == list:
        value = exe_orden(value, procedure)

    # Si no es una variable valida.
    if not var_verification(line, procedure, ID, value):
        # El error se agrega en la verificacion.
        return None

    # Si se cumplen todas las validaciones.
    # print("-> {0} : {1}".format(ID, procedure[ID]))
    print("▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ", ID, value)
    return [ID, value]


def get_sublist(procedure, sublist):
    # print("P  :", sublist)
    return sublist_assign(procedure, sublist, None)


def sublist_assign(procedure, sublist, value=None):
    '''
    Auxiliar para verificar la asignacion de las variables a una sublista.
    :param sublist: sublista de entrada
    :param value:  lista de los valores o valor individual.
    :param procedure: diccionario en donde se está trabajando la asignación.
    :return: lista con ID y value si se cumplen todas las verificaciones, False en caso contrario.
    '''

    # ROW ES LISTA SIEMPRE ES TAMANO 1
    # ROW COL , O ROW ROW SIEMPRE TAMANO 1
    # COL SIEMRPE ES TAMA'O 1
    # SUBLIST SUBLIST
    # SUBLIST ROW
    # SUBLIST COL

    line = sublist[0]
    ID = sublist[2]

    # Verificar que la variable existe en el diccionario recibido o en el global.
    # print("SUBLIST >> ", sublist)
    var = getVariable(ID, procedure)
    if var is None:
        if value is not None:
            errorList.append("ERROR in line {0}! \"{1}\" is not yet defined.".format(line, value))
        return False


    # Si la variable existe pero no es una lista.
    else:
        if type(var) != list:
            errorList.append("TypeError in line {0}: {1} object is not subscriptable.".format(line, var_type(var)))
            return False

    indexes = sublist[3]

    if len(indexes) == 1:
        newAssign = get_sublist_one_index(line, procedure, ID, indexes[0], value)

    # elif len(indexes) == 2:
    #     newAssign = False

    else:
        newAssign = False

    return newAssign


def get_sublist_one_index(line, procedure, ID, indexes, value):
    action = indexes[0]

    if action == 'row':
        row = indexes[1]
        return do_row(line, procedure, ID, row, value)

    elif action == 'col':
        col = indexes[1]
        return do_col(line, procedure, ID, col, value)

    elif action == 'row,col':
        row = indexes[1]
        col = indexes[2]
        return do_row_col(line, procedure, ID, row, col, value)

    elif action == 'sublist':
        start = indexes[1]
        end = indexes[2]
        return do_sublist(line, procedure, ID, start, end, value)


def do_row(line, procedure, ID, row, value=None):
    lst = getVariable(ID, procedure)

    # Verificaciones de asignacion y de llamada.
    esApto = row_verification(line, procedure, lst, row, value)

    # Si no cumple con los requisitos.
    if not esApto:
        return False

    # Si no se está asignando.
    if value is None:
        return lst[row]

    # Si es un ID, obtener el valor que corresponde.
    if type(value) == str:
        value = getVariable(value, procedure)

    # Actualizar lista.
    lst[row] = value
    return lst


def do_col(line, procedure, ID, col, value=None):
    lst = getVariable(ID, procedure)

    # Verificaciones de asignacion y de llamada.
    esApto = col_verification(line, procedure, lst, col, value)

    # Si no cumple con los requisitos.
    if not esApto:
        return False

    # Si no se está asignando.
    if value is None:
        return get_matrix_column(lst, col)

    # Si es un ID, obtener el valor que corresponde.
    if type(value) == str:
        value = getVariable(value, procedure)

    # Actualizar lista.
    lst = matrix_column_assign(lst, col, value)
    lst[col] = value
    return lst


# Funcion que retorna la lista de columnas de una matriz.
def get_matrix_column(matrix, col):
    tmp = []
    for row in matrix:
        tmp.append(row[col])
    return tmp


# Funcion que asigna los valores de columna de una matriz a otra.
def matrix_column_assign(matrix, col, new_val_list):
    for r in range(len(matrix)):
        # print(var[r][col], "|", new_val_list[r])
        matrix[r][col] = new_val_list[r]
    return matrix


def do_row_col(line, procedure, ID, row, col, value=None):
    lst = getVariable(ID, procedure)

    # Verificaciones de asignacion y de llamada.
    esApto = row_col_verification(line, procedure, lst, row, col, value)

    # Si no cumple con los requisitos.
    if not esApto:
        return False

    # Si no se está asignando.
    if value is None:
        return lst[row][col]

    # Si es un ID, obtener el valor que corresponde.
    if type(value) == str:
        value = getVariable(value, procedure)

    # Actualizar lista.
    lst[row][col] = value
    return lst


def do_sublist(line, procedure, ID, start, end, value=None):
    lst = getVariable(ID, procedure)

    # Verificaciones de asignacion y de llamada.
    esApto = sublist_verification(line, procedure, lst, start, end, value)

    # Si no cumple con los requisitos.
    if not esApto:
        return False

    # Si no se está asignando.
    if value is None:
        return lst[start:end]

    # Si es un ID, obtener el valor que corresponde.
    if type(value) == str:
        value = getVariable(value, procedure)

    # Actualizar lista.
    lst[start:end] = value
    return lst


def get_real_value(value, dct):
    if type(value) == str:
        return getVariable(value, dct)
    return value


def entry_type_verification(line, procedure, lst, ID, value):
    # Si el valor es un ID y aun no se ha creado.
    if type(value) == str:
        if not var_ID_validation(line, value, procedure):
            return False

    # Si el valor es una lista y no coincide el tipo con los elementos de la lista a la que se debe asignar.
    if type(value) == lst:
        if get_type_list_or_var(lst) != get_type_list_or_var(value):
            errorList.append(
                "TypeError in line {0}: Elements in \"{2}\" does not match the type of \"{1}\"."
                    .format(line, ID, value))
            return False

    # Si el valor no es lista y no coincide con los elementos dentro de la lista a la que se debe asignar.
    else:

        # Si es una variable, se obtiene su valor primero.
        value = getVariable(value, procedure)
        print("VAL ", value)

        # Si la variable es una lista, los elementos dentro deben cumplir con el tipo.
        if list_check_type_validation(line, value):
            if get_type_list_or_var(lst) != get_type_list_or_var(value):
                errorList.append("TypeError in line {0}: \"{2}\" does not match the type of elements in \"{1}\"."
                                 .format(line, ID, value))
                return False
        else:
            return False

    return True


def row_verification(line, procedure, lst, row, ID=None, value=None):
    '''
    # Funcion que verifica el indice de fila en una lista.
    :param line: linea en donde se encuentra el lector.
    :param lst: lista a analizar.
    :param row: columna en la que se debe sustituir
    :param value: Entrada que se debe validar
    :param ID: ID de la variable que se debe validar la entrada
    :return: True si se cumplen todas las verificaciones, False en caso contrario.
    '''

    if row >= len(lst):
        errorList.append("LenError in line {0}: Index \"{1}\" out of range.".format(line, row))
        return False

    # Validaciones de la entrada
    if value is not None:
        if not entry_type_verification(line, procedure, lst, ID, value):
            return False

    return True


def col_verification(line, procedure, lst, col, ID=None, value=None):
    '''
    Funcion que verifica el indice de columna en una lista.
    :param procedure: dictionario que se debe utilizar
    :param line: linea en donde se encuentra el lector.
    :param lst: lista a analizar.
    :param col: columna en la que se debe sustituir
    :param value: Entrada que se debe validar
    :param ID: ID de la variable que se debe validar la entrada
    :return: True si se cumplen todas las verificaciones, False en caso contrario.
    '''

    if type(lst[0]) != lst:
        errorList.append("TypeError in line {0}: {1} object is not subscriptable.".format(line, var_type(lst)))
        return False

    if col >= len(lst[0]):
        errorList.append("LenError in line {0}: Index \"{1}\" out of range.".format(line, col))
        return False

    # Validaciones de la entrada.
    if value is not None:
        if not entry_type_verification(line, procedure, lst, ID, value):
            return False

        if type(value) != list:
            if len(lst) != 1:
                errorList.append("IndexError in line {0}: Assignment \"{1}\" must match the number of columns in {2}."
                                 .format(line, value, ID))
                return False
        else:
            if len(value) != len(lst):
                errorList.append("IndexError in line {0}: Assignment \"{1}\" must match the number of columns in {2}."
                                 .format(line, value, ID))
                return False

    return True


def row_col_verification(line, procedure, lst, row, col, ID=None, value=None):
    '''
    Funcion que verifica los indices fila y columna de una matriz.
    :param value: Entrada que se debe validar
    :param ID: ID de la variable que se debe validar la entrada
    :param line: linea en donde se encuentra el lector.
    :param lst: lista a analizar.
    :param row: fila en la que se debe buscar
    :param col: columna en la que se debe buscar
    :return: True si se cumplen todas las verificaciones, False en caso contrario.
    '''
    if type(lst[0]) != list:
        errorList.append("TypeError in line {0}: {1} object is not subscriptable.".format(line, var_type(lst)))
        return False

    if row >= len(lst):
        errorList.append("LenError in line {0}: Index \"{1}\" out of range.".format(line, row))
        return False

    if col >= len(lst):
        errorList.append("LenError in line {0}: Index \"{1}\" out of range.".format(line, col))
        return False

    # Validaciones de la entrada
    if value is not None:
        if not entry_type_verification(line, procedure, lst, ID, value):
            return False

    return True


def sublist_verification(line, procedure, lst, start, end, ID=None, value=None):
    if end < start:
        errorList.append("RangeError in line {0}: Index 'start' cannot be greater than 'end'.".format(line, start))
        return False
    if start >= len(lst):
        errorList.append("LenError in line {0}: Index \"{1}\" out of range.".format(line, start))
        return False
    if end >= len(lst):
        errorList.append("LenError in line {0}: Index \"{1}\" out of range.".format(line, end))
        return False

    # Validaciones de la entrada
    if value is not None:
        if not entry_type_verification(line, procedure, lst, ID, value):
            return False

        distance = end - start
        if type(value) != list:
            if distance != 1:
                errorList.append(
                    "RangeError in line {0}: The range between index must be equal to the number of elements."
                        .format(line))
                return False
        elif distance != len(value):
            errorList.append(
                "RangeError in line {0}: The range between index must be equal to the number of elements.".format(line))
            return False

    return True


def ID_a_sublist(line, ID, value, procedure_name):
    val = exe_orden(value, procedure_name)
    var = getVariable(ID, procedure_name)

    if var is None:
        setVariable(procedure_name, ID, val)
        return True


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●      VALIDACIONES DE VARIABLES      ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def multi_assign_validation(line, ids, values, procedure):
    '''
    Funcion para verificar que la lista de IDS y VALUES corresponden al mismo tamaño,
    conservan los mismos tipos y que cada ID es unico.
    :param line: linea en donde se encuentra el lector.
    :param ids: lista de los ids.
    :param values: lista de los valores.
    :param procedure: diccionario en donde se está trabajando la asignación.
    :return: True si se cumplen todas las verificaciones, False en caso contrario.
    '''

    # Number of values must match the numbers of ids.
    if len(ids) != len(values):
        errorList.append("LenError in line {0}! The number of values does not match the number of IDs.".format(line))
        return False

    # All values type must be the same.
    if not list_check_type_validation(line, values):
        errorList.append("TypeError in line {0}! All values type must be the same.".format(line))
        return False

    # IDs must be unique.
    for ID in ids:
        if ID in procedure.keys():
            text = "TypeError in line {1}! \"{0}\" is already declared.".format(ID, line)
            errorList.append(text)
            return False
    return True


# Funcion auxiliar para verificar una reasignacion de la variable.
def var_verification(line, procedure, ID, value):
    '''
    Funcion auxiliar para verificar una asignacion o reasignacion de la variable.
    :param line: linea en donde se encuentra el lector.
    :param ids: lista de los ids.
    :param values: lista de los valores.
    :param procedure: diccionario en donde se está trabajando la asignación.
    :return: False si no se cumple alguna de las validaciones, True en caso contrario.
    '''
    # CHECK VALUE...

    # Si value es un string.
    if type(value) == str:
        # Si el valor es un ID y aun no se ha creado
        print("Value", procedure)
        print("Val12 ", value)
        if not isGlobalDeclared(value, procedure):
            errorList.append("ERROR in line {0}! \"{1}\" is not yet defined.".format(line, value))
            return False

        # CHECK ID...

        # Si el tipo de ambas variables no coincide.
        else:
            if getVariable(ID, procedure) is not None:
                if type(getVariable(ID, procedure)) != type(getVariable(value, procedure)):
                    errorList.append("TypeError in line {0}! The type of \"{2}\" does not match the type of {1}."
                                     .format(line, ID, value))

    # CHECK ID...

    # Si el tipo del ID y la variable no coincide.
    if getVariable(ID, procedure) is not None:
        if type(getVariable(ID, procedure)) != type(value):
            errorList.append("TypeError in line {0}! The type of \"{2}\" does not match the type of {1}."
                             .format(line, ID, value))
            return False

    # Si pasa lo anterior significa que es una nueva variable.
    # Si es una lista y no cumple con los tipos iguales.
    if not list_check_type_validation(line, value):
        return False

    if value is None:
        return False
    return True


def var_ID_validation(line, value, procedure):
    # Si value es un string.
    if type(value) == str:
        # Si el valor es un ID y aun no se ha creado
        if not isGlobalDeclared(value, procedure):
            errorList.append("ERROR in line {0}! \"{1}\" is not yet defined.".format(line, value))
            return False
    return True


def var_type(var):
    '''
    Funcion auxiliar para obtener el tipo de una variable en string.
    :param var: variable
    :return: el tipo de la variable en string.
    '''
    if equalsType(var, bool):
        return 'bool'
    elif equalsType(var, int):
        return 'int'
    elif equalsType(var, list):
        return 'list'
    elif equalsType(var, str):
        return 'str'
    elif equalsType(var, None):
        return 'NoneType'
    else:
        print("ERROR in type!")


def list_check_type_validation(line, lst):
    '''
    Función para validar que todos los elementos de una lista de listas anidadas corresponden al mismo tipo.
    :param line: linea en donde se encuentra el lector.
    :param lst: lista de entrada
    :return: False si no se cumple alguna de las validaciones, True en caso contrario.
    '''
    # If not a list or list is empty.
    if not equalsType(lst, list) or not lst:
        return True

    # If its not a list of lists.
    if not equalsType(lst[0], list):
        return check_type_aux(line, lst)

    # If its a list of lists.
    else:
        # Get the type that all items in the list are supposed to be.
        supposedType = get_type_list_or_var(lst)
        return list_check_type_validation_aux(line, lst, supposedType)


def list_check_type_validation_aux(line, lst, supposedType):
    '''
    Función auxiliar que valida que todos los elementos de una lista de listas anidadas corresponden al mismo tipo.
    :param line: linea en donde se encuentra el lector.
    :param lst: lista de entrada
    :param supposedType: el tipo del primer elemento de la lista.
    :return: False si no se cumple alguna de las validaciones, True en caso contrario.
    '''
    for i in range(len(lst)):
        sublist = lst[i]

        # If its a sublist.
        if equalsType(sublist, list):
            # If all elements are type list.
            if check_type_aux(line, sublist):
                if not list_check_type_validation_aux(line, sublist, supposedType):
                    return False

        # If its an int or bool.
        else:
            # If all elements are the same type.
            if check_type_aux(line, lst):
                return True
            return False
    return True


def check_type_aux(line, lst, supposedType=None):
    '''
    Función auxiliar que valida que todos los elementos de una lista corresponden al mismo tipo.
    :param line: linea en donde se encuentra el lector.
    :param lst: lista de entrada
    :param supposedType: el tipo del primer elemento de la lista.
    :return: False si no se cumple alguna de las validaciones, True en caso contrario.
    '''
    # If not a list or list is empty.
    if not equalsType(lst, list) or not lst:
        return True

    # Get the type that all items in the list are supposed to be.
    if supposedType is None:
        supposedType = type(lst[0])

    for i in lst:
        if not equalsType(i, supposedType):
            text = "TypeError in line {1}: \"{0}\" type does not match the type of elements.".format(i, line)
            errorList.append(text)
            return False
    return True


def get_type_list_or_var(lst):
    '''
    Funcion auxiliar para obtener el primer elemento de una lista que no sea una sublista.
    :param lst: lista de entrada
    :return: el tipo al que corresponde el primer elemento de la lista.
    '''
    if equalsType(lst, list):
        return get_type_list_or_var(lst[0])
    return type(lst)


""" ################################ COMPROBACIONES INICIALES #################################################### """


def validate_iterable_for(iterable, procedure_name):
    if type(iterable) == int or type(iterable) == list:
        return True
    elif type(iterable) == str:
        var = buscar_variable(iterable, procedure_name)
        if var is not None:
            return True
        else:
            errorList.append("ERROR: el iterable no existe")
    errorList.append("ERROR: el iterable del for debe ser una lista o un entero")
    return False


def get_var_for_type(iterable):
    if type(iterable) == int:
        return "INT"
    elif type(iterable) == list:
        if len(iterable) > 0:
            if type(iterable[0]) == int:
                return "INT"
            elif type(iterable[0]) == bool:
                return "BOOL"
    return None


""" ############################################################################################################### """

""" ###################################### Ciclos y Bifurcacion ################################################### """


def ciclo_for(temp_var, iterable, step, ordenes, procedure_name):
    """
    Ejecuta el ciclo for
    :param temp_var: variable que cambiará
    :param iterable: estructura usada para recorrer, normalmente será una lista, pero puede ser un entero (igual que range)
    :param step: incremento, por defecto es 1
    :param ordenes: ordenes que se ejecutaran
    :return: None
    """

    if not validate_iterable_for(iterable, procedure_name):
        return

    if type(iterable) == str:
        iterable = buscar_variable(iterable, procedure_name)

    if iterable is None:
        errorList.append("Error, la variable del iterable no existe")
        return

    var = buscar_variable(temp_var, procedure_name)

    if var is None:
        print("La variable de cambio no se ha encontrado, se procede a crearla")
        tipo_var = get_var_for_type(iterable)
        if tipo_var == "INT":
            exe_orden([0, "=", temp_var, None], procedure_name)
        elif tipo_var == "BOOL":
            exe_orden([0, "=", temp_var, None], procedure_name)

    if step == 1:
        if isinstance(iterable, list):
            for var in iterable:

                tipo_var = get_var_for_type(iterable)
                if tipo_var == "INT":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                elif tipo_var == "BOOL":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                exe_ordenes(ordenes, procedure_name)

        elif isinstance(iterable, int):
            for var in range(iterable):
                tipo_var = get_var_for_type(iterable)
                if tipo_var == "INT":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                elif tipo_var == "BOOL":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                exe_ordenes(ordenes, procedure_name)
    else:
        if isinstance(iterable, list):

            for var in iterable[::step]:
                tipo_var = get_var_for_type(iterable)
                if tipo_var == "INT":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                elif tipo_var == "BOOL":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                exe_ordenes(ordenes, procedure_name)

        elif isinstance(iterable, int):

            for var in range(0, iterable, step):
                tipo_var = get_var_for_type(iterable)
                if tipo_var == "INT":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                elif tipo_var == "BOOL":
                    exe_orden([0, "=", temp_var, var], procedure_name)
                exe_ordenes(ordenes, procedure_name)

    if procedure_name == "Main" and temp_var in global_variables.keys():
        del global_variables[temp_var]
    elif procedure_name != "Main":
        dict = local_variables[procedure_name]
        if temp_var in dict.keys():
            del dict[temp_var]


def bifurcacion(iterable, operator, value, ordenes, procedure_name):
    """
    Ejecuta el condicional if
    :param iterable: estructura que sera utilizada para realizar la validacion, puede ser variable o lista
    :param operator: operador de comparacion, ( == , <, <=, >, >=)
    :param value: puede ser numero, o bool
    :return: bool
    """
    print()
    print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
    print(" ✱ EJECUTANDO IF: ", "if {0}".format(iterable), operator, str(value))

    if isinstance(iterable, list):

        flag = True

        for x in iterable:

            if operator == '==':
                if not x == value:
                    flag = False
            elif operator == '<':
                if not x < value:
                    flag = False
            elif operator == '<=':
                if not x <= value:
                    flag = False
            elif operator == '>':
                if not x > value:
                    flag = False
            elif operator == '>=':
                if not x >= value:
                    flag = False
            elif operator == '<>':
                if not x != value:
                    flag = False

        if flag:
            print("\t ◖ ejecutando ordenes:  IF")
            exe_ordenes(ordenes, procedure_name)
            print("\t ◗ finalizadas ordenes: IF")
            print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")

        else:
            print("\t ✘ NO se ha cumplido: IF")
            print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
            return

    elif isinstance(iterable, int) or isinstance(iterable, bool):

        flag = False

        if operator == '==':
            if iterable == value:
                exe_ordenes(ordenes, procedure_name)

        elif operator == '<':
            if iterable < value:
                flag = True

        elif operator == '<=':
            if iterable <= value:
                flag = True

        elif operator == '>':
            if iterable > value:
                flag = True

        elif operator == '>=':
            if iterable >= value:
                flag = True

        elif operator == '<>':
            if iterable != value:
                flag = True

        if flag:
            print("\t ◖ ejecutando ordenes:  IF")
            exe_ordenes(ordenes, procedure_name)
            print("\t ◗ finalizadas ordenes: IF")
            print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")

        else:
            print("\t ✘ NO se ha cumplido: IF")
            print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
            return


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●        EJECUCION PRINCIPAL          ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def main_execute():
    print("\n\n◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆"
          " EJECUTANDO PROCEDURE: Main ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆\n\n")
    exe_ordenes(main_code, "Main")
    print("\n◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆"
          " FIN Main ◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆\n")
    print()


def procedure_execute(nombre, params):
    print()
    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
    # print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")

    print(" ➽ EJECUTANDO PROCEDURE:", nombre)
    print("\t↪ params: ", params)
    print()

    print("\t ◖ ejecutando ordenes de : ", nombre)

    for procedure in sintacticList:
        if procedure[2] == nombre:
            exe_ordenes(procedure[4], nombre)

    print("\t ◗ finalizadas ordenes de :", nombre)
    print("★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★")
    # print("••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••")
    print()


def buscar_variable(id, procedure_name):
    var = getVariableFromDict(id, procedure_name)
    if var is None:
        print("Busqueda sin resultados, la variable no se encuentra declarada globalmente ni localmente")
    return var


"""
Busca una variable:
Primero busca si esta en las variables globales
Si no la encuentra y no es el main, la busca localmente
"""


# Funcion para obtener una de las variables del dictionario recibido
def getVariableFromDict(key, procedure):
    '''
    Funcion que retorna el valor de un key en el diccionario recibido, si no se encuentra en
    el diccionario recibido se busca en el diccionario global.
    :param key: key de la variable en el diccionario
    :param procedure: diccionario en donde se debe buscar
    :return: Value del key correspondiente, si no se encuentra retorna None.
    '''

    # print("Procedure", procedure)

    if procedure.lower() == "main":
        if key in global_variables.keys():
            return global_variables.get(key)
    else:
        if key in local_variables[procedure].keys():
            return local_variables[procedure].get(key)
        elif key in global_variables.keys():
            return global_variables.get(key)
    return None


def buscar_valor_param(value, procedure_name):
    if type(value) == str:

        var = buscar_variable(value, procedure_name)

        if var is None:
            errorList.append("Error, no se ha encontrado la variable {0}".format(value))
        else:
            return var


    elif value is None:
        errorList.append("Error, el valor del parametro es None")
    else:
        return value


def exe_ordenes(ordenes, procedure_name):
    for orden in ordenes:
        print()
        print("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯")
        result = exe_orden(orden, procedure_name)

        if result is None:
            print('[ERROR]  \t➤\t', orden[1])
            continue
        # print("☀ Resultado:\t", exe_orden(orden, procedure_name))
        print("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯")



def exe_orden(tree, procedure_name):
    global arithmetic_operators

    if equalsType(tree, list):

        # No corresponden a un arbol.
        if len(tree) == 1:
            return tree

        print("◉ EJECUTANDO\t• • • • •\t{0}".format(tree))
        # print("◉ EJECUTANDO ", tree[1], "\t  • • • • •  \t", tree)
        # """   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●  VARIABLES Y OPERACIONES ARITMETICAS  ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●  """

        if tree[1] in arithmetic_operators:  # OPERACIONES ARITMETICAS
            return arithmetic_operation(tree[0], tree[1], tree[2], tree[3], procedure_name)


        elif tree[1] == '=':
            a = var_assign_operation(tree[0], procedure_name, tree[2], tree[3])
            # print("----------------FIN DE DECLARACION------------------\n")
            if a is None or a is False:
                return None
            print("[EJECUTADO CORRECTAMENTE]\t➤\t", "DECLARATION     ", "\t→\t", tree)
            return getVariable(tree[2], procedure_name)

        elif tree[1] == 'var':  # DEFINIR UNA VARIABLE
            return get_var(tree[0], tree[2], procedure_name)



        elif tree[1] == '=sublist':
            ID_a_sublist(tree[0], tree[2], tree[3], procedure_name)

        # """   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●  LISTA Y MATRICES   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●  """

        elif tree[1] == '[]':
            lst = get_sublist(procedure_name, tree)
            if lst is None:
                return None
            print("[EJECUTADO CORRECTAMENTE]\t➤\t", "[]              ", "\t→\t", lst)
            return lst


        elif tree[1] == '[]*':
            return var_assign_operation(tree[0], procedure_name, tree[2], tree[3])


        elif tree[1] == 'LEN':
            return exe_len_operation(tree[0], tree[2], procedure_name)


        elif tree[1] == 'RANGE':  ## ESTE ES EL RANGEEEEEEEEEEEEEEEEEEEEE
            return exe_range_operation(tree[0], tree[2], tree[3], procedure_name)


        elif tree[1] == 'INSERT_LIST':  # [line, 'INSERT_LIST', lista, num, bool] ## IMPLEMENTAAAAAAAAAAAAAAAAAAAR
            return exe_insert_listas_operation(tree, procedure_name)


        elif tree[1] == 'DELETE_LIST':  ## del para listas
            return exe_del_listas_operation(tree[0], tree[2], tree[3], procedure_name)



        elif tree[1] == 'NEG':
            """        
            matriz.Neg;
            matriz[1].Neg;
            matriz[1][1].Neg;
            [4, 'NEG', 'matriz'],
            [5, 'NEG', 'matriz', 1],
            [6, 'NEG', 'matriz', 1, 1]
            """
            print(tree, "  ----->   NEG")
            exe_neg(tree, procedure_name)


        elif tree[1] == 'T':
            """
            lista.T;
            lista[1].T;
            lista[1][1].T;
            [11, 'T', 'lista'],
            [12, 'T', 'lista', 1],
            [13, 'T', 'lista', 1, 1],
            """
            print(tree, "  ----->   T")
            exe_T(tree, procedure_name)


        elif tree[1] == 'F':
            """
            lista.F;
            lista[1].F;
            lista[1][1].F;
            [14, 'F', 'lista'],
            [15, 'F', 'lista', 1],
            [16, 'F', 'lista', 1, 1],
            """
            print(tree, "  ----->   F")
            exe_F(tree, procedure_name)


        elif tree[1] == 'SHAPEF':
            """
            matriz.shapeF;
            [37, 'SHAPEF', 'matriz']
            """
            print(tree, "  ----->   SHAPEF")


        elif tree[1] == 'SHAPEC':
            """
            matriz.shapeC;
            [39, 'SHAPEC', 'matriz']
            """
            print(tree, "  ----->   SHAPEC")


        elif tree[1] == 'INSERT_MATRIX':

            return exe_insert_matrix_operation(tree, procedure_name)



        elif tree[1] == 'DELETE_MATRIX':
            """
            matriz.delete(0,0);
            [45, 'DELETE_MATRIX', 'matriz', 0, 0],
            """
            print(tree, "  ----->   DELETE_MATRIX")


        elif tree[1] == '=sf':
            """
            a = matriz.shapeF;
            [37, 'sf', 'a', 'matriz']
            """
            print(tree, "  ----->   DELETE_MATRIX")
            exe_def_shapef(tree, procedure_name)


        elif tree[1] == '=sc':
            """
            a = matriz.shapeC;
            [37, 'sc', 'a', 'matriz']
            """
            print(tree, "  ----->   DELETE_MATRIX")
            exe_def_shapec(tree, procedure_name)




        # """   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●  FUNCIONES   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●   ●  """

        elif tree[1] == 'CALL':
            print("[EJECUTADO CORRECTAMENTE]\t➤\t", "CALL     ", "\t→\t", tree)
            procedure_execute(tree[2], tree[3])


        elif tree[1] == 'BLINK':
            print(tree, "  ----->   BLINK")


        elif tree[1] == 'DELAY':
            exe_delay(buscar_valor_param(tree[2], procedure_name), tree[3])
            print("[EJECUTADO CORRECTAMENTE]\t➤\t", "DELAY     ", "\t→\t", tree)


        elif tree[1] == 'PRINTLED':
            exe_print_led(buscar_valor_param(tree[2], procedure_name), buscar_valor_param(tree[3], procedure_name),
                          buscar_valor_param(tree[4], procedure_name), procedure_name)

            print("[EJECUTADO CORRECTAMENTE]\t➤\t", "PRINTLED  ", "\t→\t", tree)
            print()


        elif tree[1] == 'PRINTLEDX':
            var = buscar_variable(tree[4], procedure_name)
            if var is not None:
                exe_print_ledx(tree[2], buscar_valor_param(tree[3], procedure_name), var)
                print("[EJECUTADO CORRECTAMENTE]\t➤\t", "PRINTLEDX ", "\t→\t", tree)
            else:
                errorList.append("Error: no se ha encontrado la variable {0}".format(tree[4]))



        elif tree[1] == 'IF':
            var = buscar_variable(tree[2][0], procedure_name)
            if var is not None:
                bifurcacion(var, tree[2][1], buscar_valor_param(tree[2][2], procedure_name), tree[3], procedure_name)
                print("[EJECUTADO CORRECTAMENTE]\t➤\t", "IF     ", "\t→\t", tree)
                print()

            else:
                errorList.append("Error: no se ha encontrado la variable {0}".format(tree[2][0]))


        elif tree[1] == 'FOR':
            ciclo_for(tree[2], tree[3], tree[5], buscar_valor_param(tree[4], procedure_name), procedure_name)
            print("[EJECUTADO CORRECTAMENTE]\t➤\t", "FOR       ", "\t→\t", tree)

    return tree


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●      METODOS DE LISTAS              ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def exe_range_operation(line, num, param, procedure_name):
    # [10, 'RANGE', expresion, params]
    num = exe_orden(num, procedure_name)
    param = exe_orden(param, procedure_name)

    if num is None:
        # errorList.append("Error en la linea {0}, no se logra procesar la operacion {1}".format(linea[0], linea[3]))
        return

    tmp = []
    i = 1
    for i in range(num):
        tmp.append(param)

    print("[EJECUTADO CORRECTAMENTE]\t➤\t", "RANGE           ", "\t→\t", tmp)
    return tmp


def exe_len_operation(line, valor, procedure_name):
    # Example [10, 'LEN', [1,2,3]]
    # Example [10, 'LEN', 'a']
    valor = exe_orden(valor, procedure_name)
    if valor is None:
        return

    return len(valor)

def exe_insert_matrix_operation(tree, procedure_name):
    """
    matriz.insert(a, b, c);
    matriz.insert(a, d);
    [41, 'INSERT_MATRIX', 'matriz', 'a', 'b', 'c'],
    [43, 'INSERT_MATRIX', 'matriz', 'a', 'd'],
    [p.lineno(1), 'INSERT_MATRIX', ID, params, tipo insercion, indice]
    """
    line = tree[0]
    ID = tree[2]
    value = exe_orden([line, "var", tree[2]], procedure_name)
    params = exe_orden(tree[3], procedure_name)
    tipo = exe_orden(tree[4], procedure_name)
    indice = exe_orden(tree[5], procedure_name)


    print("\t➤ CASTEO: ", line, ID, value, params, tipo, indice)

    print(tree, "  ----->   INSERT_MATRIX")
    return None




def exe_insert_delete_operation(tree, procedure_name):
    """
    matriz.insert(a, b, c);
    matriz.insert(a, d);
    [41, 'INSERT_MATRIX', 'matriz', 'a', 'b', 'c'],
    [43, 'INSERT_MATRIX', 'matriz', 'a', 'd'],
    [p.lineno(1), 'INSERT_MATRIX', ID, params, tipo insercion, indice]
    """
    line = tree[0]
    ID = tree[2]
    value = exe_orden([line, "var", tree[2]], procedure_name)
    indice = exe_orden(tree[3], procedure_name)
    params = exe_orden(tree[4], procedure_name)
    # print("\t➤ CASTEO: ", line, ID, value, indice, params)

    print(tree, "  ----->   INSERT_MATRIX")
    return



def exe_insert_listas_operation(tree, procedure_name):
    """
    lista.insert(a,True);
    [24, 'INSERT_LIST', 'ID', 'a', True]
    """
    line = tree[0]
    ID = tree[2]
    value = exe_orden([line, "var", tree[2]], procedure_name)
    indice = exe_orden(tree[3], procedure_name)
    params = exe_orden(tree[4], procedure_name)

    # print("\t➤ CASTEO: ", line, ID, value, indice, params)

    if value is None:
        errorList.append("Error en la linea {0}, no se ha definidio {1}".format(line, ID))
        return None

    if indice is None:
        return

    if type(value) != list:
        errorList.append("Error en la linea {0}. {1} debe ser una lista.".format(line, ID))
        return None

    if get_type_list_or_var(value) != type(params):
        errorList.append(
            "Error en linea {0}. El valor de insercion \"{2}\" no coincide con el tipo de {1}.".format(line, ID, value))
        return None

    value.insert(indice, params)
    print("[EJECUTADO CORRECTAMENTE]\t➤\t", "INSERT_LIST     ", "\t→\t", value)
    return value



def exe_del_listas_operation(line, ID, indice, procedure_name):
    """
    lista.del(0);
    [10, 'DELETE_LIST', 'lista', 0]
    """

    value = exe_orden([line, "var", ID], procedure_name)
    indice = exe_orden(indice, procedure_name)

    # print("\t➤ CASTEO : ", line, ID, indice)

    # print("\t\t➤ ➤ ➤ ➤ ➤ ➤  1  ➤ ➤ ➤ ➤ ➤ ➤ ➤ ➤")

    # si la variable no existe
    if value is None:
        errorList.append("Error en la linea {0}, no se ha definidio {1}".format(line, ID))
        return None

    # si el indice esta fuera de cuestion
    if indice >= len(value):
        errorList.append("Error en la linea {0}. El indice {1} se encuentra fuera de rango.".format(line, indice))
        return None

    value.pop(indice)
    print("[EJECUTADO CORRECTAMENTE]\t➤\t", "DELETE_LIST     ", "\t→\t", value)
    return value


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●         METODOS DE MATRICES         ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""



def validaciones_insert_matrix(m1, m2):
    pass





# def validaciones_insert_matrix(line, ID, value, params, row, col=None):
#     # Si son matrices
#     if not is_matriz(params):
#         errorList.append("Error en la linea {0}. \'{1}\' no corresponde a una matriz".format(line, params))
#         return None
#
#     if not is_matriz(params):
#         errorList.append("Error en la linea {0}. \'{1}\' no corresponde a una matriz".format(line, ID))
#         return None
#
#     # Si el tamano de las filas no es el mismo
#     if not validaciones_insert_matrix_aux(line, ID, value, params, row):
#         errorList.append(
#             "Error en la linea {0}. El numero de filas de \'{1}\' no coincide con el de \'{2}\'".format(line, params,
#                                                                                                         ID))
#         return None
#
#     # Si hay columnas.
#     if col is not None:
#         for r in value:
#             if validaciones_insert_matrix_aux(line, ID, value[r], params[r], col) is None:
#                 errorList.append(
#                     "Error en la linea {0}. El numero de columnas de \'{1}\' no coincide con el de \'{2}\'".format(line,
#                                                                                                                    params,
#                                                                                                                    ID))
#                 return None
#
#     # value.insert(row, params)
#     # print("[EJECUTADO CORRECTAMENTE]\t➤\t", "INSERT_MATRIX     ", "\t→\t", value)
#     return True


"""
a = matriz.shapeF;
[37, 'sf', 'a', 'matriz']
"""


def exe_def_shapef(linea, procedure_name):
    id = linea[2]

    var = buscar_variable(id, procedure_name)
    mat = buscar_variable(linea[3], procedure_name)

    if mat is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la matriz {1}".format(linea[0], linea[3]))
        return

    value = exe_shapef([linea[0], linea[1], linea[3]], procedure_name)

    if var is None:
        exe_orden([0, '=', id, value], procedure_name)
    else:
        setVariable(procedure_name, id, value)


"""
matriz.shapeF;
[37, 'SHAPEF', 'matriz']
"""


def exe_shapef(linea, procedure_name):
    id = linea[2]
    var = buscar_variable(id, procedure_name)

    if var is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la variable {1}".format(linea[0], id))
        return

    if type(var) == list:

        if is_matriz(var):
            if len(var) == 0:
                errorList.append("Error en la linea {0}, la matriz {1} esta vacia".format(linea[0], id))
                return
            else:
                return len(var)
        else:
            errorList.append("Error en la linea {0}, la variable {1} no es una matriz".format(linea[0], id))
            return

    else:
        errorList.append("Error en la linea {0}, la variable {1} no es una matriz".format(linea[0], id))
        return


"""
a = matriz.shapeC;
[37, 'sc', 'a', 'matriz']
"""


def exe_def_shapec(linea, procedure_name):
    id = linea[2]

    var = buscar_variable(id, procedure_name)
    mat = buscar_variable(linea[3], procedure_name)

    if mat is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la matriz {1}".format(linea[0], linea[3]))
        return

    value = exe_shapec([linea[0], linea[1], linea[3]], procedure_name)

    if var is None:
        exe_orden([0, '=', id, value], procedure_name)
    else:
        setVariable(procedure_name, id, value)


"""
matriz.shapeC;
[39, 'SHAPEC', 'matriz']
"""


def exe_shapec(linea, procedure_name):
    id = linea[2]
    var = buscar_variable(id, procedure_name)

    if var is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la variable {1}".format(linea[0], id))
        return

    if type(var) == list:

        if is_matriz(var):

            if len(var) > 0:
                return len(var[0])
            else:
                errorList.append("Error en la linea {0}, la matriz {1} esta vacia".format(linea[0], id))
                return

        else:
            errorList.append("Error en la linea {0}, la variable {1} no es una matriz".format(linea[0], id))
            return

    else:
        errorList.append("Error en la linea {0}, la variable {1} no es una matriz".format(linea[0], id))
        return


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●        OPERACIONES BOOLEANAS        ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def is_matriz(var):
    if type(var) == list and len(var) > 0:
        if type(var[0]) is list:  # es una matriz
            return True
    return False


"""        
matriz.Neg;
matriz[1].Neg;
matriz[1][1].Neg;
[4, 'NEG', 'matriz'],        len 3
[5, 'NEG', 'matriz', 1],     len 4
[6, 'NEG', 'matriz', 1, 1]   len 5
"""


def exe_neg(linea, procedure_name):
    print("------------------- EJECUTANDO NEG ---------------------------")

    id = linea[2]
    var = buscar_variable(id, procedure_name)

    if var is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la variable {1}".format(linea[0], id))
        print("------------------------ FIN DEL NEG, SE PRODUJO UN ERROR --------------------------")
        return

    if is_matriz(var) and len(var) == 0:
        errorList.append("Error en la linea {0}, la matriz {1} esta vacia".format(linea[0], id))
        return

    if len(linea) == 3:

        if type(var) == list:
            if is_matriz(var):  # Es una matriz    FALTA IMPLEMENTAR SHAPEC Y SHAPEF

                for filas in range(len(var)):
                    for columnas in range(len(var[0])):

                        if type(var[filas][columnas]) == bool:
                            if var[filas][columnas] == True:
                                var[filas][columnas] = False
                            elif var[filas][columnas] == False:
                                var[filas][columnas] = True
                        elif type(var[filas][columnas]) == int:
                            if var[filas][columnas] == 0:
                                var[filas][columnas] = 1
                            elif var[filas][columnas] == 1:
                                var[filas][columnas] = 0
                            else:
                                errorList.append(
                                    "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(
                                        linea[0]))
                                print(
                                    "------------------------ FIN DEL NEG, SE PRODUJO UN ERROR --------------------------")


            else:  # Es una lista
                for i in range(len(var)):

                    if type(var[i]) == bool:
                        if var[i] == True:
                            var[i] = False
                        elif var[i] == False:
                            var[i] = True
                    elif type(var[i]) == int:
                        if var[i] == 1 or var[i] == 0:
                            var[i] = 0
                        else:
                            errorList.append(
                                "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(
                                    linea[0]))
                            print(
                                "------------------------ FIN DEL NEG, SE PRODUJO UN ERROR --------------------------")

        elif type(var) == int:
            if var == 1:
                setVariable(procedure_name, id, 0)
            else:
                setVariable(procedure_name, id, 1)
        elif type(var) == bool:
            if var == True:
                setVariable(procedure_name, id, False)
            else:
                setVariable(procedure_name, id, True)

    # [5, 'NEG', 'matriz', 1],     len 4
    if len(linea) == 4:
        if is_matriz(var):  # negar toda la fila

            l = linea[3]

            for index in range(len(var[0])):

                if type(var[l][index]) == int:
                    if var[l][index] == 1:
                        var[l][index] = 0
                    elif var[l][index] == 0:
                        var[l][index] = 1
                    else:
                        errorList.append(
                            "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(linea[0]))
                elif type(var[l][index]) == bool:
                    var[l][index] = not var[l][index]


        elif type(var) == list:
            if type(var[linea[3]]) == bool:
                var[linea[3]] = not var[linea[3]]
            elif type(var[linea[3]]) == int:
                if var[linea[3]] == 0:
                    var[linea[3]] = 1
                elif var[linea[3]] == 1:
                    var[linea[3]] = 0
                else:
                    errorList.append(
                        "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(linea[0]))
                    print(
                        "------------------------ FIN DEL NEG, SE PRODUJO UN ERROR --------------------------")

    # [6, 'NEG', 'matriz', 1, 1]   len 5
    if len(linea) == 5:
        if is_matriz(var):
            try:

                if type(var[linea[3]][linea[4]]) == int:
                    if var[linea[3]][linea[4]] == 1:
                        var[linea[3]][linea[4]] = 0
                    elif var[linea[3]][linea[4]] == 0:
                        var[linea[3]][linea[4]] = 1
                    else:
                        errorList.append(
                            "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(linea[0]))
                elif type(var[linea[3]][linea[4]]) == bool:
                    var[linea[3]][linea[4]] = not var[linea[3]][linea[4]]


            except Exception:
                errorList.append(
                    "Error en la linea {0}, el indice supera el limite del tamaño de la matriz {1}".format(linea[0],
                                                                                                           id))

    print("------------------- NEG EJECUTADO CORRECTAMENTE ---------------------------")


"""
lista.T;
lista[1].T;
lista[1][1].T;
[11, 'T', 'lista'],
[12, 'T', 'lista', 1],
[13, 'T', 'lista', 1, 1],
"""


def exe_F(linea, procedure_name):
    print("------------------- EJECUTANDO F ---------------------------")

    id = linea[2]
    var = buscar_variable(id, procedure_name)

    if var is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la variable {1}".format(linea[0], id))
        print("------------------------ FIN DEL F, SE PRODUJO UN ERROR --------------------------")
        return

    if is_matriz(var) and len(var) == 0:
        errorList.append("Error en la linea {0}, la matriz {1} esta vacia".format(linea[0], id))
        return

    if len(linea) == 3:

        if type(var) == list:
            if is_matriz(var):  # es una matriz

                for filas in range(len(var)):
                    for columnas in range(len(var[0])):

                        if type(var[filas][columnas]) == bool:
                            var[filas][columnas] = False
                        elif type(var[filas][columnas]) == int:
                            if var[filas][columnas] == 0 or var[filas][columnas] == 1:
                                var[filas][columnas] = 0
                            else:
                                errorList.append(
                                    "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(
                                        linea[0]))
                                print(
                                    "------------------------ FIN DEL F, SE PRODUJO UN ERROR --------------------------")

            else:  # es una lista

                for i in range(len(var)):

                    if type(var[i]) == bool:
                        var[i] = False
                    elif type(var[i]) == int and (var[i] == 1 or var[i] == 0):
                        var[i] = 0
                    else:
                        errorList.append(
                            "Error en la linea {0}, la lista {1} contiene valores que no se pueden negar".format(
                                linea[0], id))
                        print(
                            "------------------------ FIN DEL F, SE PRODUJO UN ERROR --------------------------")
                        return

                print("-------------- F ejecutado correctamente -------------")
                return

    # [12, 'T', 'lista', 1],

    if len(linea) == 4:

        if type(var) == list:
            if is_matriz(var):  # es matriz, negar toda la fila

                l = linea[3]

                for index in range(len(var[0])):

                    if type(var[l][index]) == int:
                        if var[l][index] == 1 or var[l][index] == 0:
                            var[l][index] = 0
                        else:
                            errorList.append(
                                "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(
                                    linea[0]))
                    elif type(var[l][index]) == bool:
                        var[l][index] = False


            else:  # es una lista, negar indice
                if not linea[3] >= len(var):

                    if type(var[linea[3]]) == bool:
                        var[linea[3]] = False
                    elif type(var[linea[3]]) == int and (var[linea[3]] == 1 or var[linea[3]] == 0):
                        var[linea[3]] = 0
                    else:
                        errorList.append(
                            "Error en la linea {0}, la lista {1} contiene valores que no se pueden negar".format(
                                linea[0], id))
                        print(
                            "------------------------ FIN DEL F, SE PRODUJO UN ERROR --------------------------")
                        return

                else:
                    errorList.append(
                        "Error en la linea {0}, el indice excede los limites de la lista {1}".format(linea[0],
                                                                                                     id))
                    print(
                        "------------------------ FIN DEL F, SE PRODUJO UN ERROR --------------------------")
                    return

    if len(linea) == 5:
        if is_matriz(var):
            try:

                if type(var[linea[3]][linea[4]]) == int:
                    if var[linea[3]][linea[4]] == 1 or var[linea[3]][linea[4]] == 0:
                        var[linea[3]][linea[4]] = 0
                    else:
                        errorList.append(
                            "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(linea[0]))
                elif type(var[linea[3]][linea[4]]) == bool:
                    var[linea[3]][linea[4]] = False


            except Exception:
                errorList.append(
                    "Error en la linea {0}, el indice supera el limite del tamaño de la matriz {1}".format(linea[0],
                                                                                                           id))

    print("------------------- F EJECUTADO CORRECTAMENTE ---------------------------")


"""
lista.T;
lista[1]T;
lista[1][1].T;
[14, 'T', 'lista'],
[15, 'T', 'lista', 1],
[16, 'T', 'lista', 1, 1],
"""


def exe_T(linea, procedure_name):
    print("------------------- EJECUTANDO T ---------------------------")

    id = linea[2]
    var = buscar_variable(id, procedure_name)

    if var is None:
        errorList.append("Error en la linea {0}, no se ha encontrado la variable {1}".format(linea[0], id))
        print("------------------------ FIN DEL T, SE PRODUJO UN ERROR --------------------------")
        return

    if is_matriz(var) and len(var) == 0:
        errorList.append("Error en la linea {0}, la matriz {1} esta vacia".format(linea[0], id))
        return

    if len(linea) == 3:

        if type(var) == list:
            if is_matriz(var):  # es una matriz

                for filas in range(len(var)):
                    for columnas in range(len(var[0])):

                        if type(var[filas][columnas]) == bool:
                            var[filas][columnas] = True
                        elif type(var[filas][columnas]) == int:
                            if var[filas][columnas] == 0 or var[filas][columnas] == 1:
                                var[filas][columnas] = 1
                            else:
                                errorList.append(
                                    "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(
                                        linea[0]))
                                print(
                                    "------------------------ FIN DEL T, SE PRODUJO UN ERROR --------------------------")

            else:  # es una lista

                for i in range(len(var)):

                    if type(var[i]) == bool:
                        var[i] = True
                    elif type(var[i]) == int and (var[i] == 1 or var[i] == 0):
                        var[i] = 1
                    else:
                        errorList.append(
                            "Error en la linea {0}, la lista {1} contiene valores que no se pueden negar".format(
                                linea[0], id))
                        print(
                            "------------------------ FIN DEL T, SE PRODUJO UN ERROR --------------------------")
                        return

                print("-------------- T ejecutado correctamente -------------")
                return

    # [12, 'T', 'lista', 1],

    if len(linea) == 4:

        if type(var) == list:
            if is_matriz(var):  # es matriz, negar toda la fila

                l = linea[3]

                for index in range(len(var[0])):

                    if type(var[l][index]) == int:
                        if var[l][index] == 1 or var[l][index] == 0:
                            var[l][index] = 1
                        else:
                            errorList.append(
                                "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(
                                    linea[0]))
                    elif type(var[l][index]) == bool:
                        var[l][index] = True


            else:  # es una lista, negar indice
                if not linea[3] >= len(var):

                    if type(var[linea[3]]) == bool:
                        var[linea[3]] = True
                    elif type(var[linea[3]]) == int and (var[linea[3]] == 1 or var[linea[3]] == 0):
                        var[linea[3]] = 1
                    else:
                        errorList.append(
                            "Error en la linea {0}, la lista {1} contiene valores que no se pueden negar".format(
                                linea[0], id))
                        print(
                            "------------------------ FIN DEL T, SE PRODUJO UN ERROR --------------------------")
                        return

                else:
                    errorList.append(
                        "Error en la linea {0}, el indice excede los limites de la lista {1}".format(linea[0],
                                                                                                     id))
                    print(
                        "------------------------ FIN DEL T, SE PRODUJO UN ERROR --------------------------")
                    return

    if len(linea) == 5:
        if is_matriz(var):
            try:

                if type(var[linea[3]][linea[4]]) == int:
                    if var[linea[3]][linea[4]] == 1 or var[linea[3]][linea[4]] == 0:
                        var[linea[3]][linea[4]] = 1
                    else:
                        errorList.append(
                            "Error en la linea {0}, no se puede negar un entero diferente de 1 o 0".format(linea[0]))
                elif type(var[linea[3]][linea[4]]) == bool:
                    var[linea[3]][linea[4]] = True


            except Exception:
                errorList.append(
                    "Error en la linea {0}, el indice supera el limite del tamaño de la matriz {1}".format(linea[0],
                                                                                                           id))

    print("------------------- T EJECUTADO CORRECTAMENTE ---------------------------")


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●      FUNCIONES DE ANIMACION         ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""

"""   
Blink(Fila, Columna, Tiempo, RangoTiempo, Estado)
Fila y columna: indice donde se encendera un led
Tiempo: Tiempo en el que se encenderan
RangoTiempo: "Seg", "Mil", "Min"
Estado: bool

['BLINK', f, c, int, rangotiempo, bool]
"""


def exe_blink(row, column, tiempo, rangoTiempo, estado):
    pass


def exe_delay(tiempo, rangoTiempo):
    instrucciones.append(['DELAY', rangoTiempo, tiempo])


"""   
PrintLed(Col, Row, Valor)
Col: Entero
Row: Entero
Valor: Bool
['PRINTLED', row, column, valor]
"""


def exe_print_led(row, column, value, procedure_name):
    if row <= 7 and column <= 7:

        temp = value

        if type(value) == str:
            print("VALUE ES STR")
            value = buscar_variable(value, procedure_name)

        if value is None:
            errorList.append("Error, no se ha encontrado la variable {0}".format(temp))
            return

        if value:
            matriz[row][column] = True
        else:
            matriz[row][column] = False

        print()
        print('▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼')

        print("Printing led: {0}|{1} with value {2}".format(row, column, value))
        pp.pprint(matriz)

        print('▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲')

        # pp.pprint(matriz)
        instrucciones.append(['PRINT', str(matriz)])

    else:
        errorList.append("ERROR: La fila o columna esta fuera de los limites de la matriz 8x8")


"""   
PrintLedX(TipoObjeto, Indice, Arreglo)
TipoObjeto: "C", "F", "M"
Indice: Entero
Arreglo: arreglo
['DELAY', 10, 'mil']
"""


def exe_print_ledx(tipo_objeto, index, arreglo):
    if 7 >= index >= 0:

        if tipo_objeto.lower() == "c":
            for row in range(8):
                for column in range(8):
                    if column == index:
                        matriz[row][column] = arreglo[row]

        elif tipo_objeto.lower() == "f":
            matriz[index] = arreglo

        elif tipo_objeto.lower() == "m":

            if index + len(arreglo) <= 8:
                count = 0
                for i in range(index, index + len(arreglo)):
                    matriz[i] = arreglo[count]
                    count += 1
            else:
                errorList.append("Error, la lista que se desea adjuntar sobrepasa los limites de la matriz 8x8")

        # pp.pprint(matriz)
        # print()

    else:
        errorList.append("Error, el indice debe ser entre 0 y 7")

    instrucciones.append(['PRINT', str(matriz)])


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●           ANALISIS                  ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


def check_procedures_name_count():
    for procedure in sintacticList:
        procedures_list.append(procedure[2])

    for procedure in procedures_list:
        if procedures_list.count(procedure) > 1:
            errorList.append("ERROR: el procedimiento: {0} esta definido mas de una vez".format(procedure))
            return
        local_variables[procedure] = {}


"""
▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲                                     ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲  
●   ●   ●   ●   ●   ●   ●   ●   ●              EJECUCION              ●   ●   ●   ●   ●   ●   ●   ●   ●
▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼                                     ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ 
"""


# Revisa que tod0 el código se encuentre dentro de PROCEDURES
def check_blocks():
    for line in sintacticList:

        if line[1] != 'PROCEDURE':
            errorList.append(
                "Error in line {0}, all the instructions must be inside of procedure block".format(line[0]))


# Revisa que solo exista un main en el codigo
def check_main_count():
    count = 0

    for line in sintacticList:
        if line[1] == "PROCEDURE":
            if line[2] == "Main":
                count += 1

    if count == 1:
        find_main()
        return

    if count == 0:
        errorList.append(
            "Error, Main not found")
    elif count > 1:
        errorList.append(
            "Error, There can only be one main")


# Busca el main y lo guarda en una variable global
def find_main():
    global global_variables
    global main_code

    for line in sintacticList:
        if line[1] == 'PROCEDURE':
            if line[2] == 'Main':
                main_code = line[4]

                sintacticList.remove(line)


def clear_all():
    global matriz
    global instrucciones
    global sintacticList
    global errorList
    global global_variables
    global local_variables
    global main_code

    matriz = [[False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False]]

    instrucciones.clear()
    global_variables.clear()
    local_variables.clear()
    procedures_list.clear()
    main_code.clear()


def compile_program(insumo):
    # Lista de arboles sintacticos generados en el analisis sintactico
    global sintacticList
    global errorList
    global global_variables
    global local_variables
    global instrucciones

    clear_all()

    syntaxResult = run_syntax_analysis(insumo)

    sintacticList = syntaxResult[0]

    # Errores generados en el analisis sintactico
    errorList = syntaxResult[1]

    """ ################################ Resultados del analisis sintactico ############################################ """

    print("\n--------- Syntactic Analysis Result ---------")

    pp.pprint(sintacticList)

    print("\n--------- Errors ---------")
    pp.pprint(errorList)

    """ ################################ Resultados del analisis sintactico ############################################ """

    check_blocks()
    check_main_count()
    check_procedures_name_count()

    print("\n--------- Main ---------")
    pp.pprint(main_code)

    # print("\n--------- Lista de procedimientos ---------")
    pp.pprint(procedures_list)

    print()
    main_execute()

    print("\n--------- Variables globales ---------")
    pp.pprint(global_variables)

    # print("\n--------- Lista de variables locales de procedimientos ---------")
    # pp.pprint(local_variables)

    # print("\n--------- INSTRUCCIONES ARDUINO ---------")
    # pp.pprint(instrucciones)

    print("\n--------- Errors ---------")
    pp.pprint(errorList)

    instrucciones = convert_instructions_to_list(str(instrucciones))

    file = open("ArduinoCompiledOutput.txt", "w")
    if len(errorList) == 0:
        file.write(str(instrucciones))
    else:
        file.write("")
    file.close()

    return errorList


def convert_instructions_to_list(instructions):
    temp = ast.literal_eval(instructions)

    for x in temp:
        if x[0] == "PRINT":
            x[1] = ast.literal_eval(x[1])

    return temp

# compile_program()

# a = None
# ciclo_for(a, [1,2,3,4,5,6,7,8,9,10],1,0)
# ciclo_for(a, [1,2,3,4,5,6,7,8,9,10],2,0)
# ciclo_for(a, 10,1,0)
# ciclo_for(a, 10,2,0)

# a = True
# print(bifurcacion(a,'==', True));
#
# a = 5
# print(bifurcacion(a,'>', 4));
#
# a = [True,True,True]
# print(bifurcacion(a,'==', True));
#
# a = [True,False,True]
# print(bifurcacion(a,'==', True));
#
# a = [1,2,3]
# print(bifurcacion(a,'<', 1));


# exe_blink(0,0,1,"seg", True)
# print("Hola")
# exe_blink(1,0,1,"seg", True)

# print("inicio")
# exe_delay(5, "seg")
# print("fin")

# exe_print_led(0,0,True)
# exe_print_led(0,0,False)


# matriz_x = [[True, True, True, True, True, True, True, True],
#           [True, True, True, True, True, True, True, True],
#           [True, True, True, True, True, True, True, True]]
#
# exe_print_ledx("m", 0, matriz_x)
#
# matriz_x = [[True, True, True, True, True, True, True, True],
#           [True, True, True, True, True, True, True, True],
#           [True, True, True, True, True, True, True, True]]
#
# exe_print_ledx("m", 5, matriz_x)

# matriz_x = [[True, True, True, True, True, True, True, True]]
#
# exe_print_ledx("f", 0, matriz_x)
# exe_print_ledx("f", 3, matriz_x)

# matriz_x = [True, True, True, True, True, True, True, True]
#
# exe_print_ledx("c", 7, matriz_x)
# exe_print_ledx("c", 4, matriz_x)
# pp.pprint(errorList)
