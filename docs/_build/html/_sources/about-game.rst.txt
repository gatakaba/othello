about this game
=================

クラス図
-----------

.. uml::

  class Othello{
  + verbose
  + turn
  + board
  + change_turn()
  + check_finish()
  + get_input()
  + run()
  }

  class Board{
  + board
  + direction_list
  + check_select()
  + count_piece()
  + get_available_cel()
  + show_board()
  + update_board()
  }

  class Turn{
  + black
  + white
  }

  Othello o-- Board
  Othello o- Turn


シーケンス図
-----------

.. uml::

  activate othello
  othello -> othello : 初期化

  loop
    othello -> player: 入力候補
    activate player
    player --> othello : 操作入力
    deactivate player

    othello -> othello : 盤面の更新
    activate othello
    deactivate othello

    othello -> player : 更新結果

    othello -> othello : 終了判定
    activate othello
    deactivate othello

    break 終了条件を満たした場合
      othello -> player : 勝敗結果
    end
  end
  deactivate othello
