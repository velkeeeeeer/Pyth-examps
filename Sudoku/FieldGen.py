from copy import deepcopy
import numpy as np
from numpy.typing import NDArray
import random
import os
import re
from pathlib import Path

def create_field() -> NDArray[np.uint8]:
        field = np.zeros((9,9), dtype=np.uint8)
        return field

def is_valid(field: NDArray[np.uint8], number: int, row: int, col: int) -> bool:
    """Правила заполнения игрового поля"""
    for cl in range(9):
        if field[row][cl] == number:
            return False
    for rw in range(9):
        if field[rw][col] == number:
            return False

    start_row: int = row - row % 3
    start_col: int = col - col % 3
    for rw in range(3):
        for cl in range(3):
            if field[start_row + rw, start_col + cl] == number:
                return False
    return True

def fill_field_by_backtrack(field: NDArray[np.uint8]):
    """Заполнение поля по правилам судоку игрового поля"""
    for row in range(0, 9):
        for col in range(0, 9):
            if field[row, col] == 0:
                numbers: list = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid(field, num, row, col):
                        field[row, col] = num
                        if fill_field_by_backtrack(field):
                            return True
                        field[row, col] = 0
                return False
    return True

def solutions_counter_by_backtrack(field: NDArray[np.uint8], cnter: list[int]) -> None:
    if cnter[0] >= 2:
        return
    for row in range(0, 9):
        for col in range(0, 9):
            if field[row][col] == 0:
                numbers: list = list(range(1, 10))
                for num in numbers:
                    if is_valid(field, num, row, col):
                        field[row, col] = num
                        solutions_counter_by_backtrack(deepcopy(field), cnter)
                        field[row, col] = 0
                        if cnter[0] >= 2:
                            return
                return
    cnter[0] += 1


#TODO Обновить алгоритм закрашивания клеток с проверкой на единственное решение.
#TODO Добавить уровни сложности игры.
def mask_random_cells(field: NDArray[np.uint8], HIDE_CELLS: int = 52) -> None:
    coords: list[tuple[int, int]] = [(i, k) for i in range(9) for k in range(9)]
    random.shuffle(coords)
    for x, y in coords[:HIDE_CELLS]:
        field[x,y] = 0


def get_field_mask(field: NDArray[np.uint8]) -> NDArray[np.bool_]:
    mask: NDArray[np.bool_] = field > 0
    return mask


def has_unique_solutions(field: NDArray[np.uint8]) -> bool:
    """Проверка количества решений у поля с замасированными ячейками"""
    new_field = deepcopy(field)
    counter: list[int] = [0]
    solutions_counter_by_backtrack(new_field, counter)
    return counter[0] == 1

# TODO Протащить код выбора уровня до маскировщика полей
def create_field_and_mask() -> tuple[NDArray[np.uint8], NDArray[np.bool_]]:
    """Функция создания игрового поля Судоку, возвращает кортеж из игрового поля и маски данного поля"""
    field: NDArray[np.uint8] = create_field()
    fill_field_by_backtrack(field)
    field_with_masked_cells: NDArray[np.uint8]
    field_mask: NDArray[np.bool_]
    while True:
        field_with_masked_cells = deepcopy(field)
        mask_random_cells(field_with_masked_cells)
        field_mask = get_field_mask(field_with_masked_cells)
        if has_unique_solutions(field_with_masked_cells):
            break
    return field, field_mask

def from_data_to_file(field: NDArray[np.uint8], field_mask: NDArray[np.bool_], filepath: str = os.getcwd() + "\\Sudoku\\Fields\\") -> None:
    Path(filepath).mkdir(parents=True, exist_ok=True)
    idx = []
    levels = os.listdir(filepath)
    for level in levels:
        match = re.match(r"Level\s(\d+)", level)
        if match:
            idx.append(int(match.group(1)))
    nxt_level = max(idx) + 1 if levels else 1
    new_dir = os.path.join(filepath, filepath + f"Level {nxt_level}")
    os.mkdir(new_dir)
    np.save(os.path.join(new_dir, "field.npy"), field)
    np.save(os.path.join(new_dir, "mask.npy"), field_mask)
    print("Уровень успешно сохранен!")
    return

def displayField(field: NDArray[np.uint8] | NDArray[np.bool_]) -> None:
        """Отображение поля"""
        print(field)
