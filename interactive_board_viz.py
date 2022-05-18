# Board visualization with ipywidgets
import copy
from time import sleep
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed, interact_manual
from ipywidgets import VBox, HBox, Label, Button, GridspecLayout
from ipywidgets import Button, GridBox, Layout, ButtonStyle, Output
from IPython.display import display, clear_output
from numpy import isin

from isolation import Board
from test_players import Player, RandomPlayer, HumanPlayer
from custom_player import CustomPlayer

import time
import platform

# import io
from io import StringIO

# import resource
if platform.system() != "Windows":
    import resource


def get_details(name):
    if name in {"11", "12", "13"}:
        color = "SpringGreen"
    elif name in {"21", "22", "23"}:
        color = "tomato"
    elif name == "q1":
        color = "#bdffbd"
        name = " "
    elif name == "q2":
        color = "#ffb6ae"
        name = " "
    elif name == "X":
        color = "black"
    elif name == "O":
        color = "orange"
        name = " "
    else:
        color = "Lavender"
    style = ButtonStyle(button_color=color)
    return name, style


def create_cell(button_name="", grid_loc=None, click_callback=None):
    layout = Layout(width="auto", height="auto")
    name, style = get_details(button_name)
    button = Button(description=name, layout=layout, style=style)
    button.x, button.y = grid_loc
    if click_callback:
        button.on_click(click_callback)
    return button


def get_viz_board_state(game, show_legal_moves):
    board_state = game.get_state()
    legal_moves = game.get_active_moves()
    active_player = "q1" if game.__active_player__ is game.__player_1__ else "q2"
    if show_legal_moves:
        for moves in legal_moves:
            for r, c in moves:
                board_state[r][c] = active_player
    return board_state


def create_board_gridbox(game, show_legal_moves, click_callback=None):
    h, w = game.height, game.width
    board_state = get_viz_board_state(game, show_legal_moves)

    grid_layout = GridspecLayout(
        n_rows=h,
        n_columns=w,
        grid_gap="2px 2px",
        width="480px",
        height="480px",
        justify_content="center",
    )
    for r in range(h):
        for c in range(w):
            cell = create_cell(board_state[r][c], grid_loc=(r, c), click_callback=click_callback)
            grid_layout[r, c] = cell

    return grid_layout


