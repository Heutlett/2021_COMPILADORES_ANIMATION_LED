import threading

from Syntax_Analysis import result
from Syntax_Analysis import errors
import pprint
import time

# Lista de arboles sintacticos generados en el analisis sintactico
sintacticList = result

# Errores generados en el analisis sintactico
errorList = errors

# Codigo main
main_code = []

# Lista de variables globales
global_variables = []

# Lista de blinks activos
blink_list = []

# Matriz actual
matriz = [[False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False],
          [False, False, False, False, False, False, False, False]]

# Pretty print para impresiones mas claras
pp = pprint.PrettyPrinter(indent=2)

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
                main_code = line[4]


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


""" ############################################################################################################### """




""" ####################################### Ejecucion principal #################################################### """



def main_execute():

    for linea in main_code:
        print(linea)






def exe_orden():
    pass



""" ####################################### Ejecucion principal #################################################### """




""" ###################################### Ejecuciones finales #################################################### """

""" #######################################  BLINK  ############################################################### """


def blink_cicle_start(row, column, tiempo, rangoTiempo):
    flag = True

    while (row, column) in blink_list:

        if rangoTiempo == "seg":
            time.sleep(tiempo)
        elif rangoTiempo == "mil":
            time.sleep(tiempo * 0.001)
        elif rangoTiempo == "min":
            time.sleep(tiempo * 60)

        matriz[row][column] = flag
        pp.pprint(matriz)
        print()
        if flag:
            flag = False
        else:
            flag = True


def init_new_blink_thread(row, column, tiempo, rangoTiempo):
    hilo = threading.Thread(target=blink_cicle_start(row, column, tiempo, rangoTiempo))
    hilo.run()


"""   
Blink(Fila, Columna, Tiempo, RangoTiempo, Estado)
Fila y columna: indice donde se encendera un led
Tiempo: Tiempo en el que se encenderan
RangoTiempo: "Seg", "Mil", "Min"
Estado: bool

['BLINK', f, c, int, rangotiempo, bool]
"""


def exe_blink(row, column, tiempo, rangoTiempo, estado):
    if estado:
        blink_list.append((row, column))
        init_new_blink_thread(row, column, tiempo, rangoTiempo)
    else:
        blink_list.remove((row, column))


""" #######################################  BLINK  ############################################################### """

""" #######################################  Delay  ############################################################### """


def delay_cicle_start(tiempo, rangoTiempo):
    count = 0

    while count <= tiempo:

        if rangoTiempo == "seg":
            time.sleep(1)
        elif rangoTiempo == "mil":
            time.sleep(1 * 0.001)
        elif rangoTiempo == "min":
            time.sleep(1 * 60)
        print("delay in " + rangoTiempo + ": " + str(count))
        count += 1


def init_new_delay_thread(tiempo, rangoTiempo):
    hilo = threading.Thread(target=delay_cicle_start(tiempo, rangoTiempo))
    hilo.run()


"""   
Delay(Tiempo, RangoTiempo)
Tiempo: Tiempo de delay
RangoTiempo: "Seg", "Mil", "Min"

['DELAY', 10, 'mil']
"""


def exe_delay(tiempo, rangoTiempo):
    init_new_delay_thread(tiempo, rangoTiempo)


""" #######################################  Delay  ############################################################### """

""" #######################################  PrintLed  ############################################################ """

"""   
PrintLed(Col, Row, Valor)
Col: Entero
Row: Entero
Valor: Bool
['PRINTLED', row, column, valor]
"""


def exe_print_led(row, column, value):
    if value:
        matriz[row][column] = True
    else:
        matriz[row][column] = False

    pp.pprint(matriz)
    print()


""" #######################################  PrintLed  ############################################################ """

""" #######################################  PrintLedX  ############################################################ """

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
                errors.append("Error, la lista que se desea adjuntar sobrepasa los limites de la matriz 8x8")

        pp.pprint(matriz)
        print()

    else:
        errors.append("Error, el indice debe ser entre 0 y 7")



""" #######################################  PrintLedX  ############################################################ """

# def contar(a):
#     '''Contar hasta cien'''
#     contador = 0
#     print(a)
#     while contador<100:
#         time.sleep(0.1)
#         contador+=1
#         print('Hilo:',
#               threading.current_thread().getName(),
#               'con identificador:',
#               threading.current_thread().ident,
#               'Contador:', contador)
#
#
# hilo1 = threading.Thread(target=contar(5))
# hilo1.start()


print("\n--------- Syntactic Analysis Result ---------")

pp.pprint(sintacticList)

print("\n--------- Errors ---------")
pp.pprint(errorList)


""" #######################################  Ejecucion  ############################################################ """

print("\n--------- Ejecutando el codigo ---------")

check_blocks()
check_main_count()

print("\n--------- Main code ---------")
pp.pprint(main_code)

print("\n--------- Linea a linea ---------")

main_execute()


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
