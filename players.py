#[win-win, win-lose, lose-win, lose-lose]
versatile=[3,5,0,1]
asian=[2,3,-1,0]
score_table=asian

class Player:
    def __init__(self, name, strategy):
        self.name = name if name is not None else "Игрок"
        self.round_score = 0
        self.round_scores = []
        self.all_rounds_scores=[]
        self.score_sum = 0
        self.scores = []
        self.strategy = strategy if strategy is not None else self.Titfortat()
        self.actions = []  # Добавляем список действий соперника
        self.opponent_actions = []  # Добавляем список действий соперника

    def cooperate(self):
        return "cooperate"

    def betray(self):
        return "betray"

    def choose_action(self):
        return self.strategy.choose_action(self.actions, self.opponent_actions)

    def get_score_sum(self):
        return self.score_sum

    def reset_scores(self):
        self.round_score=0
        self.round_scores = []
        self.all_rounds_scores=[]
        self.score_sum = 0
        self.scores = []
        self.actions = []
        self.opponent_actions = []

class Game:
    def __init__(self, *args):
        self.players=[]
        for item in args:
            self.players.append(item)
        self.player1 = args[0]
        self.player2 = args[1]



    def play_round(self, player1, player2):
        action1 = player1.choose_action()
        action2 = player2.choose_action()



        if action1 == "cooperate" and action2 == "cooperate":
            player1.round_score = score_table[0]
            player2.round_score = score_table[0]
        elif action1 == "cooperate" and action2 == "betray":
            player1.round_score = score_table[2]
            player2.round_score = score_table[1]
        elif action1 == "betray" and action2 == "cooperate":
            player1.round_score = score_table[1]
            player2.round_score = score_table[2]
        else:
            player1.round_score = score_table[3]
            player2.round_score = score_table[3]


        player1.score_sum += player1.round_score
        player2.score_sum += player2.round_score
        player1.scores.append(player1.score_sum)
        player2.scores.append(player2.score_sum)

        player1.round_scores.append(player1.round_score)
        player2.round_scores.append(player2.round_score)
        player1.all_rounds_scores.append(player1.round_score)
        player2.all_rounds_scores.append(player2.round_score)
        player1.actions.append(action1)    
        player1.opponent_actions.append(action2)
        player2.actions.append(action2)
        player2.opponent_actions.append(action1)

        # print(f"{player1.name} ({player1.strategy.name}) выбрал {action1} и получил {player1.round_score} очков.")
        # print(f"{player2.name} ({player2.strategy.name}) выбрал {action2} и получил {player2.round_score} очков.")
        # print(f"Очки {player1.name}: {player1.score_sum}, очки {player2.name}: {player2.get_score_sum()}")
        # print(f"1 игрок очки списком: {player1.round_scores}")
        # print(f"очки очки сумма: {sum(player1.round_scores)}")
        return sum(player1.round_scores), sum(player1.round_scores)


    def play_tournament(self, rounds):
        counter=0
        for player in self.players[:-1]:
            counter+=1
            for opponent in self.players[counter:]:

                self.play_match(player, opponent, rounds)



    def play_match(self, player1, player2, rounds=10):
        # print(f"Матч: {player1.strategy.name} vs {player2.strategy.name}:")
        player1.actions=[]
        player1.opponent_actions=[]
        player1.round_scores=[]

        player2.actions=[]
        player2.opponent_actions=[]
        player2.round_scores=[]

        for i in range(rounds):
            # print(f"Раунд: {i+1}")
            match_scores=self.play_round(player1, player2)
        # print("Результат матча: {} : {}".format(match_scores[0], match_scores[1]))

    def reset_scores(self):
        self.player1.round_score = 0
        self.player2.round_score = 0

        # Обнуляем суммарные очки
        self.player1.score_sum = 0
        self.player2.score_sum = 0

        # Очищаем историю ходов
        self.player1.scores = []
        self.player2.scores = []
        self.player1.actions = []
        self.player1.opponent_actions = []
        self.player2.actions = []
        self.player2.opponent_actions = []
