from concave_sides import *

class Crumple:

    def __init__(self, pnts, slp):
        southwest_side = concave_side(pnts, slp)
        r_pnts = mirror_pnts(pnts, slp, TOP)
        northeast_side = concave_side(r_pnts, slp)
        northeast_side = mirror_pnts(northeast_side, slp, BOTTOM)
        self.points = pnts
        self.slope = slp
        self.ne, self.sw = northeast_side, southwest_side

        if np.allclose(self.sw[0], self.ne[0]):
            self.hull = np.concatenate((self.sw[:-1], self.ne[::-1]))
            self.ne = self.ne[::-1]
        else:
            self.hull = np.concatenate((self.sw[:-1], self.ne))

        convex_hull = pnts[ConvexHull(pnts).vertices]
        self.sw_convex = convex_side(convex_hull, self.ne[0], self.ne[-1])
        self.ne_convex = convex_side(convex_hull, self.sw[0], self.sw[-1])

    def smoothen(self, maxd=1, winsize=7):
        p1 = np.array([0, 0])
        p2 = np.array([1, self.slope])
        dist = lambda pnt: np.linalg.norm(np.cross(p2 - p1, p1 - pnt)) / np.linalg.norm(p2 - p1)
        new_sides = []
        for side in [self.sw, self.ne]:
            perp = np.array([dist(p) for p in side])
            indices = [r for r in range(winsize)]
            i = winsize
            for d in perp[winsize:-(winsize+1)]:
                med, mad = mstats(perp[i-winsize:i+winsize])
                if abs(med - d) < maxd*mad or i in [0, len(perp)-1]:
                    indices.append(i)
                i += 1
            indices += [r for r in range(i, len(perp))]
            indices = np.array(indices)
            new_sides.append(side[indices])
        self.sw, self.ne = new_sides[0], new_sides[1]




