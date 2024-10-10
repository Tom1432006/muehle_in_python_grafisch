import game, random, player, pygame
from renderer import *

pygame.init()
pygame.font.init()

# pygame settings
screen_width = 700
screen_height = 500
fps = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Mühle")
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)

# Colors
BACKGROUND = (230, 163, 108)
LINES_COLOR = (58, 41, 33)
RED = (255,0,0)
GRAY = (125, 125, 125)
YELLOW = (255, 255, 0)

not_done = True
game_done = False
turn = 0
pieces_left = 9
players = []
player_won = 0
player_can_take_piece = False
construct_move = []

def load_field_positions():
    positions = []

    with open("field_positions.mgd", "r") as f:
        for x in f:
            positions.append([int(n) for n in x.replace("\n", "").split(" ")])

    return positions

FIELD_POSITIONS = load_field_positions()

""" Possible game states:
0 -> starting phase, players put down their pieces
1 -> second phase, players slider their pieces over the board
"""
game_state = 0
test = False # generate a random 0th phase, to test the second phase

def take_piece():
    game.print_board()
    isvalid = False
    while not isvalid:
        if test and game_state == 0: take = random.randint(0,23)
        else: take = input("Stein zum wegnehmen: ")
        isvalid = game.take_piece(int(take), players[turn], players[(turn+1)%2])

def initiate_players():
    player1 = player.Player(1)
    player2 = player.Player(2)

    players.append(player1)
    players.append(player2)

def translate_click(mpos):
    for i in range(0, len(FIELD_POSITIONS)):
        if FIELD_POSITIONS[i][0]-20 < mpos[0] < FIELD_POSITIONS[i][0]+20 and FIELD_POSITIONS[i][1]-20 < mpos[1] < FIELD_POSITIONS[i][1]+20:
            return i
    return 404 # no matching field

def move():
    global player_can_take_piece
    global turn
    global game_state
    global construct_move
    global players
    global game
    global player_won

    if test and game_state == 0:
        move = random.randint(0,23)
    else:
        move = translate_click(pygame.mouse.get_pos())
        if move == 404: return
    
    if player_can_take_piece:
        isvalid = game.take_piece(move, players[turn], players[(turn+1)%2])
        if not isvalid: return

        player_can_take_piece = False
        if game_state == 1 and players[(turn+1)%2].pieces_left_on_board == 2:
            player_won = players[turn].player_index
    else:
        construct_move.append(move)
        if game_state == 1 and len(construct_move) != 2:
            if game.board[move].hold_piece != players[turn].player_index:
                construct_move = []
            return
        
        if game_state == 0:
            valid_move = game.turn_p0(construct_move[0], players[turn])
            if not valid_move:
                construct_move = []
                return
            
            if game.check_muehle(construct_move[0]):
                player_can_take_piece = True
                return

            if players[1].pieces_in_hand == 0:
                game_state = 1
        elif game_state == 1:
            valid_move = game.turn_p1(construct_move, players[turn])
            if not valid_move:
                construct_move = []
                return

            if game.check_muehle(construct_move[1]):
                player_can_take_piece = True
                return
            
    construct_move = []
    turn = (turn+1) % 2 # alternate between 0 and 1

if __name__ == "__main__":
    initiate_players()
    game = game.Game()

    # game loop
    while not_done:
        screen.fill(BACKGROUND)

        highlighted_pieces = [0 for _ in range(24)]
        highlightcolor = BLACK
        if player_can_take_piece:
            highlighted_pieces = game.get_removable_pieces(players[turn], players[(turn+1)%2])
            highlightcolor = RED
        if game_state == 1 and len(construct_move) == 1:
            highlighted_pieces[construct_move[0]] = 1
            highlightcolor = GRAY
        if player_won != 0:
            highlighted_pieces = game.get_pieces_with_index(player_won)
            highlightcolor = YELLOW

        render_board(screen, LINES_COLOR)
        render_pieces(screen, game.get_board(), players, FIELD_POSITIONS, translate_click(pygame.mouse.get_pos()), turn, highlighted_pieces, highlightcolor)

        if test and game_state == 0: move()

        # event handeling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_done = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    not_done = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player_won == 0: move()

        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()