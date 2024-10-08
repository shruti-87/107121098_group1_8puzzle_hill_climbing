# -*- coding: utf-8 -*-
"""8_puzzle_hill_climbing.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rlDJd_xA7oZdolW0VGdk91HzXm6lk3Fl
"""

import random

class Puzzle:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        self.size = int(len(initial) ** 0.5)

    def find_blank(self, state):
        #Find the index of the blank tile (represented by 0).
        return state.index(0)

    def manhattan_distance(self, state):
        #Calculate the Manhattan distance of the current state from the goal.
        distance = 0
        for i, tile in enumerate(state):
            if tile != 0:  # Don't count the blank tile
                goal_index = self.goal.index(tile)
                distance += abs(i // self.size - goal_index // self.size) + abs(i % self.size - goal_index % self.size)
        return distance

    def get_neighbors(self, state):
        #All valid neighbors of the current puzzle state.
        blank = self.find_blank(state)
        neighbors = []
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right moves
        for move in moves:
            x, y = divmod(blank, self.size)
            nx, ny = x + move[0], y + move[1]
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbor = state[:]
                swap_idx = nx * self.size + ny
                neighbor[blank], neighbor[swap_idx] = neighbor[swap_idx], neighbor[blank]
                neighbors.append(neighbor)
        return neighbors

# Random Restart Hill Climbing

class PuzzleWithRestart(Puzzle):
    def random_state(self):
        #Generate a random puzzle state.
        state = self.goal[:]
        random.shuffle(state)
        return state

    def random_restart_hill_climbing(self, max_restarts=100):
        for restart in range(max_restarts):
            current = self.random_state()
            initial_state = current[:]  # Store the initial random state
            while True:
                neighbors = self.get_neighbors(current)
                next_state = min(neighbors, key=lambda x: self.manhattan_distance(x))
                if self.manhattan_distance(next_state) >= self.manhattan_distance(current):
                    break  # Stuck at local optimum
                current = next_state
            if self.manhattan_distance(current) == 0:
                return initial_state, current  # Return the initial and goal state when found
        return None, None  # Failed to find solution after max_restarts

# First Choice Hill Climbing

class PuzzleWithFirstChoice(Puzzle):
    def first_choice_hill_climbing(self, max_attempts=100):
        current = self.initial[:]
        initial_state = current[:]  # Store the initial state
        attempts = 0
        while attempts < max_attempts:
            neighbors = self.get_neighbors(current)
            random.shuffle(neighbors)  # Shuffle the neighbors to make the search random
            for neighbor in neighbors:
                if self.manhattan_distance(neighbor) < self.manhattan_distance(current):
                    current = neighbor
                    attempts = 0  # Reset attempts as we made progress
                    break
            else:
                attempts += 1  # No progress made, increment attempts
        return initial_state, current if self.manhattan_distance(current) == 0 else None

initial_state = [1, 2, 5, 3, 4, 0, 6, 7, 8]
goal_state = [1, 4, 2, 3, 5, 0, 6, 7, 8]

# Random Restart Hill Climbing
puzzle_with_restart = PuzzleWithRestart(initial_state, goal_state)
initial, final = puzzle_with_restart.random_restart_hill_climbing(max_restarts=100)
print("Random Restart Hill Climbing Initial State:", initial)
print("Random Restart Hill Climbing Final State:", final)

# First Choice Hill Climbing
puzzle_with_first_choice = PuzzleWithFirstChoice(initial_state, goal_state)
initial, final = puzzle_with_first_choice.first_choice_hill_climbing(max_attempts=100)
print("First Choice Hill Climbing Initial State:", initial)
print("First Choice Hill Climbing Final State:", final)