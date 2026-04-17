import pygame
import sys
import math

# =========================================================
# 1. INITIALIZATION & CONSTANTS
# =========================================================
pygame.init()

WIDTH, HEIGHT = 300, 400  # Increased height to fit text at bottom
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = 100 # Consistent 100px squares
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
# Nordic Night
BG_COLOR = (46, 52, 64)      # Deep slate blue
LINE_COLOR = (59, 66, 82)    # Muted dark blue
CIRCLE_COLOR = (143, 188, 187) # Frosted mint
CROSS_COLOR = (216, 222, 233)  # Snow white
TEXT_COLOR = (236, 239, 244)   # Bright white

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')
screen.fill(BG_COLOR)

# Fonts
FONT = pygame.font.SysFont('arial', 30, bold=True)

# =========================================================
# 2. LOGIC FUNCTIONS
# =========================================================
board = [[' ' for _ in range(3)] for _ in range(3)]

def draw_lines():
    screen.fill(BG_COLOR)
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, 300), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, 300), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

def show_result(message):
    # Draw a rectangle at the bottom
    pygame.draw.rect(screen, LINE_COLOR, (0, 300, WIDTH, 100))
    text = FONT.render(message, True, TEXT_COLOR)
    restart_text = pygame.font.SysFont('arial', 15).render("Press 'R' to Restart", True, TEXT_COLOR)
    
    # Center text
    text_rect = text.get_rect(center=(WIDTH // 2, 335))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, 375))
    
    screen.blit(text, text_rect)
    screen.blit(restart_text, restart_rect)

def is_winner(b, p):
    for i in range(3):
        if all([b[i][j] == p for j in range(3)]): return True
        if all([b[j][i] == p for j in range(3)]): return True
    if b[0][0] == b[1][1] == b[2][2] == p: return True
    if b[0][2] == b[1][1] == b[2][0] == p: return True
    return False

def is_full(b):
    return all(cell != ' ' for row in b for cell in row)

# =========================================================
# 3. ALPHA-BETA MINIMAX
# =========================================================
def minimax(current_board, depth, alpha, beta, is_maximizing):
    if is_winner(current_board, 'O'): return 10 - depth
    if is_winner(current_board, 'X'): return depth - 10
    if is_full(current_board): return 0

    if is_maximizing:
        max_eval = -math.inf
        for r in range(3):
            for c in range(3):
                if current_board[r][c] == ' ':
                    current_board[r][c] = 'O'
                    eval = minimax(current_board, depth + 1, alpha, beta, False)
                    current_board[r][c] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha: break
        return max_eval
    else:
        min_eval = math.inf
        for r in range(3):
            for c in range(3):
                if current_board[r][c] == ' ':
                    current_board[r][c] = 'X'
                    eval = minimax(current_board, depth + 1, alpha, beta, True)
                    current_board[r][c] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha: break
        return min_eval

# =========================================================
# 4. MAIN GAME LOOP
# =========================================================
def restart():
    global board, player, game_over
    board = [[' ' for _ in range(3)] for _ in range(3)]
    player = 'X'
    game_over = False
    draw_lines()

draw_lines()
player = 'X'
game_over = False
result_msg = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 'X':
            mouseX, mouseY = event.pos
            if mouseY < 300: # Only register clicks on the board
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if board[clicked_row][clicked_col] == ' ':
                    board[clicked_row][clicked_col] = 'X'
                    if is_winner(board, 'X'):
                        game_over = True
                        result_msg = "Human Wins!"
                    elif is_full(board):
                        game_over = True
                        result_msg = "It's a Draw!"
                    else:
                        player = 'O'
                    draw_figures()

    # AI Turn
    if player == 'O' and not game_over:
        best_score = -math.inf
        move = (-1, -1)
        for r in range(3):
            for c in range(3):
                if board[r][c] == ' ':
                    board[r][c] = 'O'
                    score = minimax(board, 0, -math.inf, math.inf, False)
                    board[r][c] = ' '
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        
        if move != (-1, -1):
            board[move[0]][move[1]] = 'O'
            if is_winner(board, 'O'):
                game_over = True
                result_msg = "You Lose!"
            elif is_full(board):
                game_over = True
                result_msg = "It's a Draw!"
            else:
                player = 'X'
            draw_figures()

    if game_over:
        show_result(result_msg)
    
    pygame.display.update()