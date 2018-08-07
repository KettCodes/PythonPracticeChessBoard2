import os
import pygame
import GameFunctions
import ChessCreateBoard

# store RGB colour codes for pygame in tuples
rgb_black = (0, 0, 0)
rgb_white = (255, 255, 255)
rgb_red = (255, 0, 0)
rgb_green = (0, 255, 0)
rgb_blue = (0, 0, 255)

colour = [rgb_black, rgb_white, rgb_blue, rgb_red, rgb_green]


class ChessPiece:
    def __init__(self, owner, row, col):
        self.img = self.img
        self.has_moved = False
        self.en_pass = False
        self.owner = owner
        self.row = row
        self.col = col

    def display(self, game_display, sqr_l, sqr_w_buffer, sqr_h_buffer):
        game_display.blit(self.img,
                          (GameFunctions.calc_x(self.col, sqr_l, sqr_w_buffer)+((sqr_l - 64) / 2),
                           GameFunctions.calc_y(self.row, sqr_l, sqr_h_buffer)+((sqr_l - 64) / 2)))

    def find_moves(self, chessboard, my_king, d_tool):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.col+i
                y = self.row+j
                while self.can_move(chessboard, x, y, my_king) == 1:
                    count += 1
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_blue,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)
                    x += i
                    y += j
                if self.can_move(chessboard, x, y, my_king) == 2:
                    count += 1
                    pygame.draw.ellipse(d_tool.screen,
                                        rgb_red,
                                        (GameFunctions.calc_x(x, d_tool.sqr_l, d_tool.w_buffer),
                                         GameFunctions.calc_y(y, d_tool.sqr_l, d_tool.h_buffer),
                                         d_tool.sqr_l, d_tool.sqr_l),
                                        4)
        return count

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
                return False
            x += x_dir
            y += y_dir
        return True

    # for these functions 0 = no move, 1 = empty space, 2 = capture
    def can_move(self, chessboard, to_x, to_y, my_king):
        pass

    def self_check(self, chessboard, to_x, to_y, my_king):
        check = False
        to_x = int(to_x)
        to_y = int(to_y)
        save_x = self.col
        save_y = self.row
        self.col = to_x
        self.row = to_y
        save_capture = chessboard[to_x][to_y]
        chessboard[save_x][save_y] = None
        chessboard[to_x][to_y] = self
        if my_king.in_check(chessboard):
            check = True
        self.col = save_x
        self.row = save_y
        chessboard[save_x][save_y] = self
        chessboard[to_x][to_y] = save_capture
        return check


