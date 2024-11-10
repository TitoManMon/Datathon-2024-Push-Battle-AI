import random
import numpy as np
from PushBattle import Game, PLAYER1, PLAYER2, EMPTY, BOARD_SIZE, NUM_PIECES, _torus, chess_notation_to_array
from training_data import Data
'''
This is a sample implementation of an agent that just plays a random valid move every turn.
I would not recommend using this lol, but you are welcome to use functions and the structure of this.
'''

class Darwin:
    WEIGHT_possible_positions = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

    def __init__(self, player=PLAYER1):
        self.player = player
        self.WEIGHT_possible_positions = [[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
    def get_possible_moves(self, game):
        """Returns list of all possible moves in current state."""
        moves = []
        current_pieces = game.p1_pieces if game.current_player == PLAYER1 else game.p2_pieces
        
        if current_pieces < NUM_PIECES:
            # placement moves
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == EMPTY:
                        moves.append((r, c))
        else:
            # movement moves
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == game.current_player:
                        for r1 in range(BOARD_SIZE):
                            for c1 in range(BOARD_SIZE):
                                if game.board[r1][c1] == EMPTY:
                                    moves.append((r0, c0, r1, c1))
        return moves
    
    def assign_board(self,game):
        for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if game.board[r][c] == 0:
                        self.WEIGHT_possible_positions[r][c] = 1
                    else:
                        self.WEIGHT_possible_positions[r][c] = 0
    def assign_AW(self,game, NA, index):
        possible_moves = self.get_possible_moves(game)
        for move in possible_moves:
            for x in range (-1,1):
                for y in range(-1,1):
                    if(x==0==y):
                        continue
                    if(self.WEIGHT_possible_positions[move[0]+x][move[1]+y] == 1):
                        self.WEIGHT_possible_positions[move[0]][move[1]] += NA[index] * self.WEIGHT_possible_positions[move[0]][move[1]]

    def assign_EW(self,game, NE, index):
        possible_moves = self.get_possible_moves(game)
        for move in possible_moves:
            for x in range (-1,1):
                for y in range(-1,1):
                    if(x==0==y):
                        continue
                    if(self.WEIGHT_possible_positions[move[0]+x][move[1]+y] == -1):
                        self.WEIGHT_possible_positions[move[0]][move[1]] += NE[index] * self.WEIGHT_possible_positions[move[0]][move[1]]
    
    def assign_VIBE(self,game, VIBE,location, index):
        for x in range(BOARD_SIZE):
            self.WEIGHT_possible_positions[x][location[index]] *= VIBE[index]


    # given the game state, gets all of the possible moves
    def find_max_value(self, matrix):
        max_value = float('-inf')
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > max_value:
                    max_value = matrix[i][j]
        return max_value
    
    def find_coordinates(self, matrix, target):
        coordinates = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == target:
                    coordinates.append((i, j))
        return coordinates
    
    def find_max_position(self, matrix):
        max_value = self.find_max_value(matrix)
        coordinates = self.find_coordinates(matrix, max_value)
        return random.choice(coordinates)
    
    def get_best_move(self, game, index, NA, NE, VIBE, LOCATION):
        """Returns a random valid move."""
        
        self.assign_board(game)
        self.assign_AW(game, NA, index)
        self.assign_EW(game, NE, index)
        #self.assign_VIBE(game, VIBE,LOCATION, index)
        move = self.find_max_position(self.WEIGHT_possible_positions)

        if(game.p1_pieces >= 8):
            for r0 in range(BOARD_SIZE):
                for c0 in range(BOARD_SIZE):
                    if game.board[r0][c0] == game.current_player:
                        move = (r0,c0,move[0],move[1])

        print("BOARD:::: ", self.WEIGHT_possible_positions)
        print("MOVE=======================================================",move)
        return move
    

