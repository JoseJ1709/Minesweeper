import math
import random
import combinations
import heuristica

ROWS = 9
COLUMNS = 9
MINE_COUNT = 10

BOARD = []
MINES = set()
EXTENDED = set()

MATRIX = [['?'] * COLUMNS for i in range(ROWS)]


class Colors(object):
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'


def colorize(s, color):
    return '{}{}{}'.format(color, s, Colors.ENDC)


def get_index(i, j):
    if 0 > i or i >= COLUMNS or 0 > j or j >= ROWS:
        return None
    return i * ROWS + j

# Funcion para crear el tablero#
def create_board():
    # Calcula el total de la matrix 10 x 10
    squares = ROWS * COLUMNS

    # Create board
    # Dijuba por cada casilla un [ ]
    for _ in range(squares):
        BOARD.append('[ ]')

    # Create mines#
    while True:
        #Mientras halla minas#
        if len(MINES) >= MINE_COUNT:
            break
        #Agrega minas aleatorias y las pone en MINES.#
        MINES.add(int(math.floor(random.random() * squares)))


def draw_board():

    lines = []
    # Recorre fila por fila#
    for j in range(ROWS):
        # Cuando la fila es 0
        if j == 0:
            #imprime los numeros de las columnas, itera por cada columna y da el formato dependiendo el x
            lines.append('   ' + ''.join(' {} '.format(x) for x in range(COLUMNS)))
        #imprime los numeros de las filas de la misma forma que las columnas pero no tiene que iterar
        line = [' {} '.format(j)]
        # Itera sobre las columnas de esa fila
        for i in range(COLUMNS):
            #Agrega cada posicion i j al arreglo line#
            line.append(BOARD[get_index(i, j)])
        #Depues de iterar sobre todas las columnas de una fila,
        #agrupa todas las lineas de line y las serpara por un espacio para sumarlas al arreglo princial
        lines.append(''.join(line))
    #Esto lo que hace es crear un arreglo fila por fila con lo que tenga el BOARD
    # Por ejemplo la primera fila que se genera son los numeros de 0 1 2 3 . que son las colunas
    # Y por cada fila, se va añadiendo el numero correspondiente y lo que tenga el BOARD en esa posicion
    # Oea la siguiente es 0 [ ] [ ] [ ].. y asi hasta construir el tablero y lo voletea para que se vea como un tablero
    return '\n'.join(reversed(lines))

# Funcion para revisar la seleccion del usuario#
def parse_selection(raw_selection):
    try:
        # primero separa los caracteres por espacions 1,2,3 = ['1,' '2,' '3']
        # despues quita las comas de cada caracter al principio o final ['1' '2' '3']
        # con int (10) convierte la lista en numeros enteros [1 2 3]
        return [int(x.strip(','), 10) for x in raw_selection.split(' ')]
    except Exception:
        #puede que no sean numeros asi que no se pueden castear#
        return None


def adjacent_squares(i, j):
    # Inicializa el numero de minas en 0
    num_mines = 0
    # Inicializa la lista de casillas a revisar
    squares_to_check = []
    # Va a revisar los adyacentes de la casilla seleccionada, por eso empieza en -1 y -1 porque deben revisar
    # las casillas de la izquierda  = '-1'
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            # cuando di y dj son 0, significa que es la misma casilla
            if di == dj == 0:
                continue
            # Obtiene las coordenadas de la casilla adyacente sumandole las coordenadas que queremos revisar
            coordinates = i + di, j + dj

            # Obtiene el index de la casilla adyacente, osea el punto que va a resviar.
            proposed_index = get_index(*coordinates)
            #revisa que el punto no este vacio
            if not proposed_index:
                continue
            #si el punto esta en MINES
            if proposed_index in MINES:
                #suma 1 a la lista de las minas#
                num_mines += 1
            # se añade la lista de casillas a revisar
            squares_to_check.append(coordinates)
    #retorna el numero de minas y las casillas a revisar
    return num_mines, squares_to_check


