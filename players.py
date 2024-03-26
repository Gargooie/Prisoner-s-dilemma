#[win-win, win-lose, lose-win, lose-lose]
versatile=[3,5,0,1]
asian=[2,3,-1,0]
score_table=asian

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.round_score = 0
        self.round_scores = []
        self.score_sum = 0
        self.scores = []
        self.strategy = strategy
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

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play_round(self):
        action1 = self.player1.choose_action()
        action2 = self.player2.choose_action()

        if action1 == "cooperate" and action2 == "cooperate":
            self.player1.round_score = score_table[0]
            self.player2.round_score = score_table[0]
        elif action1 == "cooperate" and action2 == "betray":
            self.player1.round_score = score_table[2]
            self.player2.round_score = score_table[1]
        elif action1 == "betray" and action2 == "cooperate":
            self.player1.round_score = score_table[1]
            self.player2.round_score = score_table[2]
        else:
            self.player1.round_score = score_table[3]
            self.player2.round_score = score_table[3]


        self.player1.score_sum += self.player1.round_score
        self.player2.score_sum += self.player2.round_score
        self.player1.scores.append(self.player1.score_sum)
        self.player2.scores.append(self.player2.score_sum)

        self.player1.round_scores.append(self.player1.round_score)
        self.player2.round_scores.append(self.player2.round_score)
        self.player1.actions.append(action1)    
        self.player1.opponent_actions.append(action2)
        self.player2.actions.append(action2)
        self.player2.opponent_actions.append(action1)

        print(f"Раунд: {len(self.player1.scores)}")
        print(f"{self.player1.name} ({self.player1.strategy.name}) выбрал {action1} и получил {self.player1.round_score} очков.")
        print(f"{self.player2.name} ({self.player2.strategy.name}) выбрал {action2} и получил {self.player2.round_score} очков.")
        print(f"Очки {self.player1.name}: {self.player1.get_score_sum()}, очки {self.player2.name}: {self.player2.get_score_sum()}")

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
