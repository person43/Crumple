from scipy.spatial import ConvexHull
import numpy as np

RED = 0
BLUE = 1
TOP = 1
BOTTOM = -1
MARGIN = 1

def mirror_pnts(pnts, slp, orientation):
    if slp == float('inf'):
        return horizontal_mirror(pnts, orientation)
    if orientation == TOP:
        f = max
        offset = MARGIN
    else:
        f = min
        offset = -MARGIN
    dim_max = f(pnts[:, 1] - slp*pnts[:, 0]) + offset
    d = (pnts[:, 0] + (pnts[:, 1] - dim_max) * slp) / (1 + slp**2)
    new_x = 2*d - pnts[:, 0]
    new_y = 2*d*slp - pnts[:, 1] + 2 * dim_max
    return np.array([new_x, new_y]).T

def horizontal_mirror(pnts, orientation):
    if orientation == TOP:
        f = max
        offset = MARGIN
    else:
        f = min
        offset = -MARGIN
    xmax = f(pnts[:,0])
    mirror = xmax + offset
    reflection = [[mirror + offset*abs(mirror-pnt[0]), pnt[1]] for pnt in pnts]
    reflection = np.array(reflection)
    return reflection


def onion_layers(pnts):
    core = pnts
    layers = []
    while len(core):
        if len(core) == 2:
            degenerate_layer = [core[0], core[1], core[0]]
            layers.append(np.array(degenerate_layer))
            break
        if len(core) == 1:
            degenerate_layer = [core[0]]
            layers.append(np.array(degenerate_layer))
            break
        hull = ConvexHull(core)
        layers.append(wrapped_hull(hull))
        core = [pnt for i, pnt in enumerate(core) if i not in hull.vertices]
        core = np.array(core)
    return layers


def wrapped_hull(hull):
    hull_pnts = hull.points[hull.vertices]
    return np.concatenate((hull_pnts, np.array([hull_pnts[0]])))


def find_breaks(layer, colors):
    in_pnt, out_pnt = None, None
    for pnt, last_pnt in zip(layer[1:], layer[:-1]):
        if colors[tuple(pnt)] == RED and colors[tuple(last_pnt)] == BLUE:
            in_pnt = last_pnt
        elif colors[tuple(pnt)] == BLUE and colors[tuple(last_pnt)] == RED:
            out_pnt = pnt
    return in_pnt, out_pnt


def find_border(layers, colors):
    inward_sides, outward_sides = [], []
    for layer in layers:
        in_pnt, out_pnt = find_breaks(layer, colors)
        inward_sides.append(in_pnt)
        outward_sides.append(out_pnt)
    return np.array(inward_sides + list(reversed(outward_sides)))


def concave_side(pnts, slp):
    r_pnts = mirror_pnts(pnts, slp, BOTTOM)
    all_pnts = np.concatenate((pnts, r_pnts))
    colors = {}
    for i, pnt in enumerate(all_pnts):
        if i < len(all_pnts)//2:
            colors[tuple(pnt)] = BLUE
        else:
            colors[tuple(pnt)] = RED
    layers = onion_layers(all_pnts)
    side = find_border(layers, colors)
    return side


def convex_side(convex_hull, top, bottom):
    for i, pnt in enumerate(convex_hull):
        if np.allclose(pnt, bottom):
            start = i
    for i, pnt in enumerate(convex_hull):
        if np.allclose(pnt, top):
            end = i
    if start > end:
        indices = [i % len(convex_hull) for i in range(start, len(convex_hull) + end + 1)]
    else:
        indices = [i % len(convex_hull) for i in (range(start, end + 1))]
    return convex_hull[np.array(indices)]

###########################################
# The following functions are helpful for #
# some of the example programs but not    #
# essential for the crumpling algorithm   #
###########################################

def rotate(pnts, angle):
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    return np.dot(pnts, R)


def find_bridges(layer, colors):
    b_0, b_1 = None, None
    for pnt, last_pnt in zip(layer[1:], layer[:-1]):
        if colors[tuple(pnt)] == RED and colors[tuple(last_pnt)] == BLUE:
            b_0 = [pnt, last_pnt]
        elif colors[tuple(pnt)] == BLUE and colors[tuple(last_pnt)] == RED:
            b_1 = [pnt, last_pnt]
    if b_0 is None or b_1 is None:
        return None
    b_0, b_1 = np.array(b_0), np.array(b_1)
    return np.concatenate((b_0, b_1))