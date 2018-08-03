import os
import pygame
import GameFunctions

# store RGB colour codes for pygame in tuples
rgb_black = (0, 0, 0)
rgb_white = (255, 255, 255)
rgb_red = (255, 0, 0)
rgb_green = (0, 255, 0)
rgb_blue = (0, 0, 255)


class ChessPiece:
    def __init__(self, owner, row, col):
        self.has_moved = False
        self.pawn_en_pass = False
        self.owner = owner
        self.row = row
        self.col = col

    def display(self, game_display, sqr_l, sqr_w_buffer, sqr_h_buffer):
        game_display.blit(self.img,
                          (GameFunctions.calc_x(self.col, sqr_l, sqr_w_buffer)+((sqr_l - 64) / 2),
                           GameFunctions.calc_y(self.row, sqr_l, sqr_h_buffer)+((sqr_l - 64) / 2)))

    def show_moves(self, chessboard, d_tool):
        pass

    def is_vert(self, to_x):
        if self.col == to_x:
            return True
        return False

    def is_horiz(self, to_y):
        if self.row == to_y:
            return True
        return False

    def is_diagonal(self, to_x, to_y):
        if (self.col-self.row == to_x-to_y)\
                or (self.col+self.row == to_x+to_y):
            return True
        return False

    def is_forward(self, to_y):
        if (self.row - to_y)*self.owner < 0:
            return True
        return False

    def vert_distance(self, to_y):
        return abs(self.row - to_y)

    def horiz_distance(self, to_x):
        return abs(self.col - to_x)

    def is_enemy(self, chessboard, to_x, to_y):
        return self.owner != chessboard[to_x][to_y].owner

    # for these functions 0 = no move, 1 = empty space, 2 = capture
    def can_move(self, chessboard, to_x, to_y):
        pass


class Pawn(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard, d_tool):
        if self.can_move(chessboard, self.col, self.row + self.owner) == 1:
            pygame.draw.ellipse(d_tool.screen,
                                rgb_blue,
                                (GameFunctions.calc_x(self.col, d_tool.sqr_l, d_tool.w_buffer),
                                 GameFunctions.calc_y(self.row + self.owner, d_tool.sqr_l, d_tool.h_buffer),
                                 d_tool.sqr_l, d_tool.sqr_l),
                                4)
            if self.can_move(chessboard, self.col, self.row + (2*self.owner)) == 1:
                pygame.draw.ellipse(d_tool.screen,
                                    rgb_blue,
                                    (GameFunctions.calc_x(self.col, d_tool.sqr_l, d_tool.w_buffer),
                                     GameFunctions.calc_y(self.row + (2*self.owner), d_tool.sqr_l, d_tool.h_buffer),
                                     d_tool.sqr_l, d_tool.sqr_l),
                                    4)
        if self.can_move(chessboard, self.col-1, self.row + self.owner) == 2:
            pygame.draw.ellipse(d_tool.screen,
                                rgb_red,
                                (GameFunctions.calc_x(self.col-1, d_tool.sqr_l, d_tool.w_buffer),
                                 GameFunctions.calc_y(self.row + self.owner, d_tool.sqr_l, d_tool.h_buffer),
                                 d_tool.sqr_l, d_tool.sqr_l),
                                4)
        if self.can_move(chessboard, self.col+1, self.row + self.owner) == 2:
            pygame.draw.ellipse(d_tool.screen,
                                rgb_red,
                                (GameFunctions.calc_x(self.col+1, d_tool.sqr_l, d_tool.w_buffer),
                                 GameFunctions.calc_y(self.row + self.owner, d_tool.sqr_l, d_tool.h_buffer),
                                 d_tool.sqr_l, d_tool.sqr_l),
                                4)

    def can_move(self, chessboard, to_x, to_y):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_forward(to_y):
                if self.is_vert(to_x):
                    if not chessboard[to_x][to_y]:
                        if self.vert_distance(to_y) == 1:
                            return 1
                        elif (self.vert_distance(to_y) == 2)\
                                and not chessboard[to_x][to_y-self.owner]\
                                and not self.has_moved:
                            return 1
                elif (self.horiz_distance(to_x) == 1)\
                        and (self.vert_distance(to_y) == 1):
                    if chessboard[to_x][to_y]\
                            and self.is_enemy(chessboard, to_x, to_y):
                        return 2
        return 0


class Knight(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight2.png')))
        super().__init__(owner, row, col)


class Bishop(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop2.png')))
        super().__init__(owner, row, col)


class Rook(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook2.png')))
        super().__init__(owner, row, col)


class Queen(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen2.png')))
        super().__init__(owner, row, col)


class King(ChessPiece):
    def __init__(self, owner, row, col):
        self.inCheck = False
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King2.png')))
        super().__init__(owner, row, col)

