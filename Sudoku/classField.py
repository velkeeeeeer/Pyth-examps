
from numpy.typing import NDArray
from FieldGen import create_field_and_mask
import numpy as np

class SudokuField:
    def __init__(self) -> None:
        self.__field : NDArray[np.int64] = np.zeros((9,9), dtype=np.int64)
        self.__mask : NDArray[np.bool_] = np.zeros((9,9), dtype=np.bool_)
    @staticmethod
    def displayField(field: NDArray[np.int64] | NDArray[np.bool_]) -> None:
        """Отображение поля"""
        print(field)
    @property
    def field(self) -> NDArray[np.int64]:
        """Возвращение объекта поля"""
        return self.__field.copy()
    
    def import_field_mask(self):
        """Импорт сгенерированного поля из файла"""
        print('Вход')
        self.__field, self.__mask = create_field_and_mask()
        print('Выход')

    def makeMotion(self, x: int, y: int, choice: int) -> None:
        """Добавление в точку (x, y) выбранного числа"""
        self.__field[x, y] = choice
        return None

field = SudokuField()
field.import_field_mask()
SudokuField.displayField(field.field)