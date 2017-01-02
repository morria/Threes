package main

import (
  "fmt"
  "strings"
  "math"
  "math/rand"
  "time"
  "sort"
)

type Strategy [][]bool
type StrategySet [][][]bool

type StrategyEvaluation struct {
  strategySet StrategySet
  average float64
  nonLossRatios []float64
}

/**
 * Print out a strategy and its average sum to
 * STDOUT
 */
func printEvaluation(eval StrategyEvaluation) {
  for _,strategy := range eval.strategySet {
    for i := range strategy {
      str := []string{}
      for j := range strategy[i] {
        if strategy[i][j] {
          str = append(str, "1")
        } else {
          str = append(str, "0")
        }
      }
      fmt.Printf("[%s]\n", strings.Join(str, ", "))
    }
    fmt.Print("\n")
  }
  fmt.Printf("= %f\n", eval.average)
  nonLossRatioStrings := []string{}
  for _,ratio := range eval.nonLossRatios {
    nonLossRatioStrings = append(nonLossRatioStrings, fmt.Sprintf("%.3f", ratio * 100.0))
  }
  fmt.Printf("  [%s]\n", strings.Join(nonLossRatioStrings, ", "))
  fmt.Printf("\n")
}

/**
 * Roll the given number of dice, getting them
 * back in a sorted order
 */
func roll(dice_count int) []int {
  dice := []int{}
  for i := 0; i < dice_count; i++ {
    dice = append(dice, rand.Intn(6) + 1)
  }
  sort.Ints(dice)
  return dice
}

/**
 * Get the sum of a list of dice
 */
func diceSum(dice []int) int {
  sum := 0
  for i,d := range dice {
    if d != 3 {
      sum += dice[i]
    }
  }
  return sum
}

/**
 * Evaluate a given strategy matrix for the given
 * number of iterations, gettings its average sum
 * back.
 */
func evaluateStrategy(strategySet StrategySet, iterations int, channel chan StrategyEvaluation) {
  globalSum := 0
  nonLossRatios := []float64{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}
  for iteration := 0; iteration < iterations; iteration++ {
    keep := []int{}
    for len(keep) < 5 {

      // Roll the dice
      dice := roll(5 - len(keep))

      // Search over the dice for ones to keep
      kept := false
      for _,d := range dice {

        // Choose the strategy from the strategy set
        strategy := strategySet[len(strategySet)-1]
        keepSum := diceSum(keep)
        if len(strategySet) > keepSum {
          strategy = strategySet[keepSum]
        }

        // Choose to keep or discard dice based on
        // the chosen strategy
        if strategy[len(keep)][d-1] {
          keep = append(keep, d)
          kept = true
        }
      }

      // If we didn't choose any, keep the lowest
      // valued dice
      if !kept {
        keep = append(keep, dice[0])
      }
    }
    sum := diceSum(keep)
    for i := 0; i < len(nonLossRatios); i++ {
      if sum <= i {
        nonLossRatios[i]++
      }
    }
    globalSum += sum
  }
  average := (float64(globalSum)/float64(iterations))
  for i := 0; i < len(nonLossRatios); i++ {
    nonLossRatios[i] /= float64(iterations)
  }
  channel<-StrategyEvaluation{strategySet, average, nonLossRatios}
}

/**
 * Produce a strategy from an integer
 */
func strategyFromInt(s int) Strategy {
    strategy := Strategy{}
    strategy = append(strategy, []bool{(s&(1<<0))>0, false,        true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<1))>0, false,        true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<2))>0, (s&(1<<3))>0, true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<4))>0, (s&(1<<5))>0, true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<6))>0, (s&(1<<7))>0, true, false, false, false})
    return strategy
}

func strategyFromInt_1(s int) Strategy {
    strategy := Strategy{}
    strategy = append(strategy, []bool{(s&(1<<0))>0, false, true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<1))>0, false, true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<2))>0, false, true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<3))>0, false, true, false, false, false})
    strategy = append(strategy, []bool{(s&(1<<4))>0, false, true, false, false, false})
    return strategy
}

func strategyFromInt_0() Strategy {
    strategy := Strategy{}
    strategy = append(strategy, []bool{false, false, true, false, false, false})
    strategy = append(strategy, []bool{false, false, true, false, false, false})
    strategy = append(strategy, []bool{false, false, true, false, false, false})
    strategy = append(strategy, []bool{false, false, true, false, false, false})
    strategy = append(strategy, []bool{false, false, true, false, false, false})
    return strategy
}

/**
 * Produce a set of strategies from a set of
 * integers
 */
func strategySetFromIntSet(s []int) StrategySet {
  strategySet := StrategySet{}
  for i := range s {
    strategySet = append(strategySet, strategyFromInt(s[i]))
  }
  return strategySet
}

/**
 * Generate strategies and evaluate them, printing
 * out the best ones as we find them
 */
func main() {

  // Choose a random-ish seed
  rand.Seed(time.Now().UTC().UnixNano())

  // Create a channel for which strategy evaluations
  // may be returned
  channel := make(chan StrategyEvaluation, 4)

  // Iterate over all possible strategies to find the one
  // that produces the lowest average values
  strategyCount := 0
  for s0 := 0; s0 <= (int(math.Pow(2, 8)) - 1); s0++ {
    for s1 := 0; s1 <= (int(math.Pow(2, 5)) - 1); s1++ {
      strategySet := StrategySet{}
      strategySet = append(strategySet, strategyFromInt(s0))
      strategySet = append(strategySet, strategyFromInt(s0))
      strategySet = append(strategySet, strategyFromInt(s0))
      strategySet = append(strategySet, strategyFromInt_1(s1))
      strategySet = append(strategySet, strategyFromInt_0())
      go evaluateStrategy(strategySet, 400000, channel)
      strategyCount++
    }
  }

  // We're going to hunt for the lowest average value
  minEval := StrategyEvaluation{strategySetFromIntSet([]int{}), 30.0, []float64{0.0, 0.0, 0.0, 0.0, 0.0}}
  for i := 0; i < strategyCount; i++ {
    eval := <-channel
    if eval.nonLossRatios[4] > minEval.nonLossRatios[4] {
      minEval = eval
    }
    if i%100 == 0 {
      fmt.Print(".")
    }
  }
  fmt.Print("\n")
  printEvaluation(minEval)
}
