# Hacer una lista donde tengamos las minas posibles dependiendo del tablero
# Revisar compatibilidad con los numeros adyacentes y las minas vistas
import itertools, random, main
jugadas = [[0,0]]
mines = []
numeros_revisar = []
def tux(MATRIX):
    # Lista de minas posibles -> osea casillas que tengan adyacentes a ellos numeros -> sacar los numeros y los adyacentes posibles
    #revisar si hay jugadas por hacer
    jugada = check_jugadas()
    if jugada is not None:
        return jugada
    #Revisar si hay minas ya puestas y si ya hay numeros adyacentes a ellas chequeados
    MATRIX = check_minas(MATRIX)
    check_numeros(MATRIX)
    #Revisar si hay casillas adyacentes a numeros que no tengan minas
    casillas_posibles = check_posibles_minas(MATRIX)
    #Empezar a revisar combinaciones de minas posibles segun los numeros, y la combinacion que ya se ecuentre
    lista_combinaciones = todas_las_combinaciones(casillas_posibles)
    # Revisar una por una las combinaciones de minas posibles
    combinaciones(0, MATRIX, lista_combinaciones, casillas_posibles)
    print("jugadas",jugadas)
    print("minas",mines)
    #Despues de estar seguro de las minas posibles, poner las jugadas posibles en un arreglo y jugarlas
    jugada = check_jugadas()
    if jugada is not None:
        return jugada
    #Hacerlo hasta que funcione
    #Condicion, si no hay minas posibles, jugar random
    print("random")
    return random.choice(casillas_posibles)
def check_jugadas():
    if len(jugadas) >= 1:
        print("jugada",jugadas[0])
        return jugadas.pop(0)
    return None
def check_minas(MATRIX):
    if len(mines) > 0:
        for mine in mines:
            for m in mine:
                MATRIX[m[0]][m[1]] = 'X'
    return MATRIX
def check_numeros(MATRIX):
    numeros_revisar = []
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[i])):
            if isinstance(MATRIX[i][j], int) and MATRIX[i][j] != 0:
                numeros_revisar.append(MATRIX[i][j])
    return numeros_revisar
def check_posibles_minas(MATRIX):
    casillas_posibles = []
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[i])):
            if MATRIX[i][j] == '?' and adyacentes(MATRIX,i,j):
                if not any([i, j] in mine for mine in mines):
                    casillas_posibles.append([i, j])
    return casillas_posibles
def adyacentes(MATRIX, i, j):
    nums_disponibles = []
    offsets = [-1, 0, 1]
    for di in offsets:
        for dj in offsets:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < len(MATRIX) and 0 <= nj < len(MATRIX[0]):
                if isinstance(MATRIX[ni][nj], int):
                    nums_disponibles.append([ni, nj])
                    return True

    return False
def todas_las_combinaciones(casillas_posibles):
    combinaciones = []
    for r in range(len(mines), len(casillas_posibles) + 1):
        for comb in itertools.combinations(casillas_posibles, r):
                combinaciones.append(comb)
    return combinaciones
def combinaciones(i, MATRIX, lista_combinaciones, casillas_posibles):
    # Si ya se revisaron todas las combinaciones posibles
    if i >= len(lista_combinaciones):
        return
    # Hacer una copia de la matriz
    MATRIX_copy = [row[:] for row in MATRIX]
    # Obtener la combinacion actual
    combinacion = lista_combinaciones[i]
    # Iterar sobre la combinacion actual y poner minas
    for j in range(len(combinacion)):
        MATRIX_copy[combinacion[j][0]][combinacion[j][1]] = 'X'
    # Poner 'P' en las casillas que no son minas y son posibles
    for j in range(len(casillas_posibles)):
        if casillas_posibles[j] not in lista_combinaciones[i]:
            MATRIX_copy[casillas_posibles[j][0]][casillas_posibles[j][1]] = 'P'
    # Revisar si la combinacion actual es valida
    if es_valida(MATRIX_copy):
        append_jugadas(MATRIX_copy)
        return
    else:
        combinaciones(i+1, MATRIX, lista_combinaciones, casillas_posibles)

    return
def es_valida(MATRIX):
    # Comprobamos si el número de minas adyacentes a cada casilla coincide con el número en esa casilla
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[i])):
            if isinstance(MATRIX[i][j], int):
                if MATRIX[i][j] != count_adjacent_mines(MATRIX, i, j):
                    return False
    return True
def count_adjacent_mines(MATRIX, i, j):
    count = 0
    offsets = [-1, 0, 1]
    for di in offsets:
        for dj in offsets:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < len(MATRIX) and 0 <= nj < len(MATRIX[0]) and MATRIX[ni][nj] == 'X':
                count += 1
    return count
def append_jugadas(MATRIX):
    mines_aux = []
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[i])):
            if MATRIX[i][j] == 'P':
                jugadas.append([i, j])
            if MATRIX[i][j] == 'X' and [i, j] not in mines:
                if not any([i, j] in mine for mine in mines):
                    mines_aux.append([i, j])
    mines.append(mines_aux)