# coding=utf-8
#importamos todas las piezas
from piece import Alfil
from piece import Rei
from piece import Torre
from piece import Peon
from piece import Reina
from piece import Caballo
import pygame


class Board:
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    # Inicialización del tablero
    def __init__(self, rows, cols):
        self.rows = 8
        self.cols = 8

        self.ready = False

        self.last = None

        self.copy = True
        self.board = [[0 for x in range(self.cols)] for _ in range(self.rows)]

        self.board[0][0] = Torre(0, 0, "b")
        self.board[0][1] = Caballo(0, 1, "b")
        self.board[0][2] = Alfil(0, 2, "b")
        self.board[0][3] = Reina(0, 3, "b")
        self.board[0][4] = Rei(0, 4, "b")
        self.board[0][5] = Alfil(0, 5, "b")
        self.board[0][6] = Caballo(0, 6, "b")
        self.board[0][7] = Torre(0, 7, "b")

        self.board[1][0] = Peon(1, 0, "b")
        self.board[1][1] = Peon(1, 1, "b")
        self.board[1][2] = Peon(1, 2, "b")
        self.board[1][3] = Peon(1, 3, "b")
        self.board[1][4] = Peon(1, 4, "b")
        self.board[1][5] = Peon(1, 5, "b")
        self.board[1][6] = Peon(1, 6, "b")
        self.board[1][7] = Peon(1, 7, "b")

        self.board[7][0] = Torre(7, 0, "w")
        self.board[7][1] = Caballo(7, 1, "w")
        self.board[7][2] = Alfil(7, 2, "w")
        self.board[7][3] = Reina(7, 3, "w")
        self.board[7][4] = Rei(7, 4, "w")
        self.board[7][5] = Alfil(7, 5, "w")
        self.board[7][6] = Caballo(7, 6, "w")
        self.board[7][7] = Torre(7, 7, "w")

        self.board[6][0] = Peon(6, 0, "w")
        self.board[6][1] = Peon(6, 1, "w")
        self.board[6][2] = Peon(6, 2, "w")
        self.board[6][3] = Peon(6, 3, "w")
        self.board[6][4] = Peon(6, 4, "w")
        self.board[6][5] = Peon(6, 5, "w")
        self.board[6][6] = Peon(6, 6, "w")
        self.board[6][7] = Peon(6, 7, "w")

        self.p1Name = "Player 1"
        self.p2Name = "Player 2"

        self.turn = "w"

        self.winner = None

    #Actualizamos la lista de todos los posibles movimientos de nuestras piezas
    def update_moves(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].update_valid_moves(self.board)

    #imprimir tablero
    def draw(self, win, color):
        if self.last and (color == self.turn):
            y, x = self.last[0]
            y1, x1 = self.last[1]

            xx = (4 - x) +round(self.startX + (x * self.rect[2] / 8))
            yy = 3 + round(self.startY + (y * self.rect[3] / 8))

            xx1 = (4 - x) + round(self.startX + (x1 * self.rect[2] / 8))
            yy1 = 3 + round(self.startY + (y1 * self.rect[3] / 8))
           

        s = None
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].draw(win, color)
                    if self.board[i][j].isSelected:
                        s = (i, j)

    #posibles movimientos de jaque
    def get_danger_moves(self, color):
        danger_moves = []
        for i in range(self.rows):
            for j in range(self.cols):
                #las casillas que esten ocupadas por piezas con un color diferente al nuestro
                if self.board[i][j] != 0:
                    if self.board[i][j].color != color:
                        #guardamos sus movimientos en la lista de peligro, por si coinciden con la posición del jaque
                        for move in self.board[i][j].move_list:
                            danger_moves.append(move)

        return danger_moves

    #Comprobamos si el rey esta en jaque
    def is_checked(self, color):
        #primero actualizamos move_list de las piezas necesario para obtener los danger_moves
        self.update_moves()
        danger_moves = self.get_danger_moves(color)
        rei_pos = (-1, -1)

        #buscamos la ubicación del rei
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].king and (self.board[i][j].color == color):
                        rei_pos = (j, i)

        #comprobamos si el rei se encuentra entre los movimientos de peligro
        if rei_pos in danger_moves:
            return True

        return False

    def select(self, col, row, color):
        changed = False
        prev = (-1, -1)

        #miramos si el sitio seleccionado tiene una pieza
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    if self.board[i][j].selected:
                        prev = (i, j)

        #si hemos seleccionado una pieza
        #comprobamos si donde la queremos mover esta vacio 
        if self.board[row][col] == 0 and prev!=(-1,-1):
            #seguidamente comprobamos si donde se desea mover la pieza pertenece a moves
            #si es el caso movemos la pieza
            if (row, col) in self.board[prev[0]][prev[1]].move_list:
                changed = self.move(prev, (row, col), color)

        #si donde la queremos mover esta ocupada o no hemos seleccionado una pieza
        else:
            #si no hemos seleccionado una pieza reseteamos selected a False
            if prev == (-1,-1):
                self.reset_selected()
                # y esta sera la nueva casilla seleccionada, pieza que queremos mover
                if self.board[row][col] != 0:
                    self.board[row][col].selected = True
            #si hemos selecionado una pieza pero donde queremos mover esta ocupado
            # MOVIMIENTO MATAR   
            else:
                #comprobamos que la pieza que queremos matar no es de nuestro color
                if self.board[prev[0]][prev[1]].color != self.board[row][col].color:
                    #si podemos movernos a su ubicacion nos movemos
                    if (row, col) in self.board[prev[0]][prev[1]].move_list:
                        changed = self.move(prev, (row, col), color)
                    # si resulta que las dos ultimas piezas seleccionadas son del mismo color
                    # comprobamos si esta pieza es de nuestro color
                    # si es el caso la seleccionamos como pieza que queremos mover
                    if self.board[row][col].color == color:
                        self.board[row][col].selected = True

                else:
                    #si es de nuestro color reseteamos la seleccion
                    if self.board[row][col].color == color:
                        self.reset_selected()
                        #la casilla donde nos queremos mover pasa a ser la seleccionada
                        self.board[row][col].selected = True
        #si se ha producido un movimiento cambiamos de jugador
        if changed:
            if self.turn == "w":
                self.turn = "b"
                self.reset_selected()
            else:
                self.turn = "w"
                self.reset_selected()

    #para resetear la selección
    def reset_selected(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].selected = False

    def check_mate(self, color):
        # si estamos en jaque
        #buscamos el rei
        #si todos los movimientos del rei coinciden con los peligrosos estamos en jaque mate
        if self.is_checked(color):
            rei = None
            
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] != 0:
                        if self.board[i][j].rei and self.board[i][j].color == color:
                            rei = self.board[i][j]
            if rei is not None:
                valid_moves = rei.valid_moves(self.board)
                danger_moves = self.get_danger_moves(color)
                danger_count = 0
                for move in valid_moves:
                    if move in danger_moves:
                        danger_count += 1
                return danger_count == len(valid_moves)

        return False

    def move(self, start, end, color):
        # primero de todo comprobamos si el rei esta en jaque
        checkedBefore = self.is_checked(color)
        changed = True
        nBoard = self.board[:]
        # si la pieza que movemos es un peon, ponemos la variable first a FALSE
        if bard[start[0]][start[1]].peon:
            board[start[0]][start[1]].first = False
        # movemos la pieza
        nBoard[start[0]][start[1]].change_pos((end[0], end[1]))
        # cambiamos la casilla por la pieza
        nBoard[end[0]][end[1]] = nBoard[start[0]][start[1]]
        #ponemos la posición origen a 0, ahora no habrá pieza ahí
        nBoard[start[0]][start[1]] = 0
        #actualizamos el tablero
        self.board = nBoard

        #si el rei ahora esta en jaque o antes lo estaba y ahora lo sigue estando
        if self.is_checked(color) or (checkedBefore and self.is_checked(color)):
            # no permitimos este movimiento y volvemos al tablero que teniamos al principio
            changed = False
            nBoard = self.board[:]
            if nBoard[end[0]][end[1]].peon:
                nBoard[end[0]][end[1]].first = True

            nBoard[end[0]][end[1]].change_pos((start[0], start[1]))
            nBoard[start[0]][start[1]] = nBoard[end[0]][end[1]]
            nBoard[end[0]][end[1]] = 0
            self.board = nBoard
        else:
            self.reset_selected()
        # actualizamos los nuevos movimientos validos
        self.update_moves()
        if changed:
            self.last = [start, end]
            if self.turn == "w":
                self.storedTime1 += (time.time() - self.startTime)
            else:
                self.storedTime2 += (time.time() - self.startTime)
            self.startTime = time.time()

        return changed
