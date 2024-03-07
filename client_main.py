import numpy as np

from client.client import MyClient

if __name__ == '__main__':
    c = MyClient('localhost:8061')
    loaded_array = np.load('test_samples/samples.npy')

    selected_rows = loaded_array[4:11, :]
    transposed_array = selected_rows.T
    split_arrays = np.array_split(transposed_array, 10)

    for a in split_arrays:
        c.send_numpy_array(a)
