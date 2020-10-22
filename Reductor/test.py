import reductor
import shutil
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from time import time
from os import listdir, mkdir
from os.path import isfile, join, dirname, realpath

#PATH_SATH = "../InstanciasTriviales/"
PATH_SATH = "../InstanciasSAT/"


def test_check_multiple_xsat(file, number):
    filename = "{}{}".format(PATH_SATH, file)
    SAT = reductor.read_file_dimacs(filename)
    print("Solver SAT: ", reductor.solver_glucose(SAT[1]))

    for i in range(3, number):
        # SAT to XSAT
        # time in
        XSAT = reductor.reductor_SAT(SAT, i)[1]
        # time out
        #print("{}SAT:".format(i), XSAT)
        # Time In()
        print("Solver {}SAT".format(i), reductor.solver_glucose(XSAT))
         # Time Out()


def test_show_especific_xsat(file, to_xsat):
    path = './test'
    shutil.rmtree(path, ignore_errors=True)
    mkdir(path)
    filename = "{}{}".format(PATH_SATH, file)
    sat = reductor.read_file_dimacs(filename)
    xsat = reductor.reductor_SAT(sat, to_xsat)
    filename = "{}/{}-SAT".format(path, to_xsat)
    reductor.write_csv_file(filename, xsat, to_xsat)
    print("Ok! ver archivo")

def count_elapsed_time(f):
    """
    ¡BORRAR DESPUÉS!
    Decorator.
    Execute the function and calculate the elapsed time.
    Print the result to the standard output.
    """
    """
    def wrapper():
        # Start counting.
        start_time = time()
        # Take the original function's return value.
        ret = f()
        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        print("Elapsed time: %0.10f seconds." % elapsed_time)
        return ret
    
    return wrapper
    """

def count_elapsed_time(f):
    """
    Decorator.
    Execute the function and calculate the elapsed time.
    Print the result to the standard output.
    """
    def wrapper():
        # Start counting.
        start_time = time()
        # Take the original function's return value.
        ret = f()
        # Calculate the elapsed time.
        elapsed_time = time() - start_time
        total_time = "%0.10f" % elapsed_time
        print(total_time)
        return ret
    
    return wrapper

# implementar decorador
@count_elapsed_time
def test_check_especific_xsat():
    file = "01.cnf"
    
    to_xsat = 10
    """
    filename = "{}{}".format(PATH_SATH, file)
    sat = reductor.read_file_dimacs(filename)
    print("Solver SAT: ", reductor.solver_glucose(sat[1]))
    """
    filename = "{}{}".format(PATH_SATH, file)
    sat = reductor.read_file_dimacs(filename)
    xsat = reductor.reductor_SAT(sat, to_xsat)
    print("Solver {}SAT".format(to_xsat), reductor.solver_glucose(xsat[1]))
    print()

def test_check_all_instances(all_sat, all_xsat):
    files_sat = [f for f in listdir(all_sat) if isfile(join(all_sat, f))]
    files_xsat = [f for f in listdir(all_sat) if isfile(join(all_sat, f))]

    for file_sat, file_xsat in zip(files_sat, files_xsat):
        instances_sat = reductor.read_file_dimacs("{}{}".format(all_sat, file_sat))
        instances_xsat = reductor.read_file_dimacs("{}{}".format(all_xsat, file_xsat))
        print("Solver SAT:", reductor.solver_glucose(instances_sat[1]), "- Solver X-SAT:", reductor.solver_glucose(instances_xsat[1]))

# FUNCIÓN DE PRUEBA SAT
def test_sat():
    # intancias negativas empiezan desde uuf50-01.cnf
    print("AQUÍ COMIENZA SAT:")
    arraySAT = []
    for i in range(0, 10):
        tiempo_inicial = time()
        filename = "../InstanciasSAT/uf20-01" + str(i) + ".cnf"
        print(filename)
        sat = reductor.read_file_dimacs(filename)
        print("Solver SAT: ", reductor.solver_glucose(sat[1]))
        tiempo_final = time()
        tiempo_ejecucion = "{:.10f}".format(tiempo_final - tiempo_inicial)
        print(tiempo_ejecucion)
        arraySAT.append(tiempo_ejecucion)
    print("\n")
    print(arraySAT)
    print("\n")

# FUNCIÓN DE PRUEBA X-SAT
def test_xsat():
    # intancias negativas empiezan desde uuf50-01.cnf
    print("AQUÍ COMIENZA XSAT:")
    arrayXSAT = []
    for j in range(0, 10):
        tiempo_inicial = time()
        filename = "../X-SAT/uf20-01" + str(j) + ".cnf"
        print(filename)
        sat = reductor.read_file_dimacs(filename)
        print("Solver SAT: ", reductor.solver_glucose(sat[1]))
        tiempo_final = time()
        tiempo_ejecucion = "{:.10f}".format(tiempo_final - tiempo_inicial)
        print(tiempo_ejecucion)
        arrayXSAT.append(tiempo_ejecucion)
    print(arrayXSAT)
    print("\n")

plt.scatter(arraySAT, arrayXSAT)
plt.show()

"""
# TEST BRYAN
@count_elapsed_time
def test_sat():
    filename = "../InstanciasSAT/uf20-01.cnf"
    sat = reductor.read_file_dimacs(filename)
    print("Solver X-SAT: ", reductor.solver_glucose(sat[1]))
"""

"""
@count_elapsed_time
def test_xsat():
    filename = "../X-SAT/uf20-010.cnf"
    sat = reductor.read_file_dimacs(filename)
    print("Solver X-SAT: ", reductor.solver_glucose(sat[1]))
"""


def main():
    # TEST BRYAN
    test_sat()
    test_xsat()



    # Instancias SAT
    # Test para verificacion general del reductor
    # test_check_all_instances("../InstanciasSAT/", "../X-SAT/")
    # Instancias Triviales

    # Test 1 SAT to 5-SAT
    
    #test_show_especific_xsat("02.cnf", 5)

    # Test 2 SAT to 5-SAT

    # Instancias Positivas
    #test_check_especific_xsat()
    #test_check_especific_xsat("02.cnf", 5)

    # Instancias Negativas
    #test_check_especific_xsat("03.cnf", 5)
    #test_check_especific_xsat("04.cnf", 5)


    #-----------------------------------------------#
    # Other tests
    #-----------------------------------------------#

    # Instancias Positivas
    #test_check_multiple_xsat("01.cnf", 20)
    #test_check_multiple_xsat("02.cnf", 20)
    
    # Instancias Negativas
    #test_check_multiple_xsat("03.cnf", 20)
    #test_check_multiple_xsat("04.cnf", 20)

    # Instancias Positivas
    #test_check_multiple_xsat("uf20-01.cnf", 15)
    #test_check_multiple_xsat("uf20-050.cnf", 15)

    # Instancias Negativas
    #test_check_multiple_xsat("uuf50-01.cnf", 15)
    #test_check_multiple_xsat("uuf50-050.cnf", 15)

main()