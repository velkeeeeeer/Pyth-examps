
from copy import deepcopy
from numpy.typing import NDArray
from FieldGen import create_field_and_mask
import numpy as np

class SudokuGame:
    def __init__(self) -> None:
        self.__field: NDArray[np.uint8] = np.zeros((9,9), dtype=np.uint8)
        self.__mask: NDArray[np.bool_] = np.zeros((9,9), dtype=np.bool_)
        self.current_field: NDArray[np.uint8] = np.zeros((9,9), dtype=np.uint8)
        self.selected_cell: list[None] | list[int] = [None, None]
        self.__is_active: bool = False
    def set_field_mask(self, field: NDArray[np.uint8], mask: NDArray[np.bool_]):
        self.__field = field
        self.__mask = mask
        self.set_current_field()
        self.__is_active = True
    def get_display_value(self, row: int, col: int) -> np.uint8:
        return self.current_field[row, col]
    def set_current_field(self):
        self.current_field = deepcopy(self.__field)
        self.current_field[~self.__mask] = 0
    def get_display_answer(self):
        return self.__field
    def has_answer(self):
        return bool(self.current_field.any())
    def complete_game(self):
        self.__is_active = False
    def get_mask_value(self, row: int, col: int):
        return self.__mask[row, col]
    def get_game_state(self):
        return self.__is_active
