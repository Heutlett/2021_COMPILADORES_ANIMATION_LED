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
global_variables = []

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

# temp_var: variable que cambiará
# iterable: estructura usada para recorrer, normalmente será una lista, pero puede ser un entero (igual que range)
# Step: incremento

def ciclo_for(temp_var, iterable, step, ordenes):

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