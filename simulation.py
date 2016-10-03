from random import randint

class Threes(object):
    def __init__(self):
        self.kept = [];
    def roll(self):
        dice = [];
        for i in range(len(self.kept), 5):
            dice.append(randint(1,6))
        return dice
    def keep(self, keep):
        assert len(keep) >= 1
        self.kept.extend(keep)
    def keptLen(self):
        return len(self.kept)
    def isComplete(self):
        return len(self.kept) == 5
    def sum(self):
        sum = 0
        for i in self.kept:
            if i != 3:
                sum += i
        return sum

# Keep all dice as they are initially thrown
class StrategyKeepAll(object):
    def __init__(self):
        self.game = Threes()
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()
        self.game.keep(dice)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Only keep threes or the lowest valued
# dice we have
class StrategyKeepOnlyThrees(object):
    def __init__(self):
        self.game = Threes()
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()

        keep = []
        for i in dice:
            if i == 3:
                keep.append(i)
        if len(keep) < 1:
            keep.append(min(dice))
        self.game.keep(keep)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Only keep threes/ones or the lowest valued
# dice we have
class StrategyKeepThreesOnes(object):
    def __init__(self):
        self.game = Threes()
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()
        keep = []
        for i in dice:
            if i == 3 or i == 1:
                keep.append(i)
        if len(keep) < 1:
            keep.append(min(dice))
        self.game.keep(keep)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Only keep threes/ones/twos or the lowest
# valued dice we have
class StrategyKeepThreesOnesTwos(object):
    def __init__(self):
        self.game = Threes()
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()
        keep = []
        for i in dice:
            if i == 3 or i == 1 or i == 2:
                keep.append(i)
        if len(keep) < 1:
            keep.append(min(dice))
        self.game.keep(keep)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Only keep threes/ones or the lowest
# valued dice we have, unless we're
# close to the end
class StrategyKeepThreesOnesLateTwos(object):
    def __init__(self):
        self.game = Threes()
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()
        keep = []
        for i in dice:
            if i == 3 or i == 1:
                keep.append(i)
            elif i == 2 and self.game.keptLen() >= 3:
                keep.append(i)
        if len(keep) < 1:
            keep.append(min(dice))
        self.game.keep(keep)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Only keep threes/ones or the lowest
# valued dice we have, unless we're
# close to the end
class StrategyKeepThreesLateOnesLateTwos(object):
    def __init__(self):
        self.game = Threes()
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()
        keep = []
        for i in dice:
            if i == 3:
                keep.append(i)
            elif i == 1 and self.game.keptLen() >= 2:
                keep.append(i)
            elif i == 2 and self.game.keptLen() >= 3:
                keep.append(i)
        if len(keep) < 1:
            keep.append(min(dice))
        self.game.keep(keep)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Test a given strategy over many iterations,
# averaging its results
class TestStrategy(object):
    def __init__(self, strategy):
        self.strategy = strategy
    def avg(self):
        iterations = 1000000
        sum = 0
        for i in range(0, iterations):
            self.strategy.reset()
            sum += self.strategy.sum()
        return sum/(iterations * 1.0)

# print "Keep all:   " + str(TestStrategy(StrategyKeepAll()).avg())
# print "Keep 3:     " + str(TestStrategy(StrategyKeepOnlyThrees()).avg())
# print "Keep 3/1:   " + str(TestStrategy(StrategyKeepThreesOnes()).avg())
# print "Keep 3/2/1: " + str(TestStrategy(StrategyKeepThreesOnesTwos()).avg())
# print "Keep 3/1 l2:  " + str(TestStrategy(StrategyKeepThreesOnesLateTwos()).avg())
print "Keep 3 l1/2:  " + str(TestStrategy(StrategyKeepThreesLateOnesLateTwos()).avg())
