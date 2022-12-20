# coding=utf-8
import pygame
import os

#descargamos las imagenes de la carpeza img 
b_alfil = pygame.image.load(os.path.join("img", "black_bishop.png"))
b_rei = pygame.image.load(os.path.join("img", "black_king.png"))
b_caballo = pygame.image.load(os.path.join("img", "black_knight.png"))
b_peon = pygame.image.load(os.path.join("img", "black_pawn.png"))
b_reina = pygame.image.load(os.path.join("img", "black_queen.png"))
b_torre = pygame.image.load(os.path.join("img", "black_rook.png"))

w_alfil = pygame.image.load(os.path.join("img", "white_bishop.png"))
w_rei = pygame.image.load(os.path.join("img", "white_king.png"))
w_caballo = pygame.image.load(os.path.join("img", "white_knight.png"))
w_peon = pygame.image.load(os.path.join("img", "white_pawn.png"))
w_reina = pygame.image.load(os.path.join("img", "white_queen.png"))
w_torre = pygame.image.load(os.path.join("img", "white_rook.png"))

#colocamos las piezas en un vector para poder identificar el tipo
b = [b_alfil, b_rei, b_caballo, b_peon, b_reina, b_torre]
w = [w_alfil, w_rei, w_caballo, w_peon, w_reina, w_torre]

B = []
W = []

for img in b:
    B.append(pygame.transform.scale(img, (55, 55)))

for img in w:
    W.append(pygame.transform.scale(img, (55, 55)))


class Piece:
    img = -1
    rect = (113, 113, 525, 525)
    startX = rect[0]
    startY = rect[1]

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.selected = False
        self.move_list = []
        self.rey = False
        self.peon = False

    def isSelected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, win, color):
        if self.color == "w":
            drawThis = W[self.img]
        else:
            drawThis = B[self.img]

        x = (4 - self.col) + round(self.startX + (self.col * self.rect[2] / 8))
        y = 3 + round(self.startY + (self.row * self.rect[3] / 8))

        if self.selected and self.color == color:
            pygame.draw.rect(win, (255, 0, 0), (x, y, 62, 62), 4)

        win.blit(drawThis, (x, y))

        '''if self.selected and self.color == color:  # Remove false to draw dots
            moves = self.move_list
            for move in moves:
                x = 33 + round(self.startX + (move[0] * self.rect[2] / 8))
                y = 33 + round(self.startY + (move[1] * self.rect[3] / 8))
                pygame.draw.circle(win, (255, 0, 0), (x, y), 10)'''

    #para cambiar la posicion de las piezas
    def change_pos(self, pos):
        self.row = pos[0]
        self.col = pos[1]

    def __str__(self):
        return str(self.col) + " " + str(self.row)


class Alfil(Piece):
    img = 0

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        #ARRIBA
        djR = j + 1 #derecha
        djL = j - 1 #izquierda
        for di in range(i - 1, -1, -1):
            #marcamos el margen, porque si no saldriamos del tablero
            if djR < 8:
                #si la posicion no esta ocupada lo consideramos un movimiento valido
                if board[di][djR] == 0:
                    moves.append((di, djR))
                #pero si esta ocupada de una pieza del adversario la matamos
                elif board[di][djR].color != self.color:
                   moves.append((di, djR))
                   break
            djR += 1
            
            if djL > -1:
                if board[di][djL] == 0:
                    mover.append((di, djL))
                elif board[di][djL].color != self.color:
                    moves.append((di,djL))
                    break
            djL -= 1

        # ABAJO
        djR = j + 1 #DERECHA
        djL = j - 1 #IZQUIERDA
        for di in range(i + 1, 8):
            if djR < 8:
                if board[di][djR] == 0:
                    moves.append((di, djL))
                elif board[di][djR].color != self.color:
                    moves.append((di, djL))
                    break
            djR += 1
            if djL > -1:
                if board[di][djL] == 0:
                    moves.append((di, djL))
                elif board[di][djL].color != self.color:
                    moves.append((di, djL))
                    break
            djL -= 1

        #devolvemos los movimientos validos del alfil
        return moves


