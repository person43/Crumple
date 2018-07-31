from crumple import  Crumple
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_s_curve

# crumples a shape along some axese, displays them
def equalize_axes():
    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    min_, max_ = min(ymin, xmin), max(xmax, ymax)
    plt.ylim(min_, max_)
    plt.xlim(min_, max_)


def plot_crumple(pnts, slp, ind):
    crumple = Crumple(pnts, slp)
    plt.subplot(2, 2, ind)
    plt.scatter(pnts[:, 0], pnts[:, 1], color='b')
    plt.plot(crumple.ne[:, 0], crumple.ne[:, 1], color='r')
    plt.plot(crumple.sw[:, 0], crumple.sw[:, 1], color='g')
    equalize_axes()

    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    center = [np.mean([xmin, xmax]), np.mean([ymin, ymax])]
    if slp == float('inf'):
        endpts = [[center[0], ymax], [center[0], ymin]]
    else:
        b = center[1] - slp*center[0]
        endpts = [[xmin, slp*xmin + b], [xmax, slp*xmax + b]]
    endpts = np.array(endpts)
    plt.plot(endpts[:, 0], endpts[:, 1], color='k', linestyle='dotted')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()

if __name__ == "__main__":
    # np.random.seed(2)
    # pnts = np.random.rand(100, 2)
    # pnts = np.random.logistic(size=(50, 2))
    pnts, _ = make_moons(100)

    plot_crumple(pnts, 1000, 1)
    plot_crumple(pnts, 0, 2)
    plot_crumple(pnts, 1, 3)
    plot_crumple(pnts, -1, 4)

    plt.show()