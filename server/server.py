import os

import grpc
from concurrent import futures
import numpy as np

from helpers import get_logger
from messages_pb2 import AnomalyDetResponse
from messages_pb2_grpc import AnomalyDetectionServiceServicer, add_AnomalyDetectionServiceServicer_to_server
from ml_classifier.classifier import FeatureClassifier1


class AnomalyDetectionServer(AnomalyDetectionServiceServicer):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.my_classifier = FeatureClassifier1()
        self.my_classifier.load_params("../classifier0.995.pkl")

    def StreamData(self, request_iterator, context):
        if not request_iterator:
            raise grpc.RpcError

        for request in request_iterator:
            print("Client request: ",
                  request.id,
                  request.sensor1,
                  request.sensor2,
                  request.sensor3,
                  request.sensor4)

            yield AnomalyDetResponse(id=1, result=True)

    def SendNumpyArray(self, request, context):
        self.logger.info("Received SendNumpyArray request")
        rows = request.rows
        cols = request.cols
        values = list(request.values)

        numpy_array = np.array(values).reshape((rows, cols))
        res = self.my_classifier.predict(numpy_array)
        return AnomalyDetResponse(id=1, result=bool(res))

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_AnomalyDetectionServiceServicer_to_server(self, server)
        server.add_insecure_port('localhost:8061')
        server.start()
        self.logger.info("Server started")
        # server.stop(None)
        server.wait_for_termination()
        self.logger.info("Server shut down successfully")


if __name__ == '__main__':
    server = AnomalyDetectionServer()
    server.serve()
