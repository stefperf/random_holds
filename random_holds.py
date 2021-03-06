# Numerical solution for Riddle Classic @ https://fivethirtyeight.com/features/can-you-hop-across-the-chessboard/
# under the assumption that new climbing holds are only placed in gaps.
#
import numpy as np
import random
from bisect import bisect


class RandomHolds:
    """simulating the riddle's climbing wall where holds are placed randomly till there are no more gaps"""
    def __init__(self, size):
        """init to the given size with no holds placed"""
        self.size = size
        self.holds = []
        self.reset()

    def reset(self):
        """reset to just the bottom and top holds"""
        self.holds = [0, self.size]

    def is_complete(self):
        """True iff there are no gaps in the wall"""
        for hold0, hold1 in zip(self.holds[:-1], self.holds[1:]):
            if hold1 - hold0 > 1.0:
                return False
        return True

    def add_random_hold(self):
        """randomly add a new hold in a gap and return True, or return False if there are no gaps"""
        if self.is_complete():
            return False
        while True:
            new_hold = random.uniform(0, self.size)
            if new_hold not in self.holds and self.benefits_from(new_hold):
                break
        self.holds = sorted(self.holds + [new_hold])
        return True

    def benefits_from(self, new_hold):
        """True iff new_hold falls in a gap"""
        index1 = bisect(self.holds, new_hold)
        index0 = index1 - 1
        return self.holds[index1] - self.holds[index0] > 1.

    def fill_up(self):
        """randomly add holds till there are no more gaps"""
        while self.add_random_hold():
            pass
        return len(self.holds) - 2

    def average_holds(self, n_scenarios):
        """Monte Carlo estimation of the avg, nr. of holds needed to fill all gaps"""
        sum_holds = 0
        for _ in range(n_scenarios):
            self.reset()
            sum_holds += self.fill_up()
        return sum_holds / n_scenarios


if __name__ == '__main__':
    n_scenarios = 100000
    incr = 0.5
    print(f'wall size -> avg. nr. of randomly placed holds needed, estimated with {n_scenarios} scenarios')
    print('-' * 120)
    for size in np.arange(1., 10. + incr, incr):
        print(f'{size} -> {RandomHolds(size).average_holds(n_scenarios)}')


"""
# OUTPUT:

wall size -> avg. nr. of randomly placed holds needed, estimated with 100000 scenarios
------------------------------------------------------------------------------------------------------------------------
1.0 -> 0.0
1.5 -> 2.00332
2.0 -> 2.99548
2.5 -> 4.00677
3.0 -> 4.995
3.5 -> 6.00711
4.0 -> 6.99595
4.5 -> 8.00856
5.0 -> 9.00316
5.5 -> 10.00007
6.0 -> 11.00847
6.5 -> 11.99075
7.0 -> 13.00122
7.5 -> 14.00126
8.0 -> 14.99505
8.5 -> 15.99701
9.0 -> 17.00716
9.5 -> 18.00627
10.0 -> 18.99608

"""
