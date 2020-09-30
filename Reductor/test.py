import reductor

#PATH_SATH = "../InstanciasTriviales/"
PATH_SATH = "../InstanciasSAT/"

def test(file, number):
    filename = "{}{}".format(PATH_SATH, file)
    SAT = reductor.read_file_dimacs(filename)
    # Solver
    #print(SAT)
    print("Solver SAT: ", reductor.solver_glucose(SAT[1]))

    for i in range(3, number):
        # SAT to XSAT
        XSAT = reductor.reductor_SAT(SAT, i)
        #print("{}SAT:".format(i), XSAT)
        print("Solver {}SAT".format(i), reductor.solver_glucose(XSAT))

def main():
    #test("01.cnf", 20)
    #test("02.cnf", 20)
    #test("03.cnf", 20)
    #test("04.cnf", 15)

    #test("uf20-01.cnf", 15)
    #test("uf20-070.cnf", 15)
    test("uf20-095.cnf", 15)


main()