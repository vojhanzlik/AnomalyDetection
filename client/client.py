from abc import ABC, abstractmethod
from typing import Iterator

import grpc

from helpers import get_logger
from messages_pb2 import NumpyArray
from messages_pb2_grpc import AnomalyDetectionServiceStub


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
