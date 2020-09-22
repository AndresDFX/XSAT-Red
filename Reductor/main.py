import itertools


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
    elements = to_SAT - 1
    clause = list(clause)

    first_clause = clause[:elements]
    middle_clauses = clause[elements:len(clause) - elements]
    last_clause = clause[len(clause) - elements:]

    # se crean la combinatoria de variables positivas y negativas
    literals = create_literals_k_greater_x(list_vars)

    # Formo la primera y ultima clausula de la concatenacion
    first_clause.append(literals[0])
    last_clause.append(literals[-1])

    # Elimino las variables usadas anteriormente en la lista de literales
    literals.pop(0)
    literals.pop(-1)

    # formar las clausulas medias
    middle_clauses = concatenate_clauses(middle_clauses, literals, to_SAT)

    result = [tuple(first_clause), *middle_clauses, tuple(last_clause)]
    return result


def create_clauses_k_less_x(clause, list_vars):
    """
    Returns the transformed clause starting from the combinatorial 
    of the variables for the specific case k < x
    """
    result = []

    for value in created_literals_k_less_x(list_vars):
        result.append((*clause, *value))

    return result


# aux func
def negative_and_positive_vars(value):
    return  -1 if value else 1


def create_literals_k_greater_x(list_vars):
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


def concatenate_clauses(middle_clauses, literals, to_SAT):
    """
    Returns the concatenation of new variables and literals for the middle clauses
    """
    result = []

    # formar las clausulas medias
    for value in middle_clauses:
        aux = []
        aux.append(value)
        while(len(aux) < to_SAT):
            aux.append(literals[0])
            literals.pop(0)
        result.append(tuple(aux))

    return result


def main(value, to_SAT):
    input_SAT = value
    num_vars = input_SAT[0][0]
    #num_clau = input_SAT[0][1]
    SAT = input_SAT[1]
    # Convertir a 3SAT

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

        new_SAT.append(create_clauses_SAT(clause, list_vars, to_SAT))

        # se inicializa nuevamente para que en la proxima clausula
        # se añadan las nuevas variables que corresponden
        list_vars = []
    
    # Reduccion del problema SAT
    print(new_SAT)

# Clase 2
# Ejercicio 1
# C = (a1, a2, -a3) (a2, -a3) (a1)
# SAT to 3SAT
# Solucion Esperada
# (1, 2, -3) (2, -3, 4) (2, -3, -4) (5, 6, 1) (5, -6, 1) (-5, 6, 1) (-5, -6, 1)
#main(([3, 3], [(1, 2, -3), (2, -3), (1, )]), 3)

# Clase 2
# Ejercicio 2
# C = (a1, a2, -a4) (a2, -a3) (a1, -a2, a3, a5, a6, -a7)
# SAT to 3SAT
# Solucion Esperada
# (1, 2, -4) (2, -3, 8) (-8, 2, -3) (1, -2, 9) (-9, 3, 10) (-10, 5, 11) (-11, 6, -7)
#main(([7, 3], [(1, 2, -4), (2, -3), (1, -2, 3, 5, 6, -7)]), 3)


# SAT to 4SAT
#Solucion Esperada
# (1, -2, 3, 7) (-7, 4, 5, -6)
# el problema radico en k - x variables, ya que se crearon dos variables
# la concatenacion considero que esta bien
#main(([6, 1], [(1, -2, 3, 4, 5, -6)]), 4)

# SAT to 5SAT
#Solucion Esperada
# Verificar esta solucion (1, -2, 3, 4, 5, 7) (-7, 3, 4, 5, -6)
main(([6, 1], [(1, -2, 3, 4, 5, -6)]), 5)