import grpc
from concurrent import futures
import numpy as np

from helpers import get_logger, extract_non_zero_id_data, SetQueue
from messages_pb2 import AnomalyDetResponse
from messages_pb2_grpc import AnomalyDetectionServiceServicer, add_AnomalyDetectionServiceServicer_to_server
from classifier import FeatureClassifier1


class AnomalyDetectionServer(AnomalyDetectionServiceServicer):
    def __init__(self, address='localhost:8061'):
        self.address = address
        self.logger = get_logger(self.__class__.__name__)
        self.my_classifier = FeatureClassifier1()
        self.my_classifier.load_params("classifier6dim0.995.pkl")

        self.identifier_idx = 6
        self.classifier_rows_num = 6

    def StreamData(self, request_iterator, context):
        self.logger.info("Received SendNumpyArray stream request")
        if not request_iterator:
            self.logger.error("Invalid request iterator")
            raise grpc.RpcError

        time_series = np.array(self.classifier_rows_num * [[]])
        ids_to_predict = SetQueue()

        for request in request_iterator:
            self.logger.info("Received SendNumpyArray request")
            rows = request.rows
            cols = request.cols
            values = list(request.values)
            array = np.array(values).reshape((rows, cols))

            identifier_arr = array[self.identifier_idx]
            unique_integers = np.unique(identifier_arr[identifier_arr != 0])
            for u_i in unique_integers:
                ids_to_predict.enqueue(u_i)

            time_series = np.concatenate((time_series, array), axis=1)

            i = ids_to_predict.peak()
            if i > 0:
                extracted_arr = extract_non_zero_id_data(time_series, i, self.identifier_idx)
                if extracted_arr is not None:
                    extracted_arr = np.delete(extracted_arr, self.identifier_idx, axis=0)
                    extracted_arr = extracted_arr.T
                    res = self.my_classifier.predict(extracted_arr)
                    yield AnomalyDetResponse(id=i, result=res)
                    ids_to_predict.dequeue()
        self.logger.info("DONE")

    def SendNumpyArray(self, request, context):
        self.logger.info("Received SendNumpyArray request")
        rows = request.rows
        cols = request.cols
        values = list(request.values)

        numpy_array = np.array(values).reshape((rows, cols))
        res = bool(self.my_classifier.predict(numpy_array))
        self.logger.info(f"Prediction done for id: {request.id}, sending response {res}")
        return AnomalyDetResponse(id=request.id, result=res)

    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_AnomalyDetectionServiceServicer_to_server(self, server)
        server.add_insecure_port(self.address)
        server.start()
        self.logger.info("Server started")
        # server.stop(None)
        server.wait_for_termination()
        self.logger.info("Server shut down successfully")
