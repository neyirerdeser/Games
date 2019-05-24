import random


class Minesweeper:
    revealed = []
    flagged = []
    board = []
    level = None
    size = None
    mines = None

    def __init__(self, level):
        self.revealed.clear()
        self.flagged.clear()
        self.board = []
        self.level = level
        self.size = self.set_level()[0]
        self.mines = self.set_level()[1]
        self.put_mines()
        self.put_numbers()

    def set_level(self):
        if self.level == 1:
            return tuple((8, 10))
        if self.level == 2:
            return tuple((16, 40))
        if self.level == 3:
            return tuple((24, 99))

    def put_mines(self):
        mine_rows = []
        mine_cols = []

        for i in range(self.mines):
            mine_rows.append(random.randint(0, self.size - 1))
            valid = False
            c = 0
            while not valid:
                valid = True
                c = random.randint(0, self.size - 1)
                for j in range(len(mine_rows) - 1):
                    if mine_rows[j] == mine_rows[i] and mine_cols[j] == c:
                        valid = False

            mine_cols.append(c)

        mined = [[0] * self.size for _ in range(self.size)]
        for i in range(self.mines):
            mined[mine_rows[i]][mine_cols[i]] = 9  # max number written on board can be 8, so 9 is a mine
        self.board.extend(mined)

    def put_numbers(self):
        for i in range(self.size):
            for j in range(self.size):
                location_keys = self.location_checks(i, j)
                if self.board[i][j] != 9:
                    self.check_increase(location_keys, i, j)

    def location_checks(self, i, j):
        # corners: A C G I
        # borders: B D F H
        end = self.size - 1
        if i == 0:
            if j == 0:
                return [5, 7, 8]  # A
            elif j == end:
                return [4, 6, 7]  # C
            else:
                return [4, 5, 6, 7, 8]  # B
        elif i == end:
            if j == 0:
                return [2, 3, 5]  # G
            elif j == end:
                return [1, 2, 4]  # I
            else:
                return [1, 2, 3, 4, 5]  # H
        elif j == 0:
            return [2, 3, 5, 7, 8]  # D
        elif j == end:
            return [1, 2, 4, 6, 7]  # F
        else:
            return [1, 2, 3, 4, 5, 6, 7, 8]  # E

    def check_increase(self, a, i, j):
        if 1 in a and self.board[i - 1][j - 1] == 9:
            self.board[i][j] += 1
        if 2 in a and self.board[i - 1][j] == 9:
            self.board[i][j] += 1
        if 3 in a and self.board[i - 1][j + 1] == 9:
            self.board[i][j] += 1
        if 4 in a and self.board[i][j - 1] == 9:
            self.board[i][j] += 1
        if 5 in a and self.board[i][j + 1] == 9:
            self.board[i][j] += 1
        if 6 in a and self.board[i + 1][j - 1] == 9:
            self.board[i][j] += 1
        if 7 in a and self.board[i + 1][j] == 9:
            self.board[i][j] += 1
        if 8 in a and self.board[i + 1][j + 1] == 9:
            self.board[i][j] += 1

    def flag(self, i, j):
        if (i, j) not in self.flagged:
            self.flagged.append((i, j))
        else:
            self.flagged.remove((i, j))

    def reveal(self, i, j):
        self.revealed.append((i, j))
        if self.board[i][j] == 0:
            a = self.location_checks(i, j)
            if 1 in a and (i - 1, j - 1) not in (self.revealed or self.flagged):
                self.reveal(i - 1, j - 1)
            if 2 in a and (i - 1, j) not in (self.revealed or self.flagged):
                self.reveal(i - 1, j)
            if 3 in a and (i - 1, j + 1) not in (self.revealed or self.flagged):
                self.reveal(i - 1, j + 1)
            if 4 in a and (i, j - 1) not in (self.revealed or self.flagged):
                self.reveal(i, j - 1)
            if 5 in a and (i, j + 1) not in (self.revealed or self.flagged):
                self.reveal(i, j + 1)
            if 6 in a and (i + 1, j - 1) not in (self.revealed or self.flagged):
                self.reveal(i + 1, j - 1)
            if 7 in a and (i + 1, j) not in (self.revealed or self.flagged):
                self.reveal(i + 1, j)
            if 8 in a and (i + 1, j + 1) not in (self.revealed or self.flagged):
                self.reveal(i + 1, j + 1)

    def reveal_all(self):
        for (a, b) in self.flagged:
            if self.board[a][b] != 9:
                self.flagged.remove((a, b))
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in self.flagged:
                    self.reveal(i, j)

    def play(self, move=None):
        i, j, key = self.make_move(move)
        if key == 'open':
            self.reveal(i, j)
            if self.board[i][j] == 9:
                return False
        if key == 'flag':
            self.flag(i, j)
        return True

    def make_move(self, move):
        if move is None:
            print('to open follow format <row> <column>\n'
                  'to flag/unflag follow <row> <column> f')
            click = input().split()
            while not self.valid_click(click):
                click = input().split()
        else:
            click = move.split()
        return self.valid_click(click)

    def valid_click(self, click):
        end = self.size - 1
        digits = len(click)
        if digits not in (2, 3):
            print('please give two numbers separated by space to enter coordinates')
            return False
        try:
            r = int(click[0])
            c = int(click[1])
        except (TypeError, ValueError):
            print('both coordinates must be integers')
            return False
        if r > end or r < 0 or c > end or r < 0:
            print('location outside the game, careful first box is 0 0. ')
            return False
        if (r, c) in self.revealed:
            print('box already open')
            return False
        if digits == 2:
            mode = 'open'
            if (r, c) in self.flagged:
                print('box is flagged, to unflag type %d %d f' % (r, c))
                return False
        elif click[2] == 'f':
            mode = 'flag'
        else:
            print('to (un)flag type f after the coordinates')
            return False

        return r, c, mode

    def print_game(self):
        def horizontal(length):
            print()
            print('--+-', end='')
            for l in range(length):
                print('----', end='')
            print()

        print('  | ', end='')
        for i in range(self.size):
            print(i % 10, end='   ')
        horizontal(self.size)
        for i in range(self.size):
            print(i % 10, '| ', end='')
            for j in range(self.size):
                char = ' '
                if (i, j) in self.revealed:
                    if self.board[i][j] == 9:
                        char = 'X'
                    elif self.board[i][j] == 0:
                        char = '.'
                    else:
                        char = self.board[i][j]
                elif (i, j) in self.flagged:
                    char = 'f'
                print(char, end=' | ')
            horizontal(self.size)
        print('mines left:', self.mines - len(self.flagged))

    @classmethod
    def intro(cls):
        print('Welcome to minesweeper\n'
              'some notes for after you choose the level you want to play\n'
              '* to open a box, you will enter your coordinates in the format:'
              ' <row> <column> of your desired number (eg. 2 5)\n'
              '* to (un)flag a box put an 'f' at the end of your coordinates (eg. 4 3 f)\n'
              '* game ends when all unopened or flagged boxes are mines\n'
              '* empty boxes are shown with a . in them for convenience\n'
              '* keep in mind that the upper left corner has coordinates 0 0\n'
              '  and that numbers on the side repeat for each 10 rows/column,'
              ' you should type the real number that would be there\n'
              'lets start :)\n')

    @classmethod
    def get_level(cls):
        print('level of difficulty:\n'
              '1. Beginner\n2. Intermediate\n3. Expert\nYour choice: ')
        level = 0
        valid = False
        while not valid:
            try:
                level = int(input())
            except (TypeError, ValueError):
                print('level must be a number')
                continue
            if level not in (1, 2, 3):
                print('invalid answer entered')
            else:
                valid = True
        return level

    def lost(self):
        mines_left = self.mines - len(self.flagged)
        self.reveal_all()
        self.print_game()
        print('GAME OVER\nmines exploded: %d\nplay again? (Y/N)' % mines_left)

    def won(self):
        for (a, b) in self.flagged:
            if self.board[a][b] != 9:
                return False
        print('CONGRATULATIONS\nplay again? (Y/N)')
        return True

    @classmethod
    def run_with_moves_list(cls, moves):
        turn = 0
        level = 1
        game = Minesweeper(level)
        game.print_game()
        while game.play(moves[turn]):
            game.print_game()
            mines_left = game.mines - len(game.flagged)
            hidden = game.size ** 2 - len(game.revealed) - len(game.flagged)
            if (mines_left == 0 or hidden == mines_left) and game.won():
                break
            turn += 1
            if turn >= len(moves):
                print('end of scenario')
                break
        else:
            game.print_game()
            game.lost()

    @classmethod
    def run_with_user_input(cls):
        playing = True
        while playing:
            level = cls.get_level()
            game = Minesweeper(level)
            game.print_game()
            while game.play():
                game.print_game()
                mines_left = game.mines - len(game.flagged)
                hidden = game.size ** 2 - len(game.revealed) - len(game.flagged)
                if (mines_left == 0 or hidden == mines_left) and game.won():
                    break
            else:
                game.print_game()
                game.lost()
            valid = False
            while not valid:
                answer = input()
                if answer not in ('Y', 'N', 'y', 'n'):
                    print('invalid answer entered\ndo you want to play again? (Y/N)')
                elif answer in ('N', 'n'):
                    print('bye')
                    playing = False
                    valid = True
                else:
                    valid = True

    @classmethod
    def run_game(cls, moves=None):
        if moves:
            cls.run_with_moves_list(moves)
            return
        cls.run_with_user_input()


if __name__ == '__main__':
    Minesweeper.intro()
    moves = ['2 2 f', '2 4']
    # Minesweeper.run_game(moves)
    Minesweeper.run_game()
