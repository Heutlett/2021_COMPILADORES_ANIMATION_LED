from Syntax_Analysis import result
from Syntax_Analysis import errors
import pprint

# Lista de arboles sintacticos generados en el analisis sintactico
sintacticList = result

# Errores generados en el analisis sintactico
errorList = errors

# Codigo main
main_code = []

# Lista de variables globales
global_variables = {}

""" ################################ COMPROBACIONES INICIALES #################################################### """


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
        if line[1] == 'PROCEDURE':
            if line[2] == 'Main':
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
    for line in sintacticList:
        if line[1] == 'PROCEDURE':
            if line[2] == 'Main':
                global main_code
                main_code = line


check_blocks()
check_main_count()

""" ############################################################################################################### """

""" ###################################### Ciclos y Bifurcacion ################################################### """


def ciclo_for(temp_var, iterable, step, ordenes):
    """
    Ejecuta el ciclo for
    :param temp_var: variable que cambiará
    :param iterable: estructura usada para recorrer, normalmente será una lista, pero puede ser un entero (igual que range)
    :param step: incremento, por defecto es 1
    :param ordenes: ordenes que se ejecutaran
    :return: None
    """

    if step == 1:
        if isinstance(iterable, list):
            for temp_var in iterable:
                print(temp_var)

        elif isinstance(iterable, int):
            for temp_var in range(iterable):
                print(temp_var)
    else:
        if isinstance(iterable, list):
            for temp_var in iterable[::step]:
                print(temp_var)

        elif isinstance(iterable, int):
            for temp_var in range(0, iterable, step):
                print(temp_var)


def bifurcacion(iterable, operator, value, ordenes):
    """
    Ejecuta el condicional if
    :param iterable: estructura que sera utilizada para realizar la validacion, puede ser variable o lista
    :param operator: operador de comparacion, ( == , <, <=, >, >=)
    :param value: puede ser numero, o bool
    :return: bool
    """
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

        if flag == True:
            # aqui se deberian ejecutar las ordenes
            pass
        return flag

    elif isinstance(iterable, int) or isinstance(iterable, bool):

        if operator == '==':
            if iterable == value:
                # ordenes
                return True
        elif operator == '<':
            if iterable < value:
                # ordenes
                return True
        elif operator == '<=':
            if iterable <= value:
                # ordenes
                return True
        elif operator == '>':
            if iterable > value:
                # ordenes
                return True
        elif operator == '>=':
            if iterable >= value:
                # ordenes
                return True
        return False


""" ###################################### Validacion de variables ################################################### """


# Funcion para obtener una de las variables del dictionario recibido
def getVariable(key, variables_dict):
    return variables_dict.get(key)


# Funcion para asignar a una variables del dictionario recibido
def setVariable(key, variables_dict, value):
    variables_dict[key] = value


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


def run(p):
    '''
    Funcion que toma todos los arboles e interpreta qué subfunción debe llamar.
    Funciona como switch case basicamente.
    :param p: Lista de entrada.
    :return: Salida respectiva dependiendo del caso que se cumpla.
    '''

    global arithmetic_operators
    # print(p)
    if equalsType(p, list):
        line = p[0]
        action = p[1]
        data1 = p[2]
        data2 = p[3]

        if action in arithmetic_operators:  # OPERACIONES ARITMETICAS
            return arithmetic_operation(line, action, data1, data2)

        elif action == '=':
            return var_assign_operation(line, data1, data2, p[4])

        # elif p[0] == 'var':  # DEFINIR UNA VARIABLE
        #     return env[p[1]]
        #
        # elif p[0] == 'type':
        #     return p[1]
        #
        # elif p[0] == '[]':
        #     return list_callable_operation(p[1], p[2])
        #
        # elif p[0] == '[]*':
        #     return list_callable_operation(p[1], p[2], False)
        #
        # elif p[0] == '[:,]':
        #     return matrix_column_operation(p[1], p[2])
        #
        # elif p[0] == '[:,]*':
        #     return matrix_column_operation(p[1], p[2], False)
        #
        # elif p[0] == 'INSERT':
        #     return list_insert_operation(p[1], p[2], p[3])
        #
        # elif p[0] == 'DEL':
        #     return list_delete_operation(p[1], p[2])
        #
        # elif p[0] == 'LEN':
        #     return list_len_operation(p[1])
        #
        # elif p[0] == "NEG":
        #     return neg_operation(p[1])
        #
        # elif p[0] == "T":
        #     return t_operation(p[1])
        #
        # elif p[0] == "F":
        #     return f_operation(p[1])
        #
        # elif p[0] == 'BLINK':
        #     return p[1]
        #
        # elif p[0] == 'DELAY':
        #     return p[1]
        #
        # elif p[0] == 'PRINTLED':
        #     return p[1]
        #
        # elif p[0] == 'PRINTLEDX':
        #     return p[1]


    else:
        return p

