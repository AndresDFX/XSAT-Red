from os import listdir
from os.path import isfile, join

import re


PATH_SAT = "../InstanciasSAT"

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
            result.append(tuple([int(num) for num in clause_ftm]))

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

# Test
#sat = read_file_dimacs("{}/{}".format(PATH_SAT, "uf20-01.cnf"))
#print(sat)

# Duda, cargar todos los archivos en memoria
# o el programa debe tener la opcion de escoger una instancia sat para ser ejecutada

instancias_SAT = [f for f in listdir(PATH_SAT) if isfile(join(PATH_SAT, f))]
#print(instancias_SAT)