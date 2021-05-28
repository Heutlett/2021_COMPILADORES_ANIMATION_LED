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
variables = {}  # Las variables almacenadas se guardarán como {ID: valor}.

# Lista de errores del programa
errors_list = []

ids_list = []
values_list = []

# Orden para asignar a las operaciones.
# Se utiliza el %prec para la declaracion de expresiones negativas.
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION', 'DIVISIONENTERA'),
    ('right', 'UMENOS'),
    ('right', 'MODULO'),
    ('right', 'EXPONENTE')
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


# Definición de posibles expresiones
def p_sentencia_expr(p):
    ''' statement : expression
                    | print
    '''
    p[0] = p[1]


def p_printVariables(p):
    """
    print : PUNTO
    """
    print(variables)


# Expresion para la declaracion de una variable.
def p_statement_assign(p):
    """
        statement : ids IGUAL values
    """
    p[0] = multiple_assign_aux()
    ids_list.clear()
    values_list.clear()
    print(" ▶ variables: ", variables)


def p_ids(p):
    """ ids : ID COMA ids
            | ID
    """
    ids_list.append(p[1])


def p_values(p):
    """
    values : value COMA values
           | value
    """
    values_list.append(p[1])


def multiple_assign_aux():
    if len(ids_list) != len(values_list):
        print("ERROR in line {0}! The number of values does not match the number of IDs.".format("LINE_NUMBER"))
    var_list = []
    ids_list.reverse()
    values_list.reverse()

    for id in ids_list:
        if id in variables.keys():
            print("ERROR in line {2}! \"{0}\" is already defined as {1}.".format(id, variables.get(id), "LINE_NUMBER"))
            return None

    for i in range(len(ids_list)):
        var_list.append(assign_aux(ids_list[i], values_list[i]))
        # print(var_list)
    return var_list


def assign_aux(id, value):
    if id in variables:
        if equalsType(variables.get(id), value):
            return getVariable(id, value)
        else:
            print("ERROR in line {2}! \"{0}\" is already type {1}.".format(id, type(value), "LINE_NUMBER"))
    else:
        return getVariable(id, value)


# Valida si dos variables son del mismo tipo.
def equalsType(var1, var2):
    return type(var1) == type(var2)


# Guarda la variable en el diccionario.
def getVariable(id, value):
    if value is not None:
        variables[id] = value
        return value


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


# # Define una una función
# def p_function_assign(p):
#     """ statement : NAME '(' NAME ')' '=' expression """
#     p[0] = p[1]

''' ARITMETICA '''

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

    # Potencia
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
            print(answer[0])

    ################################## MAIN #################################
