import itertools, random, main

#Algoritmo con heuristica para resolver buscaminas
jugadas = [[0,0]]
mines = []
def octocat(MATRIX):
    #---Si hay un 0 todas las del lado son seguras--
    # Si el valor de la celda es igual a los vecinos marcados, el resto de vecinos estan a salvo
    #Si el valor de la celda es igual a las de sus vecinos, esos vecinos son minas
    jugada = check_jugadas()
    if jugada is not None:
        return jugada
    #Esto debe hacerse en un bucle hasta que no haya mas minas que encuentres
    #Pones las minas encontradas en el tablero
    MATRIX_copy = check_minas(MATRIX)
    # Si el valor de la celda es igual a las de sus vecinos, esos vecinos son minas
    # Si el valor de la celda es igual a los vecinos marcados, el resto de vecinos estan a salvo
    search_mines(MATRIX_copy)
    print("minas",mines)
    print("jugadas",jugadas)
    jugada = check_jugadas()
    if jugada is not None:
        return jugada
    search_mines(MATRIX_copy)
    #si no hay retorna una combinacion posible de las que son posible sin las minas
    casillas_posibles = check_posibles_minas(MATRIX)
    return random.choice(casillas_posibles)
def check_posibles_minas(MATRIX):
    casillas_posibles = []
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[i])):
            if MATRIX[i][j] == '?' and adyacentes(MATRIX,i,j):
                if not any(mine == [i, j] for mine in mines):
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
def check_jugadas():
    if len(jugadas) >= 1:
        print("jugada",jugadas[0])
        return jugadas.pop(0)
    return None
def check_minas(MATRIX):
    if len(mines) > 0:
        for mine in mines:
            MATRIX[mine[0]][mine[1]] = 'X'
    return MATRIX
def search_mines(MATRIX):
    for i in range(len(MATRIX)):
        for j in range(len(MATRIX[i])):
            #chequear numeros si se quiere mas rapido
            if isinstance(MATRIX[i][j], int) and MATRIX[i][j] != 0:
                count,minas = count_mines(MATRIX,i,j)
                #si el numero es igual a sus vecinos, esos vecinos son minas o la cantidad de minas es igual a la casilla
                if MATRIX[i][j] == len(count) and count != []:
                    for c in count:
                        if c not in mines:
                            MATRIX[c[0]][c[1]] = 'X'
                            mines.append(c)
                    check_save(MATRIX, i, j, count)
                if MATRIX[i][j] == len(minas):
                    for c in minas:
                        if c not in mines:
                            MATRIX[c[0]][c[1]] = 'X'
                            mines.append(c)
                    check_save(MATRIX, i, j, minas)
def count_mines(MATRIX,i,j):
    count = []
    minas = []
    offsets = [-1, 0, 1]
    for di in offsets:
        for dj in offsets:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < len(MATRIX) and 0 <= nj < len(MATRIX[0]) and (MATRIX[ni][nj] == '?' or MATRIX[ni][nj] == 'X' ):
                count.append([ni,nj])
            if 0 <= ni < len(MATRIX) and 0 <= nj < len(MATRIX[0]) and MATRIX[ni][nj] == 'X':
                minas.append([ni,nj])
    return count, minas
def check_save(MATRIX, i, j, count):
    offsets = [-1, 0, 1]
    for di in offsets:
        for dj in offsets:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < len(MATRIX) and 0 <= nj < len(MATRIX[0]) and MATRIX[ni][nj] == '?':
                if [ni, nj] not in count:
                    if [ni, nj] not in jugadas:
                        MATRIX[ni][nj] = 'S'
                        jugadas.append([ni, nj])