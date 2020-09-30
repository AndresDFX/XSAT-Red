
from os import listdir
from os.path import isfile, join
from pysat.solvers import Glucose3
from pysat.formula import CNF
from pysat.solvers import Lingeling


import re
import itertools


#------------------------------------------------#
# AUX FUNCTIONS FOR TRANSFORM SAT TO X SAT
#------------------------------------------------#

def create_clauses_SAT(clause, list_vars, to_SAT):
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
    x = to_SAT
    
    if k < x:
       return create_clauses_k_less_x(clause, list_vars)
    
    if k > x:
        return create_clauses_k_greater_x(clause, list_vars, to_SAT)

    return clause


def create_clauses_k_greater_x(clause, list_vars, to_SAT):
    """
    Returns the transformed clause starting from the combinatorial 
    of the variables for the specific case k > x
    """
    iterations = len(list_vars) + 1
    # Numero de elementos para la primera y ultima clausula
    elements = to_SAT - 1
    
    result = list()

    # Se crean la combinatoria de variables positivas y negativas
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
            while(len(aux) < to_SAT):
                aux.append(variables[0])
                variables.pop(0)
            
            result.append(aux)

    return result


def create_clauses_k_less_x(clause, list_vars):
    """
    Returns the transformed clause starting from the combinatorial 
    of the variables for the specific case k < x
    """
    result = []

    for value in created_literals_k_less_x(list_vars):
        result.append([*clause, *value])

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

    return bol


def check_list_flatten(list):
    return type(list[0]) == int


#------------------------------------------------#
# AUX FUNCTIONS FOR READING FILES CNF 
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
                sat = info_format(line), clause_format(lines[index + 1:])
                break

    return sat


def clause_format(clauses):
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


def reductor_SAT(value, to_SAT):
    """
    Input:
      value  - SAT instance with format ([nvar, nclausules], [clause1, clause2, clausen])
    Output:
      Returns the transformed instance SAT to XSAT
    """
    input_SAT = value
    num_vars = input_SAT[0][0]
    SAT = input_SAT[1]
    list_vars = []
    new_SAT = []

    var = num_vars
    for clause in SAT:

        num_new_vars = abs(len(clause) - to_SAT)
    
        # Crea las nuevas variables dependiendo de los K literales de cada clausula
        while num_new_vars > 0:
            var = var + 1
            list_vars.append(var)
            num_new_vars = num_new_vars - 1

        clause_transform = create_clauses_SAT(clause, list_vars, to_SAT)

        if check_list_flatten(clause_transform):
            new_SAT.append(clause_transform)
        else:
            for element in clause_transform:
                new_SAT.append(element)

        # se inicializa nuevamente para que en la proxima clausula
        # se añadan las nuevas variables que corresponden
        list_vars = []
    
    # Reduccion del problema SAT
    return new_SAT



def main():
    #instancias_SAT = [f for f in listdir(PATH_SAT) if isfile(join(PATH_SAT, f))]
    #print(instancias_SAT)
    pass
    


main()