from typing import List
import numpy as np
import matplotlib.pyplot as plt


class RandomTSPInstance(object):
    def __init__(self, ncity: int = 10):
        self.ncity = ncity
        self.locations = np.random.uniform(size=(ncity, 2))
        all_diffs = np.expand_dims(
            self.locations, axis=1) - np.expand_dims(self.locations, axis=0)
        self.distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    def __str__(self):
        return f"RandomTSPInstance(\n{self.locations}\n)"


def show_plot(instance: RandomTSPInstance, size: int = 5, route: List[int] = [], filename: str = "output.png"):
    f = plt.figure(figsize=(size, size))
    plt.xlabel("x")
    plt.ylabel("y")

    # draw route
    if len(route) > 0:
        ncity = instance.ncity
        path_length = sum(
            [instance.distances[route[i]]
                [route[(i + 1) % ncity]] for i in range(ncity)]
        )
        plt.title(f"path length: {path_length}")

        x = [i[0] for i in instance.locations]
        y = [i[1] for i in instance.locations]
        for i in range(ncity):
            r = route[i]
            n = route[(i + 1) % ncity]
            plt.plot([x[r], x[n]], [y[r], y[n]], "b--", alpha=0.5)

    plt.scatter(*zip(*instance.locations))
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


if __name__ == '__main__':
    print(RandomTSPInstance(ncity=10))
