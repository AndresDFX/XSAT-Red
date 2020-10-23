import re
import itertools
import shutil
import sys

from os import listdir, mkdir
from os.path import isfile, join, dirname, realpath
from pysat.solvers import Glucose3
from pysat.formula import CNF
from pysat.solvers import Lingeling

#PATH_SAT = "../InstanciasTriviales/"
PATH_SAT = "../graph_test/InstanciasSAT-Test/" # Instancias de prueba satisfactibles (7) e insatisfactibles (3)
#PATH_SAT = "../InstanciasSAT/"
PATH_XSAT = "../X-SAT/"

#------------------------------------------------#
# AUX FUNCTIONS FOR TRANSFORM SAT TO X SAT
#------------------------------------------------#

def create_clauses_SAT(clause, list_vars, to_sat):
    """
    Input:
      clause    : SAT instance clause
      list_vars : list of the new variables that must be added
                  depending on the case k < x or k > x
      to_SAT    : Variable that indicates the reduction of SAT
    Output:
      Returns the transformed clauses depending on the case k < x, k > x or k = x
    """
    k = len(clause)
    x = to_sat

    if k < x:
       return create_clauses_k_less_x(clause, list_vars)

    if k > x:
        return create_clauses_k_greater_x(clause, list_vars, to_sat)

    return clause


def create_clauses_k_greater_x(clause, list_vars, to_sat):
    """
    Returns the transformed clause starting from the combinatorial
    of the variables for the specific case k > x
    """
    iterations = len(list_vars) + 1
    # Numero de elementos para la primera y ultima clausula
    elements = to_sat - 1

    result = list()

    # Se crean las variables positivas y negativas
    # Ejemplo [8, -8, 9, -9]
    variables = create_vars_k_greater_x(list_vars)

    for index in range(iterations):
        if index == 0:
            firts_clause = clause[:elements]
            firts_clause.append(variables[0])
            variables.pop(0)
            result.append(firts_clause)

        elif index == iterations - 1:
            last_clause = clause[len(clause) - elements:]
            last_clause.append(variables[-1])
            variables.pop(0)
            result.append(last_clause)

        else:
            aux = clause[index+1:elements+index]
            while(len(aux) < to_sat):
                aux.append(variables[0])
                variables.pop(0)

            result.append(aux)

    # Ejemplo
    # [1, 2, 3, 8] [-8, 3, 4, 9] [-9, 4, 5, 6]
    return result


def create_clauses_k_less_x(clause, list_vars):
    """
    Returns the transformed clause starting from the combinatorial
    of the variables for the specific case k < x
    """
    result = []

    for value in created_literals_k_less_x(list_vars):
        result.append([*clause, *value])

    # Ejemplo, tenemos una clausula con tres literales 1, 2, 3
    # las nuevas clausulas seria
    # [[1, 2, 3, 8, 9], [1, 2, 3, 8, -9], [1, 2, 3, -8, 9], [1, 2, 3, -8, -9]]
    return result


def negative_and_positive_vars(value):
    return  -1 if value else 1


def create_vars_k_greater_x(list_vars):
    """
    Create a combinatorial of positive and negative variables
    from a list of variables
    """
    result = []

    for vars in list_vars:
        result.append(vars * negative_and_positive_vars(False))
        result.append(vars * negative_and_positive_vars(True))

    return result


def created_literals_k_less_x(list_vars):
    """
    Create a combinatorial of positive and negative variables
    from a list of variables
    """
    l = [False,True]
    bol = [list(i) for i in itertools.product(l,repeat=len(list_vars))]

    for i in range(len(bol)):
        for j in range(len(bol[i])):
            bol[i][j] = list_vars[j] * negative_and_positive_vars(bol[i][j])

    # Ejemplo si tenemos dos variables x1 y x2
    # [[8, 9], [8, -9], [-8, 9], [-8, -9]]
    return bol


def check_list_flatten(list):
    return type(list[0]) == int


#------------------------------------------------#
# AUX FUNCTIONS FOR READING AND WRITING FILES CNF
#------------------------------------------------#


