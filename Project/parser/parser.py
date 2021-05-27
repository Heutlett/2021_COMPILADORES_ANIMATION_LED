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


# Define una recursion entre expresiones.
def p_statments(p):
    """ statements : statements statement
                   | statement
    """

    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


# def p_statement_assign_multiple_ids(p):
#     """ IDs :  ID COMA IDs
#             | ID IGUAL values
#         values :  value COMA values
#                | value
#     """
#
#     print(p.type)
#
# def p_statement_assign_multiple_values(p):
#     """
#     """


# Expresion para la declaracion de una variable.
def p_statement_assign(p):
    """
        statement : ID IGUAL value
    """
    # NOTA: P[0] corresponde al valor que toma la variable.
    # Los indices empiezan en 1.
    if p[1] in variables:
        if equalsType(variables.get(p[1]), p[3]):
            p[0] = getVariable(p[1], p[3])
        else:
            print("ERROR in line {2}! \"{0}\" is already type {1}.".format(p[1], type(p[3]), "LINE_NUMBER"))
    else:
        p[0] = getVariable(p[1], p[3])
    print(" ▶ variables: ", variables)


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
    print(p)
    print("\nSyntax error in input: ", p.type)
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
