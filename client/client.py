import time
from abc import ABC, abstractmethod
from typing import Iterator

import grpc
import numpy as np

from helpers import get_logger, extract_non_zero_id_data
from test import main, main_realtime
from messages_pb2 import NumpyArray
from messages_pb2_grpc import AnomalyDetectionServiceStub


def wait_for_nonempty(iterator, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            next(iterator)
            return True  # Iterator is not empty
        except StopIteration:
            # Iterator is empty, wait for a short interval before retrying
            time.sleep(0.1)
    return False  # Timeout reached without nonempty response


class ClientBase(ABC):

    def __init__(self, address='localhost:8061'):
        self.logger = get_logger(self.__class__.__name__)
        channel = grpc.insecure_channel(address)
        self.stub = AnomalyDetectionServiceStub(channel)

    @abstractmethod
    def _stream_messages(self) -> Iterator[NumpyArray]:
        """Server request callback function"""
        pass

    def stream_data(self):
        try:
            response_iterator = self.stub.StreamData(self._stream_messages())
            f = open("./results.csv", "a")
            for response in response_iterator:
                self.logger.info(f"Server response: result: {bool(response.result)} id: {int(response.id)}")
                f.write(f"{int(response.id)},{bool(response.result)}\n")
                f.flush()
        except Exception as e:
            self.logger.exception(e)

    def send_opc_outputs(self, generator):
        for arr in generator:
            max_id = int(arr[-1].max())
            for i in range(max_id - 3, max_id + 1):
                self.send_numpy_array(arr, i)

    def send_numpy_array(self, array, i):
        extracted_arr = extract_non_zero_id_data(array, i, 6)
        if extracted_arr is None:
            self.logger.error("could not extract a valid array")
            return
        extracted_arr = extracted_arr[:-1]
        extracted_arr = extracted_arr.T
        rows = extracted_arr.shape[0]
        cols = extracted_arr.shape[1]
        vals = extracted_arr.flatten()

        request = NumpyArray(values=vals, rows=rows, cols=cols, id=i)
        response = self.stub.SendNumpyArray(request)
        self.logger.info(f"Prediction received for id: {response.id}, prediction: {response.result}")


