import random
import os
from datetime import datetime

def create_stats_directory():
    stats_dir = "game_stats"
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
    return stats_dir
def save_game_results(size, game_mode, first_player, result, board):
    stats_dir = create_stats_directory()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{stats_dir}/game_{timestamp}.txt"

    with open(filename, 'w', encoding = 'utf-8') as f:
        f.write(f"Размер поля: {size}\n")
        f.write(f"Режим игры: {"Игрок против игрока" if game_mode == 1 else "Игрок против Робота"}\n")
        f.write(f"Первый ход: {first_player}\n")
        f.write(f"Результат: {result}\n")
        f.write("Финальное поле после завершения игры:\n")
        f.write(board_to_string(board))

def get_valid_size():
    while True:
        try:
            size = int(input("Введите поля от 3 до 9"))
            if 3 <= size <= 9:
                return size
            else:
                print('Неверный размер поля')
        except ValueError:
            print('Неверный размер поля, введите новый')
def initialize_board(size):
    return [['.' for _ in range(size)] for _ in range(size)]

def choose_first_player():
    first_player = 'X' if random.choice([True, False]) else '0'
    print(f'Первым ходит: {first_player}')
    return first_player

def choose_game_mode():
    while True:
        try:
            print('Выбери режим игры')
            print('1 - Игрок против Игрока')
            print('2 - Игрок против Робота')
            mode = int(input('Выбор: '))
            if mode in [1,2]:
                return mode
            else:
                print('Неверный выбор')
        except ValueError:
            print('Введи корректные данные')

def board_to_string(board):
    size = len(board)
    result = " " + " ".join(str(i) for i in range(1, size + 1)) + "\n"
    for i in range(size):
        result += f"{i + 1}" + " ".join(board[i]) + "\n"
    return result


def print_board(board):
    print(board_to_string(board))

def is_valid_move(board, row, col):
    size = len(board)
    return (0 <= row < size and 0 <= col < size and board[row][col] == '.')

def get_player_move(board, current_player):
    while True:
        try:
            move = input('Введи ход')
            parts = move.split()
            row, col = int(parts[0]) - 1, int(parts[1]) - 1
            if is_valid_move(board, row, col):
                return row, col
            else:
                print("Неправильный ход")
        except ValueError:
            print("Введи корректные данные")

def get_ai_move(board):
    size = len(board)
    available_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == '.':
                available_moves.append((i,j))
    return random.choice(available_moves)

def check_winner(board, current_player):
    size = len(board)
    for i in range(size):
        if all(board[i][j] == current_player for j in range(size)):
            return True
    for j in range(size):
        if all(board[i][j] == current_player for i in range(size)):
            return True


    if all(board[i][i] == current_player for i in range(size)):
        return True
    if all(board[i][size - 1 - i] == current_player for i in range(size)):
        return True
    return False

def is_board_full(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == '.':
                return False
    return True
def make_move(board, row, col, current_player):
    board[row][col] = current_player

def switch_player(current_player):
    return 'O' if current_player == 'X' else 'X'


def play_game():
    game_mode = choose_game_mode()
    size = get_valid_size()
    board = initialize_board(size)
    current_player = choose_first_player()
    first_player = current_player
    while True:
        print_board(board)
        if current_player == 'O' and game_mode == 2:
            print('Робот делает ход')
            row, col = get_ai_move(board)
        else:

            row, col = get_player_move(board, current_player)
        make_move(board, row, col, current_player)

        if check_winner(board, current_player):
            print_board(board)
            save_game_results(size, game_mode, first_player, current_player, board)
            break
        if is_board_full(board):
            print_board(board)
            save_game_results(size, game_mode, first_player, "НИЧЬЯ", board)
            break
        current_player = switch_player(current_player)

def main():
    print("Начинается игра в крестики нолики!!!!!!!")
    while True:
        play_game()

if __name__ == "__main__":
    main()