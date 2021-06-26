# Importa el módulo yacc para el compilador
import ply.yacc as yacc

import sys
from lexer.lexer import tokens

# Pretty Printer
import pprint

# Define el archivo del programa
program_file = "insumo.txt"

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
    '''
    statements : empty
               | primitive
               | statement
               | statements statement
    '''
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
              | error_string
    '''
    p[0] = p[1]


# Expresiones para variables primitivas.
def p_primitive_var(p):
    '''
    primitive : BOOLEAN
              | INT
              | list
              | STRING
    '''
    # print("PRIMITIVE", p[1])
    p[0] = p[1]


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

    # # If param is None
    # if p[1][0] is None:
    #     p[0] = "No params"
    #
    # # If only one param
    # elif len(p[1]) == 1:
    #     p[0] = p[1][0]

    # else:
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
        # Si el parametro es una lista.
        # if type(p[1]) == list:
        p[0] = [p[1]]
        # else:
        #     p[0] = [p[1]].append(p[3])

    # Si son más de dos input
    else:
        p[0] = p[1] + p[3]


# Expresion para asignacion de variables.
def p_var_assign(p):
    """
    var_assign : ID IGUAL expression PYC
               | ID IGUAL primitive PYC
               | ids IGUAL params PYC
    """
    # Build our tree
    # Examples:
    # [line, '=', ID, value]
    # [line, '=', [ID1,ID2,..., IDn], [val1,val2,..., valn]]

    # print("ID:", p[1])
    # print("Val:", p[3])
    values = p[3]
    if type(p[1]) == list:
        values = p[3][0]

    p[0] = [p.lineno(4), '=', p[1], values]


def p_var_sublist_assign(p):
    """
    var_assign : sublist IGUAL params PYC
    """
    # [line, '=', ['[]*', 'a', [['row', 0, 4]]] , [1, 2, 3, 4]]
    values = p[3][0]
    newSublist = [p[1][0], p[1][1]+'*', p[1][2], p[1][3]]
    p[0] = [p.lineno(4), '=', newSublist, values]


# Expresion para variables de string.
def p_var_error_string(p):
    """
    error_string : ID IGUAL STRING PYC
    """
    print("Error")
    errors.append("Error in  linea")
    p[0] = None


# Expresion para consultar el tipo de una variable.
def p_var_type(p):
    """
        statement : TYPE PARENTESISIZQ ID PARENTESISDER PYC
    """
    # [line, TYPE, ID]
    p[0] = [p.lineno(5), 'TYPE', p[3]]


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
        p[0] = p[2]
        # print("LIST", p[2])


# Expresion para mostrar una lista  o sublista.
def p_callable(p):
    '''
    callable  : sublist
    '''
    p[0] = p[1]


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


# Expresion para obtener un indice de una fila.
def p_index_f(p):
    """
    index  : CORCHETEIZQ expression CORCHETEDER
    """
    # [1]
    p[0] = ['row', p[2]]


# Expresion para obtener un indice de las columnas en una matriz.
def p_index_c(p):
    """
    index  : CORCHETEIZQ DOSPUNTOS COMA expression CORCHETEDER
    """
    # [:, 1]
    p[0] = ['col', p[4]]


def p_index_sublist(p):
    """
    index  : CORCHETEIZQ expression DOSPUNTOS expression CORCHETEDER
    """
    # [1:2]
    p[0] = ["sublist", p[2], p[4]]


# Expresion para obtener indices equivalentes en matrices.
def p_index_matrix(p):
    """
    index  : CORCHETEIZQ expression COMA expression CORCHETEDER
           | CORCHETEIZQ expression CORCHETEDER CORCHETEIZQ expression CORCHETEDER
    """
    # [1][2]
    # [1,2]
    if len(p) == 6:
        p[0] = ["row,col", p[2], p[4]]
    else:
        p[0] = ["row,col", p[2], p[5]]


# Expresion para obtener una sublista de una lista.
def p_sublist(p):
    '''
    sublist  : ID multi_index
    '''
    p[0] = [p.lineno(1), '[]', p[1], p[2]]


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
    operation = p[2]
    expr1, expr2 = p[1], p[3]
    # [line, OPERATION, exp1, exp2]
    p[0] = [p.lineno(1), operation, expr1, expr2]


# Expresiones entre paréntesis.
def p_expression_parentesis(p):
    'expression : PARENTESISIZQ expression PARENTESISDER'
    p[0] = p[2]


# Expresiones para variable.
def p_expression_var(p):
    '''
    expression : ID
               | INT
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


def p_valor_param(p):
    """ valor_param : BOOLEAN
                      | INT
                      | ID
    """
    p[0] = p[1]

