from concurrent import futures

import grpc
import numpy as np
from classifier_model.classifier import FeatureClassifier1

from helpers import get_logger, extract_non_zero_id_data, UniqueQueue
from messages_pb2 import AnomalyDetResponse
from messages_pb2_grpc import AnomalyDetectionServiceServicer, add_AnomalyDetectionServiceServicer_to_server


def rpc_request_arr_to_np_arr(request):
    rows = request.rows
    cols = request.cols
    values = list(request.values)
    return np.array(values).reshape((rows, cols))


class AnomalyDetectionServer(AnomalyDetectionServiceServicer):
    def __init__(self, address='0.0.0.0:8061'):
        self.address = address
        self.logger = get_logger(self.__class__.__name__)
        self.my_classifier = FeatureClassifier1()
        self.my_classifier.load_params("classifier6dim_new.pkl")

        self.identifier_idx = 6
        self.input_rows_num = 7

    def StreamData(self, request_iterator, context):
        self.logger.info("Received SendNumpyArray stream request")
        if not request_iterator:
            self.logger.error("Invalid request iterator")
            raise grpc.RpcError

        time_series = np.array(self.input_rows_num * [[]])
        ids_to_predict = UniqueQueue()

        for request in request_iterator:
            self.logger.info("Received SendNumpyArray request")
            array = rpc_request_arr_to_np_arr(request)
            self.logger.info("Request converted to np array")

            self._update_identifiers(array, ids_to_predict)
            time_series = self._append_to_time_series(array, time_series)

            for pred in self._attempt_prediction(ids_to_predict, time_series):
                yield pred

        self.logger.info("STREAMING DONE")

    def _attempt_prediction(self, ids_to_predict, time_series):
        i = ids_to_predict.peak()
        if i > 0:
            extracted_arr = extract_non_zero_id_data(time_series, i, self.identifier_idx)
            if extracted_arr is not None:
                extracted_arr = self._prep_arr_for_prediction(extracted_arr)
                res = self.my_classifier.predict(extracted_arr)

                yield AnomalyDetResponse(id=i, result=res)
                self.logger.info(f"Send SendNumpyArray response: result: {res}, id: {i}")
                ids_to_predict.dequeue()

    def _prep_arr_for_prediction(self, arr):
        #arr = np.delete(arr, self.identifier_idx, axis=0)
        return arr.T

    def _update_identifiers(self, array, ids_to_predict):
        unique_ids = self._extract_unique_identifiers(array)
        for u_i in unique_ids:
            try:
                u_i = int(u_i)
                ids_to_predict.enqueue(u_i)
            except Exception as e:
                self.logger.error(e)

    def _extract_unique_identifiers(self, array):
        identifier_arr = array[self.identifier_idx]
        self.logger.info("Extracted identifier array")
        unique_ids = np.unique(identifier_arr[identifier_arr != 0])
        return unique_ids

    def _append_to_time_series(self, array, time_series):
        return np.concatenate((time_series, array), axis=1)

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