class PlayInteractiveGame:
    """This class is used to play the game interactively (only works in jupyter)"""

    def __init__(
        self,
        player1=Player("Player1"),
        opponent=Player("Player2"),
        show_legal_moves=False,
        output_section=widgets.Output(
            layout={
                "border": "1px solid black",
                "overflow_y": "auto",
                "height": "80px",
                "width": "480px",
            }
        ),
    ):
        self.player1 = player1
        self.opponent = opponent
        self.game = Board(player1, opponent)
        self.output_section = output_section
        self.width = self.game.width
        self.height = self.game.height
        self.show_legal_moves = show_legal_moves
        self.__click_count = 0
        self.__move = []
        self.callback_func = self.select_callback_func(player1, opponent)
        self.gridb = create_board_gridbox(
            self.game, self.show_legal_moves, click_callback=self.callback_func
        )
        self.visualized_state = None
        self.game_is_over = False

    def null_callback(self, b):
        """ Initial callback function before player options are set
        """
        # global output section widget
        with out:
            output = "Please Select Players first \n"
            out.append_stdout(output)

    def select_callback_func(self, player1, player2):
        """ Function to determine which callback function to use based on the type of players
            involved in the game
        """

        if isinstance(player1, Player) and isinstance(player2, RandomPlayer):
            #             print(f"Human vs Random Player")
            return self.select_move

        elif isinstance(player1, RandomPlayer) and isinstance(player2, CustomPlayer):
            with self.output_section:
                return None

        elif isinstance(player1, RandomPlayer) and isinstance(player2, RandomPlayer):
            raise NotImplementedError("Random vs Random not implemented")

        elif isinstance(player1, RandomPlayer) and isinstance(player2, Player):
            raise NotImplementedError("Random (P1) vs Human (P2) not implemented")

        elif isinstance(player1, Player) and isinstance(player2, Player):
            # Human Vs. Human
            return self.select_move

        elif not player1 and not player2:
            return self.null_callback

        else:
            return None

    def __reset_turn(self):
        self.__click_count = 0
        self.__move = []
        with self.output_section:
            self.output_section.append_stdout("-" * 50 + "\n")

    #         self.output_section.clear_output()

    def run_cpu_ai_game(self, run_game=False):
        """ Function to run a game against the Random CPU and Custom AI Agent
        """
        if run_game:
            # counter = 0
            while not self.game_is_over:
                # counter += 1
                with out:
                    out.append_stdout("Computing Best Move for AI Agent \n")
                self.select_custom_move()
                time.sleep(2.5)

    #                 print(f"Next Move")

    def select_custom_move(self):

        if platform.system() == "Windows":

            def curr_time_millis():
                return int(round(time.time() * 1000))

        else:

            def curr_time_millis():
                return 1000 * resource.getrusage(resource.RUSAGE_SELF).ru_utime

        move_start = curr_time_millis()

        def time_left(time_limit=1000):
            # print("Limit: "+str(time_limit) +" - "+str(curr_time_millis()-move_start))
            return time_limit - (curr_time_millis() - move_start)

        active_player = self.game.get_active_player()
        #         self.output_section.append_stdout(f"Active Players Turn: {active_player}")

        if isinstance(active_player, RandomPlayer):
            self.output_section.append_stdout("Random Player's Turn \n")

        elif isinstance(active_player, CustomPlayer):
            self.output_section.append_stdout("Custom AI Player's Turn \n")

            start = time.time()

        ############
        # TODO: Illegal moves being allowed in the game
        all_player_moves = self.game.get_active_moves()
        player_move = active_player.move(self.game, time_left=time_left)

        if not player_move in all_player_moves:
            print(
                f"{type(active_player)} move {player_move} is not in list of legal moves {all_player_moves}"
            )

        self.game_is_over, winner = self.game.__apply_move__(player_move)

        if self.game_is_over:
            print(f"Game is over, the winner is: {winner}")

        board_vis_state = get_viz_board_state(self.game, self.show_legal_moves)
        for r in range(self.height):
            for c in range(self.width):
                new_name, new_style = get_details(board_vis_state[r][c])
                self.gridb[r, c].description = new_name
                self.gridb[r, c].style = new_style
        self.__reset_turn()

        if isinstance(active_player, CustomPlayer):
            end = time.time()
            print(f"Run time to compute move: {end - start}")

    def select_move(self, b):
        if platform.system() == "Windows":

            def curr_time_millis():
                return int(round(time.time() * 1000))

        else:

            def curr_time_millis():
                return 1000 * resource.getrusage(resource.RUSAGE_SELF).ru_utime

        move_start = curr_time_millis()

        def time_left(time_limit=1000):
            # print("Limit: "+str(time_limit) +" - "+str(curr_time_millis()-move_start))
            return time_limit - (curr_time_millis() - move_start)

        global ig
        if isinstance(ig.player1, HumanPlayer) and isinstance(ig.opponent, HumanPlayer):
            with ig.output_section:
                out.append_stdout("Human Vs. Human")

        self.__move.append((b.x, b.y))
        with self.output_section:
            self.output_section.append_stdout(f"Move {self.__click_count + 1}: {b.x}, {b.y} \n")

        if self.__click_count < 2:
            self.__click_count += 1
            return

        #         self.output_section.append_stdout("Test1")
        if self.game_is_over:
            with self.output_section:
                self.output_section.append_stdout("The game is over! \n")
            return
        ### swap move workaround ###
        # find if current location is in the legal moves
        # legal_moves is of length 1 if move exists, and len 0 if move is illegal
        moves = self.game.get_active_moves()
        legal_moves = [(x, y, z) for x, y, z in moves if [x, y, z] == self.__move]
        if not legal_moves:
            output = f"move {self.__move} is illegal!"
            self.__reset_turn()
            with self.output_section:
                self.output_section.append_stdout(output)
            return
        else:
            # there is only one move in swap isolation game
            self.__move = legal_moves[0]

        #         self.output_section.append_stdout("Test2")
        ### swap move workaround end ###
        self.game_is_over, winner = self.game.__apply_move__(self.__move)
        if (not self.game_is_over) and (type(self.opponent) != Player):
            opponents_legal_moves = self.game.get_active_moves()
            opponent_move = self.opponent.move(self.game, time_left=time_left)

            assert (
                opponent_move in opponents_legal_moves
            ), f"Opponents move {opponent_move} is not in list of legal moves {opponents_legal_moves}"

            self.game_is_over, winner = self.game.__apply_move__(opponent_move)

        #         self.output_section.append_stdout("Test3")
        if self.game_is_over:
            #             print(f"Game is over, the winner is: {winner} \n")
            self.output_section.append_stdout(f"Game is over, the winner is: {winner} \n")

        board_vis_state = get_viz_board_state(self.game, self.show_legal_moves)
        for r in range(self.height):
            for c in range(self.width):
                new_name, new_style = get_details(board_vis_state[r][c])
                self.gridb[r, c].description = new_name
                self.gridb[r, c].style = new_style

        if self.game_is_over:
            # Remove callback functions from buttons
            for r in range(self.height):
                for c in range(self.width):
                    self.gridb[r, c].on_click(None)
                return
        # Reset turn and clear output state for next players turn
        self.__reset_turn()