###################################### FUNCIONES DE LISTAS #####################################################


# Expresion para crear lista con range.
def p_statement_assign_range(p):
    """
    var_assign : ID IGUAL rango PYC
    """
    # Build tree
    # [10, '=', ID, [10, 'range', ID, expresion, params]]
    p[0] = [p.lineno(1), '=', p[1], p[3]]

def p_statement_range(p):
    """
    rango : LIST PARENTESISIZQ RANGE PARENTESISIZQ expression COMA params PARENTESISDER PARENTESISDER
    """

    # Build tree
    # [10, 'range', ID, expresion, params]
    p[0] = [p.lineno(1), 'RANGE', p[5], p[7][0]]


# Expresion para crear lista con range.
def p_statement_assign_len(p):
    """
    var_assign : ID IGUAL length PYC
    """
    # Build tree
    # [10, '=', ID, [10, 'LEN', [1,2,3]]]
    p[0] = [p.lineno(1), '=', p[1], p[3]]


# Expresion para crear lista con len.
def p_statement_len(p):
    """
    length : LEN PARENTESISIZQ ID PARENTESISDER
            | LEN PARENTESISIZQ list PARENTESISDER
    """
    # Build tree
    # Example [10, 'LEN', [1,2,3]]
    # Example [10, 'LEN', 'a']
    tree = [p.lineno(1), "LEN", p[3]]
    p[0] = tree


def p_insert(p):
    '''
    funcionreservada : ID PUNTO INSERT PARENTESISIZQ input COMA input PARENTESISDER PYC
    '''

    # [linea, INSERT, ID, Indice, Valor]
    p[0] = [p.lineno(1), 'INSERT_LIST', p[1], p[5][0], p[7][0]]


# del para listas
def p_del(p):
    '''
    funcionreservada : ID PUNTO DEL PARENTESISIZQ expression PARENTESISDER PYC
   '''

    # [linea, "DELETE", ID, Indice]
    p[0] = [p.lineno(1), 'DELETE_LIST', p[1], p[5]]



def p_len(p):
    '''
    funcionreservada : LEN PARENTESISIZQ ID PARENTESISDER PYC
    '''

    p[0] = [p.lineno(1), 'LEN', p[3]]


############################ OPERACIONES BOOLEANAS


def p_neg(p):

    '''
    funcionreservada :   ID CORCHETEIZQ expression CORCHETEDER CORCHETEIZQ expression CORCHETEDER PUNTO NEG PYC
                       | ID CORCHETEIZQ expression CORCHETEDER PUNTO NEG PYC
                       | ID PUNTO NEG PYC
    '''

    # [p.lineno(1), 'NEG', ID, INDICE]

    if len(p) == 5:
        p[0] = [p.lineno(1), 'NEG', p[1]]
    elif len(p) == 11:
        p[0] = [p.lineno(1), 'NEG', p[1], p[3], p[6]]
    else:
        p[0] = [p.lineno(1), 'NEG', p[1], p[3]]


def p_T(p):

    '''
    funcionreservada :    ID CORCHETEIZQ expression CORCHETEDER CORCHETEIZQ expression CORCHETEDER PUNTO T PYC
                        | ID CORCHETEIZQ expression CORCHETEDER PUNTO T PYC
                        | ID PUNTO T PYC
    '''

    # [p.lineno(1), 'NEG', ID, INDICE]

    if len(p) == 5:
        p[0] = [p.lineno(1), 'T', p[1]]
    elif len(p) == 8:
        p[0] = [p.lineno(1), 'T', p[1], p[3]]
    elif len(p) == 11:
        p[0] = [p.lineno(1), 'T', p[1], p[3], p[6]]



def p_F(p):
    '''
    funcionreservada :    ID CORCHETEIZQ expression CORCHETEDER CORCHETEIZQ expression CORCHETEDER PUNTO F PYC
                        | ID CORCHETEIZQ expression CORCHETEDER PUNTO F PYC
                        | ID PUNTO F PYC
    '''

    # [p.lineno(1), 'F', ID, INDICE]

    if len(p) == 5:
        p[0] = [p.lineno(1), 'F', p[1]]
    elif len(p) == 8:
        p[0] = [p.lineno(1), 'F', p[1], p[3]]
    elif len(p) == 11:
        p[0] = [p.lineno(1), 'F', p[1], p[3], p[6]]


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  DEFAULT FUNCTIONS  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''

rangoTiempo = ["seg", "mil", "min"]
tipoObjeto = ["c", "f", "m"]

