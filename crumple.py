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