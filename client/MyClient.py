import time
from typing import Iterator

import numpy as np
from client import ClientBase
from messages_pb2 import NumpyArray
from test import main_realtime


class MyClient(ClientBase):

    def __init__(self):
        super().__init__()

    def yield_test(self):
        for i in range(1):
            data = np.load(f"test_samples/samples{i}.npy")
            selected_rows = data[4:11, :]
            split_arrays = np.array_split(selected_rows, 24, axis=1)
            time.sleep(2)
            for array in split_arrays:
                yield array

    def _stream_messages(self) -> Iterator[NumpyArray]:
        for array in self.yield_test():
            rows = array.shape[0]
            cols = array.shape[1]
            vals = array.flatten()
            request = NumpyArray(values=vals, rows=rows, cols=cols, id=0)
            yield request
