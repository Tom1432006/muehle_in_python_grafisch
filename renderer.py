import pygame

WHITE = (255, 255, 255)
WHITE_L = (155, 155, 155)
BLACK = (0,0,0)
BLACK_L = (100,100,100)

def render_board(screen, col):
    o = 70 # offset DONT CHANGE
    top_corner = (130, 30)
    outer_width = 440
    lw = 10 # linewidth

    #outer square
    rect1 = pygame.Rect(top_corner[0], top_corner[1], outer_width, outer_width)
    pygame.draw.rect(screen, col, rect1, lw)

    # middle square
    rect2 = pygame.Rect(top_corner[0] + o, top_corner[1] + o, outer_width - 2*o, outer_width - 2*o)
    pygame.draw.rect(screen, col, rect2, lw)

    # inner square
    rect3 = pygame.Rect(top_corner[0] + 2*o, top_corner[1] + 2*o, outer_width - 4*o, outer_width - 4*o)
    pygame.draw.rect(screen, col, rect3, lw)

    # draw the lines
    pygame.draw.line(screen, col, (130, 250), (130+2*o, 250), lw)
    pygame.draw.line(screen, col, (350, 30), (350, 30+2*o), lw)
    pygame.draw.line(screen, col, (565, 250), (570-2*o, 250), lw)
    pygame.draw.line(screen, col, (350, 465), (350, 470-2*o), lw)

def render_pieces(screen, board, players, field_positions, preview_index, turn, highlighted_pieces, highlightedcolor):
    if preview_index != 404:
        if turn == 0:
            pygame.draw.circle(screen, WHITE_L, (field_positions[preview_index][0], field_positions[preview_index][1]), 20)
        elif turn == 1:
            pygame.draw.circle(screen, BLACK_L, (field_positions[preview_index][0], field_positions[preview_index][1]), 20)

    for i in range(0, len(board)):
        if highlighted_pieces[i] == 1:
            pygame.draw.circle(screen, highlightedcolor, (field_positions[i][0], field_positions[i][1]), 25)

        if board[i] == 1:
            pygame.draw.circle(screen, WHITE, (field_positions[i][0], field_positions[i][1]), 20)
        elif board[i] == 2:
            pygame.draw.circle(screen, BLACK, (field_positions[i][0], field_positions[i][1]), 20)
    
    for x in range(players[0].pieces_in_hand):
        pygame.draw.circle(screen, WHITE, (50, 450-25*x), 20)
    for y in range(players[1].pieces_in_hand):
        pygame.draw.circle(screen, BLACK, (650, 450-25*y), 20)