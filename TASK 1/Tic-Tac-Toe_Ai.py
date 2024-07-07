import tkinter as tk
import math
import random

def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            return board[i][0], ((i, 0), (i, 2))
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            return board[0][i], ((0, i), (2, i))
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0], ((0, 0), (2, 2))
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2], ((0, 2), (2, 0))
    return None, None

def minimax(board, depth, is_maximizing, alpha, beta):
    winner, _ = check_winner(board)
    if winner == 'X':
        return -1
    if winner == 'O':
        return 1
    if all(cell != ' ' for row in board for cell in row):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

def best_move(board, difficulty):
    if difficulty == 'Easy':
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        return random.choice(available_moves) if available_moves else None
    elif difficulty == 'Medium':
        if random.random() < 0.5:
            available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
            return random.choice(available_moves) if available_moves else None
        else:
            return best_move(board, 'Hard')
    else:
        best_score = -math.inf
        move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, 0, False, -math.inf, math.inf)
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        move = (i, j)
        return move

def button_click(row, col):
    if board[row][col] == ' ' and not check_winner(board)[0]:
        board[row][col] = 'X'
        buttons[row][col].config(text='X', fg='red')
        winner, line = check_winner(board)
        if winner:
            result_label.config(text=f"{winner} wins!")
            draw_winning_line(line)
            animate_winner(winner)
        elif all(cell != ' ' for row in board for cell in row):
            result_label.config(text="It's a tie!")
        else:
            move = best_move(board, difficulty.get())
            if move:
                board[move[0]][move[1]] = 'O'
                buttons[move[0]][move[1]].config(text='O', fg='blue')
                winner, line = check_winner(board)
                if winner:
                    result_label.config(text=f"{winner} wins!")
                    draw_winning_line(line)
                    animate_winner(winner)
                elif all(cell != ' ' for row in board for cell in row):
                    result_label.config(text="It's a tie!")

def draw_winning_line(line):
    if line:
        start, end = line
        x1, y1 = start[1] * 100 + 48, start[0] * 100 + 48
        x2, y2 = end[1] * 100 + 48, end[0] * 100 + 48
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="line")

def animate_winner(winner):
    colors = ["red", "green", "blue", "yellow", "purple", "orange"]

    def change_color():
        color = colors.pop(0)
        colors.append(color)
        result_label.config(fg=color)
        root.after(250, change_color)

    change_color()

def reset_game():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text=' ', fg='black', bg='white')
    result_label.config(text="")
    canvas.delete("line")

def set_difficulty(level):
    difficulty.set(level)
    reset_game()
    update_difficulty_buttons()

def update_difficulty_buttons():
    easy_button.config(bg='lightgreen' if difficulty.get() == 'Easy' else 'white')
    medium_button.config(bg='yellow' if difficulty.get() == 'Medium' else 'white')
    hard_button.config(bg='red' if difficulty.get() == 'Hard' else 'white')

# Initialize the game board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Set up the Tkinter window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.geometry("320x500")
root.configure(bg='black')

buttons = [[None for _ in range(3)] for _ in range(3)]

# Canvas for drawing the winning line
canvas = tk.Canvas(root, width=300, height=300, bg='black', highlightthickness=0)
canvas.grid(row=1, column=0, rowspan=3, columnspan=3, padx=10, pady=10)

for row in range(3):
    for col in range(3):
        button = tk.Button(root, text=' ', font='Arial 15', width=5, height=2, fg='black', bg='white',
                           command=lambda row=row, col=col: button_click(row, col))
        button.grid(row=row+1, column=col, padx=10, pady=10)
        buttons[row][col] = button

result_label = tk.Label(root, text="", font='Arial 13', bg='black', fg='white')
result_label.grid(row=4, column=0, columnspan=3, pady=10)

difficulty = tk.StringVar(value='Medium')

easy_button = tk.Button(root, text="Easy", font='Arial 15', command=lambda: set_difficulty('Easy'))
easy_button.grid(row=0, column=0, padx=10, pady=10)

medium_button = tk.Button(root, text="Medium", font='Arial 15', command=lambda: set_difficulty('Medium'))
medium_button.grid(row=0, column=1, padx=10, pady=10)

hard_button = tk.Button(root, text="Hard", font='Arial 15', command=lambda: set_difficulty('Hard'))
hard_button.grid(row=0, column=2, padx=10, pady=10)

reset_button = tk.Button(root, text="Reset", font='Arial 15', command=reset_game)
reset_button.grid(row=5, column=0, columnspan=3, pady=10)

update_difficulty_buttons()

root.mainloop()