class Pawn(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Pawn2.png')))
        super().__init__(owner, row, col)

    def find_moves(self, chessboard, my_king, d_tool):
        count = 0
        if self.can_move(chessboard, self.col, self.row + self.owner, my_king) == 1:
            count += 1
            pygame.draw.ellipse(d_tool.screen,
                                rgb_blue,
                                (GameFunctions.calc_x(self.col, d_tool.sqr_l, d_tool.w_buffer),
                                 GameFunctions.calc_y(self.row + self.owner, d_tool.sqr_l, d_tool.h_buffer),
                                 d_tool.sqr_l, d_tool.sqr_l),
                                4)
            if self.can_move(chessboard, self.col, self.row + (2*self.owner), my_king) == 1:
                count += 1
                pygame.draw.ellipse(d_tool.screen,
                                    rgb_blue,
                                    (GameFunctions.calc_x(self.col, d_tool.sqr_l, d_tool.w_buffer),
                                     GameFunctions.calc_y(self.row + (2*self.owner), d_tool.sqr_l, d_tool.h_buffer),
                                     d_tool.sqr_l, d_tool.sqr_l),
                                    4)
        if self.can_move(chessboard, self.col-1, self.row + self.owner, my_king) == 2:
            count += 1
            pygame.draw.ellipse(d_tool.screen,
                                rgb_red,
                                (GameFunctions.calc_x(self.col-1, d_tool.sqr_l, d_tool.w_buffer),
                                 GameFunctions.calc_y(self.row + self.owner, d_tool.sqr_l, d_tool.h_buffer),
                                 d_tool.sqr_l, d_tool.sqr_l),
                                4)
        if self.can_move(chessboard, self.col+1, self.row + self.owner, my_king) == 2:
            count += 1
            pygame.draw.ellipse(d_tool.screen,
                                rgb_red,
                                (GameFunctions.calc_x(self.col+1, d_tool.sqr_l, d_tool.w_buffer),
                                 GameFunctions.calc_y(self.row + self.owner, d_tool.sqr_l, d_tool.h_buffer),
                                 d_tool.sqr_l, d_tool.sqr_l),
                                4)
        return count

    def can_move(self, chessboard, to_x, to_y, my_king):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_forward(to_y):
                if self.is_vert(to_x):
                    if not chessboard[to_x][to_y]:
                        if self.vert_distance(to_y) == 1:
                            if not self.self_check(chessboard, to_x, to_y, my_king):
                                return 1
                        elif (self.vert_distance(to_y) == 2)\
                                and not chessboard[to_x][to_y-self.owner]\
                                and not self.has_moved:
                            if not self.self_check(chessboard, to_x, to_y, my_king):
                                return 1
                elif (self.horiz_distance(to_x) == 1)\
                        and (self.vert_distance(to_y) == 1):
                    if chessboard[to_x][to_y]\
                            and self.is_enemy(chessboard, to_x, to_y):
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 2
                    elif not chessboard[to_x][to_y] \
                            and chessboard[to_x][self.row] and chessboard[to_x][self.row].en_pass:
                        temp = chessboard[to_x][self.row]
                        chessboard[to_x][self.row] = None
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            chessboard[to_x][self.row] = temp
                            return 2
                        chessboard[to_x][self.row] = temp
        return 0


class Knight(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Knight2.png')))
        super().__init__(owner, row, col)

    def find_moves(self, chessboard, my_king, d_tool):
        count = 0
        for i in range(-2, 3):
            check = self.can_move(chessboard, self.col+i, self.row-(3-abs(i)), my_king)
            if check > 0:
                count += 1
                pygame.draw.ellipse(d_tool.screen,
                                    colour[check+1],
                                    (GameFunctions.calc_x(self.col + i, d_tool.sqr_l, d_tool.w_buffer),
                                     GameFunctions.calc_y(self.row - (3-abs(i)), d_tool.sqr_l, d_tool.h_buffer),
                                     d_tool.sqr_l, d_tool.sqr_l),
                                    4)
            check = self.can_move(chessboard, self.col+i, self.row+(3-abs(i)), my_king)
            if check > 0:
                count += 1
                pygame.draw.ellipse(d_tool.screen,
                                    colour[check+1],
                                    (GameFunctions.calc_x(self.col + i, d_tool.sqr_l, d_tool.w_buffer),
                                     GameFunctions.calc_y(self.row + (3-abs(i)), d_tool.sqr_l, d_tool.h_buffer),
                                     d_tool.sqr_l, d_tool.sqr_l),
                                    4)
        return count

    def can_move(self, chessboard, to_x, to_y, my_king):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if (self.vert_distance(to_y) > 0)\
                    and (self.horiz_distance(to_x) > 0)\
                    and (self.vert_distance(to_y)+self.horiz_distance(to_x) == 3):
                if not chessboard[to_x][to_y]:
                    if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 1
                if self.is_enemy(chessboard, to_x, to_y):
                    if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 2

        return 0


class Bishop(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Bishop2.png')))
        super().__init__(owner, row, col)

    def can_move(self, chessboard, to_x, to_y, my_king):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_diagonal(to_x, to_y):
                if self.open_between(chessboard, to_x, to_y):
                    if not chessboard[to_x][to_y]:
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 1
                    elif self.is_enemy(chessboard, to_x, to_y):
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 2
        return 0


class Rook(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Rook2.png')))
        super().__init__(owner, row, col)

    def can_move(self, chessboard, to_x, to_y, my_king):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_horiz(to_y) or self.is_vert(to_x):
                if self.open_between(chessboard, to_x, to_y):
                    if not chessboard[to_x][to_y]:
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 1
                    elif self.is_enemy(chessboard, to_x, to_y):
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 2
        return 0


class Queen(ChessPiece):
    def __init__(self, owner, row, col):
        if owner == 1:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen.png')))
        else:
            self.img = pygame.image.load(os.path.abspath(os.path.join('.', 'sprites\Queen2.png')))
        super().__init__(owner, row, col)

    def can_move(self, chessboard, to_x, to_y, my_king):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if self.is_horiz(to_y) or self.is_vert(to_x) or self.is_diagonal(to_x, to_y):
                if self.open_between(chessboard, to_x, to_y):
                    if not chessboard[to_x][to_y]:
                        if not self.self_check(chessboard, to_x, to_y, my_king):
                            return 1
                    elif self.is_enemy(chessboard, to_x, to_y):
                        if not self.self_check(chessboard, to_x, to_y, my_king):
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

    def can_move(self, chessboard, to_x, to_y, my_king):
        if (0 < to_x < 9) and (0 < to_y < 9):
            if (self.horiz_distance(to_x) < 2)\
                    and (self.vert_distance(to_y) < 2)\
                    and (self.horiz_distance(to_x) + self.vert_distance(to_y)):
                if not chessboard[to_x][to_y]:
                    if not self.self_check(chessboard, to_x, to_y, my_king):
                        return 1
                elif self.is_enemy(chessboard, to_x, to_y):
                    if not self.self_check(chessboard, to_x, to_y, my_king):
                        return 2
            if not self.has_moved and self.vert_distance(to_y) == 0\
                    and self.horiz_distance(to_x) == 2:
                x_change = (to_x - self.col)/2
                new_x = self.col
                for i in range(3):
                    if self.self_check(chessboard, new_x, to_y, my_king):
                        return 0
                    new_x += x_change
                while 1 < new_x < 8:
                    new_x += x_change
                new_x = int(new_x)
                if self.open_between(chessboard, new_x, to_y)\
                        and chessboard[new_x][to_y] and not chessboard[new_x][to_y].has_moved:
                    return 1
        return 0

    def in_check(self, chessboard):
        # check non-knight pieces
        for i in range(-1, 2):
            for j in range(-1, 2):
                x = self.col+i
                y = self.row+j

                while (0 < x < 9) and (0 < y < 9)\
                        and not chessboard[x][y]:
                    x += i
                    y += j
                if (0 < x < 9) and (0 < y < 9):
                    if self.is_enemy(chessboard, x, y):
                        if i == 0 or j == 0:
                            if chessboard[x][y].__class__.__name__ == 'Queen'\
                                    or chessboard[x][y].__class__.__name__ == 'Rook':
                                return True
                            elif chessboard[x][y].__class__.__name__ == 'King'\
                                    and self.horiz_distance(x) < 2 and self.vert_distance(y) < 2:
                                return True
                        elif chessboard[x][y].__class__.__name__ == 'Queen'\
                                or chessboard[x][y].__class__.__name__ == 'Bishop':
                            return True
                        elif self.horiz_distance(x) < 2 and self.vert_distance(y) < 2:
                            if chessboard[x][y].__class__.__name__ == 'King':
                                return True
                            elif self.is_forward(y) and chessboard[x][y].__class__.__name__ == 'Pawn':
                                return True
        # check knight pieces
        for k in range(-2, 3):
            x = self.col+k
            y = self.row+(3-abs(k))
            z = self.row-(3-abs(k))
            if k != 0:
                if (0 < x < 9) and (0 < y < 9):
                    if chessboard[x][y] and self.is_enemy(chessboard, x, y)\
                            and chessboard[x][y].__class__.__name__ == 'Knight':
                                return True
                if (0 < x < 9) and (0 < z < 9):
                    if chessboard[x][z] and self.is_enemy(chessboard, x, z)\
                            and chessboard[x][z].__class__.__name__ == 'Knight':
                                return True
        return False

