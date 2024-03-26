import random
import matplotlib.pyplot as plt
import inspect
import sys
from strategies import *
from players import *
from collections import Counter

ROUNDS=10

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
#меняем порядок
strategy_instances_copy=[]
for item in strategy_instances:
    if item.name == "TitForTat":
        strategy_instances_copy.append(item)

for item in strategy_instances:
    if item.name != "TitForTat":
        strategy_instances_copy.append(item)

strategy_instances=strategy_instances_copy

# print("================================================================")

result_dict = []
result_dict2 = {}
#словарь для таблицы наращивания ресурсов и вывода графика
result_dict3={}
game_results ={}




def all_versus_all()-> None:
    """
    один игрок играет с другим только один раз

    """
    #перебираем стратегии по разу
    for i in range(len(strategy_instances)-1):
        result_score_1=0
        result_score_2=0
        #идем циклом по любой другой стратегии один раз
        for j in range(i+1, len(strategy_instances)):
            strategy_to_save=strategy_instances[i].name
            #создаем персонажа с каждой стратегией и создаем игру с ними
            player1 = Player("Игрок 1", strategy_instances[i])
            player2 = Player("Игрок 2", strategy_instances[j])
            game = Game(player1, player2)

            print("match: " + strategy_instances[i].name + " vs " + strategy_instances[j].name)
            #играем раунды 2 игроков
            for _ in range(10):
                game.play_round()

            #Выводим в консоль результаты
            print("**** очки за баттл: "  + str(player1.score_sum) + " vs " +  str(player2.score_sum)+ " *******************************************")
            print(player1.round_scores)
            #сохраняем итоговые суммы за раунд в общие суммы
            if strategy_instances[i].name in game_results:
                game_results[strategy_instances[i].name].extend(player1.round_scores)
            else:
                game_results[strategy_instances[i].name] =player1.round_scores
            if strategy_instances[j].name in game_results:
                game_results[strategy_instances[j].name].extend(player2.round_scores)
            else:
                game_results[strategy_instances[j].name] = player2.round_scores


            result_score_1+=player1.score_sum
            result_score_2+=player2.score_sum

            if strategy_to_save not in result_dict2:
                result_dict2[strategy_to_save] = []
            result_dict2[strategy_to_save].extend(player1.round_scores)

        print("^^^^^^^^^ result scores are: " + str(result_score_1)+" : "+ str(result_score_2)+" ^^^^^^^^^^^^^^^^^^^^^^^")

# all_versus_all()
        

def all_versus_all_mod(players)-> None:
    """
    один игрок играет с другим только один раз

    """
    if len(players) <2:
        print("Not enough players")
        exit()

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
    player_best=players[:5]
    
    del players[-5:]
    players[:0]=players[:5]


    return(players)


players=[]
# players.append(Player("Игрок 1", TitForTat()))
# players.append(Player("Игрок 2", Negative()))
# players.append(Player("Игрок 3", Positive()))
# players.append(Player("Игрок 4", Friedman()))
# players.append(Player("Игрок 5", Detective()))

# for _ in range(15):
#     players.append(Player("Игрок", Positive()))
# for _ in range(5):
#     players.append(Player("Игрок", Negative()))
# for _ in range(5):
#     players.append(Player("Игрок", TitForTat()))

for _ in range(3):
    players.append(Player("Игрок", Sample()))
for _ in range(3):
    players.append(Player("Игрок", Simpleton()))
for _ in range(3):
    players.append(Player("Игрок", Random()))
for _ in range(3):
    players.append(Player("Игрок", TitForTat()))
for _ in range(13):
    players.append(Player("Игрок", Negative()))

# for _ in range(25):
#     players.append(Player("Игрок", Random()))


for _ in range(45):
    endless_game = False
    players=all_versus_all_mod(players)
    players = Culture(players)
    print()
    #если все одинаковые то остановить игру
    if not endless_game:
        if len({player.strategy.name for player in players })==1:
            players=all_versus_all_mod(players)
            players = Culture(players)
            break


for key, value in game_results.items():
    sum=0
    if key not in result_dict3:
        result_dict3[key] = []
    for x in value:
        sum+=x

        result_dict3[key].append(sum)
#сортировка по лучшим стратегиям
result_dict3 = dict(sorted(result_dict3.items(), key=lambda x: x[1][-1], reverse=True))


# for player in players:
#     print(player.all_rounds_scores)
#     print(player.scores)
#выводим из словаря список игроков и их результат
for key, value in result_dict3.items():
    print(key, value[-1])

#заносим все в график
for player in players:
    plt.plot(player.scores, label=player.strategy.name)

#заносим все в график
for key, value in result_dict3.items():
    plt.plot(value, label=key)

plt.xlabel('Раунд')
plt.ylabel('Очки')
# plt.legend()
# last_x = 200
# last_y = max(player1.score_sum, player2.score_sum)
# plt.annotate(f'({last_y})', xy=(last_x, last_y), xytext=(last_x, last_y-50),
#              arrowprops=dict(arrowstyle='->'))
# plt.show()