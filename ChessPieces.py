import os
import pygame
import GameFunctions


class ChessPiece:
    def __init__(self, owner, row, col):
        self.has_moved = 0
        self.owner = owner
        self.row = row
        self.col = col

    def display(self, game_display, sqr_l, sqr_w_buffer, sqr_h_buffer):
        game_display.blit(self.img,
                          (GameFunctions.calc_x(self.col, sqr_l, sqr_w_buffer)+ ((sqr_l - 64) / 2),
                           GameFunctions.calc_y(self.row, sqr_l, sqr_h_buffer)+ ((sqr_l - 64) / 2)))

    def show_moves(self):
        pass

    # for these functions 0 = no move, 1 = empty space, 2 = capture
    def can_move(self):
        return False


class Pawn(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn2.png')))
        super().__init__(owner, row, col)


class Knight(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight2.png')))
        super().__init__(owner, row, col)

    def show_moves(self):
        pass


class Bishop(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop2.png')))
        super().__init__(owner, row, col)

    def show_moves(self):
        pass


class Rook(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook2.png')))
        super().__init__(owner, row, col)

    def show_moves(self):
        pass


class Queen(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen2.png')))
        super().__init__(owner, row, col)

    def show_moves(self):
        pass


class King(ChessPiece):
    def __init__(self, owner, row, col):
        self.inCheck = False
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King2.png')))
        super().__init__(owner, row, col)

    def show_moves(self):
        pass
