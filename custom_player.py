# Heuristic for evluation of the board state
class OpenMoveEvalFn:
    def score(self, game, my_player=None):
        """Score the current game state
        Evaluation function that outputs a score equal to how many
        moves are open for AI player on the board minus how many moves
        are open for Opponent's player on the board.

        Note:
            If you think of better evaluation function, do it in CustomEvalFn below.

            Args
                game (Board): The board and game state.
                my_player (Player object): This specifies which player you are.

            Returns:
                float: The current state's score. MyMoves-OppMoves.

            """
        # Simple crude heuristic which favours the number of possible moves our AI has in comparison
        # to the other player. CustomPlayer is always trying to maximize this value
        # and RandomPlayer is trying to minimimize
        if my_player:

            num_active_moves_my_player = game.get_player_moves(my_player=my_player)
            num_active_moves_opponent = game.get_opponent_moves(my_player=my_player)

        else:
            num_active_moves_my_player = game.get_opponent_moves(my_player=my_player)
            num_active_moves_opponent = game.get_player_moves(my_player=my_player)

        return len(num_active_moves_my_player) - len(num_active_moves_opponent)


# Algorithm for finding the best move
def minimax(player, game, time_left, depth, my_turn=True):
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
    player.count += 1

    # Determine whose turn it is
    if my_turn:
        ai_player = game.get_active_player()
        cpu_player = game.get_inactive_player()

    else:
        ai_player = game.get_inactive_player()
        cpu_player = game.get_active_player()

    ai_moves = game.get_player_moves(my_player=ai_player)
    cpu_moves = game.get_opponent_moves(my_player=ai_player)

    # Handle time running out
    # TODO
    # print(f"Time left {time_left()}")
    #     if time_left() < 10:
    #         return None, None

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

        #         # Get possible moves of the CustomPlayer
        #         ai_moves = game.get_player_moves(my_player=current_player)

        for move in ai_moves:
            #             print(f"Possible Move: {move}")

            # Check all possible moves to see if a winner can be found
            new_board_state, is_over, winner = game.forecast_move(move)

            # Check to see if the game is ended while it is the AI's turn and after the next move
            next_moves_possible = new_board_state.get_player_moves(my_player=ai_player)

            if is_over and len(next_moves_possible) == 0:
                #                 print(f"AI Player: Game is over with move {move}")
                return move, float("inf")

            else:
                #                 print(f"Searching game tree for move {move}")
                # Recursively search through the game tree
                forecasted_move, forecasted_value = minimax(
                    ai_player, new_board_state, time_left, depth=depth - 1, my_turn=False
                )

                if forecasted_value > max_value:
                    #                     print(f"Swapping Max Value {max_value} with forecasted value {forecasted_value} with move {forecasted_move}")
                    max_value = forecasted_value
                    best_move = move
                    # print(f"Found new best move: {best_move} with value {max_value}")

        #         print(f"Returning Best Move {best_move} with value {max_value}")
        #         print()
        return best_move, max_value

    else:  # Opponents turn

        # Initialize values
        min_value = float("inf")
        best_move = None

        #         # Get possible moves of the CustomPlayer
        #         cpu_moves = game.get_opponent_moves(my_player=current_player)

        for move in cpu_moves:
            #             print(f"Possible Move: {move}")

            # Check all possible moves to see if a winner can be found
            new_board_state, is_over, winner = game.forecast_move(move)

            # Check to see if the game is ended while it is the opponents turn and after the next move
            next_moves_possible = new_board_state.get_opponent_moves(my_player=ai_player)

            if is_over and len(next_moves_possible) == 0:
                #                 print(f"Opponent Player: Game is over with move {move}")
                return move, float("-inf")
            else:
                #                 print(f"Searching game tree for move {move}")
                # Recursively search through the game tree
                forecasted_move, forecasted_value = minimax(
                    ai_player, new_board_state, time_left, depth=depth - 1, my_turn=True
                )

                if forecasted_value < min_value:
                    #                     print(f"Swapping Max Value {min_value} with forecasted value {forecasted_value} with move {forecasted_move}")
                    min_value = forecasted_value
                    best_move = move
                    print(f"Finding Opponents best move: {best_move} with value {min_value}")

        #         print(f"Returning Best Move {best_move} with value {min_value}")
        #         print()
        return best_move, min_value


class CustomAIPlayer:
    # TODO: finish this class!
    """Player that chooses a move using your evaluation function
    and a minimax algorithm with alpha-beta pruning.
    You must finish and test this player to make sure it properly
    uses minimax and alpha-beta to return a good move."""

    def __init__(self, search_depth=3, eval_fn=OpenMoveEvalFn()):
        """Initializes your player.

        if you find yourself with a superior eval function, update the default
        value of `eval_fn` to `CustomEvalFn()`

        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Evaluation function used by your agent
        """
        self.eval_fn = eval_fn
        self.search_depth = search_depth
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
        print("Calculating best move...")
        best_move, utility = minimax(self, game, time_left, depth=self.search_depth)
        print(f"AI Player: Moving {best_move} with value {utility}")
        print(f"AI Player searched through {self.count} game states to find it's next move")
        print("---------------------------")
        self.count = 0
        return best_move

    def utility(self, game, my_turn):
        """You can handle special cases here (e.g. endgame)"""
        return self.eval_fn.score(game, self)
