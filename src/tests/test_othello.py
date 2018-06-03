# coding:utf-8
from othello.othello import Turn


def test_change_turn(othello):
    assert othello.turn == Turn.black
    othello.change_turn()
    assert othello.turn == Turn.white
    othello.change_turn()
    assert othello.turn == Turn.black


def test_run(othello):
    # othello.verbose = True
    othello.run()