class ReplayGame:
    """This class is used to replay games (only works in jupyter)"""

    def __init__(self, game, move_history, show_legal_moves=False):
        self.game = game
        self.width = self.game.width
        self.height = self.game.height
        self.move_history = move_history
        self.show_legal_moves = show_legal_moves
        self.board_history = []
        self.new_board = self.setup_new_board()
        self.gridb = create_board_gridbox(self.new_board, self.show_legal_moves)
        self.generate_board_state_history()
        self.visualized_state = None
        self.output_section = widgets.Output(layout={"border": "1px solid black"})

    def setup_new_board(self,):
        return Board(
            player_1=self.game.__player_1__,
            player_2=self.game.__player_2__,
            width=self.width,
            height=self.height,
        )

    def update_board_gridbox(self, move_i):
        board_vis_state, board_state = self.board_history[move_i]
        self.visualized_state = board_state
        for r in range(self.height):
            for c in range(self.width):
                new_name, new_style = get_details(board_vis_state[r][c])
                self.gridb[r, c].description = new_name
                self.gridb[r, c].style = new_style

    def equal_board_states(self, state1, state2):
        for r in range(self.height):
            for c in range(self.width):
                if state1[r][c] != state2[r][c]:
                    return False
        return True

    def generate_board_state_history(self,):
        for move_pair in self.move_history:
            for move in move_pair:
                self.new_board.__apply_move__(move[0])
                board_vis_state = get_viz_board_state(self.new_board, self.show_legal_moves)
                board_state = self.new_board.get_state()
                self.board_history.append(
                    (copy.deepcopy(board_vis_state), copy.deepcopy(board_state))
                )
        assert self.equal_board_states(
            self.game.get_state(), self.new_board.get_state()
        ), "End game state based of move history is not consistent with state of the 'game' object."

    def get_board_state(self, x):
        """You can use this state to with game.set_state() to replicate same Board instance."""
        self.output_section.clear_output()
        with self.output_section:
            display(self.visualized_state)

    def show_board(self):
        # Show slider for move selection
        input_move_i = widgets.IntText(layout=Layout(width="auto"))
        slider_move_i = widgets.IntSlider(
            description=r"\(move[i]\)",
            min=0,
            max=len(self.board_history) - 1,
            continuous_update=False,
            layout=Layout(width="auto"),
        )
        mylink = widgets.link((input_move_i, "value"), (slider_move_i, "value"))
        slider = VBox([input_move_i, interactive(self.update_board_gridbox, move_i=slider_move_i)])

        get_state_button = Button(description="get board state")
        get_state_button.on_click(self.get_board_state)

        grid = GridspecLayout(4, 6)  # , width='auto')
        # Left side
        grid[:3, :-3] = self.gridb
        grid[3, :-3] = slider

        # Right side
        grid[:-1, -3:] = self.output_section
        grid[-1, -3:] = get_state_button
        display(grid)
