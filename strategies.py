import random
# from main import MISTAKES_RATIO

MISTAKES_RATIO= 0.00

class Strategy:
    def __init__(self, name):
        self.name = name

    def choose_action(self, player_actions, opponent_actions):
        pass

    def proceed(self, action):
        if random.random() < MISTAKES_RATIO:
            if action == "betray":
                return "cooperate"
            else:
                return "betray"
        return action
    
class User(Strategy):
    """
    Класс игрок
    
    """
    def __init__(self):
        self.name = "User"
        self.auto=""
    def choose_action(self, player_actions, opponent_actions):
        if self.auto=="4":
            return random.choice(["cooperate", "betray"])
        elif self.auto=="11":
            return "cooperate"
        elif self.auto=="00":
            return "betray"
        while True:
            action= input("Ваш ход, сотрудничать(1) / предать(0). Всегда сотрудничество(11), всегда предать(00). Рандом(4): ")
            if action not in ["0", "1", "11", "00", "4"]:
                print("Ошибка ввода.")
                continue
            else:
                break
        if action == "1":
            return "cooperate"
        elif action == "0":
            return "betray"
        if action == "11":
            self.auto="11"
            return "cooperate"
        if action == "00":
            self.auto="00"
            return "betray"
        elif action == "4":
            self.auto="4"
            return random.choice(["cooperate", "betray"])

class Positive(Strategy):
    """
    Класс всегда сотрудничество
    
    """
    def __init__(self):
        self.name = "Positive"
    def choose_action(self, player_actions, opponent_actions):
        return self.proceed("cooperate")

class Negative(Strategy):
    """
    Класс всегда предательство

    """
    def __init__(self):
        self.name = "Negative"
    def choose_action(self, player_actions, opponent_actions):
        return self.proceed("betray")

class Majority(Strategy):
    """
    Класс Следование мажоритарному выбору: Игрок анализирует предыдущие ходы другого заключенного и выбирает наиболее популярный ход.
    не протестирован
    """
    def __init__(self):
        self.name = "Majority"
    def choose_action(self, player_actions, opponent_actions):
        cooperate_count = opponent_actions.count("cooperate")
        betray_count = opponent_actions.count("betray")
        if cooperate_count > betray_count:
            return self.proceed("cooperate")
        else:
            return self.proceed("betray")

class Random(Strategy):
    """
    Класс случайных чисел
    не протестирован
    """
    def __init__(self):
        self.name = "random"
    def choose_action(self, player_actions, opponent_actions):

        return self.proceed(random.choice(["cooperate","betray"]))

class Sample(Strategy):
    """
    Класс Sample, начинает с сотрудничества. Если предают 2 раза предает один раз
    не протестирован
    """
    def __init__(self):
        self.name = "Sample"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions[-2:] == ["betray", "betray"]:
            return self.proceed("betray")
        else:
            return self.proceed("cooperate")

class Friedman(Strategy):
    """
    Класс Фридман, начинает с сотрудничества. Если предают 1 раз начинает предавать всегда
    """
    def __init__(self):
        self.name = "Friedman"
        self.betrayed = False

    def choose_action(self, player_actions, opponent_actions):
        self.betrayed = False
        if opponent_actions and "betray" in opponent_actions:
            self.betrayed = True

        if self.betrayed:

            return self.proceed("betray")
        else:
            return self.proceed("cooperate")
        
class JossStrategy(Strategy):
    """
    Класс Джосс, начинает с сотрудничества. Следующий раунд это копия предыдущего у соперника.
    С 10% вероятностью предательство 
    не протестирован
    """
    def __init__(self):
        self.name = "Joss"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and (opponent_actions[-1] == "betray" or random.random() < 0.1):
            return self.proceed("betray")
        else:
            return self.proceed("cooperate")

