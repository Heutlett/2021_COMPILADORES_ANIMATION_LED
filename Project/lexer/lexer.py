import ply.lex as lex
from ply.lex import TOKEN

"""
AnimationLed

lexer.py: Imprime la línea que se recorre y los tokens en forma de pares ordenados 

Para correr el programa:
   1. En CMD "pip install ply" y luego "pip install pyhcl"
   2. Luego igual en CMD a la ubicación del archivo (cd Documentos o Descargas o c://Users/nombre...) y
   correr "python lexer.py"

TODO: Solucionar la detección de multiplicaciones

"""


# Lista de palabras reservadas, se hace aparte de los tokens para no generar una expresión regular para cada una
palabras_reservadas = {

    'type': 'TYPE',
    'range': 'RANGE',
    'list': 'LIST',
    'insert': 'INSERT',
    'del': 'DEL',        # PARA LISTAS
    'delete': 'DELETE',  # PARA MATRICES
    'len': 'LEN',
    'Neg': 'NEG',
    'T': 'T',
    'F': 'F',
    'Blink': 'BLINK',
    'Seg': 'SEG',
    'Mil': 'MIL',
    'Min': 'MIN',
    'Delay': 'DELAY',
    'PrintLed': 'PRINTLED',
    'PrintLedX': 'PRINTLEDX',
    'for': 'FOR',
    'in': 'IN',
    'Step': 'STEP',
    'shapeF': 'SHAPEF',
    'shapeC': 'SHAPEC',
    'If': 'IF',
    'Procedure': 'PROCEDURE',
    'Begin': 'BEGIN',
    'end': 'END',
    'Main': 'MAIN',
    'call': 'CALL'

}

# Lista de tokens que identificará el programa
# Se agrega la lista de palabras reservadas al final
tokens = [

    'PARENTESISIZQ',
    'PARENTESISDER',

    'INT',

    # Operadores aritmeticos

    'SUMA',
    'RESTA',
    'DIVISION',
    'MULTIPLICACION',
    'EXPONENTE',
    'DIVISIONENTERA',
    'MODULO',


    # Operadores de comparacion

    'IGUALES',
    'MAYORQUE',
    'MAYORIGUAL',
    'MENORQUE',
    'MENORIGUAL',
    'DIFERENTE',

    # Literal caracteres

    'PYC',
    'PUNTO',
    'DOSPUNTOS',
    'COMA',
    'IGUAL',
    'CORCHETEIZQ',
    'CORCHETEDER',
    'LLAVEIZQ',
    'LLAVEDER',
    'STRING',
    'ID',

     # Booleanos

    'BOOLEAN'] + list(palabras_reservadas.values())

# Expresiones regulares de los tokens
t_ignore = '  \t'  # Esto indica que ignorará tabs, espacios en blanco
t_ignore_COMENTARIO = r'\#\#.*'  # Ignorará los comentarios (empiezan con ##)

# Operadores aritmeticos

t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = '\*'
t_EXPONENTE = r'\*\*'
t_DIVISION = r'/'
t_DIVISIONENTERA = r'//'
t_MODULO = r'%'

# Operadores de comparacion

t_IGUALES = r'=='
t_MAYORQUE = r'>'
t_MAYORIGUAL = r'>='
t_MENORQUE = r'<'
t_MENORIGUAL = r'<='
t_DIFERENTE = r'<>'

# Literales

t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PARENTESISIZQ = r'\('
t_PARENTESISDER = r'\)'
t_PUNTO = r'\.'
t_DOSPUNTOS = r':'
t_PYC = r';'   # Punto y coma
t_COMA = r','
t_IGUAL = r'='
t_CORCHETEIZQ = r'\['
t_CORCHETEDER = r'\]'
t_STRING = r'"[a-zA-Z0-9_ ]*"'
""" REGLAS DEL LEXER """


# Define el token del valor booleano TRUE
def t_BOOLEAN(token):
    r'(True|False)'
    if token.value == 'True':
        token.value = True
    else:
        token.value = False

    return token

