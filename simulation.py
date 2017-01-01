from __future__ import print_function
from random import randint
import sys

class Threes(object):
    def __init__(self):
        self.kept = [];
    def roll(self):
        dice = [];
        for i in range(len(self.kept), 5):
            dice.append(randint(1,6))
        return sorted(dice)
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
class StrategyMatrix(object):
    def __init__(self, matrix):
        self.game = Threes()
        self.matrix = matrix;
    def reset(self):
        self.game = Threes()
    def round(self):
        dice = self.game.roll()
        keep = []
        for i in dice:
            if self.matrix[self.game.keptLen() + len(keep)][i-1] == True:
                keep.append(i)
        if (len(keep) < 1):
            keep.append(min(dice))
        self.game.keep(keep)
    def sum(self):
        while not self.game.isComplete():
            self.round()
        return self.game.sum()

# Test a given strategy over many iterations,
# averaging its results
class TestStrategy(object):
    def __init__(self, strategy, iterations):
        self.strategy = strategy
        self.iterations = iterations
    def avg(self):
        sum = 0
        for i in range(0, self.iterations):
            self.strategy.reset()
            sum += self.strategy.sum()
        return sum/(self.iterations * 1.0)

def p(m, avg):
  for i in range(5):
    print(str(map(lambda x: int(x), m[i])), end="\n")
  print(' = ' + str(avg), end="\n")

# s = []
# s.append([False, False, True, False, False, False])
# s.append([False, False, True, False, False, False])
# s.append([True, True, True, False, False, False])
# s.append([True, True, True, False, False, False])
# s.append([True, True, True, False, False, False])
# print(str(500000) + "\t" + str(TestStrategy(StrategyMatrix(s), 500000).avg()))
# for i in range(1, 100):
#  print(str(i*1000) + "\t" + str(TestStrategy(StrategyMatrix(s), i*1000).avg()))
#  sys.stdout.flush()

# 6.3805368
# s = []
# s.append([0, 0, 1, 0, 0, 0])
# s.append([1, 0, 1, 0, 0, 0])
# s.append([1, 0, 1, 0, 0, 0])
# s.append([1, 1, 1, 0, 0, 0])
# s.append([1, 1, 1, 0, 0, 0])
# avg = TestStrategy(StrategyMatrix(s), 5000000).avg()
# print(str(avg))
# sys.exit(0)

min_s = 0;
min_avg = 100;
for m in range(0, 2**6):
    s = []
    s.append([m&(1<<2)>0, False,      True, False,      False, False])
    s.append([m&(1<<1)>0, m&(1<<5)>0, True, False,      False, False])
    s.append([m&(1<<0)>0, m&(1<<4)>0, True, False,      False, False])
    s.append([True,       m&(1<<3)>0, True, False,      False, False])
    s.append([True,       True,       True, m&(1<<6)>0, False, False])
    avg = TestStrategy(StrategyMatrix(s), 500000).avg()
    if avg < min_avg:
        min_avg = avg
        min_s = s
        p(min_s, avg)
        sys.stdout.flush()
