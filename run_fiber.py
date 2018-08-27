from fibers import *
import matplotlib.pyplot as plt
import matplotlib as mpl

def make_paisley(init_size=10000):
    def f(x): return x**5
    margin = 0.05
    pnts = np.random.uniform(-1.5, 1.5, (init_size, 2))
    norms = [np.linalg.norm(p) for p in pnts]
    med = np.median(norms)
    pnts = [p for i, p in enumerate(pnts) if norms[i] < med]
    pnts = np.array(pnts)
    pnts += [0, 0.4]
    pnts = [pnt for pnt in pnts if f(pnt[0]) > pnt[1] + margin]
    return np.array(pnts)

def compare_fibrations(pnts):
    plt.subplot(1, 2, 1)
    fibers = fiberize(pnts, 10000, TOP)
    plt.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in fibers:
        plt.plot(layer[:, 0], layer[:, 1], linewidth='1', color='k')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()

    plt.subplot(1, 2, 2)
    fibers = fiberize_corner(pnts)
    plt.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in fibers:
        plt.plot(layer[:, 0], layer[:, 1], linewidth='1', color='k')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()

def fiberization_demo(pnts, slp):
    top_fibers = fiberize(pnts, slp, TOP)
    bottom_fibers = fiberize(pnts, slp, BOTTOM)

    fig = plt.figure()
    mpl.rcParams['lines.markersize'] = 4
    mpl.rcParams['lines.linewidth'] = 1

    ax = fig.add_subplot(1, 3, 1)
    ax.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in top_fibers:
        ax.plot(layer[:, 0], layer[:, 1], color='k')
        ax.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()

    ax = fig.add_subplot(1, 3, 2)
    ax.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in bottom_fibers:
        ax.plot(layer[:, 0], layer[:, 1], color='k')
        ax.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()

    ax = fig.add_subplot(1, 3, 3)
    ax.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in bottom_fibers:
        ax.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')
    for layer in top_fibers:
        ax.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    # pnts = np.random.randn(1000, 2)
    # compare_fibrations(pnts)
    # exit()

    pnts = make_paisley()
    # pnts = rotate(pnts, -90)
    fiberization_demo(pnts, 1)