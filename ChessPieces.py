import os
import pygame


class ChessPiece:
    def __init__(self, owner, row, col):
        self.moves = 0
        self.owner = owner
        self.row = row
        self.col = col

    def display(self, game_display, sqr_l, sqr_w_buffer, sqr_h_buffer):
        game_display.blit(self.img, (self.__calc_x(sqr_l, sqr_w_buffer), self.__calc_y(sqr_l, sqr_h_buffer)))

    def __calc_x(self, sqr_l, sqr_w_buffer):
        x_start = ((self.col - 1) * sqr_l) + ((sqr_l - 64) / 2) + sqr_w_buffer
        return x_start

    def __calc_y(self, sqr_l, sqr_h_buffer):
        y_start = ((self.row - 1) * sqr_l) + ((sqr_l - 64) / 2) + sqr_h_buffer
        return y_start

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass

    def can_move(self, x, y):
        return False


class Pawn(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass

    def can_move(self, x, y):
        return False


class Knight(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass


class Bishop(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass


class Rook(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass


class Queen(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass


class King(ChessPiece):
    def __init__(self, owner, row, col):
        self.inCheck = False
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard_window, sqr_l,
                   sqr_w_buffer, sqr_h_buffer,
                   chessboard, white_turn):
        pass
