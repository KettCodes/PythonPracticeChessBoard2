def calc_x(col, sqr_l, sqr_w_buffer):
    return ((col - 1) * sqr_l) + sqr_w_buffer


def calc_y(row, sqr_l, sqr_h_buffer):
    return ((row - 1) * sqr_l) + sqr_h_buffer
