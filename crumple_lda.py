from crumple import Crumple
from concave_sides import *
import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from scipy.interpolate import interp1d

from scipy.signal import butter, lfilter

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False, output='ba')
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


# returns slope orthogonal to lda slope and correspoinding vector
def do_lda(all_pnts, labels):
    lda = LDA()
    lda.fit(all_pnts, labels)
    return -lda.coef_[0][0] / lda.coef_[0][1], np.array([lda.coef_[0][1], -lda.coef_[0][0]])

def plot_pnts(upper, lower):
    plt.scatter(upper[:, 0], upper[:, 1], color='r')
    plt.scatter(lower[:, 0], lower[:, 1], color='b')
    plt.gca().set_aspect('equal', adjustable='box')

def plot_hulls(upper_crumple, lower_crumple):
    plt.plot(upper_crumple.ne[:, 0], upper_crumple.ne[:, 1], color='k')
    plt.plot(upper_crumple.sw_convex[:, 0], upper_crumple.sw_convex[:, 1], color='k')

    plt.plot(lower_crumple.ne_convex[:, 0], lower_crumple.ne_convex[:, 1], color='g')
    plt.plot(lower_crumple.sw[:, 0], lower_crumple.sw[:, 1], color='g')

def plot_axis(vec):
    ax.set_autoscale_on(False)
    vec *= 1000
    plt.plot([0, vec[0]], [0, vec[1]], color='m', linestyle='dashed')
    plt.plot([0, -vec[0]], [0, -vec[1]], color='m', linestyle='dashed')
    vec /= 1000

def find_border(upper_crumple, lower_crumple, vec):
    upper_proj = project(lower_crumple.sw, vec)
    lower_proj = project(upper_crumple.ne, vec)

    if upper_proj[0][0] > upper_proj[-1][0]:
        upper_proj = upper_proj[::-1]
    if lower_proj[0][0] > lower_proj[-1][0]:
        lower_proj = lower_proj[::-1]

    xmin = max(upper_proj[0][0], lower_proj[0][0])
    xmax = min(upper_proj[-1][0], lower_proj[-1][0])
    f_upper = interp1d(upper_proj[:,0], upper_proj[:,1], kind=1)
    f_lower = interp1d(lower_proj[:,0], lower_proj[:,1], kind=1)

    num_pnts = np.mean((len(upper_proj), len(lower_proj)))
    time = np.linspace(xmin, xmax, num_pnts)
    ynew = [(a + b) / 2 for a, b in zip(f_upper(time), f_lower(time))]

    # ynew = butter_lowpass_filter(ynew, 10, )
    sig = [[t, y] for t, y in zip(time, ynew)]
    sig = np.array(sig)



    return project(sig, vec, -1)

def project(pnts, vec, sgn=1):
    angle = np.arctan(vec[1]/vec[0])
    angle *= (180/np.pi)
    return rotate(pnts, angle*sgn)


if __name__ == "__main__":
    # np.random.seed(1)
    # generate some points, split them into two classes according to
    # function f and a margin
    # def f(x): return 0.7*np.sin(2*x)
    def f(x): return x**5
    margin = 0.05
    pnts = np.random.randn(200, 2)
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
    upper, lower = np.array(upper), np.array(lower)


    # find axis of crompression using LDA and compress
    slp, vec = do_lda(all_pnts, labels)
    upper_crumple = Crumple(upper, slp)
    lower_crumple = Crumple(lower, slp)

    # plot points
    ax = plt.subplot(1, 2, 1)
    plot_pnts(upper, lower)

    # plot crumpled hulls
    plot_hulls(upper_crumple, lower_crumple)

    # plot crumple axis
    plot_axis(vec)

    ###############
    # SECOND PLOT #
    ###############

    ax = plt.subplot(1, 2, 2)
    sig = find_border(upper_crumple, lower_crumple, vec)

    plot_pnts(upper, lower)
    lines = plt.plot(sig[:,0], sig[:,1])
    plt.setp(lines, linewidth=2, color = 'g')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.draw()
    plt.show()