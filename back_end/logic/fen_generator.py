def piece_labels_to_board(piece_labels):
    fen_map = {
        'wP': 'P', 'wR': 'R', 'wN': 'N', 'wB': 'B', 'wQ': 'Q', 'wK': 'K',
        'bP': 'p', 'bR': 'r', 'bN': 'n', 'bB': 'b', 'bQ': 'q', 'bK': 'k',
    }
    board = []
    for rank in range(8):
        row = []
        for file in range(8):
            label = piece_labels[rank * 8 + file]
            if label in fen_map:
                row.append(fen_map[label])
            else:
                row.append('.')
        board.append(row)
    return board

def board_to_fen(board, active_color='w', castling='KQkq', en_passant='-', halfmove=0, fullmove=1):
    fen_rows = []
    for row in board:
        fen_row = ''
        empty_count = 0
        for cell in row:
            if cell == '.' or cell == '' or cell is None:
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)
    fen_position = '/'.join(fen_rows)
    fen = f"{fen_position} {active_color} {castling} {en_passant} {halfmove} {fullmove}"
    return fen

def generate_fen(board):
    piece_labels_flat = [cell for row in board for cell in row]
    fen_board = piece_labels_to_board(piece_labels_flat)
    fen_board.reverse()
    return board_to_fen(fen_board, active_color='w', castling='-', en_passant='-')
