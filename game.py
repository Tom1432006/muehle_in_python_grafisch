import field, copy, pygame

EMPTY_FIELD = 0
class Game:
    # List of all the fields
    board = []

    def __init__(self):

        # create all the fields
        for i in range(24):
            self.board.append(field.Field(i))

        # create all the connections
        connections = self.load_connections()

        for i, f in enumerate(self.board):
            f.connections = connections[i]
        
    def turn_p0(self, move, player):
        """
        Turn function for phase 0
        """
        if move < 0 or move > 23 or self.board[move].hold_piece != EMPTY_FIELD: return False
        self.board[move].change_hold_piece(player.player_index)
        player.place_piece()
        return True
    
    def turn_p1(self, move, player):
        """
        Turn function for phase 1
        """
        try:
            move_from, move_to = int(move[0]), int(move[1])
        except: return False

        # move from has to hold a piece of the player and move to has to be empty
        if 0 > move_from > 23 or self.board[move_from].hold_piece != player.player_index or self.board[move_to].hold_piece != EMPTY_FIELD: return False
        # move to has to connect to move from
        if player.pieces_left_on_board > 3 and move_to not in self.board[move_from].connections: return False

        # if all checks pass, perform the move
        self.board[move_from].change_hold_piece(EMPTY_FIELD)
        self.board[move_to].change_hold_piece(player.player_index)
        return True

    
    def take_piece(self, index, player, opponent, debug=False):
        if self.board[index].hold_piece == EMPTY_FIELD or self.board[index].hold_piece == player.player_index: return False

        if self.opponent_has_piece_to_remove(opponent):
            # check if the number of muehle has changed
            board_copy = copy.deepcopy(self.board)
            muehle_before = self.count_muehle(board_copy)
            board_copy[index].change_hold_piece(EMPTY_FIELD)
            muehle_after = self.count_muehle(board_copy)

            if muehle_before != muehle_after:
                return False
            
        # if all checks pass, perform the action
        if debug: return True
        opponent.take_piece()
        self.board[index].change_hold_piece(EMPTY_FIELD)
        return True

    def check_muehle(self, index):
        """ 
        check if the number of mühles has changed with the placement of the new piece
        """
        board_copy = copy.deepcopy(self.board)
        muehle_after = self.count_muehle(board_copy)
        board_copy[index].change_hold_piece(EMPTY_FIELD)
        muehle_before = self.count_muehle(board_copy)

        return muehle_after != muehle_before
    
    @staticmethod
    def count_muehle(board):
        """
        This function counts the number of mühle, so you can check if, when the player can take a piece,
        he doesn't take any of the locked pieces.
        How I calculate if the player has a mühle:
        I go through every 3 connected fields (starting at the field, that the player as put a piece on, to only count new mühles),
        where the player has a piece on it.
        To filter out non valid rows of three (over the corner), I count the total number of connections (for the middle pieces I always count 3)
        and if the number of connections are 7 or 9, then the player has a valid mühle.
        """
        num_muehle = 0

        for x in range(len(board)):
            current_piece = board[x].hold_piece
            if current_piece == EMPTY_FIELD: continue
            total_connections = min(len(board[x].connections), 3) # only count the middel fields with 4 connections as 3, to make the calulation easier

            for y in board[x].connections:
                if board[y].hold_piece != current_piece or y < x: continue

                total_connections += min(len(board[y].connections), 3)

                for z in board[y].connections:
                    if board[z].hold_piece != current_piece or z == x or z < y: continue

                    total_connections += min(len(board[z].connections), 3)
                    if total_connections == 7 or total_connections == 9:
                        num_muehle += 1
                    
                    total_connections -= min(len(board[z].connections), 3)

                total_connections -= min(len(board[y].connections), 3)
        
        return num_muehle
    
    def opponent_has_piece_to_remove(self, player):
        """
        check if the opponent has any non locked pieces. To do that, I go through every piece of the opponent, remove it
        and check if the number of mühles have changed. If for every piece the number of mühles has changed, then every piece is locked
        and the player can also take locked pieces.
        """
        board_copy = copy.deepcopy(self.board)
        for x in board_copy:
            if x.hold_piece != player.player_index: continue

            before = self.count_muehle(board_copy)
            x.hold_piece = EMPTY_FIELD
            after = self.count_muehle(board_copy)
            
            if before == after:
                # the number of mühle hasn't changed and the opponent has a piece to remove
                return True

            # reset for the next piece
            x.hold_piece = player.player_index

        # player has no piece to remove
        return False

    def load_connections(self):
        """
        Load the board connections from the connections file
        """
        connections = []

        with open("connections.mgd", "r") as f:
            for x in f:
                connections.append([int(n) for n in x.replace("\n", "").split(" ")])

        return connections
    
    def get_board(self):
        board_copy = []

        for i in range(0, len(self.board)):
            board_copy.append(self.board[i].hold_piece)
        
        return board_copy
    
    def get_removable_pieces(self, player, opponent):
        board_copy = []

        for i in range(0, len(self.board)):
            if self.board[i].hold_piece == opponent.player_index and self.take_piece(i, player, opponent, True):
                board_copy.append(1)
            else:
                board_copy.append(0)
        
        return board_copy
    
    def get_pieces_with_index(self, player_index):
        board_copy = []

        for i in range(0, len(self.board)):
            if self.board[i].hold_piece == player_index:
                board_copy.append(1)
            else:
                board_copy.append(0)
        
        return board_copy