# Identifica las variables del programa, excluye las palabras reservadas
def t_ID(token):
    # Define como se ve una variable o ID
    r'[a-z][a-zA-Z_0-9@?]*'
    if token.value in palabras_reservadas:
        # token.type devuelve los valores de arriba (p.e: token.type devuelve de t_CORCHETEDER : CORCHETEDER)
        token.type = palabras_reservadas[token.value]
    # Regresa la variable

    # Checkea si el tamano de la variable es mayor menor a 10
    if len(token.value) <= 10:
        return token
    print("Token no permitido '{0} en la linea {1}'".format(token.value, token.lineno))
    token.lexer.skip(1)


# Identifica las variables del programa, excluye las palabras reservadas
def t_RESERVADA(token):
    # Define como se ve una variable o ID
    r'[a-zA-Z_][a-zA-Z]*'
    if token.value in palabras_reservadas:
        # token.type devuelve los valores de arriba (p.e: token.type devuelve de t_CORCHETEDER : CORCHETEDER)
        token.type = palabras_reservadas[token.value]
        # Regresa la variable
        return token    # Crea el token solo si esta dentro de las palabras reservadas
    print("Token no permitido '{0} en la linea {1}'".format(token.value, token.lineno))
    token.lexer.skip(1)

# Regla de expresión regular para un número (int)
def t_INT(token):
    # Define un INT como un token de uno o más dígitos
    r'\d+'
    if token.value in palabras_reservadas:
        token.type = palabras_reservadas[token.value]
    # Convierte el valor de token a int y se lo asigna en su propiedad de "Valor"
    token.value = int(token.value)
    # Regresa el token con el valor del número en forma de int
    return token


# Se define el token "newline" para que el lexer pueda saber actualizar el número de línea que está recorriendo (útil en el futuro para indicar errores)
def t_newline(token):

    r'\n+'
    token.lexer.lineno += len(token.value)


# Regla para manejar los errores
def t_error(token):
    # Si hay un caracter para el cual no existe un token (p.e: '?' o '!', imprime Caracter no permitido y el caracter al lado)
    print("Caracter no permitido '{0} en la linea {1}'".format(token.value[0], token.lineno))
    token.lexer.skip(1)


# Maneja el fin del archivo (EOF o End-Of-File)
def t_eof(t):
    return None


# Construir el lexer después de crear las reglas
lexer = lex.lex()



# Prueba para el lexer
# Detecta e ignore comentarios - Check
# Diferencia entre ID y String - Check
# Detecta palabras reservadas - Check
# Recibe _, & y @ como caracteres aceptados para un string - Check

# lexer.input("""var47 = 3 * 4 - 5 * 6 + -2 ?
#  ## COMENTARIO IGNORADO.
# var4567890 = 3
# casa
# CASA
# var123456789 = 3
# + - * ** / // %
# range
# type
# list
# LIST
# insert
# del
# T
# F
# Blink
# Delay
# PrintLed
# PrintLedX
# "C"
# for var in x Step 3
# shapeF
# shapeC
# ShapeC
# If miVariable == 5
# < <= > >=
# Procedure rutina (True)
# Begin
# end;
# Main
# call
# x = 5 + 6; , True False type [ ] : .
# len
# Neg "asdadsadsads"
# °
# miLista[2]
# True
# False
# miLista[True]
# """)

# print("\n--------- Resultados del lexer: (Incluye errores que debe dar) ---------")
# # Mientras hayan tokens, los imprime en el respectivo par ordenado
# while True:
#     token = lexer.token()
#
#     # Si se acaban los tokens del input, se acaba
#     if not token:
#         break
#
#     # Imprime la línea y, en forma de par ordenado, el tipo de token y qué fue lo que catalogó de esa manera
#     print("En la linea " + str(token.lineno) + " se encontró el token: "
#           + '(' + str(token.type) + ', ' + str(token.value) + ')')

