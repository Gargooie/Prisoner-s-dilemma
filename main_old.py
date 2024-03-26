import random
import matplotlib.pyplot as plt
import inspect
import sys
from strategies_five import *

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
        # self.round_scores_history = []

    def play_round(self):
        action1 = self.player1.choose_action()
        action2 = self.player2.choose_action()

        if action1 == "cooperate" and action2 == "cooperate":
            self.player1.round_score = 3
            self.player2.round_score = 3
        elif action1 == "cooperate" and action2 == "betray":
            self.player1.round_score = 0
            self.player2.round_score = 5
        elif action1 == "betray" and action2 == "cooperate":
            self.player1.round_score = 5
            self.player2.round_score = 0
        else:
            self.player1.round_score = 1
            self.player2.round_score = 1

        self.player1.score_sum += self.player1.round_score
        self.player2.score_sum += self.player2.round_score
        self.player1.scores.append(self.player1.score_sum)
        self.player2.scores.append(self.player2.score_sum)

        self.player1.round_scores.append(self.player1.round_score)
        self.player1.actions.append(action1)    
        self.player1.actions.append(action1)
        self.player1.opponent_actions.append(action2)
        self.player2.actions.append(action2)
        self.player2.opponent_actions.append(action1)

        # Сохраняем текущую промежуточную сумму и номер раунда в историю
        # self.round_scores_history.append((len(self.player1.scores), self.player1.strategy.name, self.player1.score_sum))
        # self.round_scores_history.append((len(self.player2.scores), self.player2.strategy.name, self.player2.score_sum))

        # print(f"Раунд: {len(self.player1.scores)}")
        # print(f"{self.player1.name} ({self.player1.strategy.name}) выбрал {action1} и получил {self.player1.round_score} очков.")
        # print(f"{self.player2.name} ({self.player2.strategy.name}) выбрал {action2} и получил {self.player2.round_score} очков.")
        # print(f"Очки {self.player1.name}: {self.player1.get_score_sum()}, очки {self.player2.name}: {self.player2.get_score_sum()}")

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

# Получаем все классы из модуля
all_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

# Фильтруем классы, чтобы оставить только те, которые унаследованы от Strategy
strategy_classes = [cls for name, cls in all_classes if issubclass(cls, Strategy) and cls != Strategy]

# Выводим список классов стратегий
strategy_instances = []
for strategy_class in strategy_classes:
    strategy_instance = strategy_class()
    strategy_instances.append(strategy_instance)



result_dict = []
result_dict2 = {}

for strategy in strategy_instances:
    strategy_to_save=strategy.name

    for _ in range(10):
        player1 = Player("Игрок 1", strategy)
        player2 = Player("Игрок 2", random.choice(strategy_instances))
        game = Game(player1, player2)

        for _ in range(10):
            game.play_round()

        if strategy_to_save not in result_dict2:
            result_dict2[strategy_to_save] = []
        result_dict2[strategy_to_save].extend(player1.round_scores)



result_dict3={}

for key, value in result_dict2.items():
    sum=0
    if key not in result_dict3:
        result_dict3[key] = []
    for x in value:
        sum+=x

        result_dict3[key].append(sum)

for key, value in result_dict3.items():
    plt.plot(value, label=key)

plt.xlabel('Раунд')
plt.ylabel('Очки')
plt.legend()
last_x = 200
# last_y = max(player1.score_sum, player2.score_sum)
# plt.annotate(f'({last_y})', xy=(last_x, last_y), xytext=(last_x, last_y-50),
#              arrowprops=dict(arrowstyle='->'))
plt.show()