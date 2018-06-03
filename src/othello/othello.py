# -*- coding:utf-8 -*-
"""オセロゲームのソースコード"""
__author__ = 'kaba'
__date__ = "2018/06/02"

import random
from enum import Enum

import numpy as np
from tabulate import tabulate


class Turn(Enum):
    """現在のターン"""

    black = 1
    white = -1


class Board(object):
    """盤面の保持と盤面操作を行うクラス

    盤面の初期状態は黒と白それぞれの駒が2つづつ中央に配置されている.

    Attributes:
        board (array-like): 盤面
        direction_list (list): 方向リスト

    """

    def __init__(self):
        """盤面を初期化する"""
        self.board = np.zeros([8, 8], dtype=np.int)
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
        self.direction_list = [[-1, -1], [0, -1], [1, -1], [-1, 0],
                               [1, 0], [-1, 1], [0, 1], [1, 1]]

    def __getitem__(self, p):
        """盤面の状態を取得する"""
        return self.board[p[0], p[1]]

    def count_piece(self, turn: Turn) -> int:
        """引数で指定したプレイヤーの駒の数を数える

        Args:
            turn: 現在のターン

        Returns:
            ピース数

        """
        return len(np.where(self.board == turn.value)[0])

    def show_board(self):
        """現在の盤面を表示する"""
        headers = list(range(0, 8))
        print(tabulate(self.board, headers=headers,
                       showindex=headers, tablefmt="fancy_grid"))

    def get_available_cell(self, turn: Turn) -> list:
        """置くことができるセルを返す

        Args:
            turn: 現在のターン

        Returns:
            置くことができるセル座標のリスト

        """
        available_cell_list = []
        for i in range(8):
            for j in range(8):
                if self.check_select(i, j, turn):
                    available_cell_list.append([i, j])
        return available_cell_list

    def _check_select(self, x: int, y: int, dx: int, dy: int, turn: Turn) -> bool:
        """dx,dyの方向に置くことができるかを判定する

        Args:
            x: x座標
            y: y座標
            dx: xの増分
            dy: yの増分
            turn : 現在のターン

        Returns:
            置ける場合はTrueを返し、置けない場合はFalseを返す

        """
        if not (self.board[x, y]) == 0:
            return False
        for i in range(8):
            x += dx
            y += dy
            # チェック対象が盤内かを判定する
            if not ((0 <= x < 8) and (0 <= y < 8)):
                break
            board_value = self.board[x, y]
            if i == 0:
                # 近接セルのチェック
                if not (board_value == turn.value * -1):
                    break
            else:
                # 近接以降のセルをチェック
                if board_value == turn.value:
                    return True
                elif board_value == 0:
                    return False

    def check_select(self, x_index: int, y_index: int, turn: Turn) -> bool:
        """置くことができるかチェックする

         8方向に対し、以下の条件を満たしているかを確認する

         1. チェック対象に近接しているセルが異なる色である
         2. 1.以降の色が異なる色または同じ色

        Args:
            x_index: x座標
            y_index: y座標
            turn: 現在のターン

        Returns:
            置ける場合はTrueを返し、置けない場合はFalseを返す

        """
        for dx, dy in self.direction_list:
            if self._check_select(x_index, y_index, dx, dy, turn):
                return True

    def update_board(self, x_index: int, y_index: int, turn: Turn):
        """盤面を更新する

        8方向に対し、置くことができるかを確認し、置けることができる場合、
        その方向に対し、同じ色を置く

        Args:
            x_index: x座標
            y_index: y座標
            turn: 現在のターン

        """
        for dx, dy in self.direction_list:
            if not self._check_select(x_index, y_index, dx, dy, turn):
                continue
            x = x_index
            y = y_index
            self.board[x, y] = turn.value
            while True:
                x += dx
                y += dy
                if not (self.board[x, y] == turn.value):
                    self.board[x, y] = turn.value
                else:
                    break


class Othello(object):
    """オセロゲームを管理するクラス

    run関数によりゲームを始めることができる
    黒か白のいずれかが置けなくなった場合ゲームを終了する

    Attributes:
        board(Board): 盤面
        turn(Turn): 現在のターン
        verbose(bool): 現在の状態を表示するか

    """

    def __init__(self, verbose=True):
        """ゲームを初期化する"""
        self.board = Board()
        self.turn = Turn.black
        self.verbose = verbose

    def get_input(self):
        """ユーザからの入力を取得する"""
        if self.verbose:
            if self.turn == Turn.black:
                print('黒のターンです')
            else:
                print('白のターンです')

            print(self.board.get_available_cell(self.turn))

        while True:
            # input_value = input()
            # x_index, y_index = input_value.split(',')
            # x_index, y_index = int(x_index), int(y_index)
            x_index, y_index = random.choice(self.board.get_available_cell(self.turn))

            return x_index, y_index

    def change_turn(self):
        """ターンを交換する"""
        self.turn = Turn.white if self.turn == Turn.black else Turn.black
        if len(self.board.get_available_cell(self.turn)) == 0:
            self.turn = Turn.white if self.turn == Turn.black else Turn.black

    def check_finish(self):
        """終了を確認する"""
        return len(self.board.get_available_cell(self.turn)) == 0

    def run(self):
        """メインシーケンス"""
        while True:
            if self.verbose:
                self.board.show_board()
            x_index, y_index = self.get_input()
            self.board.update_board(x_index, y_index, self.turn)
            self.change_turn()

            if self.check_finish():
                black_num = self.board.count_piece(Turn.black)
                white_num = self.board.count_piece(Turn.white)
                if black_num > white_num:
                    print(black_num, white_num, '黒の勝ち')
                else:
                    print(black_num, white_num, '白の勝ち')
                break
