import matplotlib.pyplot as plt
import numpy as np


def basic_visual_series(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(4,3))
    plt.plot(x, y)
    plt.xticks(rotation=90)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def group_bar(data, xlab, ylab):
    fig, ax = plt.subplots(figsize=(4, 3))
    width = 0.3
    x = 1 * np.arange(len(data)) - width * (len(data.columns) / 2) + width / 2
    for i in range(len(data.columns)):
        plt.bar(x + i * width, data.iloc[:, i], width=width)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.legend(data.columns)
        plt.xticks(list(range(len(data))), list(data.index), rotation=45)

