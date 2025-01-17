#
# The GUI engine for Python Chess
#
# Author: Boo Sung Kim, Eddie Sharick
# Note: The pygame tutorial by Eddie Sharick was used for the GUI engine. The GUI code was altered by Boo Sung Kim to
# fit in with the rest of the project.
#
import speech_recognition as sr
from cgitb import text
from trace import Trace
import chess_engine
import pygame as py

import ai_engine
from enums import Player

"""Variables"""
WIDTH = HEIGHT = 512  # width and height of the chess board
DIMENSION = 8  # the dimensions of the chess board
LEFT_PADDING = 1
TOP_PADDING = 1
SQ_SIZE = HEIGHT // DIMENSION  # the size of each of the squares in the board
MAX_FPS = 15  # FPS for animations
IMAGES = {}  # images for the chess pieces
colors = [py.Color("white"), py.Color("gray")]

# TODO: AI black has been worked on. Mirror progress for other two modes
def load_images():
    '''
    Load images for the chess pieces
    '''
    for p in Player.PIECES:
        IMAGES[p] = py.transform.scale(py.image.load("images/" + p + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_game_state(screen, game_state, valid_moves, square_selected, isVoice):
    ''' Draw the complete chess board with pieces

    Keyword arguments:
        :param screen       -- the pygame screen
        :param game_state   -- the state of the current chess game
    '''
    screen.fill(py.Color("black"))
    draw_squares(screen)
    draw_columns_rows_number(screen)
    draw_turn(screen, game_state.whose_turn())
    highlight_square(screen, game_state, valid_moves, square_selected)
    draw_pieces(screen, game_state)
    draw_voice(screen, isVoice)


def draw_squares(screen):
    ''' Draw the chess board with the alternating two colors

    :param screen:          -- the pygame screen
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            py.draw.rect(screen, color, py.Rect((c + LEFT_PADDING) * SQ_SIZE, (r + TOP_PADDING) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_columns_rows_number(screen):
    ''' Draw the chess board aux rows and columns numbers

    :param screen:          -- the pygame screen
    '''

    for r in range(DIMENSION):
        text = str(r + 1)
        font = py.font.SysFont(py.font.get_default_font(), 50)
        text = font.render(text, True, (255,255,255))
        screen.blit(text, (SQ_SIZE/3, ((r + TOP_PADDING) * SQ_SIZE) + SQ_SIZE / 3))

    for c in range(DIMENSION):
        text = str(c + 1)
        font = py.font.SysFont(py.font.get_default_font(), 50)
        text = font.render(text, True, (255,255,255))
        screen.blit(text, (((c + LEFT_PADDING) * SQ_SIZE) + SQ_SIZE/3, SQ_SIZE/4))

def draw_turn(screen, isWhiteTurn):
    ''' Draw the chess board aux turn text

    :param screen:          -- the pygame screen
    '''
    text = "Vez: "+ ("Branco" if isWhiteTurn else "Preto")
    font = py.font.SysFont(py.font.get_default_font(), 50)
    text = font.render(text, True, (255,255,255))
    screen.blit(text, (SQ_SIZE, ((DIMENSION + 1) * SQ_SIZE) + SQ_SIZE / 3))

def draw_voice(screen, isVoice):
    if isVoice:
        text = "Experimente falar a linha e coluna"
        text2 = "da sua peça, por exemplo: linha 1 coluna 1"
        font = py.font.SysFont(py.font.get_default_font(), 16)
        text = font.render(text, True, (255,255,255))
        text2 = font.render(text2, True, (255,255,255))
        screen.blit(text, (SQ_SIZE * 5, ((DIMENSION + 1) * SQ_SIZE) + SQ_SIZE / 4))
        screen.blit(text2, (SQ_SIZE * 5, ((DIMENSION + 1) * SQ_SIZE) + SQ_SIZE / 2))

def draw_pieces(screen, game_state):
    ''' Draw the chess pieces onto the board

    :param screen:          -- the pygame screen
    :param game_state:      -- the current state of the chess game
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = game_state.get_piece(r, c)
            if piece is not None and piece != Player.EMPTY:
                screen.blit(IMAGES[piece.get_player() + "_" + piece.get_name()],
                            py.Rect((c + LEFT_PADDING) * SQ_SIZE, (r + TOP_PADDING) * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def highlight_square(screen, game_state, valid_moves, square_selected):
    if square_selected != () and game_state.is_valid_piece(square_selected[0], square_selected[1]):
        row = square_selected[0]
        col = square_selected[1]

        if (game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_1)) or \
                (not game_state.whose_turn() and game_state.get_piece(row, col).is_player(Player.PLAYER_2)):
            # hightlight selected square
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(py.Color("blue"))
            screen.blit(s, ((col+LEFT_PADDING) * SQ_SIZE, (row + TOP_PADDING) * SQ_SIZE))

            # highlight move squares
            s.fill(py.Color("green"))

            for move in valid_moves:
                screen.blit(s, ((move[1] + LEFT_PADDING) * SQ_SIZE, (move[0] + TOP_PADDING) * SQ_SIZE))


def handlePlayerInput(row, col, square_selected, player_clicks, valid_moves, game_state):
     # If clicked on the same square, deselect it
    if square_selected == (row, col):
        square_selected = ()
        player_clicks = []
    else:
        square_selected = (row, col)
        player_clicks.append(square_selected)
    if len(player_clicks) == 2:
        # If second click not a valid move
        if (player_clicks[1][0], player_clicks[1][1]) not in valid_moves:
            square_selected = (row, col)
            player_clicks = []
            player_clicks.append(square_selected)

            valid_moves = game_state.get_valid_moves((row, col))
            if valid_moves is None:
                valid_moves = []
        else: # Moves the piece
            game_state.move_piece((player_clicks[0][0], player_clicks[0][1]),
                                    (player_clicks[1][0], player_clicks[1][1]), False)
            square_selected = ()
            player_clicks = []
            valid_moves = []
    else:
        valid_moves = game_state.get_valid_moves((row, col))
        if valid_moves is None:
            valid_moves = []

    return (square_selected, player_clicks, valid_moves)

def getRowColumnFromSpeak(speakText: str):
    try:
        if not(" " in speakText) or not("linha" in speakText) or not("coluna" in speakText):
            return (-1, -1)
        
        speakText = speakText.replace("colunas", "coluna").replace("linhas", "linha").replace("oi", "8")
        textParts = speakText.split(" ")
        if len(textParts) != 4:
            return (-1, -1)

        row = 0
        col = 0

        for i in range(len(textParts)):
            if textParts[i] == "linha":
                row = int(textParts[i + 1])
            if textParts[i] == "coluna":
                col = int(textParts[i + 1])

        return (row, col)
    except:
        return (-1, -1)
    

def main():
    py.init()
    screen = py.display.set_mode((WIDTH + (SQ_SIZE * LEFT_PADDING)+ SQ_SIZE, HEIGHT + (SQ_SIZE * TOP_PADDING) + SQ_SIZE))
    clock = py.time.Clock()
    game_state = chess_engine.game_state()
    load_images()
    running = True
    square_selected = ()  # keeps track of the last selected square
    player_clicks = []  # keeps track of player clicks (two tuples)
    valid_moves = []
    game_over = False

    game_state = chess_engine.game_state()

    print("Selecione o tipo de entrada (apenas numero):")
    print("1 - Mouse")
    print("2 - Comandos de voz")

    x = int(input())

    usingSpeak = x == 2

    draw_game_state(screen, game_state, valid_moves, square_selected, usingSpeak)
    clock.tick(MAX_FPS)
    py.display.flip()

    while running:
        if usingSpeak:
            r = sr.Recognizer()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Ouvindo...")
                py.event.get()
                audio = r.listen(source)

            res = r.recognize_google(audio, language="pt-BR")
            print("Ouvi: ", res)

            row, col = getRowColumnFromSpeak(res.lower())

            print("row", row, "col", col)

            if row != -1 and col != -1:
                square_selected, player_clicks, valid_moves = handlePlayerInput(row - 1, col - 1, square_selected, player_clicks, valid_moves, game_state)
        else:
            for e in py.event.get():
                if e.type == py.QUIT:
                    running = False
                elif e.type == py.MOUSEBUTTONDOWN: #Mouse events
                    if not game_over:
                        location = py.mouse.get_pos()
                        col = (location[0] // SQ_SIZE) - LEFT_PADDING
                        row = (location[1] // SQ_SIZE) - TOP_PADDING

                        square_selected, player_clicks, valid_moves = handlePlayerInput(row, col, square_selected, player_clicks, valid_moves, game_state)
                    
                elif e.type == py.KEYDOWN:
                    if e.key == py.K_r:
                        game_over = False
                        game_state = chess_engine.game_state()
                        valid_moves = []
                        square_selected = ()
                        player_clicks = []
                        valid_moves = []
                    elif e.key == py.K_u:
                        game_state.undo_move()
                        print(len(game_state.move_log))

        draw_game_state(screen, game_state, valid_moves, square_selected, usingSpeak)

        endgame = game_state.checkmate_stalemate_checker()
        if endgame == 0:
            game_over = True
            draw_text(screen, "Black wins.")
        elif endgame == 1:
            game_over = True
            draw_text(screen, "White wins.")
        elif endgame == 2:
            game_over = True
            draw_text(screen, "Stalemate.")

        clock.tick(MAX_FPS)
        py.display.flip()

def draw_text(screen, text):
    font = py.font.SysFont("Helvitca", 32, True, False)
    text_object = font.render(text, False, py.Color("Black"))
    text_location = py.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - text_object.get_width() / 2,
                                                      HEIGHT / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)


if __name__ == "__main__":
    main()
