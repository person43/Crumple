from crumple import  Crumple
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons, make_s_curve
from run_fiber import make_paisley

# crumples a shape along some axese, displays them
def equalize_axes():
    ymin, ymax = plt.ylim()
    xmin, xmax = plt.xlim()
    min_, max_ = min(ymin, xmin), max(xmax, ymax)
    plt.ylim(min_, max_)
    plt.xlim(min_, max_)


def plot_crumple(pnts, slp, shape=(1,1), ind=1):
    crumple = Crumple(pnts, slp)
    plt.subplot(shape[0], shape[1], ind)
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
    # pnts, _ = make_moons(20)
    # shape = (2, 2)
    # plot_crumple(pnts, 1000, shape, 1)
    # plot_crumple(pnts, 0, shape, 2)
    # plot_crumple(pnts, 1, shape, 3)
    # plot_crumple(pnts, -1, shape, 4)

    pnts = make_paisley()
    plot_crumple(pnts, 1)
    plt.show()