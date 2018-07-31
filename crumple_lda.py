from crumple import Crumple
from concave_sides import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

# returns slope orthogonal to lda slope
def get_slope_lda(all_pnts, labels):
    lda = LDA()
    lda.fit(all_pnts, labels)
    return -lda.coef_[0][0] / lda.coef_[0][1]

def plot_pnts(upper, lower):
    plt.scatter(upper[:, 0], upper[:, 1], color='r')
    plt.scatter(lower[:, 0], lower[:, 1], color='b')
    plt.gca().set_aspect('equal', adjustable='box')


if __name__ == "__main__":
    np.random.seed(0)
    # generate some points, split them into two classes according to
    # function f and a margin
    # def f(x): return 0.7*np.sin(2*x)
    def f(x): return x**5
    margin = 0.2
    pnts = np.random.randn(1000, 2) + np.array([-0.2, -0.2])
    pnts += [0, 0.4]
    upper = [pnt for pnt in pnts if f(pnt[0]) > pnt[1] + margin]
    lower = [pnt for pnt in pnts if f(pnt[0]) < pnt[1] - margin]

    # rotate the points
    angle = np.random.randint(0, 90)
    upper, lower = rotate(upper, angle), rotate(lower, angle)

    # combine points into one array and create a label vector to distinguish them
    # (red vs. blue)
    all_pnts = np.concatenate((upper, lower))
    labels = [RED] * len(upper) + [BLUE] * len(lower)
    all_pnts, labels = np.array(all_pnts), np.array(labels)

    ##
    upper, lower = np.array(upper), np.array(lower)

    # plot points colored by classes
    plt.subplot(1, 2, 1)
    plot_pnts(upper, lower)

    # find axis of crompression using LDA and compress
    slp = get_slope_lda(all_pnts, labels)
    upper_crumple = Crumple(upper, slp)
    lower_crumple = Crumple(lower, slp)

    # plot points again
    plt.subplot(1, 2, 2)
    plot_pnts(upper, lower)

    # plot crumpled hulls
    plt.plot(upper_crumple.ne[:, 0], upper_crumple.ne[:, 1], color='k')
    plt.plot(upper_crumple.sw_convex[:, 0], upper_crumple.sw_convex[:, 1], color='k')

    plt.plot(lower_crumple.ne_convex[:, 0], lower_crumple.ne_convex[:, 1], color='g')
    plt.plot(lower_crumple.sw[:, 0], lower_crumple.sw[:, 1], color='g')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()