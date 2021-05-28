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
   correr "python parser.py [nombre_archivo].txt" El archivo de lexer.py tiene que estar en la misma carpeta
TODO:
1. Generar los errores para cada error de sintaxis
2. Generar las reglas para todo a partir de las reglas de POS
"""

# Diccionarios
functions = {}  # Lista de funciones almacenadas del programa.
variables = {"c": 15, "d": True, "e": False}  # Las variables almacenadas se guardarán como {ID: valor}.

# Variables para multiple asignacion
ids_list = []
values_list = []

# Orden para asignar a las operaciones.
prioridad = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
    ('right', 'UMENOS'),
    ('right', 'POTENCIA')
)

''' GRAMMARS '''

'''Cada regla gramatical está definida por una función de Python donde la cadena de documentación 
de esa función contiene la especificación gramatical libre de contexto apropiada.
Los enunciados que componen el cuerpo de la función implementan las acciones semánticas de la regla. 
Cada función acepta un solo argumento p que es una secuencia que contiene los valores de cada 
símbolo gramatical en la regla correspondiente. Los valores de p [i] se asignan a símbolos gramaticales.'''


# The parser grammar rules are defined.
# The rule name does not matter as long as it starts with "p_".


# Expresion que define una recursion entre expresiones.
def p_statments(p):
    """ statements : statements statement
                   | statement
    """
    # NOTA: P[0] corresponde al valor que toma la variable.
    # El conteo de indices para los datos empieza en 1.
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_printVariables(p):
    """ statement : PUNTO
    """
    print(values_list)

# Expresion para la declaracion de una variable.
def p_statement_assign(p):
    """
        statement : ids IGUAL values
                  | ID IGUAL value
    """
    print(len(p))
    if len(p) > 4:  # p[0], p[1], p[2], ...
        pass
    else:
        p[0] = assign_aux(p[1], p[3])

    # ids_list.clear()
    # values_list.clear()
    print(variables)

# def p_valuestest(p):
#     """
#     statement : values
#     """
#
#     if len(p) == 2:  # p[0], p[1]
#         print(p[0])
#         print(p[1])
#         values_list.append(p[1])
#
#     else:
#         print(p[0])
#         print(p[1])
#         print(p[2])
#         values_list.append(p[3])
#     p[0] = values_list
#     print(values_list)

def assign_aux(id, value):
    if id in variables:
        if equalsType(variables.get(id), value):
            return getVariable(id, value)
        else:
            print("ERROR in line {2}! \"{0}\" is already type {1}.".format(id, type(value), "LINE_NUMBER"))
    else:
        return getVariable(id, value)
    print(" ▶ variables: ", variables)


def p_ids(p):
    """ ids : ID COMA ids
            | ID
    """
    print("\n")

    if len(p) == 2:  # p[0], p[1]
        print(p[0])
        print(p[1])
        ids_list.append(p[1])
    else:
        print(p[0])
        print(p[1])
        print(p[2])
        ids_list.append(p[3])
        p[0] = ids_list
    p[0] = ids_list
    print(ids_list)


def p_values(p):
    """
    values : value COMA values
           | value
    """

    if len(p) == 2:  # p[0], p[1]
        # print(p[0])
        # print(p[1])
        p[0] = p[1]

    else:
        # print(p[0])
        # print(p[1])
        # print(p[2])
        p[0] = p[3]
    print(p[0])


# Expresion para la determinar el valor de una variable.
def p_value(p):
    """ value : INT
              | BOOLEAN
              | ID
   """
    if isVariable(p[1], "LINE_NUMBER"):
        p[0] = variables.get(p[1])
    else:
        p[0] = p[1]


# Expresion para consultar el tipo de una variable.
def p_type(p):
    """
        statement : TYPE PARENTESISIZQ ID PARENTESISDER
    """
    if isVariable(p[3], "LINE_NUMBER"):
        var = variables.get(p[3])
        if isinstance(var, bool):
            p[0] = 'bool'
        elif isinstance(var, int):
            p[0] = 'int'
        else:
            print("ERROR in type!")


# Valida si dos variables son del mismo tipo.
def equalsType(var1, var2):
    return type(var1) == type(var2)


# Verifica si ID existe en el diccionario.
def isVariable(var, line):
    # Si el valor es una instancia de ID.
    if not isinstance(var, str):
        return False
    # Si no existe el ID dentro del diccionario, return false.
    if variables.get(var) is None:
        print("ERROR in line {1}! \"{0}\" is not yet defined.".format(var, line))
        return False
    return True


# Verifica si el dato es un valor y no un ID.
def isValue(data):
    if isinstance(data, int):
        return True
    elif isinstance(data, bool):
        return True
    else:
        return False


# Guarda la variable en el diccionario.
def getVariable(id, value):
    if value is not None:
        variables[id] = value
        return value


# # Define una una función
# def p_function_assign(p):
#     """ statement : NAME '(' NAME ')' '=' expression """
#     p[0] = p[1]


''' ERRORS '''


# Error rule for syntax errors.
def p_error(p):
    # print(p)
    print("Syntax error in input: ", p.type)
    parser.errok()
    # Reinicia el parser
    parser.restart()


# Build the parser.
parser = yacc.yacc()

# parser.parse('a=1'
#              'b=2'
#              'a=b')

while True:
    while True:
        try:
            question = raw_input('>>> ')
        except:
            question = input('>>> ')

        answer = parser.parse(question)
        if answer is not None:
            print(answer)

    ################################## MAIN #################################
