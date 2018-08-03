import ChessPieces


def create_board():
    chessboard = [[None for i in range(9)] for j in range(9)]

    for i in range(1, 9):
        chessboard[i][7] = ChessPieces.Pawn(-1, 7, i)
        chessboard[i][2] = ChessPieces.Pawn(1, 2, i)
        if abs(i - 4.5) > 3:
            chessboard[i][8] = ChessPieces.Rook(-1, 8, i)
            chessboard[i][1] = ChessPieces.Rook(1, 1, i)
        elif abs(i - 4.5) > 2:
            chessboard[i][8] = ChessPieces.Knight(-1, 8, i)
            chessboard[i][1] = ChessPieces.Knight(1, 1, i)
        elif abs(i - 4.5) > 1:
            chessboard[i][8] = ChessPieces.Bishop(-1, 8, i)
            chessboard[i][1] = ChessPieces.Bishop(1, 1, i)
        elif i == 5:
            chessboard[i][8] = ChessPieces.King(-1, 8, i)
            chessboard[i][1] = ChessPieces.King(1, 1, i)
        else:
            chessboard[i][8] = ChessPieces.Queen(-1, 8, i)
            chessboard[i][1] = ChessPieces.Queen(1, 1, i)

    return chessboard
