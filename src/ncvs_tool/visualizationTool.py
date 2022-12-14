import matplotlib.pyplot as plt
import numpy as np


def basic_visual_series(x, y, title, xlabel, ylabel, color="purple"):
    plt.plot(x, y, c=color)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def group_bar(data, xlabel, ylabel):
    width = 0.3
    x = 1 * np.arange(len(data)) - width * (len(data.columns) / 2) + width / 2
    for i in range(len(data.columns)):
        plt.bar(x + i * width, data.iloc[:, i], width=width)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(data.index)
