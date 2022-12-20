import Client
import pygame
import sys

pygame.init()  
pygame.font.init()  


screen = pygame.display.set_mode((800, 60 * 8))
pygame.display.set_caption('Escacs')

from modules.board import *
from modules.computer import *


bg = pygame.image.load("assets/chessboard.png").convert()
sidebg = pygame.image.load("assets/woodsidemenu.jpg").convert()
player = 1
myfont = pygame.font.Font("assets/Roboto-Black.ttf", 30)


board = Board()


all_sprites_list = pygame.sprite.Group()
sprites = [piece for row in board.array for piece in row if piece]
all_sprites_list.add(sprites)


all_sprites_list.draw(screen)

clock = pygame.time.Clock()
def main():

    Client.connectar_servidor
    welcome()
    Color = Client.rebre_msg(Client.client)
    if (Color == 'Blanques'):
        juguen_blanques()
        game_over()

    elif (Color == 'Negres'):
        juguen_negres()
        game_over()





def select_piece(color):

    pos = pygame.mouse.get_pos()
    #llista de sprites en el cursor
    clicked_sprites = [s for s in sprites if s.rect.collidepoint(pos)]

    #només agafa la peça si és del color de l'usuari
    if len(clicked_sprites) == 1 and clicked_sprites[0].color == color:
        clicked_sprites[0].highlight()
        return clicked_sprites[0]


def select_square():
    #retorna coordenades
    x, y = pygame.mouse.get_pos()
    x = x // 60
    y = y // 60
    return (y, x)


def juguen_blanques():
    
    # Funció que cridarà el client que jugui amb blanques
    update_sidemenu('És el teu torn', (255, 255, 255))

    gameover = False

    seleccionat = False  # seleccionat 
    checkWhite = False #hi ha escac (fa un moviment no valid)

    while not gameover:

        #Torn del client
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Selecciona peça per moure
                elif event.type == pygame.MOUSEBUTTONDOWN and not seleccionat:
                    piece = select_piece("w")

                    # Es selecciona peça blanca i generem els moviments legals
                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        seleccionat = True

                # Ja tenim una peça seleccionada, ara mirem següent acció: on la mou
                elif event.type == pygame.MOUSEBUTTONDOWN and seleccionat:
                    square = select_square()
                    special_moves = special_move_gen(board, "w")

                    # Si la jugada és possible
                    if square in player_moves:
                        #Guardem la posició antiga per si hi ha alguna acció especial
                        #També ens interessa per poder enviar el missatge al servidor
                        oldx = piece.x 
                        oldy = piece.y
                        dest = board.array[square[0]][square[1]]

                        # provem de moure la peça i mirem si tenim promoció de peó
                        pawn_promotion = board.move_piece(
                            piece, square[0], square[1])
                        #si peó arriba a l'última fila el canviem per una reina
                        if pawn_promotion:  # remove the pawn sprite, add the queen sprite
                            all_sprites_list.add(pawn_promotion[0])
                            sprites.append(pawn_promotion[0])
                            all_sprites_list.remove(pawn_promotion[1])
                            sprites.remove(pawn_promotion[1])

                        # Canviem atribut de rei i torre si els movem per saber que ja no podem fer enroc
                        if type(piece) == King or type(piece) == Rook:
                            piece.moved = True
                        # Si la posició destí està ocupada eliminem la peça que hi ha
                        if dest:
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)

                        #Comprovem que el moviment no sigui il·legal deixant rei desprotegit
                        attacked = move_gen(board, "b", True)
                        if (board.white_king.y, board.white_king.x) not in attacked:
                            #no hi ha check, tot ok, treiem variable seleccionat perquè es fa el moviment
                            #passem el torn a l'altre jugador
                            seleccionat = False
                            player = 2
                            update_sidemenu('Li toca al rival', (255, 255, 255))

                            # Canviem el tauler
                            if dest:
                                board.score -= board.pvalue_dict[type(dest)]

                        else:
                            #el moviment deixa rei desprotegit, per tant no és possible i l'hem de revertir
                            board.move_piece(piece, oldy, oldx)
                            if type(piece) == King or type(piece) == Rook:
                                piece.moved = False
                            board.array[square[0]][square[1]] = dest
                            if dest:
                                all_sprites_list.add(dest)
                                sprites.append(dest)
                            if pawn_promotion:
                                all_sprites_list.add(pawn_promotion[1])
                                sprites.append(pawn_promotion[1])
                            piece.highlight()

                    #Cancel·lem moviment si apreten el mateix lloc
                    elif (piece.y, piece.x) == square:
                        piece.unhighlight()
                        seleccionat = False

                    #Selecciona un quadrat que podria ser moviment especial (enroc o en peasant)
                    elif special_moves and square in special_moves:

                        special = special_moves[square]
                        #utilitzem els mètodes per saber si es pot fer l'enroc
                        if (special == "CR" or special == "CL") and type(piece) == King:
                            board.move_piece(
                                piece, square[0], square[1], special)
                            seleccionat = False
                            player = 2

                        #no es pot fer l'enroc
                        else:
                            update_sidemenu('', (255, 0, 0))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            if checkWhite:
                                update_sidemenu(
                                    'Estàs en escac', (255, 0, 0))
                            else:
                                update_sidemenu('Moviment no vàlid', (255, 255, 255))

                    # move is invalid
                    else:

                        update_sidemenu('Moviment no vàlid', (255, 0, 0))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        if checkWhite:
                            update_sidemenu('Estàs en escac', (255, 0, 0))

            move = (str(oldy), str(oldx) ,str(piece.y),str(piece.x))
            Client.enviar_msg(''.join(move))
        # Turn rival
        elif player == 2:
            moviment = Client.rebre_msg(Client.client)

            #El rival torna un 0 quan has fet mat
            if moviment == '0':
                gameover = True
                player = 1
                update_sidemenu('Has guanyat', (255, 255, 0))

            #apliquem el moviment del rival
            else:
                move[3] = tuple(moviment)
                start = [move[0], move[1]]
                end = [move[2], move[3]]
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]

                #apliquem mateixos mètodes que abans pel cas de promoció peons
                pawn_promotion = board.move_piece(piece, end[0], end[1])
                if pawn_promotion:
                    all_sprites_list.add(pawn_promotion[0])
                    sprites.append(pawn_promotion[0])
                    all_sprites_list.remove(pawn_promotion[1])
                    sprites.remove(pawn_promotion[1])

                if dest:
                    all_sprites_list.remove(dest)
                    sprites.remove(dest)
                    board.score += board.pvalue_dict[type(dest)]

                player = 1
                #mirem que el jugador no estigui en escac ara
                attacked = move_gen(board, "b", True)
                if (board.white_king.y, board.white_king.x) in attacked:
                    update_sidemenu('Your Turn: Check!', (255, 0, 0))
                    checkWhite = True
                else:
                    update_sidemenu('Your Turn!', (255, 255, 255))
                    checkWhite = False

            if value == float("inf"):
                print("Player checkmate")
                gameover = True
                player = 2
                update_sidemenu(
                    'Checkmate!\nCPU Wins!\nPress any key to quit.', (255, 255, 0))

        # Actualitzem pantalla després del moviment
        screen.blit(bg, (0, 0))
        all_sprites_list.draw(screen)
        pygame.display.update()
        clock.tick(60)

