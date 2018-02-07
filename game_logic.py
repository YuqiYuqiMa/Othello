
# game_logic

### This module contains class othello which is the main game logic

NONE = 0
BLACK = 1
WHITE = 2
NOT_OVER = -1

all_direction = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
turn_dictionary = {BLACK: 'B', WHITE: 'W', NONE: 'NONE'}

### Exceptions

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass

class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass

### class othello

### class othello contains functions which create new game board,
# checks current discs of a player, checks all possible valid spots
# changes the current board if the move is valid, switches player's turn
# checks if there are any valid moves, if not, checks winner

class Othello:
    
    def __init__(self, info_list):
        self._row = info_list[0]
        self._col = info_list[1]
        self._turn = info_list[2]
        self._upper_left = info_list[3]
        self._rule = info_list[4]

        self._board = self.new_game_board()
        self._winner = NOT_OVER

        
    def new_game_board(self) -> '2D list':
        '''
        Creates a 2D list of the initial game board with
        the two white discs separated diagonally
        and the two black discs separated diagonally in the center
        self._upper_left will be in the top-left position
        '''
        player = self._upper_left
        opponent = self.opposite_turn(player)
        board = []
        for col in range(self._col):
            board.append([])
            for row in range(self._row):
                board[-1].append(NONE)
        board[(self._col // 2) - 1][(self._row // 2) - 1] = player
        board[self._col // 2][self._row // 2] = player
        board[(self._col // 2) - 1][self._row // 2] = opponent
        board[self._col // 2][(self._row // 2) - 1] = opponent
        return board


    def copy_game_board(self, board: '2D list') -> list:
        '''
        Copies the game board for further use
        '''
        board_copy = []

        for col in range(self._col):
            board_copy.append([])
            for row in range(self._row):
                board_copy[-1].append(board[col][row])

        return board_copy

   
    def opposite_turn(self, turn: int) -> int:
        '''
        Given the player whose turn it is now, returns the opposite player
        '''
        if turn == BLACK:
            turn = WHITE
        else:
            turn = BLACK
        return turn

             
    def check_valid_num(self, location_list: list) -> bool:
        '''
        Checks if the given location(list) is in the range of the board
        '''
        return 0 <= location_list[0] <= self._row - 1 and 0 <= location_list[1] <= self._col - 1


    def same_color_disc(self, player: int, board: '2D list') -> list:
        '''
        Finds all the discs one player currently have on board
        returns a list of the coordinates of all the same color discs
        '''
        # This function can be used to check both player WHITE and BLACK
        look_up = []
        for row in range(len(board[0])):
            for col in range(len(board)):
                spot = board[row][col]
                if spot == player:
                    look_up.append([row, col])
        return look_up


    def valid_moves(self, board: '2D list', player: int) -> list:
        '''
        Takes a game board and a player turn
        returns a list which consists of two sublists:
        1: A list of coordinates where is valid to make a move
        2: A list of coordinates of discs to bt flipped
           This list is in the same order as the valid move list
           seperated by every direction
        '''
        discs = self.same_color_disc(player, board)
        opponent = self.opposite_turn(player)
        flip_list = []
        move_list = []
        general_list = []
        for x_dir, y_dir in all_direction:
            for spot in discs:
                x = spot[0]
                y = spot[1]
                x += x_dir # the adjacent spot
                y += y_dir
                if self.check_valid_num([x, y]) and board[x][y] == opponent:
                    # check if the adjacent spot is opposite color
                    while board[x][y] == opponent:
                        x += x_dir
                        y += y_dir # checks the next spot in the same direction
                        if not self.check_valid_num([x, y]):
                            break
                        else:
                    # if it is empty, then it is a valid spot to make a move
                            if board[x][y] == NONE:
                                move_list.append([x, y])
                                every = []
                                while True:
                                    x -= x_dir
                                    y -= y_dir
                                    if board[x][y] == player:
                                        break
                                    every.append([x, y])
                                flip_list.append(every)
# appends all the spots between the original spot and the spot of valid move
# to the list of all the discs to be flipped

        general_list.append(move_list)
        general_list.append(flip_list)
        return general_list


    def if_game_over(self, board: '2D list', player: int) -> bool:
        player_valid = len(self.valid_moves(board, player)[0])
        opponent = self.opposite_turn(player)
        opponent_valid = len(self.valid_moves(board, opponent)[0])
        # checks if both players have no valid moves
        return player_valid == 0 and opponent_valid == 0
            # both players don't have any valid moves

            
    def make_moves(self, board: '2D list', player: int, move: list) -> '2D list':
        '''
        returns a board with the move being made
        '''
        if self.if_game_over(board, player):
            raise GameOverError
        
        moves_and_flip = self.valid_moves(board, player)
        valid_moves = moves_and_flip[0]
        discs_to_flip = moves_and_flip[1]
        indices = []
        # the following steps make sure that once a move is made
        # the discs around it from all possible directions are flipped
        if move in valid_moves:
            for index, value in enumerate(valid_moves):
                if value == move:
                    indices.append(index)

            board[move[0]][move[1]] = player
            for unit in indices:
                for every_disc in discs_to_flip[unit]:
                    board[every_disc[0]][every_disc[1]] = player
            new_board = self.copy_game_board(board)
        else:
            raise InvalidMoveError
        return new_board

                
    def players_score(self, board: '2D list') -> list:
        '''
        returns a list of integers
        black player score
        and white player score
        '''
        scores = []
        black_score = len(self.same_color_disc(1, board))
        scores.append(black_score)
        white_score = len(self.same_color_disc(2, board))
        scores.append(white_score)
        return scores

    
    def show_player_turn(self, player: int) -> str:
        '''
        Prints the player turn in the required format
        '''
        return "TURN: {}".format(turn_dictionary[self._turn])
        

    def print_score(self, board: '2D list') -> str:
        '''
        prints the players' scores in the required format
        '''
        score_list = self.players_score(self._board)
        black_score = score_list[0]
        white_score = score_list[1]
        return "B: {}  W: {}".format(black_score, white_score)

        
    def winning_player(self, board: '2D list', player: int) -> None:
        '''
        checks if there is any winner
        if yes, returns a winner: BLACK or WHITE or NONE
        if not, returns NOT_OVER
        '''
        rule = self._rule
        score_list = self.players_score(board)
        if self.if_game_over(board, player):
            if score_list[0] == score_list[1]:
                self._winner = NONE # equal, both players have the same score
            else:
                # returns winner with respect to the given rule
                if rule == '>':
                    idx = score_list.index(max(score_list))
                    if idx == 0:
                        self._winner = BLACK
                    elif idx == 1:
                        self._winner = WHITE
                elif rule == '<':
                    idx = score_list.index(min(score_list))
                    if idx == 0:
                        self._winner = BLACK
                    elif idx == 1:
                        self._winner = WHITE
        else:
# if there is still a chance for either player to make a move -> NOT_OVER
            self._winner = NOT_OVER
