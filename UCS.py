import tkinter as tk
from tkinter import messagebox
import random
from collections import deque
class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("UCS")
        self.board = [""] * 9
        self.current_player = "X"
        self.buttons = [tk.Button(master, text="", font='Arial 20', width=5, height=2,
                                   command=lambda i=i: self.player_move(i)) for i in range(9)]
        for i, button in enumerate(self.buttons):
            button.grid(row=i // 3, column=i % 3)

    def player_move(self, index):
        if self.board[index] == "" and self.current_player == "X":
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            if self.check_winner("X"):
                messagebox.showinfo("Game Over", "You win!")
                self.reset_game()
            else:
                self.current_player = "O"
                self.computer_move()

    def computer_move(self):
        # Placeholder for your search algorithm
        index = self.get_computer_move()
        if index is not None:
            self.board[index] = "O"
            self.buttons[index].config(text="O")
            if self.check_winner("O"):
                messagebox.showinfo("Game Over", "Computer wins!")
                self.reset_game()
            else:
                self.current_player = "X"

    #<---------------------------UCS------------------------------>

    def get_computer_move(self):
        queue = deque()
        visited = set()
        available_moves = [i for i in range(9) if self.board[i] == ""]

        # First, check if O can win in the next move
        for move in available_moves:
            new_board = self.board[:]
            new_board[move] = "O"
            if self.check_winner_for_board("O", new_board):
                return move  # This move wins the game for O

        # Then, check if X can win in the next move and block it
        for move in available_moves:
            new_board = self.board[:]
            new_board[move] = "X"
            if self.check_winner_for_board("X", new_board):
                return move  # This move blocks X from winning
        
        # If no immediate win or block is needed, continue with UCS
        for move in available_moves:
            new_board = self.board[:]
            new_board[move] = "O"
            queue.append((new_board, move, 0))  # (board_state, initial_move, cost)


        while queue:
            current_state, initial_move, cost = queue.popleft()
            state_tuple = tuple(current_state)

            if state_tuple in visited:
                continue

            visited.add(state_tuple)

            # Check if this move leads to a win for O
            if self.check_winner_for_board("O", current_state):
                return initial_move

            # Generate next possible moves
            next_moves = [i for i in range(9) if current_state[i] == ""]
            for next_move in next_moves:
                new_state = current_state[:]
                new_state[next_move] = "X"  # Simulate player's move
                new_cost = cost + 1

                # Evaluate the board state
                if self.check_winner_for_board("X", new_state):
                    new_cost += 10  # Penalize states where X wins
                elif self.check_winner_for_board("O", new_state):
                    new_cost -= 10  # Favor states where O wins

                queue.append((new_state, initial_move, new_cost))

            # Sort the queue based on cost (UCS)
            queue = deque(sorted(queue, key=lambda x: x[2]))

        # If no strategic move found, return a random available move
        return random.choice(available_moves)

    # Add this new method to check for a winner on a given board state
    def check_winner_for_board(self, player, board):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        return any(all(board[i] == player for i in combo) for combo in winning_combinations)

    def check_winner(self, player):
        winning_combinations = [(0, 1, 2), (3, 4,  5), (6, 7, 8), #winning rows
                                (0, 3, 6), (1, 4, 7), (2, 5, 8), #winning columns
                                (0, 4, 8), (2, 4, 6)] #winning diagonals
        return any(all(self.board[i] == player for i in combo) for combo in winning_combinations)

    def reset_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="")
        self.current_player = "X"

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
