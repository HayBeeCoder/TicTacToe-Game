



class BotPlay():

    wining_moves = [["1", "4", "7"],["2","5","8"],["3","6","9"],
    ["1", "2", "3"],["4","5","6"],["7","8","9"],
    ["1", "5", "9"],["3","5","7"]]

    def __init__(self, bot_moves, player_moves):
        self.bot_moves = bot_moves
        self.player_moves = player_moves


    def check_player_win_move(self, player_moves, other_move):
        for i in range(1,10):
            if str(i) not in player_moves:
                player_moves.append(str(i))
                print(player_moves)
                if self.can_win(player_moves) and str(i) not in other_move:
                    player_moves.pop()
                    return str(i)
                player_moves.pop()
        return False

    def can_win(self, moves):
        for winning_move in self.wining_moves:
            if set(winning_move) & set(moves) == set(winning_move):
                return True
            print("No")
        return False
    
    def play_in_the_middle_or_elsewhere(self):
        if "5" not in self.player_moves and "5" not in self.bot_moves:
            print("Middle")
            return "5"
        
        edge_moves = ["1", "3", "7", "9"]
        for move in edge_moves:
            print("This is player move: ", self.player_moves)
            if move not in self.player_moves and move not in self.bot_moves:
                print("Edge")
                return move

        other_moves = ["2", "4", "6", "8"]

        for move in other_moves:
            if move not in self.player_moves and move not in self.bot_moves:
                print("Player_move:", self.player_moves, move)
                print("Edge me")
                return move



