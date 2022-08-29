import re
from core import ProxxCore, MoveResult


DEBUG = True


class ConsoleGameProxx:
    def __init__(self, board_size: int, holes: int):
        self.board_size = board_size
        self.holes = holes
        self.numbers_pattern = "^\\d+$"

    def play(self):
        proxx = ProxxCore(self.board_size, self.holes)

        print('\nLegend:\n'
              '# - closed cell\n'
              'H - black hole\n'
              '0-8 - number of adjacent black holes')
        print('Left-top cell has 0/0 coordinates\n'
              'Right-bottom cell has board_size-1 coordinates respectively')
        print('\n\n0_______________________________________ board_size - 1\n'
              '|                 y\n'
              '|\n'
              '|\n'
              '|\n'
              '| x\n'
              '|\n'
              '|\n'
              '|\n'
              '|\n'
              'board_size - 1\n\n')

        if DEBUG:
            print('Current board (debug mode):')
            self.__print_board(proxx.board)

        while True:
            try:
                x, y = self.__input(self.board_size)
            except ValueError as e:
                print(f'{e}. Please try again.')
                continue

            result = proxx.step(x, y)

            if result == MoveResult.CONTINUE:
                self.__print_board(proxx.board, only_opened=True)
            else:
                self.__print_board(proxx.board)
                print(result.name)

                print("Press 'y' if you want to restart. If you want to quit press any other button.")
                restart = input()
                if restart == 'y':
                    proxx.restart()
                    if DEBUG:
                        print('Current board (debug mode):')
                        self.__print_board(proxx.board)
                else:
                    break

    def __print_board(self, board, only_opened=False):
        for line in board:
            line_visualization_msg = ''
            for cell in line:
                if only_opened:
                    if not cell.is_open:
                        line_visualization_msg += '# '
                    else:
                        line_visualization_msg += str(cell.adjacent_black_holes) + ' '
                else:
                    if cell.is_black_hole:
                        line_visualization_msg += 'H '
                    else:
                        line_visualization_msg += str(cell.adjacent_black_holes) + ' '

            print(line_visualization_msg)

    def __input(self, board_size: int) -> tuple:
        print('Select x: ')
        x = re.match(self.numbers_pattern, input())

        if x is None or int(x.group(0)) >= board_size:
            raise ValueError('Incorrect input')

        print('Select y: ')
        y = re.match(self.numbers_pattern, input())

        if y is None or int(y.group(0)) >= board_size:
            raise ValueError('Incorrect input')

        return int(x.group(0)), int(y.group(0))


if __name__ == '__main__':
    game = ConsoleGameProxx(7, 5)
    game.play()
