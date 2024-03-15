import numpy as np
import matplotlib.pyplot as plt

from client.MyClient import MyClient


def plot_array(data):
    for i in range(data.shape[0]):
        plt.subplot(20, 1, i + 1)
        plt.plot(data[i])

    plt.show()


def main_t():
    for i in range(5):
        data = np.load(f"test_samples/samples{i}.npy")
        selected_rows = data[4:11, :]
        yield selected_rows


def realtime_main():
    for i in range(5):
        data = np.load(f"test_samples/samples{i}.npy")
        selected_rows = data[4:11, :]
        split_arrays = np.array_split(selected_rows, 24)
        yield split_arrays


if __name__ == '__main__':
    c = MyClient()
    # c.send_opc_outputs(main_t())
    c.stream_data()

    # transposed_array = data.T
    # selected_cols = transposed_array[:, 4:11]
    # plot_array(data)
    # split_arrays = np.array_split(selected_cols, 10)
