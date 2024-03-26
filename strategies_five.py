import random

class Strategy:
    def __init__(self, name):
        self.name = name

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

class TitForTat(Strategy):
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

            return "betray"
        else:
            return "cooperate"
        
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