""" ###################################### Operaciones aritmeticas ################################################### """

def arithmetic_operation(line, operator, a, b):
    '''
    Funcion auxiliar para operar los calculos aritmeticos por aparte.
    Funciona como switch case para la operacion que se debe realizar.
    :param line: linea en donde se encuentra el lector.
    :param operator: operacion que se debe realizar
    :param a: expresion uno
    :param b: expresion dos
    :return: el resultado de aplicar el operando a ambas expresiones recibididas.
    '''
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
    else:
        errors.append("ArithmeticError in line {0}!".format(line))
        return "Error aritmetico"


""" ###################################### Asignacion de variables ################################################### """


# Funcion para operar la asignacion de las variables.
def var_assign_operation(line, ID, value, variables_dict):
    '''
    Funcion que asigna una variable y realiza las verificaciones necesarias.
    :param line: linea en donde se encuentra el lector.
    :param ID:  lista de los ids o ID individual
    :param value:  lista de los valores o valor individual.
    :param variables_dict: diccionario en donde se está trabajando la asignación.
    :return: asignacion de la variable deseada en el diccionario deseado.
    '''

    # Si es más de una variable.
    # [line, '=', [ID1,ID2,..., IDn], [val1,val2,..., valn], dict]
    if type(ID) == list and type(value) == list:

        # Validaciones.
        if not multi_assign_validation(line, ID, value, variables_dict):
            # Error se agrega en la funcion anterior.
            return False

        # Asignacion en cascada.
        for i in range(len(ID)):
            tmp = var_assign_operation(line,  ID[i], value[i], variables_dict)
            if tmp is False:
                return False
            # Asignación
            variables_dict[tmp[0]] = tmp[1]
        return variables_dict

    # Si es solo una variable.
    # [line, ID, value, dict]
    else:
        return individual_assign_validation(line, ID, value, variables_dict)



def individual_assign_validation(line, ID, value, variables_dict):
    '''
    Funcion para verificar la asignacion de las variables individualmente.
    :param line: linea en donde se encuentra el lector.
    :param ID:  lista de los ids o ID individual
    :param value:  lista de los valores o valor individual.
    :param variables_dict: diccionario en donde se está trabajando la asignación.
    :return: lista con ID y value si se cumplen todas las verificaciones, False en caso contrario.
    '''

    # insumo :  [line, ID, value, dict]

    # De [[18, '=', [18, 'a', [['row', 1]]], [True]]]
    #  se recibe[18, [18, 'a', [['row', 1]]], [True], "dictionary"]

    # De [16, '=', 'h', 5]
    #     se recibe [16, 'h', 5, "dictionary"]

    # Si es una asignacion a una sublista.
    if type(ID) == list:
        return sublist_assign(line, ID, value, variables_dict)

    # Si la variable es una lista, obtener el valor si es una operacion.
    if type(value) == list:
        value = run(value)

    # Si no es una variable valida.
    if not var_verification(line, ID, value, variables_dict):
        # El error se agrega en la verificacion.
        return False

    # Si se cumplen todas las validaciones.
    print("-> {0} : {1}".format(ID, variables_dict[ID]))
    return [ID, value]


