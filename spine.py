import matplotlib.pyplot as plt
from fibers import *
from run_fiber import make_paisley


if __name__ == "__main__":
    np.random.seed(0)
    pnts = make_paisley(5000)
    r_pnts = mirror_pnts(pnts, -1, TOP) - np.array([2.5, 2.5])
    t_pnts = pnts + np.array([1, 1])
    t_pnts = rotate(t_pnts, 30)
    pnts = np.concatenate((pnts, r_pnts, t_pnts))
    spine = spinal_tap(pnts)
    plt.scatter(pnts[:,0], pnts[:,1], color='b')
    plt.scatter(spine[:,0], spine[:,1], color='r')
    plt.show()
