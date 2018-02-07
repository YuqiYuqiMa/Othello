
# graphical_ui

import game_logic
import tkinter

### This module communicates with the user within the tkinter window
# draw every valid move on the graphical game boaard
# main function - graph_user_interface()

DEFAULT_FONT = ('Helvetica', 20)
color_dictionary = {1: 'black', 2: 'white'}

class Spot:
    def __init__(self, center: [float, float]):
        self._center = center

    def center(self) -> [float, float]:
        return self._center

    
class Spotstate:
    def __init__(self):
        self._spots = []

    def all_spots(self) -> [Spot]:
        return self._spots
               
    def handle_click(self, click_point: [float, float], game) -> None:
        self._spots.append(Spot(click_point))

# The Hello class creates objects that represent a modal
# dialog box that asks the user for game info: row_num, col_num
# first player, upper left, rule and to fill in the infos.
# After the user fills these values in, and presses either OK or Cancel,
# we can use the list of all infos to set up the game
class Hello:
    def __init__(self):
        self._root_window = tkinter.Toplevel()

        self._first_player = tkinter.IntVar()
        self._upper_left = tkinter.IntVar()
        self._rule = tkinter.StringVar()

        self._greeting_text = tkinter.StringVar()
        self._greeting_text.set('please fill in information')
        greet = tkinter.Label(
            master = self._root_window, textvariable = self._greeting_text,
            font = DEFAULT_FONT) # greeting message
        greet.grid(
            row = 0, column = 0, padx = 10, pady = 10)

        row_num = tkinter.Label(
            master = self._root_window, text = 'row number',
            font = DEFAULT_FONT) # row number
        row_num.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        self._row_num_entry = tkinter.Entry(
            master = self._root_window, width = 20, font = DEFAULT_FONT)
        self._row_num_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E) # row_num entry
        
        col_num = tkinter.Label(
            master = self._root_window, text = 'column number',
            font = DEFAULT_FONT) # column number
        col_num.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        self._col_num_entry = tkinter.Entry(
            master = self._root_window, width = 20, font = DEFAULT_FONT)
        self._col_num_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E) # col_num entry

        who_first = tkinter.Label(
            master = self._root_window, text = 'who first',
            font = DEFAULT_FONT) # the first player
        who_first.grid(row = 4, column = 0, sticky = tkinter.W)
        self._first_black = tkinter.Radiobutton(
            master = self._root_window, text = 'black',
            variable = self._first_player,
            value = game_logic.BLACK) # button black
        self._first_black.select() # select black by default
        self._first_black.grid(row = 4, column = 1, sticky = tkinter.W)
        self._first_white = tkinter.Radiobutton(
            master = self._root_window, text = 'white',
            variable = self._first_player,
            value = game_logic.WHITE)# button white
        self._first_white.grid(row = 4, column = 1, sticky = tkinter.E)

        upper_left = tkinter.Label(
            master = self._root_window, text = 'upper left player',
            font = DEFAULT_FONT) # upper left player
        upper_left.grid(row = 3, column = 0, sticky = tkinter.W)
        self._move_black = tkinter.Radiobutton(
            master = self._root_window, text = 'black',
            variable = self._upper_left,
            value = game_logic.BLACK) # button black
        self._move_black.select() # selet black by default
        self._move_black.grid(row = 3, column = 1, sticky = tkinter.W)
        self._move_white = tkinter.Radiobutton(
            master = self._root_window, text = 'white',
            variable = self._upper_left,
            value = game_logic.WHITE) # button white
        self._move_white.grid(row = 3, column = 1, sticky = tkinter.E)

        rule = tkinter.Label(
            master = self._root_window, text = 'choose rule',
            font = DEFAULT_FONT) # rule
        rule.grid(row = 5, column = 0, sticky = tkinter.W)       
        self._largest = tkinter.Radiobutton(
            master = self._root_window, text = 'largest',
            variable = self._rule,
            value = '>') # button largest
        self._largest.select() # select largest by default
        self._largest.grid(row = 5, column = 1, sticky = tkinter.W)
        self._smallest = tkinter.Radiobutton(
            master = self._root_window, text = 'smallest',
            variable = self._rule,
            value = '<') # button smallest
        self._smallest.grid(row = 5, column = 1, sticky = tkinter.E)
        
        button_frame = tkinter.Frame(master = self._root_window)
        button_frame.grid(
            row = 6, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S) # the bottom row

        ok_button = tkinter.Button(
            master = button_frame, text = 'OK', font = DEFAULT_FONT,
            command = self._on_ok_button) # OK button
        ok_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button) # Cancle button
        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.rowconfigure(3, weight = 1)
        self._root_window.rowconfigure(4, weight = 1)
        self._root_window.rowconfigure(5, weight = 1)
        self._root_window.rowconfigure(6, weight = 1)
        
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.columnconfigure(1, weight = 1)

        self._ok_clicked = False
        self._row_num = 0
        self._col_num = 0

    def show(self) -> None:
        '''
        turns control over to our dialog box and make that dialog box modal
        '''
        self._root_window.grab_set()
        self._root_window.wait_window()

    def was_ok_clicked(self) -> bool:
        return self._ok_clicked

    def check_num(self, n: int) -> bool:
        ''' checks if the number user typed is valid'''
        return n % 2 == 0 and 4 <= n <= 16

    def _on_ok_button(self) -> None:
        self._ok_clicked = True
        try:
            self._row_num = int(self._row_num_entry.get())
            self._col_num = int(self._col_num_entry.get())
            x = self._row_num
            y = self._col_num
            # if the inputs of row_num and col_num are both valid:
            # gets all the info and updates self._all_info
            if self.check_num(x) and self.check_num(y):
                self._upper_left = self._upper_left.get()
                self._first_player = self._first_player.get()
                self._rule = self._rule.get()
                self._root_window.destroy()
        except:
            self.update_text() # if not valid, prints error message
            
    def update_text(self) -> None:
        '''updates error message in the window'''
        error_mes = 'ERROR, please try again'
        self._greeting_text.set(error_mes)

    def _on_cancel_button(self) -> None:
        '''destroys the window if cancle is clicked'''
        self._root_window.destroy()


