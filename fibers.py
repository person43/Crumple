from concave_sides import *
from sklearn.decomposition import PCA
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

    return fibers


# INCOMPLETE: so far only works in one slope/orientation, with y=x and
# y=-x being the reflection axese, and having the original point set be
# the left most square in that arrangement
def fiberize_corner(pnts, slp):
    angle = np.arctan(slp)
    angle = np.degrees(angle)
    pnts = rotate(pnts, angle)

    # br is the original pnts
    tr_pnts = mirror_pnts(pnts, 1, TOP)
    tl_pnts = mirror_pnts(tr_pnts, -1, BOTTOM)
    bl_pnts = mirror_pnts(pnts, -1, BOTTOM)
    all_pnts = np.concatenate((pnts, tr_pnts, tl_pnts, bl_pnts))
    colors = {}
    for i, pnt in enumerate(all_pnts):
        if i < len(pnts):
            colors[tuple(pnt)] = BLUE
        else:
            colors[tuple(pnt)] = RED
    layers = onion_layers(all_pnts)
    vec = np.array([1, 1])
    fibers = []
    for layer in layers:
        layer = np.array([pnt for pnt in layer if colors[tuple(pnt)] == BLUE])
        if len(layer) == 0:
            continue
        if np.array_equal(layer[0], layer[-1]) and len(layer) > 1:
            layer = layer[:-1]
        proj = np.dot(layer, vec)
        i_min = np.argmin(proj)
        layer = np.concatenate((layer[i_min:], layer[:i_min]))
        layer = rotate(layer, -angle)
        fibers.append(np.array(layer))
    return fibers


def spinal_tap(pnts):
    slp = do_pca(pnts)
    fibers = fiberize_corner(pnts, slp)
    spine = []
    for layer in fibers:
        # plt.plot(layer[:,0], layer[:,1], color='k', linewidth=2)
        # if len(layer) % 2:
        #     ind = len(layer) // 2
        #     med = layer[ind]
        # else:
        #     hi = len(layer) // 2
        #     lo = hi - 1
        #     med = np.mean(np.array([layer[hi], layer[lo]]), 0)
        ind = len(layer) // 2
        med = layer[ind]
        spine.append(med)
    spine = np.array(spine)
    proj = np.dot(spine, np.array([1, slp*1]))
    indices = np.argsort(proj)
    return spine[indices]


def do_pca(pnts):
    pca = PCA(n_components=1)
    pca.fit(pnts)
    vec = pca.components_[0]
    return vec[1]/vec[0]