import matplotlib.pyplot as plt

from MyClient import MyClient


def plot_array(data):
    for i in range(data.shape[0]):
        plt.subplot(20, 1, i + 1)
        plt.plot(data[i])

    plt.show()


if __name__ == '__main__':
    c = MyClient()
    c.stream_data()
