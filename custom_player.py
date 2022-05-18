# Algorithm for finding the best move
def minimax(player, game, time_left, depth, my_turn=True, debug=False, output=None):
    """Implementation of the minimax algorithm.
    Args:
        player (CustomPlayer): This is the instantiation of CustomPlayer()
            that represents your agent. It is used to call anything you
            need from the CustomPlayer class (the utility() method, for example,
            or any class variables that belong to CustomPlayer()).
        game (Board): A board and game state.
        time_left (function): Used to determine time left before timeout
        depth: Used to track how deep you are in the search tree
        my_turn (bool): True if you are computing scores during your turn.

    Returns:
        (tuple, int): best_move, val

    # Note:
        depth --> tells us when to stop searching the tree
    # Steps in the algorithm:
    1. Terminal state check. If at the root node, return the utility of the node/state
    2. Get all possible moves for the current player
    3. Determine if a winner is found for any of the moves from step 2
        a. If the winner is MAX, return the move, utility == +inf
        b. if the winner is MIN, return the move, utility == -inf

    4. If no winner is found, continue searching the game tree by recursively calling MINIMAX to get
    the best forecast value
    5. Set best_move, best_value to be highest utility moves based on forecasted value

    """

    # Determine whose turn it is
    if my_turn:
        ai_player = game.get_active_player()
        cpu_player = game.get_inactive_player()

    else:
        ai_player = game.get_inactive_player()
        cpu_player = game.get_active_player()

    # Handle time running out
    # TODO
    if time_left() < 5:
        # print(f"Move timing out. Selecting currently best found move")
        return None, ai_player.utility(game, my_turn)

    ####################################################################################################
    # Search the game tree
    ####################################################################################################

    # If depth is 0, we know we've arrived at the lowest depth desired. Return number of available moves
    # for the AI - number of moves available for the opponent
    if depth == 0:
        best_value = ai_player.utility(game, my_turn)
        return None, best_value

    if my_turn:
        # Initialize values
        max_value = float("-inf")
        best_move = None

        # Get possible moves of the CustomPlayer
        my_moves = game.get_active_moves()

        for move in my_moves:
            player.count += 1

            # Check all possible moves to see if a winner can be found
            new_board_state, is_over, winner = game.forecast_move(move)

            # Check to see if the game is ended while it is the AI's turn and after the next move
            next_moves_possible = new_board_state.get_active_moves()

            if is_over and len(next_moves_possible) == 0:
                return move, float("inf")

            else:
                # Recursively search through the game tree
                forecasted_move, forecasted_value = minimax(
                    player, new_board_state, time_left, depth=depth - 1, my_turn=not my_turn
                )

                if forecasted_value > max_value:
                    max_value = forecasted_value
                    best_move = move

        return best_move, max_value

    else:  # Opponents turn
        # Initialize values
        min_value = float("inf")
        best_move = None

        # Get possible moves of the CustomPlayer
        cpu_moves = game.get_active_moves()

        for move in cpu_moves:

            # Check all possible moves to see if a winner can be found
            new_board_state, is_over, winner = game.forecast_move(move)

            # Check to see if the game is ended while it is the opponents turn and after the next move
            next_moves_possible = new_board_state.get_active_moves()

            if is_over and len(next_moves_possible) == 0:
                return move, float("-inf")
            else:
                # Recursively search through the game tree
                forecasted_move, forecasted_value = minimax(
                    player, new_board_state, time_left, depth=depth - 1, my_turn=not my_turn
                )

                if forecasted_value < min_value:
                    min_value = forecasted_value
                    best_move = move

        return best_move, min_value


class CustomPlayer:
    """Player that chooses a move using your evaluation function
    and a minimax algorithm with alpha-beta pruning.
    You must finish and test this player to make sure it properly
    uses minimax and alpha-beta to return a good move."""

    def __init__(self, eval_fn=None, search_depth=3, output=None):
        """Initializes your player.

        if you find yourself with a superior eval function, update the default
        value of `eval_fn` to `CustomEvalFn()`

        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Evaluation function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth
        self.output = output
        self.count = 0

    def move(self, game, time_left):
        """Called to determine one move by your agent

        Note:
            1. Do NOT change the name of this 'move' function. We are going to call
            this function directly.
            2. Call alphabeta instead of minimax once implemented.
        Args:
            game (Board): The board and game state.
            time_left (function): Used to determine time left before timeout

        Returns:
            tuple: ((int,int),(int,int),(int,int)): Your best move
        """
        with self.output:
            self.output.append_stdout("Calculating best move...\n")
        # print("Calculating best move...")
        best_move, utility = minimax(self, game, time_left, depth=self.search_depth)

        with self.output:
            self.output.append_stdout(f"AI Player: Moving {best_move} with value {utility} \n")
            self.output.append_stdout(
                f"AI Player searched through {self.count} game states to find it's next move \n"
            )

        # print(f"AI Player: Moving {best_move} with value {utility}")
        # print(f"AI Player searched through {self.count} game states to find it's next move")
        # print("---------------------------")
        self.count = 0
        return best_move

    def utility(self, game, my_turn):
        """You can handle special cases here (e.g. endgame)"""
        return self.eval_fn.score(game, self)
