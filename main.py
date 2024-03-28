import random
import matplotlib.pyplot as plt
import inspect
import sys
from strategies import *
from players import *
from collections import Counter

ROUNDS=10
CLEAR_PLAYERS=5

# Получаем все классы из модуля
all_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

# Фильтруем классы, чтобы оставить только те, которые унаследованы от Strategy
strategy_classes = [cls for name, cls in all_classes if issubclass(cls, Strategy) and cls != Strategy]

# print(strategy_classes)

# Выводим список классов стратегий
strategy_instances = []
for strategy_class in strategy_classes:
    strategy_instance = strategy_class()
    strategy_instances.append(strategy_instance)
# print(strategy_instances)

result_dict = {}
#словарь для таблицы наращивания ресурсов и вывода графика

game_results ={}
players=[]

def all_versus_all_mod(players)-> None:
    """
    один игрок играет с другим только один раз

    """
    if len(players) <2:
        print("Not enough players")
        # raise ValueError("Необходимо указать 2 игрока")
        # exit()

    players_copy=[]
    for player in players:
        players_copy.append(Player("Игрок", player.strategy))
    players=players_copy


    match = Game(*players)
    match.play_tournament(ROUNDS)

    
    #создадим словарь для игрока и его счета
    players_dict=[]
    for player in players:
        # print(player)
        players_dict.append((player.strategy.name, player.scores[-1]))
    #сортировка по суммам
    players_dict.sort(key=lambda x: x[1], reverse=True)

# Подсчет количества каждого элемента
    element_count = Counter(players_dict)
    for key, value in dict(element_count).items():
        print("{}x {} : {}".format(value, key[0], key[1] ))
    return players


def Culture(players):
    random.shuffle(players)
    players.sort(key=lambda x: x.scores[-1], reverse=True)
    del players[-CLEAR_PLAYERS:]
    players[:0]=players[:CLEAR_PLAYERS]
    return(players)

def play_game(players=None):
    # возвращаем в конце список игроков 
    result_game=[]

    if players == None:
        players=[]
    # players.append(Player("Игрок 1", TitForTat()))
    # players.append(Player("Игрок 2", Negative()))
    # players.append(Player("Игрок 3", Positive()))
    # players.append(Player("Игрок 4", Friedman()))
    # players.append(Player("Игрок 5", Detective()))

# [players.append(Player("Игрок", Positive()))  for _ in range(15)]
# [players.append(Player("Игрок", Negative()))  for _ in range(5) ]
# [players.append(Player("Игрок", TitForTat())) for _ in range(5) ]

# for _ in range(3):
#     players.append(Player("Игрок", Sample()))
# for _ in range(3):
#     players.append(Player("Игрок", Simpleton()))
# for _ in range(3):
#     players.append(Player("Игрок", Random()))
# for _ in range(3):
#     players.append(Player("Игрок", TitForTat()))
# for _ in range(13):
#     players.append(Player("Игрок", Negative()))

# for _ in range(4):
#     players.append(Player("Игрок", Random()))


    for _ in range(45):
        # result_game=[]
        #игра не прерывается последним оставшимся
        endless_game = True
        if len(players)<2:
            # остался один
            break
        
        players=all_versus_all_mod(players)
        if players!=[]:
            result_game=players[:]
        players = Culture(players)
        print()
        #если все одинаковые то остановить игру
        if not endless_game:
            if len({player.strategy.name for player in players })==1:
                players=all_versus_all_mod(players)
                players = Culture(players)
                print(players[0].strategy.name, "остался один")
                break


    return result_game

def test_game():
    
    players=[]
    players.append(Player("Игрок 1", User()))
    players.append(Player("Игрок 2", Negative()))
    players.append(Player("Игрок 3", Positive()))
    players.append(Player("Игрок 4", Friedman()))
    players.append(Player("Игрок 5", Detective()))
    answer = play_game(players)

    # assert answer[0].scores[-1] == 57 and answer[0].strategy.name == "TitForTat"
    # assert answer[1].scores[-1] == 45 and answer[1].strategy.name == "Negative"
    # assert answer[2].scores[-1] == 29 and answer[2].strategy.name == "Positive"
    # assert answer[3].scores[-1] == 46 and answer[3].strategy.name == "Friedman"
    # assert answer[4].scores[-1] == 45 and answer[4].strategy.name == "Detective"
    return answer

new_results=test_game()

#выводим из словаря список игроков и их результат
# for key, value in result_dict.items():
#     print(key, value[-1])
#сортировка по лучшим стратегиям
new_results = sorted(new_results, key=lambda x: x.scores[-1], reverse=True)


#заносим все в график
for player in new_results:
    plt.plot(player.scores, label=player.strategy.name)

plt.xlabel('Раунд')
plt.ylabel('Очки')
plt.legend()
last_x = len(new_results[0].scores)
last_y = new_results[0].score_sum
plt.annotate(f'{last_y}', xy=(last_x, last_y), xytext=(last_x, last_y-10),
             arrowprops=dict(arrowstyle='->'))
plt.show()