"""   
Blink(Fila, Columna, Tiempo, RangoTiempo, Estado)
Fila y columna: indice donde se encendera un led
Tiempo: Tiempo en el que se encenderan
RangoTiempo: "Seg", "Mil", "Min"
Estado: bool
"""


def p_blink(p):
    '''
    funcionreservada : BLINK PARENTESISIZQ params PARENTESISDER PYC
    '''
    params = p[3]
    if type(params[3]) != str:
        errors.append("ERROR in line {0}! The forth param must be a (Seg, Mil, Min)! "
                      "".format(p.lineno(1)))
        return "Error in Blink, line {0}.".format(p.lineno(5))

    rango = params[3].lower()[1:-1]  # De '"seg"' a "seg"

    global rangoTiempo
    if not rango in rangoTiempo:
        errors.append("ERROR in line {0}! The forth param must be a (Seg, Mil, Min)! "
                      "".format(p.lineno(1)))
        return "Error in Blink, line {0}.".format(p.lineno(5))
    if type(params[4]) == int:
        errors.append("ERROR in line {0}! The estado param must be a boolean "
                      "".format(p.lineno(1)))
        return

    # ['BLINK', f, c, int, rangotiempo, bool]
    p[0] = [p.lineno(1), "BLINK", params[0], params[1], params[2], rango, params[4]]



"""   
Delay(Cantidad, RangoTiempo)
Cantidad: Entero
RangoTiempo: "Seg", "Mil", "Min"
"""


def p_delay(p):
    '''
    funcionreservada : DELAY PARENTESISIZQ params PARENTESISDER PYC
    '''

    params = p[3]
    rango = params[1].lower()[1:-1]  # De '"seg"' a "seg"

    global rangoTiempo
    if not rango in rangoTiempo:
        errors.append("ERROR in line {0}! The third param must be a (Seg, Mil, Min)! "
                      "".format(p.lineno(1)))
        return "Error in Delay, line {0}.".format(p.lineno(5))

    # ['DELAY', 10, 'mil']
    p[0] = [p.lineno(1), "DELAY", params[0], rango]


"""   
PrintLed(Row, Colum, Valor)
Row: Entero
Col: Entero
Valor: Bool
"""


def p_PrintLed(p):
    '''
    funcionreservada : PRINTLED PARENTESISIZQ params PARENTESISDER PYC
    '''
    params = p[3]

    # ['PRINTLED', row, column, valor]
    p[0] = [p.lineno(1), "PRINTLED", params[0], params[1], params[2]]


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

    params = p[3]
    objeto = params[0].lower()[1:-1]  # De '"C"' a "c"

    global tipoObjeto
    if not objeto in tipoObjeto:
        errors.append("ERROR in line {0}! The param tipoObjeto must be (C,F,M)".format(p.lineno(1)))
        return "Error in PrintLedX, line {0}.".format(p.lineno(5))

    # ['DELAY', 10, 'mil']
    p[0] = [p.lineno(1), "PRINTLEDX", objeto, params[1], params[2]]


''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  ADRIAN  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''


def p_for(p):
    '''
    funcionreservada : FOR expression IN INT LLAVEIZQ ordenes LLAVEDER
                        | FOR expression IN expression LLAVEIZQ ordenes LLAVEDER
                        | FOR expression IN INT STEP INT LLAVEIZQ ordenes LLAVEDER
                        | FOR expression IN expression STEP INT LLAVEIZQ ordenes LLAVEDER
    '''

    if 'Step' not in p:
        p[0] = [p.lineno(1), 'FOR', p[2], p[4], p[6], 1]
    else:
        p[0] = [p.lineno(1), 'FOR', p[2], p[4], p[8], p[6]]


####################################### MATRICES ########################################################

def p_def_shapef(p):

    '''
    funcionreservada : ID IGUAL ID PUNTO SHAPEF PYC
    '''

    # [p.lineno(1), 'NEG', ID, INDICE]

    p[0] = [p.lineno(1), '=sf', p[1], p[3]]


def p_shapeF(p):

    '''
    funcionreservada : ID PUNTO SHAPEF PYC
    '''

    # [p.lineno(1), 'NEG', ID, INDICE]

    p[0] = [p.lineno(1), 'SHAPEF', p[1]]


def p_def_shapec(p):

    '''
    funcionreservada : ID IGUAL ID PUNTO SHAPEC PYC
    '''

    # [p.lineno(1), 'NEG', ID, INDICE]

    p[0] = [p.lineno(1), '=sc', p[1], p[3]]


def p_shapeC(p):

    '''
    funcionreservada : ID PUNTO SHAPEC PYC
    '''

    # [p.lineno(1), 'NEG', ID, INDICE]

    p[0] = [p.lineno(1), 'SHAPEC', p[1]]