class Rei(Piece):
    img = 1

    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.rei = True

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        #ABAJO
        if i+1 < 8:

            if j+1 < 8:
                if board[i+1][j+1] == 0:
                    moves.append((i+1,j+1))
                elif board[i+1][j+1].color != self.color:
                    moves.append((i+1,j+1))

            if j-1 > -1:
                if board[i+1][j-1] == 0:
                    moves.append((i+1,j-1))
                elif board[i+1][j-1].color != self.color:
                    moves.append((i+1,j-1))

            if board[i+1][j] == 0:
                moves.append((i+1,j))
            elif board[i+1][j].color != swlf.color:
                moves.append((i+1,j))

        #ARRIBA
        if i-1 > -1:

            if j+1 < 8:
                if board[i-1][j+1] == 0:
                    moves.append((i-1,j+1))
                elif board[i-1][j+1].color != self.color:
                    moves.append((i-1,j+1))

            if j-1 > -1:
                if board[i-1][j-1] == 0:
                    moves.append((i-1,j-1))
                elif board[i-1][j-1].color != self.color:
                    moves.append((i+1,j-1))

            if board[i-1][j] == 0:
                moves.append((i-1,j))
            elif board[i-1][j].color != swlf.color:
                moves.append((i-1,j))
        
        #MEDIO
        if j+1 > 8:
            if board[i][j+1] == 0:
                moves.append((i,j+1))
            elif board[i][j+1].color != self.color:
                moves.append((i,j+1))
                

        if j-1 < -1:
            if board[i][j-1] == 0:
                moves.append((i,j-1))
            elif board[i][j-1].color != self.color:
                moves.append((i,j-1))
    
        return moves


class Caballo(Piece):
    img = 2

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        #DERECHA
        if i+2 < 8:
            if j+1 < 8:
                if board[i+2][j+1] == 0:
                    moves.append((i+2,j+1))
                elif board[i+2][j+1].color != self.color:
                    moves.append((i+2,j+1))
            if j-1 > -1:
                if board[i+2][j-1] == 0:
                    moves.append((i+2,j-1))
                elif board[i+2][j-1].color != self.color:
                    moves.append((i+2,j-1))
        #IZQUIERDA
        if i-2 > -1:
            if j+1 < 8:
                if board[i-2][j+1] == 0:
                    moves.append((i-2,j+1))
                elif board[i-2][j+1].color != self.color:
                    moves.append((i-2,j+1))
            if j-1 > -1:
                if board[i-2][j-1] == 0:
                    moves.append((i-2,j+1))
                elif board[i-2][j-1].color != self.color:
                    moves.append((i-2,j-1))
        
        #ARRIBA Y ABAJO
        if i+1 < 8:
            if j+2 < 8:
                if board[i+1][j+2] == 0:
                    moves.append((i+1,j+2))
                elif board[i+1][j+2].color != self.color:
                    moves.append((i+1,j+2))
            if j-2 > -1:
                if board[i+1][j-2] == 0:
                    moves.append((i+1,j-2))
                elif board[i+1][j-2].color != self.color:
                    moves.append((i+1,j-2))

        if i-1 > -1:
            if j+2 < 8:
                if board[i-1][j+2] == 0:
                    moves.append((i-1,j+2))
                elif board[i-1][j+2].color != self.color:
                    moves.append((i-1,j+2))
            if j-2 > -1:
                if board[i-1][j-2] == 0:
                    moves.append((i-1,j-2))
                elif board[i-1][j-2].color != self.color:
                    moves.append((i-1,j-2))

        return moves


