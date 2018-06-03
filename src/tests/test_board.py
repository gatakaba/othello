from othello.othello import Turn


def test_get_item(board):
    assert board[3, 3] == 1
    assert board[3, 4] == -1
    assert board[4, 3] == -1
    assert board[4, 4] == 1


def test_check_select(board):
    assert board.check_select(2, 3, Turn.white)
    assert board.check_select(3, 2, Turn.white)

    assert board.check_select(4, 2, Turn.black)
    assert board.check_select(2, 4, Turn.black)


def test_update_board(board):
    assert not board[2, 3] == -1
    assert not board[3, 3] == -1
    assert board[4, 3] == -1
    board.update_board(2, 3, Turn.white)
    assert board[2, 3] == -1
    assert board[3, 3] == -1
    assert board[4, 3] == -1


def test_count(board):
    assert board.count_piece(Turn.white) == 2
    assert board.count_piece(Turn.black) == 2

    board.update_board(2, 3, Turn.white)

    assert board.count_piece(Turn.white) == 4
    assert board.count_piece(Turn.black) == 1