class Greeting:
    def __init__(self):
        '''
        checks if user wants to start the game
        if yes, call class Hello() to get all the info
        and returns a list of all info
        '''
        self._root_window = tkinter.Tk()
        greet_text = tkinter.Label(
            master = self._root_window, text = 'Othello Game',
            font = DEFAULT_FONT)
        greet_text.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E)
        # the top line in the window: Othello Game
        start_button = tkinter.Button(
            master = self._root_window, text = 'Start', font = DEFAULT_FONT,
            command = self.on_greet)
        start_button.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E)
        # button: Start, game starts when clicked
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

        self._all_info = []

    def start(self) -> None:
        self._root_window.mainloop()

    def on_greet(self) -> list:
        dialog = Hello()# calss the class Hello()
        dialog.show()
        self._root_window.destroy()
        if dialog.was_ok_clicked:
            new_list = [dialog._row_num, dialog._col_num, dialog._first_player, dialog._upper_left, dialog._rule]
            self._all_info.extend(new_list) # gets all the info from user
            return self._all_info

        
class Graph:
    def __init__(self, state: Spotstate, info_list: list):
        '''
        sets graphical game board and info box
        prints game information in info box
        updates every move in graphical game board
        draws discs (graphically)
        '''
        self._state = state
        self._game = game_logic.Othello(info_list) # call game logic
        self._window = tkinter.Tk()
        
        self._canvas = tkinter.Canvas(
            master = self._window, width = self._game._row * 100,
            height = self._game._col * 100,
            background = 'grey') # main game board
        self._canvas.grid(
            row = 0, column = 0, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        self._infobox = tkinter.Canvas(
            master = self._window, width = self._game._row * 100 / 2,
            height = self._game._col * 100,
            background = 'yellow') # conatains scores and turn
        self._infobox.grid(
            row = 0, column = 1, padx = 10, pady = 10,
            sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W)
        
        self._window.rowconfigure(0, weight = 1)
        self._window.columnconfigure(0, weight = 1)
        self._window.columnconfigure(1, weight = 1)

        self._canvas.bind('<Configure>', self.on_canvas_resized)
        self._canvas.bind('<Button-1>', self.on_canvas_clicked)

        self._infobox.rowconfigure(0, weight = 1)
        self._infobox.rowconfigure(1, weight = 1)
        self._infobox.rowconfigure(2, weight = 1)
        self._infobox.columnconfigure(0, weight = 1)
        # prints game rule : FULL
        full_label = tkinter.Label(
            master = self._infobox, text = 'FULL', font = DEFAULT_FONT)
        full_label.grid(
            row = 0, column = 0, padx = 10, pady = 10)
        # sets up score information (changeable)
        self._score_info = tkinter.StringVar()
        self._score_info.set('B: 2  W: 2')
        score_label = tkinter.Label(
            master = self._infobox, textvariable = self._score_info,
            font = DEFAULT_FONT)
        score_label.grid(
            row = 1, column = 0, padx = 10, pady = 10)
        
        # sets turn information (changeable)
        self._turn_info = tkinter.StringVar()
        self._turn_info.set("TURN: {}".format(game_logic.turn_dictionary[self._game._turn]))
        turn_label = tkinter.Label(
            master = self._infobox, textvariable = self._turn_info,
            font = DEFAULT_FONT)
        turn_label.grid(
            row = 2, column = 0, padx = 10, pady = 10)
        

    def run(self) -> None:
        self._window.mainloop()
        
    def on_canvas_resized(self, event: tkinter.Event) -> None:
        self._canvas.delete(tkinter.ALL)
        self._infobox.delete(tkinter.ALL)
        self.draw_line()
        self.draw_all_spots(self.draw_board())

    def row_and_col(self, original: list) -> list:
        '''
        converts the given list of coordinates
        to row number and column number
        for further use to update the game board
        returns the new list of row number and column number
        '''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        new = [original[0] / canvas_width, original[1] / canvas_height]
               
        every_x = canvas_width / self._game._row
        every_y = canvas_height / self._game._col
        x = (new[0] * canvas_width) // every_x
        y = (new[1] * canvas_height) // every_y
        new_point = [int(y), int(x)]
        return new_point

    def update_score(self, game) -> None:
        '''
        updates the score information in info box
        '''
        player_score = self._game.print_score(self._game._board)
        self._score_info.set(player_score)
       
    def on_canvas_clicked(self, event: tkinter.Event) -> None:
        '''
        makes a move when the user clicks the game board window,
        checks if the opponent has any valid moves:
           if yes, switch turn,
           if not, switch back to current player
        ends game and prints winner when a winner is found
        '''
        ### It is important to check if there is valid move for the next player
        # or if there is winner after each click (before the next click)
        # so that if there is any switching turn or winner
        # after each click, it will update the game info before the next click
        try:
            click_point = [event.x, event.y]
            new_point = self.row_and_col(click_point)
            # makes a move and update the game board
            self._game._board = self._game.make_moves(self._game._board, self._game._turn, new_point)
            self._state.handle_click(click_point, self._game)
            self.update_score(self._game) # update scores
            self.draw_all_spots(self.draw_board()) # draw the updated game board
            self._game.winning_player(self._game._board, self._game._turn)
            # checks if there is winner using te updated game board
            if self._game._winner == game_logic.NOT_OVER:
                opponent = self._game.opposite_turn(self._game._turn)
                all_moves = self._game.valid_moves(self._game._board, opponent)[0]
                if len(all_moves) > 0: # checks if opponent has any valid moves
                    self._game._turn = opponent # if yes, switch turn
                    turn = self._game.show_player_turn(self._game._turn)
                    self._turn_info.set(turn)
                else: # if not, switch turn back to the current player
                    opposite = self._game.show_player_turn(self._game._turn)
                    self._turn_info.set(opposite)
            else: # prints winner
                winning = "WINNER: {}".format(game_logic.turn_dictionary[self._game._winner])
                self._turn_info.set(winning)
                
        except game_logic.InvalidMoveError:
            pass
        except game_logic.GameOverError:
            pass
        

    def draw_line(self) -> None:
        '''
        draws all the vertical and horiaontal lines
        in the game using the given row_num and col_num
        '''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        row_num = 1 / self._game._row # the percentage(float) each row takes up
        col_num = 1 / self._game._col
        for row in range(self._game._row):
            every_row = row_num * row * canvas_width
            self._canvas.create_line(every_row, 0, every_row, canvas_height, fill = 'black')

        for col in range(self._game._col):
            every_col = col_num * col * canvas_height
            self._canvas.create_line(0, every_col, canvas_width, every_col, fill = 'black')
                    
    def draw_board(self) -> list:
        '''
        finds all the discs (black or wihte) on the current game board
        and returns a list of their coordinates
        and color
        '''
        all_discs = []
        for row in range(len(self._game._board[0])):
            for col in range(len(self._game._board)):
                color = self._game._board[row][col]
                if color in [1, 2]:
                    all_discs.append([col / self._game._col, row / self._game._row, color])
        return all_discs
                    
        
    def draw_all_spots(self, discs: list) -> None:
        '''
        draws all the discs in the given list on board
        '''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()

        for spot in discs:
            every_x = canvas_width / self._game._row # length of every row
            every_y = canvas_height / self._game._col

            radius_x = every_x / 2 # radius on x-direction
            radius_y = every_y / 2 # radius on y-direction

            center_x = (spot[0] * canvas_width) + radius_x # x-value of center
            center_y = (spot[1] * canvas_height) + radius_y # y-value of center
            color = spot[2]

            if 0 < center_x % every_x < every_x and 0 < center_y % every_y < every_y :
                dr_x = (((center_x // every_x) / self._game._row) * canvas_width) + radius_x
                dr_y = (((center_y // every_y) / self._game._col) * canvas_height) + radius_y

                self._canvas.create_oval(
                    dr_x - radius_x, dr_y - radius_y,
                    dr_x + radius_x, dr_y + radius_y,
                    fill = color_dictionary[color])
                

def graph_user_interface() -> None:
    try:
        dialog = Greeting()
        dialog.start()
        game_info = dialog._all_info
        app = Graph(Spotstate(), game_info)
        app.run()
    except:
        pass


if __name__ == '__main__':
    graph_user_interface()
