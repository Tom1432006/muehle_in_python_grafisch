class Player:
    pieces_in_hand = 9
    pieces_left_on_board = 0

    player_index = 0

    def __init__(self, index):
        self.player_index = index

    def take_piece(self):
        self.pieces_left_on_board -= 1
    
    def place_piece(self):
        self.pieces_in_hand -= 1
        self.pieces_left_on_board += 1
        