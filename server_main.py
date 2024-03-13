import pickle

from server.server import AnomalyDetectionServer

if __name__ == '__main__':

    server = AnomalyDetectionServer()
    server.serve()