def juguen_negres():
    update_sidemenu('Comença el rival', (255, 255, 255))

    gameover = False

    seleccionat = False
    checkBlack = False

    while not gameover:

        if player == 2:
            moviment = Client.rebre_msg(Client.client)
            #El rival torna un 0 quan has fet mat
            if moviment == '0':
                gameover = True
                player = 1
                update_sidemenu('Has guanyat', (255, 255, 0))

            #apliquem el moviment del rival
            else:
                move[3] = tuple(moviment)
                start = [move[0], move[1]]
                end = [move[2], move[3]]
                piece = board.array[start[0]][start[1]]
                dest = board.array[end[0]][end[1]]

                #apliquem mateixos mètodes que abans pel cas de promoció peons
                pawn_promotion = board.move_piece(piece, end[0], end[1])
                if pawn_promotion:
                    all_sprites_list.add(pawn_promotion[0])
                    sprites.append(pawn_promotion[0])
                    all_sprites_list.remove(pawn_promotion[1])
                    sprites.remove(pawn_promotion[1])

                if dest:
                    all_sprites_list.remove(dest)
                    sprites.remove(dest)
                    board.score += board.pvalue_dict[type(dest)]

                player = 1
                #mirem que el jugador no estigui en escac ara
                attacked = move_gen(board, "b", True)
                if (board.white_king.y, board.white_king.x) in attacked:
                    update_sidemenu('Your Turn: Check!', (255, 0, 0))
                    checkWhite = True
                else:
                    update_sidemenu('Your Turn!', (255, 255, 255))
                    checkWhite = False

            if value == float("inf"):
                print("Player checkmate")
                gameover = True
                player = 2
                update_sidemenu(
                    'Checkmate!\nCPU Wins!\nPress any key to quit.', (255, 255, 0))

            # Actualitzem pantalla després del moviment
            screen.blit(bg, (0, 0))
            all_sprites_list.draw(screen)
            pygame.display.update()
            clock.tick(60)

        elif player == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


                elif event.type == pygame.MOUSEBUTTONDOWN and not seleccionat:
                    piece = select_piece("b")


                    if piece != None:
                        player_moves = piece.gen_legal_moves(board)
                        seleccionat = True

  
                elif event.type == pygame.MOUSEBUTTONDOWN and seleccionat:
                    square = select_square()
                    special_moves = special_move_gen(board, "b")


                    if square in player_moves:
                        oldx = piece.x  
                        oldy = piece.y
                        dest = board.array[square[0]][square[1]]
                        pawn_promotion = board.move_piece(
                            piece, square[0], square[1])

                        if pawn_promotion:
                            all_sprites_list.add(pawn_promotion[0])
                            sprites.append(pawn_promotion[0])
                            all_sprites_list.remove(pawn_promotion[1])
                            sprites.remove(pawn_promotion[1])

                        if type(piece) == King or type(piece) == Rook:
                            piece.moved = True
                        if dest:
                            all_sprites_list.remove(dest)
                            sprites.remove(dest)

                        attacked = move_gen(board, "w", True)
                        if (board.black_king.y, board.black_king.x) not in attacked:
                            seleccionat = False
                            player = 2
                            update_sidemenu('Li toca al rival', (255, 255, 255))

                            if dest:
                                board.score -= board.pvalue_dict[type(dest)]

                        else:
                            board.move_piece(piece, oldy, oldx)
                            if type(piece) == King or type(piece) == Rook:
                                piece.moved = False
                            board.array[square[0]][square[1]] = dest
                            if dest:
                                all_sprites_list.add(dest)
                                sprites.append(dest)
                            if pawn_promotion:
                                all_sprites_list.add(pawn_promotion[1])
                                sprites.append(pawn_promotion[1])
                            piece.highlight()

                            if checkBlack:
                                update_sidemenu(
                                    'Estàs en escac!', (255, 0, 0))
                                pygame.display.update()
                                pygame.time.wait(1000)
                            else:
                                update_sidemenu(
                                    'Moviment il·legal', (255, 0, 0))
                                pygame.display.update()
                    elif (piece.y, piece.x) == square:
                        piece.unhighlight()
                        seleccionat = False

                    elif special_moves and square in special_moves:
                        special = special_moves[square]
                        if (special == "CR" or special == "CL") and type(piece) == King:
                            board.move_piece(
                                piece, square[0], square[1], special)
                            seleccionat = False
                            player = 2
                        else:
                            update_sidemenu('Moviment il·legal', (255, 0, 0))
                            pygame.display.update()
                            pygame.time.wait(1000)
                            if checkBlack:
                                update_sidemenu(
                                    'Estàs en escac', (255, 0, 0))
                    else:

                        update_sidemenu('Moviment il·legal', (255, 0, 0))
                        pygame.display.update()
                        pygame.time.wait(1000)
                        if checkBlack:
                            update_sidemenu('Estàs en escac!', (255, 0, 0))
            move = (str(oldy), str(oldx) ,str(piece.y),str(piece.x))
            Client.enviar_msg(''.join(move))

