from typing import Type
from numpy.typing import NDArray
import numpy as np

class SudokuField:
    def __init__(self, field: NDArray[np.int64]) -> None:
        self.__field = field

    @classmethod
    def create_field(cls) -> NDArray[np.int64]:
        field = np.zeros((9,9), dtype=int)
        return field
    @classmethod
    def displayField(cls, field: NDArray[np.int64] | NDArray[np.bool]) -> None:
        """Отображение поля"""
        print(field)

    def getField(self) -> NDArray[np.int64]:
        """Возвращение объекта поля"""
        return self.__field
    
    def importField(self, filepath: str):
        """Импорт сгенерированного поля из файла"""
        self.__field = np.fromfile(filepath, dtype=np.int64)

    def makeMotion(self, x: int, y: int, choice: int) -> None:
        """Добавление в точку (x, y) выбранного числа"""
        try:
            self.__field[x, y] = choice
            return None
        except:
            if (x < 0 | x > 9 | y < 0 | y > 9):
                raise IndexError()
                return None
            elif (choice > 9 | choice < 0):
                raise ValueError()
                return None
            else:
                raise TypeError()
                return None