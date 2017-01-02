from __future__ import print_function
from random import randint
import sys

# Definition of a game of Threes
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
    def keptSum(self):
        return sum(self.kept)
    def isComplete(self):
        return len(self.kept) == 5
    def sum(self):
        sum = 0
        for i in self.kept:
            if i != 3:
                sum += i
        return sum

# Definition of a strategy that plays Threes
class Strategy(object):
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

# A strategy defined by a 2D matrix with axes being
# the number of 'keeps' and a boolean for each of the
# six dice, choosing if they should be kept at the
# given keep-length.
class StrategyMatrix(Strategy):
    def __init__(self, matrix):
        Strategy.__init__(self)
        self.matrix = matrix;
    def round(self):
        dice = self.game.roll()
        keep = []
        for i in dice:
            if self.matrix[self.game.keptLen() + len(keep)][i-1] == True:
                keep.append(i)
        if (len(keep) < 1):
            keep.append(min(dice))
        self.game.keep(keep)

class Strategy3D(Strategy):
    def __init__(self, matrix):
        Strategy.__init__(self)
        self.matrix = matrix;
    def round(self):
        keep = []
        kept_sum= self.game.keptSum()
        dice = self.game.roll()
        for i in dice:
            matrix = self.matrix[kept_sum] if len(self.matrix) > kept_sum else self.matrix[-1]
            if matrix[self.game.keptLen() + len(keep)][i-1]:
                kept_sum += i
                keep.append(i)
        if (len(keep) < 1):
            keep.append(min(dice))
        self.game.keep(keep)

# An example strategy where all dice are always kept
class StrategyKeepAll(StrategyMatrix):
    def __init__(self):
        matrix = []
        matrix.append([True, True, True, True, True, True])
        matrix.append([True, True, True, True, True, True])
        matrix.append([True, True, True, True, True, True])
        matrix.append([True, True, True, True, True, True])
        matrix.append([True, True, True, True, True, True])
        StrategyMatrix.__init__(self)

# An example strategy where only threes are kept
class StrategyKeepOnlyThrees(StrategyMatrix):
    def __init__(self):
        matrix = []
        matrix.append([False, False, True, False, False, False])
        matrix.append([False, False, True, False, False, False])
        matrix.append([False, False, True, False, False, False])
        matrix.append([False, False, True, False, False, False])
        matrix.append([False, False, True, False, False, False])
        StrategyMatrix.__init__(self)

def evaluateStrategy(strategy, iterations):
    sum = 0
    wins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, iterations):
        strategy.reset()
        s = strategy.sum()
        sum += s
        for i in range(10):
            if s <= i:
                wins[i] += 1
    return (
            sum/(iterations*1.0),
            map(lambda x: round((x/(iterations*1.0))*100.0, 2), wins)
            )

def p(m, avg, win_ratios):
  for s in m:
    for i in range(5):
      print(str(map(lambda x: int(x), s[i])), end="\n")
    print("")
  print(' = ' + str(avg), end="\n")
  print(win_ratios, end="\n\n")

min_s = 0;
min_avg = 100;
win_ratio = 0;
for m in range(0, 2**7):

    s0 = []
    s0.append([False,            False,            True, False, False, False])
    s0.append([True,             False,            True, False, False, False])
    s0.append([True,             False,            True, False, False, False])
    s0.append([True,             True,             True, False, False, False])
    s0.append([True,             True,             True, False, False, False])

    s1 = []
    s1.append([False,            False,            True, False, False, False])
    s1.append([True,             False,            True, False, False, False])
    s1.append([True,             False,            True, False, False, False])
    s1.append([True,             True,             True, False, False, False])
    s1.append([True,             True,             True, False, False, False])

    s2 = []
    s2.append([False,            False,            True, False, False, False])
    s2.append([(m&(1<<3)>0),     False,            True, False, False, False])
    s2.append([(m&(1<<2)>0),     False,            True, False, False, False])
    s2.append([(m&(1<<1)>0),     False,            True, False, False, False])
    s2.append([(m&(1<<0)>0),     True,             True, False, False, False])

    s3 = []
    s3.append([False,            False,            True, False, False, False])
    s3.append([(m&(1<<7)>0),     False,            True, False, False, False])
    s3.append([(m&(1<<6)>0),     False,            True, False, False, False])
    s3.append([(m&(1<<5)>0),     False,            True, False, False, False])
    s3.append([(m&(1<<4)>0),     False,            True, False, False, False])

    s4 = []
    s4.append([False, False, True, False, False, False])
    s4.append([False, False, True, False, False, False])
    s4.append([False, False, True, False, False, False])
    s4.append([False, False, True, False, False, False])
    s4.append([False, False, True, False, False, False])

    (avg, win_ratios) = evaluateStrategy(Strategy3D([s0, s1, s3, s4]), 100000)
    if win_ratios[4] > win_ratio:
        win_ratio = win_ratios[4]
#    if avg < min_avg:
#         min_avg = avg
        min_s = [s0, s1, s2, s3]
        p(min_s, avg, win_ratios)
        sys.stdout.flush()
