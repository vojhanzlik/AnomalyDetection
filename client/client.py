from abc import ABC, abstractmethod
from typing import Iterator

import grpc
import numpy as np

from messages_pb2 import AnomalyDetRequest, NumpyArray
from messages_pb2_grpc import AnomalyDetectionServiceStub


class ClientBase(ABC):

    def __init__(self, port):
        channel = grpc.insecure_channel(port)
        self.stub = AnomalyDetectionServiceStub(channel)

    @abstractmethod
    def _stream_messages(self) -> Iterator[AnomalyDetRequest]:
        """Server request callback function"""
        pass

    def stream_data(self, stub):
        response_iterator = stub.StreamData(self._stream_messages())
        for response in response_iterator:
            print("Server response: ", int(response.id),
                  bool(response.result))

    def send_numpy_array(self, array):
        rows = array.shape[0]
        cols = array.shape[1]
        vals = array.flatten()
        request = NumpyArray(values=vals, rows=rows, cols=cols)
        response = self.stub.SendNumpyArray(request)
        print(response.result)


class MyClient(ClientBase):

    def __init__(self, port):
        super().__init__(port)

    def _stream_messages(self) -> Iterator[AnomalyDetRequest]:
        request = AnomalyDetRequest(id=int(0),
                                    sensor1=float(0),
                                    sensor2=float(0),
                                    sensor3=float(0),
                                    sensor4=float(0))
        yield request