class Peon(Piece):
    img = 3

    def __init__(self, row, col, color):
        Piece.__init__(self, row, col, color)
        self.first = True
        self.reina = False
        self.peon = True

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        # NEGRO
        if self.color == "b":
            # el primer movimiento de los peones puede abanzar dos casillas en el caso de las negras ubicados en la fila 1
            if i == 1:
                # ABANZAR
                if board[i+1][j] == 0:
                    moves.append((i+1, j))
                if board[i+2][j] == 0:
                    moves.append((i+2, j))

                # MATAR
                if j+1 < 8:
                    if board[i+1][j+1] != 0:
                        if board[i+1][j+1].color != self.color:
                            moves.append((i+1, j+1))
                if j-1 > -1:
                    if board[i+1][j-1] != 0:
                        if board[i+1][j-1].color != self.color:
                            moves.append((i+1, j-1))

            elif i < 7:
                # ABANZAR
                if board[i+1] == 0:
                    moves.append((j, i + 1))
                # MATAR
                if j+1 < 8:
                    if board[i+1][j+1] != 0:
                        if board[i+1][j+1].color != self.color:
                            moves.append((j+1, i+1))

                if j-1 > -1:
                    if board[i+1][j-1] != 0:
                        if board[i+1][j-1].color != self.color:
                            moves.append((j-1, i+1))

        # BLANCO
        else:
            if i == 6:
                # ABANZAR
                if board[i-1][j] == 0:
                    moves.append((i-1, j))
                if board[i-2][j] == 0:
                    moves.append((i-2, j))

                # MATAR
                if j+1 < 8:
                    if board[i-1][j+1] != 0:
                        if board[i-1][j+1].color != self.color:
                            moves.append((i-1, j+1))
                if j-1 > -1:
                    if board[i-1][j-1] != 0:
                        if board[i-1][j-1].color != self.color:
                            moves.append((i-1, j-1))

            elif i < 7:
                # ABANZAR
                if board[i+1] == 0:
                    moves.append((j, i + 1))
                # MATAR
                if j+1 < 8:
                    if board[i+1][j+1] != 0:
                        if board[i+1][j+1].color != self.color:
                            moves.append((j+1, i+1))

                if j-1 > -1:
                    if board[i+1][j-1] != 0:
                        if board[i+1][j-1].color != self.color:
                            moves.append((j-1, i+1))

        return moves


class Reina(Piece):
    img = 4

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = [] 

        #ABAJO
        if i+1 < 8:
            for di in range(i+1, 8):
            #DERECHA
                if j+1 < 8:
                    for dj in range(j+1, 8):
                        if dj < 8:
                            if board[di][dj] == 0:
                                moves.append((di,dj))
                            elif board[di][dj].color != self.color:
                                moves.append((di,dj))
                                break
            #IZQUIERDA
                if j-1 > -1:
                    for dj in range(j-1, -1, -1):
                        if dj > -1:
                            if board[di][dj] == 0:
                                moves.append((di,dj))
                            elif board[di][dj].color != self.color:
                                moves.append((di,dj))
                                break
            #MEDIO
            if board[di][j] == 0:
                moves.append((di,j))
            elif board[di][j].color != self.color:
                moves.append((di,j))
        
        #ARRIBA
        if i-1 > -1:
            for di in range(i-1, -1, -1):
            #DERECHA
                if j+1 < 8:
                    for dj in range(j+1, 8):
                        if dj < 8:
                            if board[di][dj] == 0:
                                moves.append((di,dj))
                            elif board[di][dj].color != self.color:
                                moves.append((di,dj))
                                break
            #IZQUIERDA
                if j-1 > -1:
                    for dj in range(j-1, -1, -1):
                        if dj > -1:
                            if board[di][dj] == 0:
                                moves.append((di,dj))
                            elif board[di][dj].color != self.color:
                                moves.append((di,dj))
                                break
            #MEDIO
            if board[di][j] == 0:
                moves.append((di,j))
            elif board[di][j].color != self.color:
                    moves.append((di,j))
 
        return moves


class Torre(Piece):
    img = 5

    def valid_moves(self, board):
        i = self.row
        j = self.col

        moves = []

        #ARRIBA 
        if i-1 > -1:
            for di in range(i-1, -1, -1):
                if board[di][j] == 0:
                    moves.append((di, j))
                elif board[di][j].color != self.color:
                    moves.append((di, j))
                    break
            
        #ABAJO
        if i+1 < 8:
            for di in range(i+1, 8):
                if board[di][j] == 0:
                    moves.append((di, j))
                elif board[di][j].color != self.color:
                    moves.append((di, j)) 
                    break       

        #IZQUIERDA
        if j-1 > -1:
            for dj in range(j-1, -1, -1):
                if board[i][dj] == 0:
                    moves.append((i, dj))
                elif board[i][dj].color != self.color:
                    moves.append((i, dj))     
                break
               
        #DERECHA
        if j+1 < 8:
            for dj in range(j+1, 8):
                if board[i][dj] == 0:
                    moves.append((i, dj))
                elif board[i][dj].color != self.color:
                    moves.append((i, dj)) 
                break

        return moves                      
        