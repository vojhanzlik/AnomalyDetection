import numpy as np
import threading


class CircularBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = np.empty(capacity, dtype=np.float32)
        self.size = 0
        self.head = 0
        self.tail = 0
        self.condition = threading.Condition()

    def is_empty(self):
        return self.size == 0

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, value):
        self.condition.acquire()
        if self.is_full():
            # If the buffer is full, overwrite the oldest element
            self.head = (self.head + 1) % self.capacity
        else:
            self.size += 1
        self.buffer[self.tail] = value
        self.tail = (self.tail + 1) % self.capacity

        self.condition.notify()
        self.condition.release()

    def dequeue(self):
        self.condition.acquire()
        if self.is_empty():
            print('buffer empty')
            self.condition.wait()
        value = self.buffer[self.head]
        self.buffer[self.head] = None
        self.head = (self.head + 1) % self.capacity
        self.size -= 1
        self.condition.release()
        return value

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty buffer")
        return self.buffer[self.head]


