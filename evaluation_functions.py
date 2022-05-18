# Heuristic for evluation of the board state
from custom_player import CustomPlayer


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
        if isinstance(my_player, CustomPlayer):

            num_active_moves_my_player = game.get_player_moves(my_player=my_player)
            num_active_moves_opponent = game.get_opponent_moves(my_player=my_player)

        else:
            num_active_moves_my_player = game.get_opponent_moves(my_player=my_player)
            num_active_moves_opponent = game.get_player_moves(my_player=my_player)

        return len(num_active_moves_my_player) - len(num_active_moves_opponent)


class DefensiveEvalFn:
    def __init__(self):
        pass

    def score(self, game, my_player=None):
        """Score the current game state.

        The defensive heuristic favors maximizing the player’s available moves at a weighted
        cost against those available to the opponent. This has the effect of strongly
        preferring to keep the player’s moves larger at all costs against the opponent

        Eval Function == Number of my_player moves * 2 - my_opponent moves

        Args:
            game (Board): The board and game state.
            my_player (Player object): This specifies which player you are.

        Returns:
            float: The current state's score, based on your own heuristic.
        """

        if isinstance(my_player, CustomPlayer):
            my_moves = game.get_player_moves(my_player=my_player)
            opp_moves = game.get_opponent_moves(my_player=my_player)

        else:
            my_moves = game.get_opponent_moves(my_player=my_player)
            opp_moves = game.get_player_moves(my_player=my_player)

        return (len(my_moves) * 2) - len(opp_moves)


class OffensiveEvalFn:
    def __init__(self):
        pass

    def score(self, game, my_player=None):
        """Score the current game state.

        By contrast to the defensive strategy, the offensive heuristic favors minimizing the
        opponent’s available moves at a weighted cost against those available to the player.
        This achieves an aggressive style of game play, attempting to force or limit the
        opponent into a weaker game position

        Eval Function == Number of my_player moves - my_opponent moves * 2

        Args:
            game (Board): The board and game state.
            my_player (Player object): This specifies which player you are.

        Returns:
            float: The current state's score, based on your own heuristic.
        """

        if isinstance(my_player, CustomPlayer):
            my_moves = game.get_player_moves(my_player=my_player)
            opp_moves = game.get_opponent_moves(my_player=my_player)

        else:
            my_moves = game.get_opponent_moves(my_player=my_player)
            opp_moves = game.get_player_moves(my_player=my_player)

        return len(my_moves) - (len(opp_moves) * 2)


class DefenseToOffenseEvalFn:
    def __init__(self):
        pass

    def score(self, game, my_player=None):
        """Score the current game state.

        The defensive to offensive heuristic applies an early-game defensive strategy, where the
        player tries to initially maximize the number of available moves. After a period half-way
        through the game, the heuristic switches to offensive, attempting to limit and block
        the opponent.

        This is achieved by taking into account a ratio value, computed from the current round
        divided by the game board size. When the number of rounds in the game is less than
        half-way through, the heuristic employs a defensive strategy. Afterwards, an
        offensive strategy is utilized

        Args:
            game (Board): The board and game state.
            my_player (Player object): This specifies which player you are.

        Returns:
            float: The current state's score, based on your own heuristic.
        """

        if isinstance(my_player, CustomPlayer):
            my_moves = game.get_player_moves(my_player=my_player)
            opp_moves = game.get_opponent_moves(my_player=my_player)

        else:
            my_moves = game.get_opponent_moves(my_player=my_player)
            opp_moves = game.get_player_moves(my_player=my_player)

        board_size = game.width * game.height
        ratio = game.move_count / board_size

        if ratio <= 0.5:
            return (len(my_moves) * 2) - len(opp_moves)
        else:
            return len(my_moves) - (len(opp_moves) * 2)


class OffenseToDefenseEvalFn:
    def __init__(self):
        pass

    def score(self, game, my_player=None):
        """Score the current game state.

        The offensive to defensive heuristic applies an early-game offensive strategy, where the
        player tries to initially minimize the number of available moves for the opponent. After
        a period half-way through the game, the heuristic switches to defensive, attempting to
        maximize the number of available moves open to the AI agent

        This is achieved by taking into account a ratio value, computed from the current round
        divided by the game board size. When the number of rounds in the game is less than
        half-way through, the heuristic employs a defensive strategy. Afterwards, an
        offensive strategy is utilized

        Args:
            game (Board): The board and game state.
            my_player (Player object): This specifies which player you are.

        Returns:
            float: The current state's score, based on your own heuristic.
        """

        if isinstance(my_player, CustomPlayer):
            my_moves = game.get_player_moves(my_player=my_player)
            opp_moves = game.get_opponent_moves(my_player=my_player)

        else:
            my_moves = game.get_opponent_moves(my_player=my_player)
            opp_moves = game.get_player_moves(my_player=my_player)

        board_size = game.width * game.height
        ratio = game.move_count / board_size

        if ratio <= 0.5:
            return len(my_moves) - (len(opp_moves) * 2)
        else:
            return (len(my_moves) * 2) - len(opp_moves)
