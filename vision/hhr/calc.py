import numpy as np

class MovingAverage(object):
    "Keeps a moving average of a certain size. As items are added, the oldest is removed."
    
    def __init__(self, size, dtype=float):
        self._values = np.zeros(size, dtype=dtype)
        self._total = 0
        self._counter = 0
        self._num_values = 0

    def add_value(self, value):
        self._num_values = min(self._values.shape[0], self._num_values + 1)
        self._total -= self._values[self._counter]
        self._total += value 
        self._values[self._counter] = value
        self._counter = (self._counter + 1) % self._values.shape[0]

    @property
    def average(self):
        if self._num_values == 0:
            return 0
        else:
            return self._total / self._num_values
