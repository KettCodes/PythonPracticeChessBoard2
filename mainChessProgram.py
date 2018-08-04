import pygame
import ChessCreateBoard
import GameFunctions


def main():
    # start pygame modules that need to be started
    pygame.init()

    # display setting information
    display_w = 1200
    display_h = 900
    length_num = 8
    if display_h < display_w:
        sqr_l = display_h / length_num
        sqr_h_buffer = 0
        sqr_w_buffer = (display_w - display_h) / 2
    else:
        sqr_l = display_w / length_num
        sqr_h_buffer = (display_h - display_w) / 2
        sqr_w_buffer = 0

    # store RGB colour codes for pygame in tuples
    rgb_black = (0, 0, 0)
    rgb_white = (255, 255, 255)
    rgb_red = (255, 0, 0)
    rgb_green = (0, 255, 0)
    rgb_blue = (0, 0, 255)

    # create the window with caption and a game clock
    chessboard_window = pygame.display.set_mode((display_w, display_h))
    pygame.display.set_caption('Python 2-Player Chess')
    clock = pygame.time.Clock()

    # create the chessboard including pieces and ready first turn
    chessboard = ChessCreateBoard.create_board()
    white_turn = True
    active_piece = None
    king = [chessboard[5][8], chessboard[5][1]]
    player_in_check = [False, False]
    drawing = GameFunctions.Dimensions(screen=chessboard_window, sqr_l=sqr_l,
                                       w_buffer=sqr_w_buffer, h_buffer=sqr_h_buffer)

    # start the game loop
    continue_game = True
    while continue_game:

        # pygame event loop stacks events in a frame
        for event in pygame.event.get():
            # activates if user closes game window
            if event.type == pygame.QUIT:
                continue_game = False
            # activates on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = pygame.mouse.get_pos()
                if (sqr_w_buffer < click_pos[0] < display_w - sqr_w_buffer)\
                        and(sqr_h_buffer < click_pos[1] < display_h - sqr_h_buffer):
                    click_x = int((click_pos[0]-sqr_w_buffer)/sqr_l)+1
                    click_y = int((click_pos[1]-sqr_h_buffer)/sqr_l)+1
                    if active_piece and active_piece.can_move(chessboard, click_x, click_y, king[1-white_turn])\
                            and ((active_piece.owner == 1) != white_turn):
                        chessboard[click_x][click_y] = active_piece
                        chessboard[active_piece.col][active_piece.row] = None
                        active_piece.col = click_x
                        active_piece.row = click_y
                        active_piece.has_moved = True
                        active_piece = None
                        white_turn = not white_turn
                        if king[1-white_turn].in_check(chessboard):
                            player_in_check[1-white_turn] = True
                            print('CHECK!')
                    else:
                        active_piece = chessboard[click_x][click_y]
                else:
                    active_piece = None

        i = 1
        j = 1
        legal_moves = 0
        while legal_moves == 0 and i < 9:
            if j > 8:
                j = 1
                i += 1
            if i < 9 and chessboard[i][j]\
                    and ((chessboard[i][j].owner == 1) != white_turn):
                legal_moves = chessboard[i][j].find_moves(chessboard, king[1-white_turn], drawing)
            j += 1
        if i == 9:
            if player_in_check[1 - white_turn]:
                print('CHECKMATE')
                continue_game = False
            else:
                print('STALEMATE')
                continue_game = False

        # starting with the background the chessboard is drawn along with the active piece paths
        chessboard_window.fill(rgb_black)
        for i in range(1, 9):
            for j in range(1, 9):
                if (i+j)%2 == 0:
                    pygame.draw.rect(chessboard_window,
                                     rgb_white,
                                     (GameFunctions.calc_x(i, sqr_l, sqr_w_buffer),
                                      GameFunctions.calc_y(j, sqr_l, sqr_h_buffer),
                                      sqr_l, sqr_l),
                                     0)
                if chessboard[i][j]:
                    chessboard[i][j].display(chessboard_window, sqr_l,
                                             sqr_w_buffer, sqr_h_buffer)
        if active_piece:
            active_piece.find_moves(chessboard, king[1-white_turn], drawing)

        # after drawing the board it is updated to the screen and frames are updated
        pygame.display.update()
        clock.tick(100)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()

# current_key = pygame.key.get_pressed()

# if current_key[pygame.K_LEFT]:
#    hero.col -= x_change
# if current_key[pygame.K_RIGHT]:
#    hero.col += x_change
