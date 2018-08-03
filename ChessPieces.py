import os
import pygame
import GameFunctions

# store RGB colour codes for pygame in tuples
rgb_black = (0, 0, 0)
rgb_white = (255, 255, 255)
rgb_red = (255, 0, 0)
rgb_green = (0, 255, 0)
rgb_blue = (0, 0, 255)

colour = [rgb_black, rgb_white, rgb_blue, rgb_red, rgb_green]


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
        if not chessboard[to_x][to_y]:
            return False
        return self.owner != chessboard[to_x][to_y].owner

    def open_between(self, chessboard, to_x, to_y):
        x = self.col
        y = self.row
        if (to_x - x) != 0:
            x_dir = int((to_x - x)/self.horiz_distance(to_x))
        else:
            x_dir = 0
        if (to_y - y) != 0:
            y_dir = int((to_y - y)/self.vert_distance(to_y))
        else:
            y_dir = 0
        x += x_dir
        y += y_dir
        while (x != to_x or y != to_y) and (0 < to_x < 9) and (0 < to_y < 9):
            if chessboard[x][y]:
                print('blocked at ({}, {})'.format(x,y))
                return False
            x += x_dir
            y += y_dir
        return True

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

    def show_moves(self, chessboard, d_tool):
        for i in range(-2, 3):
            check = self.can_move(chessboard, self.col+i, self.row-(3-abs(i)))
            if check > 0:
                pygame.draw.ellipse(d_tool.screen,
                                    colour[check+1],
                                    (GameFunctions.calc_x(self.col + i, d_tool.sqr_l, d_tool.w_buffer),
                                     GameFunctions.calc_y(self.row - (3-abs(i)), d_tool.sqr_l, d_tool.h_buffer),
                                     d_tool.sqr_l, d_tool.sqr_l),
                                    4)
            check = self.can_move(chessboard, self.col+i, self.row+(3-abs(i)))
            if check > 0:
                pygame.draw.ellipse(d_tool.screen,
                                    colour[check+1],
                                    (GameFunctions.calc_x(self.col + i, d_tool.sqr_l, d_tool.w_buffer),
                                     GameFunctions.calc_y(self.row + (3-abs(i)), d_tool.sqr_l, d_tool.h_buffer),
                                     d_tool.sqr_l, d_tool.sqr_l),
                                    4)

    def can_move(self, chessboard, to_x, to_y):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if (self.vert_distance(to_y) > 0)\
                    and (self.horiz_distance(to_x) > 0)\
                    and (self.vert_distance(to_y)+self.horiz_distance(to_x) == 3):
                if not chessboard[to_x][to_y]:
                    return 1
                if self.is_enemy(chessboard, to_x, to_y):
                    return 2

        return 0


class Bishop(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard, d_tool):
        for i in range(-1,2):
            for j in range(-1,2):
                x = self.col+i
                y = self.row+j
                while self.can_move(chessboard, x, y) == 1:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_blue,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)
                    x += i
                    y += j
                if self.can_move(chessboard, x, y) == 2:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_red,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)

    def can_move(self, chessboard, to_x, to_y):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_diagonal(to_x, to_y):
                if self.open_between(chessboard, to_x, to_y):
                    if not chessboard[to_x][to_y]:
                        return 1
                    elif self.is_enemy(chessboard, to_x, to_y):
                        return 2
        return 0


class Rook(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard, d_tool):
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.col+i
                y = self.row+j
                while self.can_move(chessboard, x, y) == 1:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_blue,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)
                    x += i
                    y += j
                if self.can_move(chessboard, x, y) == 2:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_red,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)

    def can_move(self, chessboard, to_x, to_y):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_horiz(to_y) or self.is_vert(to_x):
                if self.open_between(chessboard, to_x, to_y):
                    if not chessboard[to_x][to_y]:
                        return 1
                    elif self.is_enemy(chessboard, to_x, to_y):
                        return 2
        return 0


class Queen(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard, d_tool):
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.col+i
                y = self.row+j
                while self.can_move(chessboard, x, y) == 1:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_blue,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)
                    x += i
                    y += j
                if self.can_move(chessboard, x, y) == 2:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_red,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)

    def can_move(self, chessboard, to_x, to_y):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_horiz(to_y) or self.is_vert(to_x) or self.is_diagonal(to_x, to_y):
                if self.open_between(chessboard, to_x, to_y):
                    if not chessboard[to_x][to_y]:
                        return 1
                    elif self.is_enemy(chessboard, to_x, to_y):
                        return 2
        return 0


class King(ChessPiece):
    def __init__(self, owner, row, col):
        self.inCheck = False
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\King2.png')))
        super().__init__(owner, row, col)

    def show_moves(self, chessboard, d_tool):
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.col+i
                y = self.row+j
                while self.can_move(chessboard, x, y) == 1:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_blue,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)
                    x += i
                    y += j
                if self.can_move(chessboard, x, y) == 2:
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_red,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)

    def can_move(self, chessboard, to_x, to_y):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if (self.horiz_distance(to_x) < 2)\
                    and (self.vert_distance(to_y) < 2)\
                    and (self.horiz_distance(to_x) + self.vert_distance(to_y)):
                if not chessboard[to_x][to_y]:
                    return 1
                elif self.is_enemy(chessboard, to_x, to_y):
                    return 2
        return 0