class GrassmanStrategy(Strategy):
    """
    Класс Грассман, копия око за око + каждый 50ый раунд предает 
    не протестирован
    """
    def __init__(self):
        self.name = "Grassman"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and (opponent_actions[-1] == "betray" or len(opponent_actions)==50):
            return self.proceed("betray")
        else:
            return self.proceed("cooperate")

class TitForTat(Strategy):
    """
    Класс Око за око, начинает с сотрудничества, копирут действие соперника
    """
    def __init__(self):
        self.name = "TitForTat"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and opponent_actions[-1] == "betray":
            return self.proceed("betray")
        else:
            return self.proceed("cooperate")

class TitForTatWithForgiveness(Strategy):
    """
    Класс TitForTatWithForgiveness, начинает с сотрудничества и прощает иногда.
    не протестирован
    """
    def __init__(self, forgiveness_probability=0.1):
        self.name = "TitForTatWithForgiveness"
        self.forgiveness_probability = forgiveness_probability

    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and random.random() < self.forgiveness_probability:
            return self.proceed("cooperate")
        elif opponent_actions:
            return self.proceed(opponent_actions[-1])
        else:
            return self.proceed("cooperate")

class TitForTatWithRandom(Strategy):
    """
    Класс TitForTatWithRandom, око за око + сотрудничество случайным образом.
    не протестирован
    """
    def __init__(self, betray_probability=0.5):
        self.name = "TitForTatWithRandom"
        self.betray_probability = betray_probability

    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and opponent_actions[-1] == "betray":
            return self.proceed("betray") if random.random() < self.betray_probability else self.proceed("cooperate")
        else:
            return self.proceed("cooperate")

class Reversed(Strategy):
    """
    Класс Обратная стратегия: Игрок всегда выбирает противоположный ход по сравнению с предыдущим ходом другого игрока.
    не протестирован
    """
    def __init__(self):
        self.name = "Reversed"
    def choose_action(self, player_actions, opponent_actions):
        if len(opponent_actions) == 0:
            return self.proceed("cooperate")
        elif opponent_actions[-1] == "cooperate":
            return self.proceed("betray")
        else:
            return self.proceed("cooperate")
        
class Pessimistic(Strategy):
    """
    Класс Pessimistic, всегда начинает с измены и продолжает, пока противник не сотрудничает.
    не протестирован
    """
    def __init__(self):
        self.name = "Pessimistic"
#todo почему из всего списка проверка? он не может знать текущее действие
    def choose_action(self, player_actions, opponent_actions):
        if "cooperate" in opponent_actions:
            return self.proceed("cooperate")
        else:
            return self.proceed("betray")

class Detective(Strategy):
    """
    Класс Detective, начинает с последовательности cooperate, betray, cooperate, cooperate.
    Если соперник предал хотя бы один раз, повторяет действия соперника, иначе всегда предает.
    """
    def __init__(self):
        self.name = "Detective"
        self.detective_actions = ["cooperate", "betray", "cooperate", "cooperate"]
        self.copy_opponent = False

    def choose_action(self, player_actions, opponent_actions):
        self.copy_opponent = False
        if len(opponent_actions) < len(self.detective_actions):
            return self.proceed(self.detective_actions[len(opponent_actions)])
        
        if "betray" in opponent_actions:
            self.copy_opponent = True

        if self.copy_opponent:
            return self.proceed(opponent_actions[-1])
        else:
            return self.proceed("betray")
        

class Simpleton(Strategy):
    """
    Класс Simpleton, начинает с сотрудничества. Если оппонент сотрудничает, повторяет свое прошлое действие. Если оппонент предал, повторяет обратное своему прошлому действию.
    """
    def __init__(self):
        self.name = "Simpleton"

    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and opponent_actions[-1] == "betray":
            return self.proceed(player_actions[-1])
        elif opponent_actions:
            return self.proceed("cooperate") if player_actions[-1]=="cooperate" else self.proceed("betray")
        else:
            return self.proceed("cooperate")
