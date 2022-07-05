# Author: Devon Miller
# Date: 8/5/2021
# Description: A class containing the game quoridor. The game is played on an 8X8 board
#              with 2 players. The pawn starts at the players baseline and the game is
#              won by getting the pawn across to the other baseline. During a turn a player
#              may either move the pawn or place a fence between spaces. There are detailed
#              rules allowing jumping and diagonal moves when pawns are touching. The game
#              board and characteristics of players are stored in private data members. One class
#              is used and multiple methods are used in each move made.

import copy

class QuoridorGame:
    """a class containing the board, validation of moves and fences
    stores which players turn it is and updates a winner"""
    def __init__(self):
        """board represented as list of lists with extra spaces added between
        each usable space to add fences, pawns can occupy 0's and fences can
        occupy 1's, other private data members store player info"""
        self._board = [[0, 1, 0, 1, 0, 1, 0, 1, "player_1", 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      [0, 1, 0, 1, 0, 1, 0, 1, "player_2", 1, 0, 1, 0, 1, 0, 1, 0]]

        self._game_state = "unfinished"
        self._player_1_fences = 11
        self._player_2_fences = 11
        self._turn = "player_1"
        self._player_1_position = [0, 8]                      # player 1 current position
        self._player_2_position = [16, 8]                     # player 2 current position


    def move_pawn(self, player, new_space):
        """performs initial validation of pawn move
        and sends to a method based on the player"""
        if new_space[1] < 0 or new_space[0] < 0:          # move is in range
            return False
        if new_space[1] > 8 or new_space[0] > 8:          # move is in range
            return False
        if self._game_state != "unfinished":              # correct turn
            return False
        if player == 1 and self._turn == "player_2":      # correct turn
            return False
        if player == 2 and self._turn == "player_1":
            return False
        row = new_space[1] + new_space[1]                # converted row to be used
        column = new_space[0] + new_space[0]             # converted column to be used
        if self._board[row][column] != 0:
            return False
        if player == 1:
            return self.player_1_move(row, column)      # send to method for player 1
        if player == 2:
            return self.player_2_move(row,column)       # send to method for player 2


    def player_1_move(self, row, column):
        """gets current position of player 1 and checks
        if pawns are touching, sends to method, try/except
        used to deal with index errors"""
        current_row = self._player_1_position[0]
        current_column = self._player_1_position[1]
        try:                                    # try and except used to handle index range error
            if self._board[current_row][current_column - 2] == "player_2":
                if column < current_column:
                    return self.player_1_move_left(row, column, current_row, current_column)
        except:
            pass
        try:              # is player 2 on space right of player 1
            if self._board[current_row][current_column + 2] == "player_2":
                if column > current_column:
                    return self.player_1_move_right(row, column, current_row_current_column)
        except:
            pass
        try:             # is player 2 above player 1
            if self._board[current_row - 2][current_column] == "player_2":
                if row < current_row:
                    return self.player_1_move_up(row, column, current_row, current_column)
        except:
            pass
        try:            # is player 2 below player 1
            if self._board[current_row + 2][current_column] == "player_2":
                if row > current_row:
                    return self.player_1_move_down(row, column, current_row, current_column)
        except:
            pass
        return self.player_1_normal_move(row, column, current_row, current_column)


    def player_1_move_left(self, row, column, current_row, current_column):
        """called when player 2 pawn is idediatly left of player1, allows for
        jumping and diagonal moves when permitted"""
        if row == current_row and column == current_column - 4:    # can a jump be made
            if self._board[current_row][current_column - 1] == 1 and \
                    self._board[current_row][current_column - 3] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column - 2:  # cand diagonal move be made
            if self._board[current_row][current_column - 1] == 1 and \
                    self._board[current_row][current_column - 3] == "fence":
                if self._board[current_row - 1][current_column - 2] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
                else:
                    return False
        if row == current_row + 2 and column == current_column - 2:   # diagonal move
            if self._board[current_row][current_column - 1] == 1 and \
                    self._board[current_row][current_column - 3] == "fence":
                if self._board[current_row + 1][current_column - 2] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
                else:
                    return False


    def player_1_move_right(self, row, column, current_row, current_column):
        """called when player 2 is directly right of player 1, allows
        jumping and diagonal moves when applicable"""
        if row == current_row and column == current_column + 4:  # jump if applicable
            if self._board[current_row][current_column + 1] == 1 and \
                    self._board[current_row][current_column + 3] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row + 2 and column == current_column + 2:  # diagonal if allowed
            if self._board[current_row][current_column + 1] == 1 and \
                    self._board[current_row][current_column + 3] == "fence":
                if self._board[current_row + 1][current_column + 2] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column + 2:    # diagonal if allowed
            if self._board[current_row][current_column + 1] == 1 and \
                    self._board[current_row][current_column + 3] == "fence":
                if self._board[current_row - 1][current_column + 2] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False


    def player_1_move_up(self, row, column, current_row, current_column):
        """called when player 2 space above player 1, allows jumping and
        diagonal moves when applicable"""
        if row == current_row - 4 and column == current_column:    # can jump be made
            if self._board[current_row - 1][current_column] == 1 and \
                    self._board[current_row - 3][current_column] == 1:

                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column + 2:    # diagonal move when allowed
            if self._board[current_row - 1][current_column] == 1 and \
                    self._board[current_row - 3][current_column] == "fence":
                if self._board[current_row - 2][current_column + 1] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
                # upper right diagonal
        if row == current_row - 2 and column == current_column - 2:   # diagonal move when allowed
            if self._board[current_row][current_column + 1] == 1 and \
                    self._board[current_row][current_column + 3] == "fence":
                if self._board[current_row - 2][current_column - 1] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False


    def player_1_move_down(self, row, column, current_row, current_column):
        """called when player 2 space below player 1, allows jumping and
        diagonal moves when applicable"""
        if row == current_row + 4 and column == current_column:    # jump when allowed
            if self._board[current_row + 1][current_column] == 1 and \
                    self._board[current_row + 3][current_column] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row + 2 and column == current_column + 2:  # diagonal when allowed
            if self._board[current_row + 1][current_column] == 1 and \
                    self._board[current_row + 3][current_column] == "fence":
                if self._board[current_row + 2][current_column + 1] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False

        if row == current_row + 2 and column == current_column - 2:   # diagonal when allowed
            if self._board[current_row + 1][current_column] == 1 and \
                    self._board[current_row + 3][current_column] == "fence":
                if self._board[current_row + 2][current_column - 1] == 1:
                    return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False


    def player_1_normal_move(self, row, column, current_row, current_column):
        """called for all valid moves where pawns are not touching, validates
        move and sends to update result"""
        try:                          # player may only move one space
            if self._board[row + 2][column] != "player_1" and \
                self._board[row - 2][column] != "player_1" and \
                self._board[row][column - 2] != "player_1" and \
                self._board[row][column + 2] != "player_1":
                return False
        except:
            pass
        if column < current_column:       # move left
            if self._board[row][column + 1] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if column > current_column:     # move right
            if self._board[row][column - 1] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row > current_row:           # move down
            if self._board[row - 1][column] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False
        if row < current_row:          # move up
            if self._board[row + 1][column] == 1:
                return self.update_player1_move(row, column, current_row, current_column)
            else:
                return False


    def update_player1_move(self,row, column, current_row, current_column):
        """updates game board, current move, checks for winner"""
        self._board[row][column] = "player_1"           # player 1 moved to new space
        self._board[current_row][current_column] = 0    # old space set to 0
        self._player_1_position = [row, column]         # current position reset
        self._turn = "player_2"
        if "player_1" in self._board[16]:               # check if player 1 won
            self._game_state = "player1 wins"
        return True


    def player_2_move(self, row, column):
        """called for player 2 moves and calls different
        method depending on whether or not the pawns are touching
        try/except used to handle index out of range"""
        current_row = self._player_2_position[0]
        current_column = self._player_2_position[1]
        try:               # is player 1 left of player 2
            if self._board[current_row][current_column - 2] == "player_1":
                if column < current_column:
                    return self.player_2_move_left(self, row, column, current_row, current_column)
        except:
            pass
        try:              # is player 1 right of player 2
            if self._board[current_row][current_column + 2] == "player_1":
                if column > current_column:
                    return self.player_2_move_right(row, column, current_row, current_column)
        except:
            pass
        try:            # is player 1 above player 2
            if self._board[current_row - 2][current_column] == "player_1":
                if row < current_row:
                    self.player_2_move_up(row, column, current_row, current_column)
        except:
            pass
        try:          # is player 1 below player 2
            if self._board[current_row + 2][current_column] == "player_1":
                if row > current_row:
                    return self.player_2_move_down(row, column, current_row, current_column)
        except:
            pass
        return self.player_2_normal_move(row, column, current_row, current_column)


    def player_2_move_left(self, row, column, current_row, current_column):
        """when player 1 pawn is left of player 2 this method allows jujping
        and diagonal moves when applicable"""
        if row == current_row and column == current_column - 4:   # jump when allowed
            if self._board[current_row][current_column - 1] == 1 and \
                    self._board[current_row][current_column - 3] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column - 2:   # diagonal when allowed
            if self._board[current_row][current_column - 1] == 1 and \
                    self._board[current_row][current_column - 3] == "fence":
                if self._board[current_row - 1][current_column - 2] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
                else:
                    return False
        if row == current_row + 2 and column == current_column - 2:   # diagonal when allowed
            if self._board[current_row][current_column - 1] == 1 and \
                    self._board[current_row][current_column - 3] == "fence":
                if self._board[current_row + 1][current_column - 2] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
                else:
                    return False


    def player_2_move_right(self, row, column, current_row, current_column):
        """called when player 1 is right of player 2, allows jumping and diagonal
        moves when applicable"""
        if row == current_row and column == current_column + 4:   # jump when allowed
            if self._board[current_row][current_column + 1] == 1 and \
                self._board[current_row][current_column + 3] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row + 2 and column == current_column + 2:   # diagonal when allowed
            if self._board[current_row][current_column + 1] == 1 and \
                self._board[current_row][current_column + 3] == "fence":
                if self._board[current_row + 1][current_column + 2] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column + 2:   # diagonal when allowed
            if self._board[current_row][current_column + 1] == 1 and \
                    self._board[current_row][current_column + 3] == "fence":
                if self._board[current_row - 1][current_column + 2] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False


    def player_2_move_up(self, row, column, current_row, current_column):
        """called when player 1 is above player 2, allows jumping and diagonal
        moves when applicable"""
        if row == current_row - 4 and column == current_column:   # jump when allowed
            if self._board[current_row - 1][current_column] == 1 and \
                self._board[current_row - 3][current_column] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column + 2:   # diagonal when allowed
            if self._board[current_row - 1][current_column] == 1 and \
                self._board[current_row - 3][current_column] == "fence":
                if self._board[current_row - 2][current_column + 1] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row - 2 and column == current_column - 2:  # diagonal when allowed
            if self._board[current_row][current_column + 1] == 1 and \
                    self._board[current_row][current_column + 3] == "fence":
                if self._board[current_row - 2][current_column - 1] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False


    def player_2_move_down(self, row, column, current_row, current_column):
        """called when player 1 is below player 2, allows jumping and diagonal
        moves when applicable"""
        if row == current_row + 4 and column == current_column:       # jump when allowed
            if self._board[current_row + 1][current_column] == 1 and \
                self._board[current_row + 3][current_column] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row == current_row + 2 and column == current_column + 2:  # diagonal when allowed
            if self._board[current_row + 1][current_column] == 1 and \
                self._board[current_row + 3][current_column] == "fence":
                if self._board[current_row + 2][current_column + 1] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False

        if row == current_row + 2 and column == current_column - 2:  # diagonal when allowed
            if self._board[current_row + 1][current_column] == 1 and \
                    self._board[current_row + 3][current_column] == "fence":
                if self._board[current_row + 2][current_column - 1] == 1:
                    return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False


    def player_2_normal_move(self, row, column, current_row, current_column):
        """used for all player 2 moves where pawns are not touching
        validates and sents to update results"""
        try:           # may only move one space at a time
            if self._board[row + 2][column] != "player_2" and \
                self._board[row - 2][column] != "player_2" and \
                self._board[row][column - 2] != "player_2" and \
                self._board[row][column + 2] != "player_2":
                return False
        except:
            pass
        if column < current_column:              # move left
            if self._board[row][column + 1] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if column > current_column:             # move right
            if self._board[row][column - 1] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row > current_row:                # move down
            if self._board[row - 1][column] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False
        if row < current_row:              # move up
            if self._board[row + 1][column] == 1:
                return self.update_player2_move(row, column, current_row, current_column)
            else:
                return False


    def update_player2_move(self, row, column, current_row,current_column):
        """updates game board current turn and checks if player 2 won"""
        self._board[current_row][current_column] = 0   # sets ond player 2 position to 0
        self._board[row][column] = "player_2"          # sets new player 2 space
        self._player_2_position = [row, column]        # sets new player 2 position
        self._turn = "player_1"
        if "player_2" in self._board[0]:               # check if player 2 won
            self._game_state = "player2 wins"
        return True


    def place_fence(self, player, direction, position):
        """does initial validation and sends to method to create
        temporary board"""
        if position[1] < 0 or position[0] < 0:     # validate range
            return False
        if position[1] > 8 or position[0] > 8:     # validate range
            return False
        if direction == "v" and position[0] == 0:  # fence may not be along edge
            return False
        if direction == "h" and position[1] == 0:  # fence may not be along edge
            return False
        if player == 1 and self._turn == "player_2":  # correct turn
            return False
        if player == 2 and self._turn == "player_1":  # correct turn
            return False
        if self._game_state != "unfinished":     # game not won yet
            return False
        row = position[1] + position[1] -1      # converts row to be used in method
        column = position[0] + position[0] -1   # converts column to be used in method
        if player == 1:
            if self._player_1_fences == 0:        # player 1 has fences left
                return False
            return self.add_p1_temp_fence(player, direction, position)
        if player == 2:
            if self._player_2_fences == 0:       # player 2 has fences left
                return False
            return self.add_p1_temp_fence(player, direction, position)


    def add_p1_temp_fence(self, player, direction, position):
        """creates temporary board to be used in fairplay validation by
        player 1, sends to fairplay rules method"""
        temp_board = copy.deepcopy(self._board)     # deep copy of game board
        row = position[1]*2
        column = position[0]*2
        if direction == "v":
            if column != 0:
                if temp_board[row][column-1] == 1:     # adds fence to temporary board
                    temp_board[row][column-1] = "fence"
                else:
                    return False
        if direction == "h":
            if row != 0:
                if temp_board[row-1][column] == 1:     # adds fence to temp board
                    temp_board[row-1][column] = "fence"
                else:
                    return False
        return self.check_fair_play_1(player, direction, position, temp_board)


    def add_p2_temp_fence(self, player, direction, position):
        """creates a temporary board for player 2 to be used in fairplay
        validation"""
        temp_board = copy.deepcopy(self._board)     # deep copy of game board
        row = position[1]*2
        column = position[0]*2
        if direction == "v":
            if column != 0:
                if temp_board[row][column-1] == 1:   # adds fence to temp board
                    temp_board[row][column-1] = "fence"
                else:
                    return False
        if direction == "h":
            if row != 0:
                if temp_board[row][column-1] == 1:   # adds fence to temp board
                    temp_board[row][column-1] = "fence"
                else:
                    return False
        return self.check_fair_play_2(player, direction, position, temp_board)


    def check_fair_play_1(self, player, direction, position, temp_board):
        """initializes the temporary board to be used in fairplay validation
        and sends to fairplay calculation"""
        p2_row = self._player_2_position[0]
        p2_column = self._player_2_position[1]
        try:                       # try and except used for index range errors
            if temp_board[p2_row + 1][p2_column] == 1:
                temp_board[p2_row + 2][p2_column] = "red"
        except:
            pass
        try:              # all spaces adjacent to posing player are 'red'
            if temp_board[p2_row - 1][p2_column] == 1:
                temp_board[p2_row - 2][p2_column] = "red"
        except:
            pass
        try:
            if temp_board[p2_row][p2_column + 1] == 1:
                temp_board[p2_row][p2_column + 2] = "red"
        except:
            pass
        try:
            if temp_board[p2_row][p2_column - 1] == 1:
                temp_board[p2_row][p2_column - 2] = "red"
        except:
            pass
        return self.calculate_fairplay(temp_board, player, direction, position)


    def check_fair_play_2(self, player, direction, position, temp_board):
        """initializes board for player 2 and sends to method for fairplay
        validation"""
        p1_row = self._player_1_position[0]
        p1_column = self._player_1_position[1]
        try:              # try and except used for index range errors
            if temp_board[p1_row + 1][p1_column] == 1:  # down
                temp_board[p1_row + 2][p1_column] = "red"
        except:
            pass
        try:              # all space adjacent to player 1 are 'red'
            if temp_board[p1_row - 1][p1_column] == 1:
                temp_board[p1_row - 2][p1_column] = "red"
        except:
            pass
        try:
            if temp_board[p1_row][p1_column + 1] == 1:
                temp_board[p1_row][p1_column + 2] = "red"
        except:
            pass
        try:
            if temp_board[p1_row][p1_column - 1] == 1:
                temp_board[p1_row][p1_column - 2] = "red"
        except:
            pass
        return self.calculate_fairplay(temp_board, player, direction, position)


    def calculate_fairplay(self, temp_board, player, direction, position, counter=0, limit=17):
        """recursive method to validate fairplay, changes every board space the opposite player
        has acces to to 'red' and continues if the opposite baseline has a 'red' space"""
        if player == 1:
            if "red" in temp_board[0]:   # continue if fairplay rule is followed
                return self.add_p1_fence(direction, position)
        if player == 2:
            if "red" in temp_board[16]:   # continue if fairplay rule is followed
                return self.add_p2_fence(direction, position)
        while 0 < limit:                # if opposite baseline not reached in 17 moves fence not allowed
            for num in range(0,8):
                num = num*2
                count = 0
                for space in temp_board[num]:
                    if space == "red":
                        try:    # adjacent squared to 'red' spaces become 'red
                            if temp_board[num+ 1][count] == 1:
                                temp_board[num + 2][count] = "red"
                        except:
                            pass
                        try:
                            if temp_board[num- 1][count] == 1:
                                temp_board[num - 2][count] = "red"
                        except:
                            pass
                        try:
                            if temp_board[num][count + 1] == 1:
                                temp_board[num][count + 2] = "red"
                        except:
                            pass
                        try:
                            if temp_board[num][count - 1] == 1:
                                temp_board[num][count - 2] = "red"
                        except:
                            pass
                        count +=2
            return self.calculate_fairplay(temp_board, player, direction, position, counter+1, limit-1)
        return "breaks the fairplay rule."


    def add_p1_fence(self, direction, position):
        """updates the board dding fence, updates turn,subtracts an
        available fence from player 1"""
        row = position[1]*2
        column = position[0]*2
        if direction == "v":                          # vertical fence
            if self._board[row - 1][column] == 1:
                self._board[row][column-1] = "fence"  # fence added
                self._player_1_fences -= 1            # fence subtracted from player 1
                self._turn = "player_2"               # player 2 turn
                return True
            else:
                return False
        if direction == "h":                          # horizontal fence
            if self._board[row-1][column] == 1:
                self._board[row-1][column] = "fence"  # fence added
                self._player_1_fences -= 1            # fence taken away after use
                self._turn = "player_2"               # player 2 turn
                return True
            else:
                return False


    def add_p2_fence(self, direction, position):
        """updates game board with fence updates turn and
        fences available to player 2"""
        row = position[1]*2
        column = position[0]*2
        if direction == "v":                          # vertical fence
            if self._board[row - 1][column] == 1:
                self._board[row][column-1] = "fence"  # fence added
                self._player_2_fences -= 1            # fence used by player 2
                self._turn = "player_1"               # player 1 turn
                return True
            else:
                return False
        if direction == "h":                           # horizontal fences
            if self._board[row-1][column] == 1:
                self._board[row-1][column] = "fence"   # fence added
                self._player_2_fences -= 1             # fence used by player 2
                self._turn = "player_1"                # player 1 turn
                return True
            else:
                return False


    def is_winner(self, player):
        """takes player and returns true if they won and
        false otherwise"""
        if player == 1:
            if self._game_state == "player1 wins":
                return True                   # player 1 win
            else:
                return False
        if player == 2:
            if self._game_state == "player2 wins":
                return True                  # player 2 win
            else:
                return False


    def print_board(self):
        """prints game board line by line"""
        for item in self._board:
            print(item)


