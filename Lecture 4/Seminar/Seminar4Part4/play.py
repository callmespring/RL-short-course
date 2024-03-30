# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

author: Junxiao Song
modified by: Bento Natura
"""

from __future__ import print_function
from logging import warning
from game import Board, Game
import argparse
from mcts_alpha_zero import MCTSPlayer
from policy_value_net_numpy import PolicyValueNetNumpy #Numpy
#from policy_value_net_tensorflow import PolicyValueNet # Tensorflow

from pathlib import Path
import warnings


from time import sleep
import tkinter
class Human(object):
    """
    human player
    """
    
    def __init__(self, use_gui):
        self.player = None
        self.use_gui = use_gui 
        self.location_updated = False
    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            if self.use_gui is False:
                location = input("Your move: ")
                if isinstance(location, str):  # for python3
                    self.location = [int(n, 10) for n in location.split(",")]
            else:
                while True:
                    if self.location_updated:
                        self.location_updated = False
                        break
                    sleep(0.05)
                    self.top.update()
            move = board.location_to_move(self.location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run(width=8, height=8, num_consecutive=5, use_gui=True):
    
    pretrained_model_string = f'models/best_pretrained_policy_{width}_{height}_{num_consecutive}.model'
    
    pretrained_model_file = Path(pretrained_model_string)
    if(pretrained_model_file.is_file()):
        best_policy = PolicyValueNetNumpy(width, height, pretrained_model_file)
    else:
        stored_model_string = f'models/best_stored_policy_{width}_{height}_{num_consecutive}.model'
        stored_model_file = Path(stored_model_string)
        if stored_model_file.is_file():
            best_policy = PolicyValueNet(width, height, stored_model_string)
        else:
            best_policy = PolicyValueNet(width, height, None)
            warnings.warn("Model does not exists. AI uses random policy.")
    try:
        board = Board(width=width, height=height, n_in_row=num_consecutive)
        game = Game(board)

        mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance

        human = Human(use_gui)

        user_move_first = False
        if use_gui:
            if not tkinter.messagebox.askyesno(title='Please choose', message='You will have the black stones. Do you want to begin?'):
                user_move_first = True

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=user_move_first, is_shown=1, use_gui=use_gui)
        game.gui.top.mainloop()
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Pipeline for training. Specify the board dimensions and number of pieces in row to win.')
    parser.add_argument('--size', type=int, nargs='?', default=8,
                        help='board size')
    parser.add_argument('--win_length', type=int, nargs='?', default=5,
                        help='number in row to win')
    parser.add_argument('--no_gui', type=bool, nargs='?', default=False,
                        help='Display GUI')    
    args = parser.parse_args()

    use_gui = not args.no_gui

    run(width=args.size,height=args.size,num_consecutive=args.win_length, use_gui=use_gui)

