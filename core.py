from dataclasses import dataclass
from enum import Enum
import random

from utils import get_logger


logger = get_logger()


class MoveResult(Enum):
    LOSE = -1
    CONTINUE = 0
    WIN = 1


@dataclass
class Cell:
    is_black_hole: bool = False
    adjacent_black_holes: int = 0
    is_open: bool = False

    def can_be_opened(self):
        return not self.is_black_hole and not self.is_open


class ProxxCore:
    def __init__(self, board_size: int, holes: int):
        self.board_size = board_size
        self.holes = holes
        self.board = self.__init_board(self.board_size, self.holes)

    def step(self, x: int, y: int) -> MoveResult:
        """
        Open cell by x-y coordinates. Game will be:
        - lost if player found black hole
        - win if opened all cells except black holes
        - otherwise -> continue

        :param x: x-coord
        :param y: y-coord
        :return: result of player's mov
        """

        if self.board[x][y].is_black_hole:
            logger.info('Black hole found, game over.')
            self.restart()
            return MoveResult.LOSE

        if self.board[x][y].is_open:
            logger.warning('Cell already opened')
            return MoveResult.CONTINUE

        self.board[x][y].is_open = True
        if self.board[x][y].adjacent_black_holes != 0:
            if self.__check_win_condition(self.board):
                return MoveResult.WIN

            return MoveResult.CONTINUE
        else:
            coordinate_limit = self.board_size - 1

            # left-top
            if x > 0 and y > 0 and self.board[x - 1][y - 1].can_be_opened():
                _ = self.step(x - 1, y - 1)

            # top
            if y > 0 and self.board[x][y - 1].can_be_opened():
                _ = self.step(x, y - 1)

            # right-top
            if x < coordinate_limit and y > 0 and self.board[x + 1][y - 1].can_be_opened():
                _ = self.step(x + 1, y - 1)

            # left
            if x > 0 and self.board[x - 1][y].can_be_opened():
                _ = self.step(x - 1, y)

            # right
            if x < coordinate_limit and self.board[x + 1][y].can_be_opened():
                _ = self.step(x + 1, y)

            # left-bottom
            if x > 0 and y < coordinate_limit and self.board[x - 1][y + 1].can_be_opened():
                _ = self.step(x - 1, y + 1)

            # bottom
            if y < coordinate_limit and self.board[x][y + 1].can_be_opened():
                _ = self.step(x, y + 1)

            # right-bottom
            if x < coordinate_limit and y < coordinate_limit and self.board[x + 1][y + 1].can_be_opened():
                _ = self.step(x + 1, y + 1)

        if self.__check_win_condition(self.board):
            return MoveResult.WIN

        return MoveResult.CONTINUE

    def restart(self):
        """
        Restart game with saved parameters
        """

        self.board = self.__init_board(self.board_size, self.holes)

    def __init_board(self, size: int, holes_count: int) -> list:
        board_coordinates = [(x, y) for x in range(0, size) for y in range(0, size)]
        holes_coordinates = random.sample(board_coordinates, holes_count)

        logger.info(f'Generating new board...\n'
                    f'Board size - {size}x{size}\n'
                    f'Black holes count - {holes_count}\n'
                    f'Black holes coordinates - {holes_coordinates}')

        board = []
        for i in range(size):
            line = []
            for j in range(size):
                cell = Cell()
                line.append(cell)

            board.append(line)

        for coordinates in holes_coordinates:
            board[coordinates[0]][coordinates[1]].is_black_hole = True

        board = self.__calculate_adjacent_black_holes(board)
        return board

    def __calculate_adjacent_black_holes(self, board: list) -> list:
        size = len(board)
        limit_index = size - 1
        for i in range(size):
            for j in range(size):
                # left-top
                if i > 0 and j > 0 and board[i - 1][j - 1].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # top
                if j > 0 and board[i][j - 1].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # right-top
                if i < limit_index and j > 0 and board[i + 1][j - 1].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # left
                if i > 0 and board[i - 1][j].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # right
                if i < limit_index and board[i + 1][j].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # left-bottom
                if i > 0 and j < limit_index and board[i - 1][j + 1].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # bottom
                if j < limit_index and board[i][j + 1].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

                # right-bottom
                if i < limit_index and j < limit_index and board[i + 1][j + 1].is_black_hole:
                    board[i][j].adjacent_black_holes += 1

        return board

    def __check_win_condition(self, board: list) -> bool:
        for line in board:
            for cell in line:
                if not cell.is_black_hole and not cell.is_open:
                    return False

        return True
