import logging
import sys
from collections import deque

import numpy as np


def get_logger(name):
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(name)s] [%(levelname)-5.5s]  %(message)s")
    root_logger = logging.getLogger(name)
    # file_handler = logging.FileHandler(f"{name}.log")
    # file_handler.setFormatter(log_formatter)
    # root_logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)
    return root_logger


def extract_non_zero_id_data(data, i, identifier_idx):
    start_indices = np.where(np.diff(data[identifier_idx, :]) == i)[0]
    if len(start_indices) == 0:
        return None

    end_indices = np.where(np.diff(data[identifier_idx, :]) == -i)[0]
    if len(end_indices) == 0:
        return None

    for start, end in zip(start_indices, end_indices):
        sliced_data = data[:, start:end + 1]
        return sliced_data


class SetQueue:

    def __init__(self):
        self.set = set()
        self.queue = deque()

    def enqueue(self, value):
        if value not in self.set:
            self.set.add(value)
            self.queue.append(value)

    def dequeue(self):
        if len(self.queue) > 0:
            value = self.queue.popleft()
            self.set.remove(value)
            return value

    def peak(self):
        if len(self.queue) > 0:
            return self.queue[0]
        return -1

    def __len__(self):

        return len(self.queue)
