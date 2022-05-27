
class Game:

    def __init__(self,id):
        self.p1_move = False
        self.p2_move =False
        self.ready = False
        self.id = id             # for each game we make a new id
        self.moves = [None,None]
        self.wins = [0,0]        # winner counter for each player
        self.ties = 0

    def get_player_movement(self,player):
        """
        this function return player0/1 move
        :param player:[0,1]
        :return:player move
        """
        return self.moves[player]

    def player_move_update(self,player,move):
        """
        This function updates the moves list
        :param player:
        :param move:
        :return:
        """
        self.moves[player] = move
        if player == 0 :
            self.p1_move = True
        else:
            self.p2_move = True

    def connected(self):
        """
        This function check if two players currently connected to game
        :return:
        """
        return self.ready

    def players_both_moves(self):
        """
        This function check if both players made their move
        :return:
        """
        return self.p1_move and self.p2_move

    def winner_of_the_game(self):
        """
        This function check which player won the game
        in such way that win_p = 0 -> player 1 win and
        win_p = 1 - > player 2 win
        :return:
        """
        posible_win=['PR','RS','SP']
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]
        if p1 + p2 in posible_win :
            winner = 0
        elif p2 + p1 in posible_win :
            winner = 1
        else:
            winner = -1
        return winner

    def reset_game(self):
        """
        This function reset the game
        :return:
        """
        self.p1_move = False
        self.p2_move = False