def sublist_assign(line, ID, value, variables_dict):
    '''
    Auxiliar para verificar la asignacion de las variables a una sublista.
    :param line: linea en donde se encuentra el lector.
    :param ID:  lista de los ids o ID individual
    :param value:  lista de los valores o valor individual.
    :param variables_dict: diccionario en donde se está trabajando la asignación.
    :return: lista con ID y value si se cumplen todas las verificaciones, False en caso contrario.
    '''
    
    # # If its an assignment to a column.
    # elif var[0] == ':':
    # ID = var[1]
    # env[ID] = matrix_column_assign(getValue(ID), var[2], value)
    #
    # # If its an assignment to a sublist.
    # else:
    # ID = var[0]
    # i, j = var[1][0][0], var[1][0][1]
    # if j is not None:
    #     getValue(ID)[i:j] = value
    # else:
    #     getValue(ID)[i] = value
    # return [ID, ":", env[ID]]

    pass


    # # If variable is a primitive but not a list.
    # if not equalsType(var, list):
    #     env[var] = run(value)
    #     return [var, ":", env[var]]
    #
    # # If its an assignment to a column.
    # elif var[0] == ':':
    #     ID = var[1]
    #     env[ID] = matrix_column_assign(getValue(ID), var[2], value)
    #
    # # If its an assignment to a sublist.
    # else:
    #     ID = var[0]
    #     i, j = var[1][0][0], var[1][0][1]
    #     if j is not None:
    #         getValue(ID)[i:j] = value
    #     else:
    #         getValue(ID)[i] = value
    #     return [ID, ":", env[ID]]


""" ###################################### Validacion de asignacion de variables ################################################### """

def multi_assign_validation(line, ids, values, variables_dict):
    '''
    Funcion para verificar que la lista de IDS y VALUES corresponden al mismo tamaño,
    conservan los mismos tipos y que cada ID es unico.
    :param line: linea en donde se encuentra el lector.
    :param ids: lista de los ids.
    :param values: lista de los valores.
    :param variables_dict: diccionario en donde se está trabajando la asignación.
    :return: True si se cumplen todas las verificaciones, False en caso contrario.
    '''

    # Number of values must match the numbers of ids.
    if len(ids) != len(values):
        errors.append("LenError in line {0}! The number of values does not match the number of IDs.".format(line))
        return False

    # All values type must be the same.
    if not list_check_type_validation(line, values):
        errors.append("TypeError in line {0}! All values type must be the same.".format(line))
        return False

    # IDs must be unique.
    for ID in ids:
        if ID in variables_dict.keys():
            text = "TypeError in line {1}! \"{0}\" is already declared.".format(ID, line)
            errors.append(text)
            return False
    return True


# Funcion auxiliar para verificar una reasignacion de la variable.
def var_verification(line, ID, value, variables_dict):
    '''
    Funcion auxiliar para verificar una asignacion o reasignacion de la variable.
    :param line: linea en donde se encuentra el lector.
    :param ids: lista de los ids.
    :param values: lista de los valores.
    :param variables_dict: diccionario en donde se está trabajando la asignación.
    :return: False si no se cumple alguna de las validaciones, True en caso contrario.
    '''
    # CHECK VALUE...

    # Si value es un string.
    if type(value) == str:
        # Si el valor es un ID y aun no se ha creado
        if not isGlobalDeclared(value, variables_dict):
            errors.append("ERROR in line {0}! \"{1}\" is not yet defined.".format(line, value))
            return False

        # CHECK ID...

        # Si el tipo de ambas variables no coincide.
        else:
            if getVariable(ID, variables_dict) is not None:
                if type(getVariable(ID, variables_dict)) != type(getVariable(value, variables_dict)):
                    errors.append("TypeError in line {0}! The type of \"{2}\" does not match the type of {1}."
                                  .format(line, ID, value))

    # CHECK ID...

    # Si el tipo del ID y la variable no coincide.
    if getVariable(ID, variables_dict) is not None:
        if type(getVariable(ID, variables_dict)) != type(value):
            errors.append("TypeError in line {0}! The type of \"{2}\" does not match the type of {1}."
                          .format(line, ID, value))
            return False

    # Return true if its a new variable and param is not and undeclared variable.
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

""" ###################################### Validaciones en listas ################################################### """

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
        supposedType = get_list_type(lst)
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
            errors.append(text)
            return False
    return True


def get_list_type(lst):
    '''
    Funcion auxiliar para obtener el primer elemento de una lista que no sea una sublista.
    :param lst: lista de entrada
    :return: el tipo al que corresponde el primer elemento de la lista.
    '''
    if equalsType(lst, list):
        return get_list_type(lst[0])
    return type(lst)




""" ###################################### Validacion de variables ################################################### """




""" ############################################################################################################### """

print("\n--------- Syntactic Analysis Result ---------")

pp = pprint.PrettyPrinter(indent=2)

pp.pprint(sintacticList)

print("\n--------- Errors ---------")
pp.pprint(errorList)

print("\n--------- Main ---------")
pp.pprint(main_code)

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