def update_board(square, selected=True):
    # Obtiene las coordenadas que selecciono
    i, j = square
    # Obtiene el index de la seleccion, osea la posicion en el tablero
    index = get_index(i, j)
    #Añade a una lista la poscicion seleccionada
    EXTENDED.add(index)

    # Si la posicion seleccionada esta en MINES osea si hay una mina en esa posicion
    if index in MINES:
        # si selected es falso, osea si no se selecciono la casilla
        if not selected:
            return
        # si se selecciono la casilla, se pone una X en la casilla, piso una mina
        BOARD[index] = colorize(' X ', Colors.RED)
        return True
    else:
        # si no hay mina en la casilla seleccionada
        # llama a la funcion para revisar las casillas adyacentes que tiene que revisar y la cantidad de minas que hay
        num_mines, squares = adjacent_squares(i, j)
        # se le asinga a la poicion seleccionada el numero de minas encontradas
        MATRIX[i][j] = num_mines
        if num_mines:
            # si hay una mina
            if num_mines == 1:
                #si hay color de el numero de minas a azul
                text = colorize(num_mines, Colors.BLUE)
            elif num_mines == 2:
                #si hay 2 el color de numero de minas en azul
                text = colorize(num_mines, Colors.GREEN)
            else:
                # si hay 3 el color de numero de minas es rojo
                text = colorize(num_mines, Colors.RED)
            # A la posicion seleccionada se le asigna el numero de minas, con su respectivo color
            BOARD[index] = ' {} '.format(text)
            return
        else:
            # si no hay minas en las casillas adyacentes se le pone un espacio
            BOARD[index] = '   '
            # Itera sobre las casillas adyacentes que se encontraron
            for asquare in squares:
                # Obtiene el index de la casilla adyacente
                aindex = get_index(*asquare)
                # si la casilla adyacente ya fue revisada
                if aindex in EXTENDED:
                    continue
                # si la casilla adyacente no ha sido revisada
                EXTENDED.add(aindex)
                # llama a la funcion para revisar la casilla adyacente
                update_board(asquare, False)


def reveal_mines():
    for index in MINES:
        if index in EXTENDED:
            continue
        BOARD[index] = colorize(' X ', Colors.YELLOW)


def has_won():
    return len(EXTENDED | MINES) == len(BOARD)


def random_player():
    options = []
    for i in range(ROWS):
        for j in range(COLUMNS):
            if MATRIX[i][j] == '?':
                options.append((i, j))
    rand_square = options[random.randint(0, len(options))]
    print(f'Random player plays {rand_square}')
    return rand_square
    # NO SE PUEDE REVISAR  MINES!!!
    #TODO: 1. Combinaciones de opciones seleccionadas y no seleccionadas (fuerza bruta)
    #TODO: 2. Heurística: Revisar combinaciones promisorias

if __name__ == '__main__':
    # Crea el tablero
    create_board()

    print('Enter coordinates (ie: 0 3)')

    while True:
        #dibuja el tablero
        print(draw_board())
        # square = random_player()
        # agarra el input de la terminal y llama a la funcion para mirar ese input#
        #square = parse_selection(input('> '))
        square = combinations.tux(MATRIX)
        #square = heuristica.octocat(MATRIX)
        print(square)
        #square contiene una cantidad de numeros enteros que el usuario ingreso
        #si son mas de dos numeros no es valido
        if not square or len(square) < 2:
            print('Unable to parse indicies, try again...')
            continue
        #llama a la funcion para actualizar el tablero con la seleccion del usuario
        mine_hit = update_board(square)
        #si se piso una mina o si ya se gano
        if mine_hit or has_won():
            # si le pego a una mina
            if mine_hit:
                #muestra las minas en el tablero
                reveal_mines()
                #Dibuja el tablero
                print(draw_board())
                #Y pone game over
                print('Game over')
            else:
                #Si gano muestra el tablero y dice que gano
                print(draw_board())
                print('You won!')
            break
