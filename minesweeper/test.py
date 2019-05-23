import minesweeper as MS
import unittest


# ATTRIBUTES:
# revealed
# flagged
# board
# level
# size
# mines


class GameTest(unittest.TestCase):

    def setUp(self):
        def fixed_init(*args, **kwargs):
            MS.Game.revealed.clear()
            MS.Game.flagged.clear()
            MS.Game.level = 1
            MS.Game.size = 5
            MS.Game.mines = 3
            MS.Game.board = []
            mined = [[0, 0, 0, 0, 9],
                     [0, 9, 0, 0, 0],
                     [0, 0, 0, 0, 0],
                     [0, 0, 9, 0, 0],
                     [0, 0, 0, 0, 0]]
            MS.Game.board.extend(mined)

        MS.Game.__init__ = fixed_init
        self.game = MS.Game()
        self.game.put_numbers()
        moves = [('open', 2, 2), ('open', 2, 4), ('flag', 0, 4)]
        self.modes = [x[0] for x in moves]
        self.i = [x[1] for x in moves]
        self.j = [x[2] for x in moves]
        # print(self.game.play(True, ['open'], [0], [4]))

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

    def test_b_get_move(self):
        # takes (True,mode,i,j), normally input
        # returns a tuple with (mode,i,j)
        for (mode, x, y) in (self.modes, self.i, self.j):
            with self.subTest(pattern=(mode, x, y)):
                self.assertEqual(self.game.get_move(True, mode, x, y), (mode, x, y))
        # with any input that would raise an error, it goes into an infinite loop

    def test_c_build(self):
        # initial build, later will be tested by mine number and empty tests
        self.assertEqual(self.game.board, [[1, 1, 1, 1, 9],
                                           [1, 9, 1, 1, 1],
                                           [1, 2, 2, 1, 0],
                                           [0, 1, 9, 1, 0],
                                           [0, 1, 1, 1, 0]])

    def test_d1_mine(self):
        # play returns False hence ends the game then a mine is clicked
        self.assertFalse(self.game.play(True, 'open', 0, 4))

    def test_d2_number(self):
        # play returns True
        # the box is added to the list 'revealed'
        self.assertTrue(self.game.play(True, 'open', 2, 2))
        self.assertIn((2, 2), self.game.revealed)

    def test_d3_empty(self):
        # play returns True
        # the box is added to the list 'revealed'
        # surrounding empty boxes and first line of number boxes also added to revealed
        self.assertTrue(self.game.play(True, 'open', 3, 4))
        for (a, b) in [(1, 3), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4), (4, 3), (4, 4)]:
            with self.subTest(pattern=(a, b)):
                self.assertIn((a, b), self.game.revealed)

    def test_e_flag(self):
        # play returns True
        # box is added to the list 'flagged'
        self.assertTrue(self.game.play(True, 'flag', 3, 2))
        self.assertIn((3, 2), self.game.flagged)

    def test_f1_win_flag(self):
        self.assertTrue(self.game.play(True, 'flag', 1, 1))
        self.assertTrue(self.game.play(True, 'flag', 0, 4))
        self.assertTrue(self.game.play(True, 'flag', 3, 2))
        self.assertTrue(self.game.won(True))

    def test_f2_win_open(self):
        self.assertTrue(self.game.play(True, 'open', 3, 4))
        self.assertTrue(self.game.play(True, 'open', 4, 0))
        self.assertTrue(self.game.play(True, 'open', 0, 0))
        self.assertTrue(self.game.play(True, 'open', 0, 1))
        self.assertTrue(self.game.play(True, 'open', 0, 2))
        self.assertTrue(self.game.play(True, 'open', 0, 3))
        self.assertTrue(self.game.play(True, 'open', 1, 0))
        self.assertTrue(self.game.play(True, 'open', 1, 2))
        self.assertTrue(self.game.play(True, 'open', 2, 2))
        self.assertTrue(self.game.play(True, 'open', 4, 2))
        self.assertTrue(self.game.won(True))
