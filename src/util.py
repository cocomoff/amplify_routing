from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt


class RandomTSPInstance(object):
    def __init__(self, ncity: int = 10, utility: bool = False, util_range: Tuple[int] = (1, 5)):
        self.ncity = ncity
        self.utility = utility
        self.locations = np.random.uniform(size=(ncity, 2))

        if utility:
            l, h = util_range
            self.utilities = np.random.randint(low=l, high=h, size=(ncity))

        all_diffs = np.expand_dims(
            self.locations, axis=1) - np.expand_dims(self.locations, axis=0)
        self.distances = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

    def __str__(self):
        if self.utility:
            return f"RandomU(\n{self.locations}\n,{self.utilities}\n)"
        else:
            return f"Random(\n{self.locations}\n)"


def show_plot(instance: RandomTSPInstance, size: int = 5, route: List[int] = [], filename: str = "output.png"):
    f = plt.figure(figsize=(size, size))
    plt.xlabel("x")
    plt.ylabel("y")

    # draw route
    if len(route) > 0:
        ncity = len(route)
        path_length = sum(
            [instance.distances[route[i]]
                [route[(i + 1) % ncity]] for i in range(ncity)]
        )
        if not instance.utility:
            plt.title(f"path length: {path_length}")
        else:
            get_util = sum(instance.utilities[j] for j in route)
            plt.title(f"path length: {path_length}, util: {get_util}")

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
