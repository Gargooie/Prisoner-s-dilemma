import random
import matplotlib.pyplot as plt
import inspect
import sys
from strategies_five import *
from players import *

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



def select_vs_select(player1, player2):
    for item in strategy_instances:
        if item.name == player1:
            strategy_chosen_1=item
    for item in strategy_instances:
        if item.name == player2:
            strategy_chosen_2=item
    # print('================================= играет ', strategy.name)
    result_score_1=0
    result_score_2=0
    for _ in range(1):

        
        player1 = Player("Игрок 1", strategy_chosen_1)
        player2 = Player("Игрок 2", strategy_chosen_2)
        game = Game(player1, player2)
        strategy_to_save=player1.strategy.name

        for _ in range(100):
            game.play_round()
            # print("**** очки за баттл: "  + str(player1.score_sum) + " vs " +  str(player2.score_sum)+ " *******************************************")
            # print(player1.round_scores)

        result_score_1+=player1.score_sum
        result_score_2+=player2.score_sum
        # print(result_score_1)

        #сохраняем итоговые суммы за раунд в общие суммы
        if player1.strategy.name in game_results:
            game_results[player1.strategy.name].extend(player1.round_scores)
        else:
            game_results[player1.strategy.name] =player1.round_scores
        if player2.strategy.name in game_results:
            game_results[player2.strategy.name].extend(player2.round_scores)
        else:
            game_results[player2.strategy.name] = player2.round_scores

                
        # print("^^^^^^^^^ resu1lt scores are: " + str(result_score_1)+" ^^^^^^^^^^^^^^^^^^^^^^^")

# select_vs_select()

def random_vs_random():
    for strategy in strategy_instances:
        # print('================================= играет ', strategy.name)
        result_score_1=0
        result_score_2=0
        for _ in range(10000):
            strategy_to_save=strategy.name
            
            player1 = Player("Игрок 1", strategy)
            player2 = Player("Игрок 2", random.choice(strategy_instances))
            game = Game(player1, player2)

            for _ in range(100):
                game.play_round()
                # print("**** очки за баттл: "  + str(player1.score_sum) + " vs " +  str(player2.score_sum)+ " *******************************************")
                # print(player1.round_scores)

            result_score_1+=player1.score_sum
            result_score_2+=player2.score_sum
            # print(result_score_1)

            #сохраняем итоговые суммы за раунд в общие суммы
            if player1.strategy.name in game_results:
                game_results[player1.strategy.name].extend(player1.round_scores)
            else:
                game_results[player1.strategy.name] =player1.round_scores
            if player2.strategy.name in game_results:
                game_results[player2.strategy.name].extend(player2.round_scores)
            else:
                game_results[player2.strategy.name] = player2.round_scores

                
        # print("^^^^^^^^^ resu1lt scores are: " + str(result_score_1)+" ^^^^^^^^^^^^^^^^^^^^^^^")

# random_vs_random()

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
        

def all_versus_all_mod()-> None:
    """
    один игрок играет с другим только один раз

    """

    # strategy_to_save=strategy_instances[i].name
    #создаем персонажа с каждой стратегией и создаем игру с ними
    players=[]
    player1 = Player("Игрок 1", TitForTat())
    player2 = Player("Игрок 2", Negative())
    player3 = Player("Игрок 3", Positive())
    player4 = Player("Игрок 4", Friedman())
    player5 = Player("Игрок 5", Detective())
    players.append(player1)
    players.append(player2)
    players.append(player3)
    players.append(player4)
    players.append(player5)
    game = Game(player1, player2)

    # print("match: " + strategy_instances[i].name + " vs " + strategy_instances[j].name)
    #играем раунды 2 игроков
    for _ in range(10):
        game.play_round()

    #Выводим в консоль результаты
    print("**** очки за баттл: "  + str(player1.score_sum) + " vs " +  str(player2.score_sum)+ " *******************************************")
    print(player1.round_scores)
    #сохраняем итоговые суммы за раунд в общие суммы
    # if strategy_instances[i].name in game_results:
    #     game_results[strategy_instances[i].name].extend(player1.round_scores)
    # else:
    #     game_results[strategy_instances[i].name] =player1.round_scores
    # if strategy_instances[j].name in game_results:
    #     game_results[strategy_instances[j].name].extend(player2.round_scores)
    # else:
    #     game_results[strategy_instances[j].name] = player2.round_scores


    # result_score_1+=player1.score_sum
    # result_score_2+=player2.score_sum

    # if strategy_to_save not in result_dict2:
    #     result_dict2[strategy_to_save] = []
    # result_dict2[strategy_to_save].extend(player1.round_scores)

all_versus_all_mod()
# print(filter(lambda obj: obj.name == 'TitForTatStrategy', strategy_instances))
print(Positive())
# print(strategy_instances[1].name)
# print(game_results)


for key, value in game_results.items():
    sum=0
    if key not in result_dict3:
        result_dict3[key] = []
    for x in value:
        sum+=x

        result_dict3[key].append(sum)
#сортировка по лучшим стратегиям
result_dict3 = dict(sorted(result_dict3.items(), key=lambda x: x[1][-1], reverse=True))



#выводим из словаря список игроков и их результат
for key, value in result_dict3.items():
    print(key, value[-1])

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