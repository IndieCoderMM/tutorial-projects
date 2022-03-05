import pygame
import sys
import random
from pygame.locals import *

board_width = 4
board_height = 4
tile_size = 80
win_width = 640
win_height = 480
fps = 30
blank = None

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 50, 255)
dark_turquoise = (3, 54, 73)
green = (0, 204, 0)

bg_color = dark_turquoise
tile_color = green
text_color = white
border_color = blue
font_size = 20

button_color = white
buttontxt_color = black
msg_color = white

x_margin = int((win_width - (tile_size * board_width + (board_width - 1))) / 2)
y_margin = int((win_height - (tile_size * board_height + (board_height - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global fps_clk, display_surf, basic_font, reset_surf, reset_rect, new_surf, new_rect, solve_surf, solve_rect

    pygame.init()
    fps_clk = pygame.time.Clock()
    display_surf = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Slide Puzzle")
    basic_font = pygame.font.Font('freesansbold.ttf', font_size)

    # Option button
    reset_surf, reset_rect = makeText('Reset', text_color, tile_color, win_width - 120, win_height - 90)
    new_surf, new_rect = makeText('New Game', text_color, tile_color, win_width - 120, win_height - 60)
    solve_surf, solve_rect = makeText('Solve', text_color, tile_color, win_width - 120, win_height - 30)

    main_board, solution_seq = generateNewPuzzle(80)
    solved_board = getStartingBoard()

    all_moves = []

    while True:
        slide_to = None
        msg = ''
        if main_board == solved_board:
            msg = 'Solved!'

        drawBoard(main_board, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(main_board, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if reset_rect.collidepoint(event.pos):
                        resetAnimation(main_board, all_moves)
                        all_moves = []
                    elif new_rect.collidepoint(event.pos):
                        main_board, solution_seq = generateNewPuzzle(80)
                        all_moves = []
                    elif solve_rect.collidepoint(event.pos):
                        resetAnimation(main_board, solution_seq + all_moves)
                        all_moves = []
                else:
                    blankx, blanky = getBlankPosition(main_board)
                    if spotx == blankx + 1 and spoty == blanky:
                        slide_to = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slide_to = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slide_to = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slide_to = DOWN

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(main_board, LEFT):
                    slide_to = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(main_board, RIGHT):
                    slide_to = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(main_board, UP):
                    slide_to = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(main_board, DOWN):
                    slide_to = DOWN
        # *****
        if slide_to:
            slideAnimation(main_board, slide_to, 'Click tile or press arrow keys to slide.', 8)
            makeMove(main_board, slide_to)
            all_moves.append(slide_to)
        pygame.display.update()
        fps_clk.tick(fps)


def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def getStartingBoard():
    counter = 1
    board = []
    for x in range(board_width):
        column = []
        for y in range(board_height):
            column.append(counter)
            counter += board_width
        board.append(column)
        counter -= board_width * (board_height - 1) + board_width - 1
    board[board_width-1][board_height-1] = None
    return board

def getBlankPosition(board):
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] is None:
                return x, y

def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or (move == DOWN and blanky != 0) or (move == LEFT and blankx != len(board) - 1) or (move == RIGHT and blankx != 0)

def getRandomMove(board, last_move=None):
    valid_moves = [UP, DOWN, LEFT, RIGHT]

    if last_move == UP or not isValidMove(board, DOWN):
        valid_moves.remove(DOWN)
    if last_move == DOWN or not isValidMove(board, UP):
        valid_moves.remove(UP)
    if last_move == LEFT or not isValidMove(board, RIGHT):
        valid_moves.remove(RIGHT)
    if last_move == RIGHT or not isValidMove(board, LEFT):
        valid_moves.remove(LEFT)

    return random.choice(valid_moves)

# Convert Tile coordinates to Pixel coordinates
def getLeftTopOfTile(tileX, tileY):
    left = x_margin + (tileX * tile_size) + (tileX - 1)
    top = y_margin + (tileY * tile_size) + (tileY - 1)
    return left, top

# Convert Pixel coordinates to Tile coordinates
def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tile_rect = pygame.Rect(left, top, tile_size, tile_size)
            if tile_rect.collidepoint(x, y):
                return tileX, tileY
    return None, None

def drawTile(tilex, tiley, num, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(display_surf, tile_color, (left + adjx, top + adjy, tile_size, tile_size))
    text_surf = basic_font.render(str(num), True, text_color)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(tile_size / 2) + adjx, top + int(tile_size / 2) + adjy
    display_surf.blit(text_surf, text_rect)

def makeText(text, color, bgcolor, top, left):
    text_surf = basic_font.render(text, True, color, bgcolor)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect

def drawBoard(board, message):
    display_surf.fill(bg_color)
    if message:
        text_surf, text_rect = makeText(message, msg_color, bg_color, 5, 5)
        display_surf.blit(text_surf, text_rect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])
    left, top = getLeftTopOfTile(0, 0)
    width = board_width * tile_size
    height = board_height * tile_size
    pygame.draw.rect(display_surf, border_color, (left - 5, top - 5, width + 11, height + 11), 4)

    display_surf.blit(reset_surf, reset_rect)
    display_surf.blit(new_surf, new_rect)
    display_surf.blit(solve_surf, solve_rect)

def slideAnimation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message)
    base_surf = display_surf.copy()
    move_left, move_top = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(base_surf, bg_color, (move_left, move_top, tile_size, tile_size))

    for i in range(0, tile_size, animationSpeed):
        checkForQuit()
        display_surf.blit(base_surf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        elif direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        elif direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        elif direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        fps_clk.tick(fps)

def generateNewPuzzle(num_slides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    last_move = None
    for i in range(num_slides):
        move = getRandomMove(board, last_move)
        slideAnimation(board, move, 'Generating new puzzle...', int(tile_size / 3))
        makeMove(board, move)
        sequence.append(move)
        last_move = move
    return board, sequence

def resetAnimation(board, all_moves):
    rev_all_moves = all_moves[:]
    rev_all_moves.reverse()

    for move in rev_all_moves:
        if move == UP:
            opposite_move = DOWN
        elif move == DOWN:
            opposite_move = UP
        elif move == RIGHT:
            opposite_move = LEFT
        elif move == LEFT:
            opposite_move = RIGHT
        slideAnimation(board, opposite_move, '', int(tile_size / 2))
        makeMove(board, opposite_move)


if __name__ == '__main__':
    main()