def read_file_dimacs(filename):
    """
    Input:
      filename  - name of cnf SAT file
    Output:
      Returns next instance of SAT in the format:
      ([nvar, nclausules], [clause1, clause2, clausen])
    """
    sat = tuple()
    with open(filename, "r", newline='') as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if line.startswith("p"):
                sat = info_format(line), read_clause_format(lines[index + 1:])
                break

    return sat


def read_clause_format(clauses):
    """
    Input:
        list of string with clausules SAT
    Output
        return list of tuples with clausules SAT
    """
    result = list()
    for clause in clauses:
        if not (clause.startswith("%") or clause.startswith("0") ) and clause.strip():
            clause_ftm = re.sub(r'[^-\d]', " ", clause).strip().split()[:-1]
            result.append([int(num) for num in clause_ftm])

    return result


def info_format(info):
    """
    Input:
        Text string containing the number of variables and SAT clauses
    Output:
        Number of variables and clauses
    """
    value = re.sub(r'[^\d]', " ", info).strip().split()
    return [int(num) for num in value]


def write_csv_file(filename, xsat, to_xsat):
    """
    Input:
      filename  - name of cnf SAT file
    Output:
      Returns the new instance of SAT
    """
    info = xsat[0]
    clauses = xsat[1]
    with open(filename, 'w', newline='') as file:
        file.write("c {}-SAT \n".format(to_xsat))
        file.write("p cnf {} {} \n".format(info[0], info[1]))
        for clause in clauses:
            file.write(write_clause_format(clause))
            file.write("\n")


def write_clause_format(clause):
    str_clause = ""
    for value in clause:
        str_clause = "{} {}".format(str_clause, str(value))
    return "{} 0".format(str_clause.strip())


#------------------------------------------------#
# SOLVER FUNCTION
#------------------------------------------------#


def solver_glucose(sat):
    g = Glucose3()

    for clause in sat:
        g.add_clause(clause)

    return g.solve()

#------------------------------------------------#
# MAIN FUNCTION FOR TRANSFORM SAT TO XSAT
#------------------------------------------------#


def reductor_SAT(value, to_sat):
    """
    Input:
      value  - SAT instance with format ([nvar, nclausules], [clause1, clause2, clausen])
    Output:
      Returns the transformed instance SAT to XSAT in format dimacs
    """
    input_sat = value
    num_vars = input_sat[0][0]
    sat = input_sat[1]
    list_vars = []
    new_sat = []
    total_clauses = 0

    var = num_vars
    # Info total vars in instances SAT
    total_vars = num_vars

    for clause in sat:

        num_new_vars = abs(len(clause) - to_sat)
        total_vars = total_vars + num_new_vars

        # Creamos un listado de nuevas variables dependiendo de los K literales de cada clausula
        # Ejemplo
        # [8, 9]
        while num_new_vars > 0:
            var = var + 1
            list_vars.append(var)
            num_new_vars = num_new_vars - 1

        # Se crean las clausulas transformadas
        clause_transform = create_clauses_SAT(clause, list_vars, to_sat)
        # total clauses instances SAT
        total_clauses = total_clauses + len(clause_transform)

        if check_list_flatten(clause_transform):
            new_sat.append(clause_transform)
        else:
            for element in clause_transform:
                new_sat.append(element)

        # se inicializa nuevamente para que en la proxima clausula
        # se añadan las nuevas variables que corresponden
        list_vars = []

    # Reduccion del problema SAT
    return ([total_vars, total_clauses], new_sat)



def read_and_reduct_sat(to_xsat):
    """
    Read all SAT instances and generate corresponding XSAT files
    """
    # Delete folder XSAT
    shutil.rmtree(PATH_XSAT, ignore_errors=True)
    # Create folder XSAT
    mkdir(PATH_XSAT)


    print("> Making the reductions, please wait...")


    files = [f for f in listdir(PATH_SAT) if isfile(join(PATH_SAT, f))]

    # Read all instances SAT
    for file in files:
        instances = read_file_dimacs("{}{}".format(PATH_SAT, file))
        xsat = reductor_SAT(instances, to_xsat)
        filename = "{}{}".format(PATH_XSAT, file)
        write_csv_file(filename, xsat, to_xsat)

# Main function
if __name__ == "__main__":
    read_and_reduct_sat(int(sys.argv[1]))
    print("> All reductions have been made!")

