from os import mkdir
import reductor
import shutil

#PATH_SATH = "../InstanciasTriviales/"
PATH_SATH = "../InstanciasSAT/"

def test_check_multiple_xsat(file, number):
    filename = "{}{}".format(PATH_SATH, file)
    SAT = reductor.read_file_dimacs(filename)
    print("Solver SAT: ", reductor.solver_glucose(SAT[1]))

    for i in range(3, number):
        # SAT to XSAT
        XSAT = reductor.reductor_SAT(SAT, i)[1]
        #print("{}SAT:".format(i), XSAT)
        print("Solver {}SAT".format(i), reductor.solver_glucose(XSAT))


def test_show_especific_xsat(file, to_xsat):
    path = './test'
    shutil.rmtree(path, ignore_errors=True)
    mkdir(path)
    filename = "{}{}".format(PATH_SATH, file)
    sat = reductor.read_file_dimacs(filename)
    xsat = reductor.reductor_SAT(sat, to_xsat)
    filename = "{}/{}-SAT".format(path, to_xsat)
    reductor.write_csv_file(filename, xsat, to_xsat)


def test_check_especific_xsat(file, to_xsat):
    filename = "{}{}".format(PATH_SATH, file)
    sat = reductor.read_file_dimacs(filename)
    print("Solver SAT: ", reductor.solver_glucose(sat[1]))
    xsat = reductor.reductor_SAT(sat, to_xsat)
    print("Solver {}SAT".format(to_xsat), reductor.solver_glucose(xsat[1]))
    print()



def main():
    # Instancias Triviales

    # Test 1 SAT to 5-SAT
    #test_show_especific_xsat("02.cnf", 5)

    # Test 2 SAT to 5-SAT

    # Instancias Positivas
    #test_check_especific_xsat("01.cnf", 5)
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