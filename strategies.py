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

class Majority(Strategy):
    """
    Класс Следование мажоритарному выбору: Игрок анализирует предыдущие ходы другого заключенного и выбирает наиболее популярный ход.

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
    
    """
    def __init__(self):
        self.name = "random"
    def choose_action(self, player_actions, opponent_actions):
        return random.choice(["cooperate", "betray"])

class SampleStrategy(Strategy):
    """
    Класс Sample, начинает с сотрудничества. Если предают 2 раза предает один раз
    
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
    
    Атрибуты:
    - name: имя игрока
    """
    def __init__(self):
        self.name = "Friedman"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and opponent_actions[-1] == "betray":
            return "betray"
        else:
            return "cooperate"

class JossStrategy(Strategy):
    """
    Класс Фридман, начинает с сотрудничества. Следующий раунд это копия предыдущего у соперника.
    С 10% вероятностью предательство 

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
    Класс Грассман, копия джоса но каждый 50ый раунд предает

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
    Класс Око за око, начинает с сотрудничества. Если предали то предает в след раунде
    """
    def __init__(self):
        self.name = "TitForTat"
    def choose_action(self, player_actions, opponent_actions):
        if opponent_actions and (opponent_actions[-1] == "betray" or random.random() < 0.1):
            return "betray"
        else:
            return "cooperate"

class TitForTatWithForgiveness(Strategy):
    """
    Класс TitForTatWithForgiveness, начинает с сотрудничества и прощает иногда.
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
    Класс TitForTatWithRandom, реагирует на измену с изменой или сотрудничеством случайным образом.
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
    """
    def __init__(self):
        self.name = "Pessimistic"

    def choose_action(self, player_actions, opponent_actions):
        if "cooperate" in opponent_actions:
            return "cooperate"
        else:
            return "betray"

