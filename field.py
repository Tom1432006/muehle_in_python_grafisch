class Field:
    field_index = 0

    player_symbols = []

    # List to store all the connections with other fields
    connections = []

    # stores the piece, that lays on the board
    hold_piece = 0

    def __init__(self, field_index):
        self.field_index = field_index

    def connect(self, field_to_connect):
        self.connections.append(field_to_connect)

    def change_hold_piece(self, new_piece):
        self.hold_piece = new_piece

    def hold_str(self):
        return str(self.hold_piece)
    