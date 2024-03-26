import random


mistake_ratio=0.05

class Strategy:
    def __init__(self, name):
        self.name = name
        self.mistake_ratio= mistake_ratio

    def choose_action(self, player_actions, opponent_actions):
        pass

class Positive(Strategy):
    """
    Класс всегда сотрудничество
    
    """
    def __init__(self):
        self.name = "Positive"
    def choose_action(self, player_actions, opponent_actions):
        return "cooperate"

class Negative(Strategy):
    """
    Класс всегда предательство

    """
    def __init__(self):
        self.name = "Negative"
    def choose_action(self, player_actions, opponent_actions):
        return "betray"

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
            return "cooperate"
        else:
            return "betray"

class RandomStrategy(Strategy):
    """
    Класс случайных чисел
    не протестирован
    """
    def __init__(self):
        self.name = "random"
    def choose_action(self, player_actions, opponent_actions):
        return random.choice(["cooperate", "betray"])

class SampleStrategy(Strategy):
    """
    Класс Sample, начинает с сотрудничества. Если предают 2 раза предает один раз
    не протестирован
    """
    def __init__(self):
        self.name = "Sample"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions[-2:] == ["betray", "betray"]:
            return "betray"
        else:
            return "cooperate"

class FriedmanStrategy(Strategy):
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

            return "betray"
        else:
            return "cooperate"
        
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
            return "betray"
        else:
            return "cooperate"

class GrassmanStrategy(Strategy):
    """
    Класс Грассман, копия око за око + каждый 50ый раунд предает 
    не протестирован
    """
    def __init__(self):
        self.name = "Grassman"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and (opponent_actions[-1] == "betray" or len(opponent_actions)==50):
            return "betray"
        else:
            return "cooperate"

class TitForTatStrategy(Strategy):
    """
    Класс Око за око, начинает с сотрудничества, копирут действие соперника
    """
    def __init__(self):
        self.name = "TitForTat"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and opponent_actions[-1] == "betray":
            return "betray"
        else:
            return "cooperate"

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
            return "cooperate"
        elif opponent_actions:
            return opponent_actions[-1]
        else:
            return "cooperate"

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
            return "betray" if random.random() < self.betray_probability else "cooperate"
        else:
            return "cooperate"

class Reversed(Strategy):
    """
    Класс Обратная стратегия: Игрок всегда выбирает противоположный ход по сравнению с предыдущим ходом другого игрока.
    не протестирован
    """
    def __init__(self):
        self.name = "Reversed"
    def choose_action(self, player_actions, opponent_actions):
        if len(opponent_actions) == 0:
            return "cooperate"
        elif opponent_actions[-1] == "cooperate":
            return "betray"
        else:
            return "cooperate"
        
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
            return "cooperate"
        else:
            return "betray"

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
            return self.detective_actions[len(opponent_actions)]
        
        if "betray" in opponent_actions:
            self.copy_opponent = True

        if self.copy_opponent:
            return opponent_actions[-1]
        else:
            return "betray"
        

class Simpleton(Strategy):
    """
    Класс Simpleton, начинает с сотрудничества. Если оппонент сотрудничает, повторяет свое прошлое действие. Если оппонент предал, повторяет обратное своему прошлому действию.
    """
    def __init__(self):
        self.name = "Simpleton"

    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and opponent_actions[-1] == "betray":
            return player_actions[-1]
        elif opponent_actions:
            return "cooperate" if player_actions[-1]=="cooperate" else "betray"
        else:
            # print("error")
            return "cooperate"

class SimpletonMistake(Strategy):
    """
    Класс Simpleton, начинает с сотрудничества. Если оппонент сотрудничает, повторяет свое прошлое действие. Если оппонент предал, повторяет обратное своему прошлому действию.
    Добавлена 5% вероятность предать просто так.
    """
    def __init__(self):
        self.name = "SimpletonMistake"

    def choose_action(self, player_actions, opponent_actions):
        if random.random() < 0.05:
            return "betray"
        if opponent_actions and opponent_actions[-1] == "betray":
            return player_actions[-1]
        elif opponent_actions:
            return "cooperate" if player_actions[-1]=="cooperate" else "betray"
        else:
            # print("error")
            return "cooperate"
