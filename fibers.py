from concave_sides import *
import matplotlib.pyplot as plt

def fiberize(pnts, slp, orientation):
    vec = np.array([1, slp * 1])
    r_pnts = mirror_pnts(pnts, slp, orientation)
    all_pnts = np.concatenate((pnts, r_pnts))
    colors = {}
    for i, pnt in enumerate(all_pnts):
        if i < len(all_pnts) // 2:
            colors[tuple(pnt)] = BLUE
        else:
            colors[tuple(pnt)] = RED
    layers = onion_layers(all_pnts)
    fibers = []
    i = 0
    for layer in layers:
        layer = np.array([pnt for pnt in layer if colors[tuple(pnt)] == BLUE])
        if np.array_equal(layer[0], layer[-1]):
            layer = layer[:-1]

        proj = np.dot(layer, vec)
        i_min = np.argmin(proj)
        i_max = np.argmax(proj)

        if orientation == BOTTOM and (i_max == i_min+1 or i_max < i_min):
            layer = layer[::-1]
            i_min = len(layer) - i_min - 1
        layer = np.concatenate((layer[i_min:], layer[:i_min]))
        fibers.append(np.array(layer))
        i += 1
    return fibers

def make_comma(init_size=10000):
    def f(x): return x**5
    margin = 0.05
    pnts = np.random.randn(init_size, 2)
    norms = [np.linalg.norm(p) for p in pnts]
    med = np.median(norms)
    pnts = [p for i, p in enumerate(pnts) if norms[i] < med]
    pnts = np.array(pnts)
    pnts += [0, 0.4]
    pnts = [pnt for pnt in pnts if f(pnt[0]) > pnt[1] + margin]
    return np.array(pnts)


if __name__ == "__main__":
    # generate some points
    pnts = make_comma()

    slp = 1
    top_fibers = fiberize(pnts, slp, TOP)
    bottom_fibers = fiberize(pnts, slp, BOTTOM)

    plt.subplot(1, 3, 1)
    plt.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in top_fibers:
        plt.plot(layer[:,0], layer[:,1], color='k', linestyle='--')
        plt.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')

    plt.subplot(1, 3, 2)
    plt.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in bottom_fibers:
        plt.plot(layer[:, 0], layer[:, 1], color='k', linestyle='--')
        plt.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')

    plt.subplot(1, 3, 3)
    plt.scatter(pnts[:, 0], pnts[:, 1], color='b')
    for layer in bottom_fibers:
        plt.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')
    for layer in top_fibers:
        plt.scatter([layer[0][0], layer[-1][0]], [layer[0][1], layer[-1][1]], color='r')

    plt.show()
