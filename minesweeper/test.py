import minesweeper as MS
import unittest


# ATTRIBUTES:
# revealed
# flagged
# board
# level
# size
# mines

# class Game(MS.Game):
#     def __init__(self, *args):
#         super(Game, self).__init__()
#
#     def get_move(self):
#         pass
#
# def fixed_init(*args, **kwargs):
#     MS.Game.revealed.clear()
#     MS.Game.flagged.clear()
#     MS.Game.level = 1
#     MS.Game.size = 5
#     MS.Game.mines = 3
#     MS.Game.board = [[1, 1, 1, 1, 9],
#                      [1, 9, 1, 1, 1],
#                      [1, 2, 2, 1, 0],
#                      [0, 1, 9, 1, 0],
#                      [0, 1, 1, 1, 0]]
#
#
# MS.Game.__init__ = fixed_init


# MS.Game.minesweeper(True,modes,i,j,1)

class GameTest(unittest.TestCase):


    def setUp(self):
        def fixed_init(*args, **kwargs):
            MS.Game.revealed.clear()
            MS.Game.flagged.clear()
            MS.Game.level = 1
            MS.Game.size = 5
            MS.Game.mines = 3
            MS.Game.board = [[1, 1, 1, 1, 9],
                             [1, 9, 1, 1, 1],
                             [1, 2, 2, 1, 0],
                             [0, 1, 9, 1, 0],
                             [0, 1, 1, 1, 0]]

        MS.Game.__init__ = fixed_init
        self.game = MS.Game()
        moves = [('open', 2, 2), ('open', 2, 4), ('flag', 0, 4)]
        self.modes = [x[0] for x in moves]
        self.i = [x[1] for x in moves]
        self.j = [x[2] for x in moves]
        # MS.Game.minesweeper(True, modes, i, j, 1)

    @classmethod
    def tearDownClass(cls):
        MS.Game.__init__ = MS.Game.__init__

    @unittest.expectedFailure
    def test_a_level_input(self):
        # should take 1 2 or 3 only
        for arg in [1, 2, 3]:
            with self.subTest(pattern=arg):
                self.assertRaises(RuntimeError, MS.Game.get_level, True, arg)
        # with any input that would raise an error, it goes into an infinite loop

    # play is too short and straight forward
    # just a middle step between minesweeper and get_move

    def test_b_get_move(self):
        # takes (True,mode,i,j), normally input
        # returns a tuple with (mode,i,j)
        for (mode, x, y) in (self.modes, self.i, self.j):
            self.assertEqual(self.game.get_move(True, mode, x, y), (mode, x, y))

    def test_c_build(self):
        # initial build, later will be tested by mine number and empty tests
        pass

    def test_d_mine(self):
        # should display the whole board with correct flags in place
        # end the game
        pass

    def test_e_number(self):
        # should display with clicked number
        # cont game
        pass

    def test_f_empty(self):
        # should display all 0s around + first row of numbers
        # cont game
        pass

    def test_g_win(self):
        # all flagged
        # all open
        # somewhere in between
        pass

    def test_h_loop(self):
        # play again for Y and y
        # say bye and exit for N and n
        pass