def p_insertMatrix(p):
    '''
    funcionreservada : ID PUNTO INSERT PARENTESISIZQ input COMA expression COMA expression PARENTESISDER PYC

    '''

    if type(p[5]) == int or type(p[5]) == bool:
        errors.append("Error en la linea {0}. \'{1}\' el elemento a insertar debe ser de tipo lista.".format(p.lineno(1), p[5]))
        return None

    if type(p[7]) == bool:
        errors.append(
            "Error en la linea {0}. \'{1}\' el tipo de insercion solo acepta 1s o 0s.".format(p.lineno(1), p[7]))
        return None

    if type(p[9]) == bool:
        errors.append(
            "Error en la linea {0}. \'{1}\' el tercer elemento debe ser un entero.".format(p.lineno(1), p[9]))
        return None

    # [10, 'INSERT_MATRIX', ID, VALOR, TIPO_ADICION]
    p[0] = [p.lineno(1), 'INSERT_MATRIX', p[1], p[5], p[7], p[9]]




def p_deleteMatrix(p):
    '''
    funcionreservada : ID PUNTO DELETE PARENTESISIZQ valor_param COMA valor_param PARENTESISDER PYC
    '''

    # ['DEL', ID, INDICE, TIPOELIMINACION]
    p[0] = [p.lineno(1), 'DELETE_MATRIX', p[1], p[5], p[7]]



############################### BIFURCACION ###############################################



# Condicion
def p_condicion(p):
    """ condicion : expression IGUALES valorIf
                             | expression  MAYORQUE valorIf
                             | expression  MENORQUE valorIf
                             | expression  MENORIGUAL valorIf
                             | expression  MAYORIGUAL valorIf
                             | expression  DIFERENTE valorIf
    """
    p[0] = [p[1], p[2], p[3]]


def p_valorIf(p):
    """ valorIf : BOOLEAN
              | INT
    """
    p[0] = p[1]


# Definición de if
def p_if(p):
    """ funcionreservada : IF PARENTESISIZQ condicion PARENTESISDER LLAVEIZQ ordenes LLAVEDER
   """

    p[0] = [p.lineno(1), 'IF', p[3], p[6]]


###################################### PROCEDIMIENTOS ###############################################

def p_procedure(p):
    '''
    procedure : PROCEDURE ID PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC
                | PROCEDURE MAIN PARENTESISIZQ params PARENTESISDER LLAVEIZQ ordenes LLAVEDER PYC
    '''

    p[0] = [p.lineno(1), 'PROCEDURE', p[2], p[4], p[7]]

def p_empty_procedure(p):
    '''
    procedure : PROCEDURE ID PARENTESISIZQ params PARENTESISDER LLAVEIZQ LLAVEDER PYC
              | PROCEDURE MAIN PARENTESISIZQ params PARENTESISDER LLAVEIZQ LLAVEDER PYC
    '''

    p[0] = [p.lineno(1), None, p[1]]

def p_call(p):
    '''
    funcionreservada : CALL ID PARENTESISIZQ params PARENTESISDER PYC
    '''

    p[0] = [p.lineno(1), 'CALL', p[2], p[4]]



# Ordenes (se dan en forma de una lista de listas)
def p_ordenes(p):
    '''
    ordenes : statement
                       | ordenes statement
                       | ordenes funcionreservada
                       | funcionreservada

   '''

    # Si es solo un elemento
    if len(p) == 2:
        p[0] = [p[1]]

    # Si es más de una orden, se concatenan
    else:
        p[0] = p[1] + [p[2]]


def p_var_sublist_ID(p):
    """
    var_assign : ID IGUAL sublist PYC
    """
    # [line, '=', ['[]*', 'a', [['row', 0, 4]]] , [1, 2, 3, 4]]
    values = p[3]


    p[0] = [p.lineno(4), '=sublist', p[1], values]
    print("Sublista : ", p[0])

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%  OUTPUT  %%%%%%%%%%%%%%%%%%%%%%%%%%%% '''
# Create the dictionary in which we will store and retrieve all errors we get.
errors = []

# Build the parser
parser = yacc.yacc()

# Create a REPL to provide a way to interface with our calculator.
# print("\n--------- RESULTS ---------")

def run_syntax_analysis(insumo):
    global errors
    global parser

    errors = []

    # Build the parser
    parser = yacc.yacc()

    errors = []
    result = parser.parse(insumo)
    return (result, errors)


# Implementación para leer un archivo que será el insumo del parser
# with open(program_file, 'r') as file:
#     insumo = file.read()
#     result = parser.parse(insumo)
#     # pp.pprint(result)
