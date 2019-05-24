import minesweeper as MS
import unittest


# ATTRIBUTES:
# revealed
# flagged
# board
# level
# size
# mines


class MinesweeperTest(unittest.TestCase):

    def setUp(self):
        self.game = MS.Minesweeper(1)
        self.game.revealed.clear()
        self.game.flagged.clear()
        self.game.level = 1
        self.game.size = 5
        self.game.mines = 4
        self.game.board = []
        mined = [[0, 0, 9, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 9],
                 [0, 0, 0, 0, 0],
                 [0, 9, 0, 0, 9]]
        self.game.board.extend(mined)
        self.game.put_numbers()
        self.moves = ['2 2', '2 4', '0 4 f']

    def test_random_board(self):
        for level in [1, 2, 3]:
            with self.subTest():
                self.game = MS.Minesweeper(level)
                count = 0
                for x in self.game.board:
                    for y in x:
                        if y == 9:
                            count += 1
                self.assertEqual(count, self.game.mines)

    @unittest.expectedFailure
    def test_a_get_level(self):
        # should take 1 2 or 3 only
        for arg in [1, 2, 3]:
            with self.subTest(pattern=arg):
                self.assertRaises(RuntimeError, MS.Minesweeper.get_level, arg)
        # with any input that would raise an error, it goes into an infinite loop

    def test_b_make_move(self):
        # takes a move
        # returns i j and key

        make_move_results = [[2, 2, 'open'], [2, 4, 'open'], [0, 4, 'flag']]
        for i in range(len(self.moves)):
            typed = self.moves[i]
            for j in (0, 1, 2):
                with self.subTest(pattern=typed):
                    tupl = self.game.make_move(typed)
                    self.assertEqual(tupl[j], make_move_results[i][j])
        # with any input that would raise an error, it goes into an infinite loop

    def test_c_build(self):
        # initial build, later will be tested by mine number and empty tests
        self.assertEqual(self.game.board, [[0, 1, 9, 1, 0],
                                           [0, 1, 1, 2, 1],
                                           [0, 0, 0, 1, 9],
                                           [1, 1, 1, 2, 2],
                                           [1, 9, 1, 1, 9]])

    def test_d1_mine(self):
        # play returns False hence ends the game then a mine is clicked
        self.assertFalse(self.game.play('0 2'))
        self.game.lost()

    def test_d2_number(self):
        # play returns True
        # the box is added to the list 'revealed'
        self.assertTrue(self.game.play('1 3'))
        self.assertIn((1, 3), self.game.revealed)

    def test_d3_empty(self):
        # play returns True
        # the box is added to the list 'revealed'
        # surrounding empty boxes and first line of number boxes also added to revealed
        self.assertTrue(self.game.play('2 2'))
        for (a, b) in [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]:
            with self.subTest(pattern=(a, b)):
                self.assertIn((a, b), self.game.revealed)

    def test_e_flag(self):
        # play returns True
        # box is added to the list 'flagged'
        # if same box is flagged for the second time, undo the flagging proccess
        self.assertTrue(self.game.play('3 2 f'))
        self.assertIn((3, 2), self.game.flagged)
        self.assertTrue(self.game.play('3 2 f'))
        self.assertNotIn((3, 2), self.game.flagged)

    def test_f1_win_flag(self):
        self.assertTrue(self.game.play('0 0 f'))
        self.assertFalse(self.game.won())
        self.assertTrue(self.game.play('0 0 f'))
        self.assertTrue(self.game.play('0 2 f'))
        self.assertTrue(self.game.play('2 4 f'))
        self.assertTrue(self.game.play('4 1 f'))
        self.assertTrue(self.game.play('4 4 f'))
        self.assertTrue(self.game.won())

    def test_f2_win_open(self):

        self.game.play('0 0')
        self.game.play('0 4')
        self.game.play('3 4')
        self.game.play('4 0')
        self.game.play('4 2')
        self.game.play('4 3')
        self.assertTrue(self.game.won())

    def test_g_reveal(self):
        self.game.play('0 0 f')
        self.game.reveal_all()
        for i in range(self.game.size):
            for j in range(self.game.size):
                self.assertIn((i, j), self.game.revealed)

    def test_simple_run(self):
        MS.Minesweeper.run_game(self.moves)

    def test_h1_run_win(self):
        moves = ['2 4 f', '4 1 f', '4 4 f', '0 2 f', '3 4']
        MS.Minesweeper.run_game(moves)

    def test_h2_run_lose(self):
        moves = ['0 2']
        MS.Minesweeper.run_game(moves)
