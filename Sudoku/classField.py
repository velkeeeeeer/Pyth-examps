
from copy import deepcopy
from numpy.typing import NDArray
from FieldGen import create_field_and_mask
import numpy as np

class SudokuGame:
    def __init__(self) -> None:
        self.__field: NDArray[np.uint8] = np.zeros((9,9), dtype=np.uint8)
        self.__mask: NDArray[np.bool_] = np.zeros((9,9), dtype=np.bool_)
        self.current_field: NDArray[np.uint8]
        self.user_input = np.zeros((9,9), dtype=np.uint8)
        self.selected_cell = [None, None]
        self.choice = None
    def set_field_mask(self, field: NDArray[np.uint8], mask: NDArray[np.bool_]):
        self.__field = field
        self.__mask = mask
    def get_display_value(self, row: int, col: int) -> np.uint8:
        return self.current_field[row, col] or self.user_input[row, col]
    def set_user_input(self, row: int, col: int, value: np.uint8) -> None:
        if not self.user_input[row, col]:
            self.user_input[row, col] = value
    def set_current_field(self):
        self.current_field = deepcopy(self.__field)
        mask = ~self.__mask
        self.current_field[mask] = [0]
    def get_display_answer(self):
        return self.__field
    def get_mask_value(self, row: int, col: int):
        return self.__mask[row, col]