def game_over():
    import os
    board.print_to_terminal()
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.event.clear()
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == pygame.QUIT:
                import sys
                sys.exit()


def update_sidemenu(message, colour):

    screen.blit(sidebg, (480, 0))  
    global playeravatar, player2avatar


    # separa el text en línies
    message = message.splitlines()
    c = 0
    for m in message:
        textsurface = myfont.render(m, False, colour)
        screen.blit(textsurface, (500, 250 + c))
        c += 40



def welcome():

    # wood background
    menubg = pygame.image.load("assets/menubg.jpg").convert()
    screen.blit(menubg, (0, 0))
    bigfont = pygame.font.Font("assets/Roboto-Black.ttf", 80)
    textsurface = bigfont.render('Escacs Sara i Arnau', False, (255, 255, 255))
    screen.blit(textsurface, (30, 10))

    medfont = pygame.font.Font("assets/Roboto-Black.ttf", 50)
    textsurface = medfont.render(
        'Projecte SAD', False, (255, 255, 255))
    screen.blit(textsurface, (100, 100))
    textsurface = myfont.render(
        'Clica per a començar!', False, (255, 255, 255))
    screen.blit(textsurface, (250, 170))




    #bucle infinit fins que jugador inicia
    pygame.display.update()
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                return
            elif event.type == pygame.QUIT:
                sys.exit()

