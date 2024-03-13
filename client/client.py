from abc import ABC, abstractmethod
from typing import Iterator

import grpc
import numpy as np

from helpers import get_logger, extract_non_zero_id_data
from test import main, main_realtime
from messages_pb2 import NumpyArray
from messages_pb2_grpc import AnomalyDetectionServiceStub


class ClientBase(ABC):

    def __init__(self, address='localhost:8061'):
        self.logger = get_logger(self.__class__.__name__)
        channel = grpc.insecure_channel(address)
        self.stub = AnomalyDetectionServiceStub(channel)

    @abstractmethod
    def _stream_messages(self, generator) -> Iterator[NumpyArray]:
        """Server request callback function"""
        pass

    def stream_data(self, generator):
        response_iterator = self.stub.StreamData(self._stream_messages(generator))
        for response in response_iterator:
            self.logger.info("Server response: ", int(response.id),
                             bool(response.result))

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




class MyClient(ClientBase):

    def __init__(self):
        super().__init__()

    def _stream_messages(self, generator) -> Iterator[NumpyArray]:
        for array in generator:
            rows = array.shape[0]
            cols = array.shape[1]
            vals = array.flatten()

            request = NumpyArray(values=vals, rows=rows, cols=cols, id=0)
            yield request
