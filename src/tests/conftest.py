import pytest

from othello.othello import Board, Othello


@pytest.fixture()
def board():
    yield Board()


@pytest.fixture()
def othello():
    return Othello(verbose=False)
