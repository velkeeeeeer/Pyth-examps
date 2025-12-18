from ctypes import alignment
from fileinput import hook_encoded
import threading
from tkinter.tix import TEXT
from turtle import onclick
from FieldGen import displayField
import classField
import flet as ft
import numpy as np
import time


game = classField.SudokuGame()

def main(page: ft.Page):
    page.window.full_screen = False
    page.window.height = 900
    page.window.width = 540
    page.window.max_height = 900
    page.window.max_width = 540
    page.window.full_screen = False
    print(page.platform_brightness)
    def main_view():
        new_game_button = ft.FilledButton(text="Новая игра",
                                      color=ft.Colors.WHITE,
                                      on_click=lambda _: page.go("/loading"),
                                      width=150,
                                      height=90,
                                      )
        continue_game_button = ft.FilledButton(text="Продолжить",
                                      color=ft.Colors.WHITE,
                                      on_click=lambda _: page.go("/game"),
                                      width=150,
                                      height=90,
                                      disabled=not game.get_game_state()
                                      )
        
        header_text = ft.Text(value="Sudoku",
                              color=ft.Colors.WHITE if page.platform_brightness == ft.Brightness.DARK else ft.Colors.BLACK,
                              size=100,
                              text_align=ft.TextAlign.CENTER)

        view = ft.View(route='/',
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Container(content=header_text,
                                                     alignment=ft.alignment.center,
                                                     ),
                                        ft.Container(content=new_game_button,
                                                     alignment=ft.alignment.center,
                                                     ),
                                        ft.Container(content=continue_game_button,
                                                     alignment=ft.alignment.center,
                                                     ),
                                    ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,              
                                ),
                            ],
                       )
        return view

    def loading_view():
        view = ft.View(route="/loading")
        progress = ft.ProgressBar(width=400, color=ft.Colors.AMBER)
        view.controls.append(ft.Text("Загрузка...", size=30))
        view.controls.append(progress)
        def load_game_data():
            time.sleep(3)
            game.set_field_mask(np.load("C:\\Users\\Pobeda\\Desktop\\Pyth examps\\Sudoku\\Fields\\Level 2\\field.npy"), np.load("C:\\Users\\Pobeda\\Desktop\\Pyth examps\\Sudoku\\Fields\\Level 2\\mask.npy"))
            game.set_current_field()
            page.go("/game")
        threading.Thread(target=load_game_data, daemon=True).start()
        return(view)


    def game_view():        
        rows = []
        for row in range(9):
            cells = []
            for col in range(9):
                value = game.get_display_value(row, col)
                text = str(value) if value != 0 else ""
                is_default_value = game.get_mask_value(row, col)
                cell = ft.Container(
                        content=ft.Text(text, color=ft.Colors.BLACK, size=30),
                        bgcolor=ft.Colors.YELLOW if [row, col] == game.selected_cell and not is_default_value else ft.Colors.WHITE,
                        on_click=lambda e, row=row, col=col: select_cell(row, col), 
                        disabled=True if game.get_mask_value(row, col) else False,
                        width=50,
                        height=50,     
                        alignment=ft.alignment.center                    
                    )
                cells.append(cell)
            rows.append(ft.Row(cells, spacing=1, alignment=ft.MainAxisAlignment.CENTER, expand=True))
        board = ft.Column(rows, spacing=1)
        num_buttons = []
        for i in range(1, 10):
            num_buttons.append(ft.ElevatedButton(
                text = str(i),
                on_click=lambda e, val = i: fill_cell(np.uint8(val)),
                width=50,
                height=50
            ))
        keyboard_rows = [ft.Row(num_buttons[0:3], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
                         ft.Row(num_buttons[3:6], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
                         ft.Row(num_buttons[6:9], spacing=1, alignment=ft.MainAxisAlignment.CENTER),
                         ]
        num_board = ft.Column(keyboard_rows, spacing=1,)

        exit_button = ft.IconButton(icon=ft.Icons.EXIT_TO_APP,
                                on_click=lambda _: page.go("/"))

        view = ft.View(
            controls=[
                ft.Column(
                    [
                        ft.Container(content=board,
                            alignment=ft.alignment.center,
                                
                        ),
                        ft.Container(content=num_board,
                            alignment=ft.alignment.center,
                                
                        ),
                        ft.Container(content=exit_button,
                                     alignment=ft.alignment.top_right)
                    ],
                    expand = True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=30,
                    ), 
            ],
            route="/game",
        )
        return view
    def show_win_snack():
        def out():
            game.complete_game()
            page.go("/")

        snack = ft.SnackBar(
                content=ft.Text(value="Победа!", size=40),
                open = True,
                duration=10000,
                action="Выйти и отчистить поле",
                on_action=lambda _:out()
                )
        page.overlay.append(snack)
        page.update()

    def is_full():
            if np.array_equal(game.current_field, game.get_display_answer()):
                show_win_snack()

    def select_cell(row, col):
        if not game.get_mask_value(row, col):
            game.selected_cell = [row, col]
            route_change(None)

    def fill_cell(text):
        if game.selected_cell is not None:
            row, col = game.selected_cell
            if row != None and col != None and not game.get_mask_value(row, col):
                game.current_field[row, col] = text
                is_full()
                route_change(None)


        

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(main_view())
        elif page.route == "/game":
            page.views.append(game_view())
        elif page.route == "/loading":
            page.views.append(loading_view())
        page.update()
    page.on_route_change = route_change
    page.go("/")
    
ft.app(target=main)
