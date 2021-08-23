"""
See https://github.com/3b1b/manim/pull/839/files
Credit to 
Garrett Credi [ddxtanx]
"""

from manim import *

def _symmetrize(dic: dict):
    symm = {}
    for key, value in dic.items():
        symm[value] = key

    symm.update(dic)
    return symm


class ImplicitFunction(VMobject):
    """
    Graphs an implicit function defined by f(x,y) = 0
    """
#     CONFIG = {
#         "res": 50
#     }

    def __init__(self, function=None, x_max=None, x_min=None, y_max=None, y_min=None, res=100, **kwargs):
        """
        :param function: Function of k and y to graph isocontour f(x,y)=0
        """
        # digest_config(self, kwargs)
        self.function = function
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.res = res

        VMobject.__init__(self, **kwargs)

    def get_function(self):
        return self.function

    def get_function_val_at_point(self, x, y):
        return self.function(x, y)

    def sample_function_mask(self):
        """
        :return: A mask over the plane at the specified resolution capturing function
                 values at each point.
        """
        delta_x = self.x_max - self.x_min
        delta_y = self.y_max - self.y_min
        mask = []  # format: [point, val]
        for yi in range(0, self.res):
            dy = delta_y*(yi/self.res)
            y = self.y_min + dy
            vals = []
            for xi in range(0, self.res):
                dx = delta_x*(xi/self.res)
                x = self.x_min + dx
                point = np.array([x, y, 0])
                val = self.get_function_val_at_point(x, y)
                if val > 0:
                    vals.append([point, 1])
                elif val <= 0:
                    vals.append([point, 0])
            mask.append(vals)
        return mask

    def get_contours(self):
        """
        :return: A dictionary consisting of start -> list(end) points to generate contours.
        """
        mask = self.sample_function_mask()
        contours = {}
        for yi in range(0, len(mask)-1):
            yarr = mask[yi]
            nyarr = mask[yi+1]
            for xi in range(0, len(yarr)-1):
                tl = yarr[xi]
                tr = yarr[xi+1]
                bl = nyarr[xi]
                br = nyarr[xi+1]

                tlp = tl[0]
                tlv = tl[1]

                trp = tr[0]
                trv = tr[1]

                blp = bl[0]
                blv = bl[1]

                brp = br[0]
                brv = br[1]

                vals = [tlv, trv, brv, blv]  # change order to match marching squares order.
                vals_strs = list(map(lambda i: str(i), vals))
                vals_str = "".join(vals_strs)

                def calc_lin_interp(fc, fe, cv, ev):
                    """
                    :param fc: Function value at 'center' vertex
                    :param fe: Function value at 'edge' vertex
                    :param cv: The 'location' of the 'center' vertex (x or y depending)
                    :param ev: Similar to above for 'edge' vertex
                    :return: The x or y coordinate of the linear interpolation
                    """
                    return -(fc/(fe-fc))*(ev-cv) + cv

                def calc_lin_interp_diag(cent, side, vert):
                    """
                    :param cent: 'Center' point
                    :param side: 'Side' point w.r.t. cent
                    :param vert: 'Vertical' point w.r.t. cent
                    :return: Dict detailing path to follow of linear interpolation.
                    """
                    centx, centy = cent[:2]

                    sidex, sidey = side[:2]

                    vertx, verty = vert[:2]

                    qx = vertx
                    py = sidey

                    f_cent = self.get_function_val_at_point(centx, centy)
                    f_vert = self.get_function_val_at_point(vertx, verty)
                    f_side = self.get_function_val_at_point(sidex, sidey)

                    qy = calc_lin_interp(f_cent, f_vert, centy, verty)
                    px = calc_lin_interp(f_cent, f_side, centx, sidex)

                    p = (px, py, 0)
                    q = (qx, qy, 0)
                    return _symmetrize({p:q})

                def calc_lin_interp_sides():
                    """
                    :return: Horizontal linear interpolation
                    """
                    tlx, tly = tlp[:2]
                    trx, tr_y = trp[:2]
                    blx, bly = blp[:2]
                    brx, bry = brp[:2]

                    ftl = self.get_function_val_at_point(tlx, tly)
                    ftr = self.get_function_val_at_point(trx, tr_y)
                    fbl = self.get_function_val_at_point(blx, bly)
                    fbr = self.get_function_val_at_point(brx, bry)

                    px = tlx
                    qx = trx

                    py = calc_lin_interp(fbl, ftl, bly, tly)
                    qy = calc_lin_interp(fbr, ftr, bry, tr_y)

                    p = (px, py, 0)
                    q = (qx, qy, 0)

                    return _symmetrize({p:q})

                def calc_lin_interp_vert():
                    """
                    :return: Vertical linear interpolation
                    """
                    tlx, tly = tlp[:2]
                    trx, tr_y = trp[:2]
                    blx, bly = blp[:2]
                    brx, bry = brp[:2]

                    ftl = self.get_function_val_at_point(tlx, tly)
                    ftr = self.get_function_val_at_point(trx, tr_y)
                    fbl = self.get_function_val_at_point(blx, bly)
                    fbr = self.get_function_val_at_point(brx, bry)

                    py = bly
                    qy = tly

                    px = calc_lin_interp(fbl, fbr, blx, brx)
                    qx = calc_lin_interp(ftl, ftr, tlx, trx)

                    p = (px, py, 0)
                    q = (qx, qy, 0)

                    return _symmetrize({p:q})

                m_sqrs_dict = {
                    "0000": {},
                    "0001": calc_lin_interp_diag(blp, brp, tlp),
                    "0010": calc_lin_interp_diag(brp, blp, trp),
                    "0011": calc_lin_interp_sides(),
                    "0100": calc_lin_interp_diag(trp, tlp, brp),
                    "0101": {**calc_lin_interp_diag(tlp, trp, blp), **calc_lin_interp_diag(brp, blp, trp)},
                    "0110": calc_lin_interp_vert(),
                    "0111": calc_lin_interp_diag(tlp, trp, blp),
                    "1000": calc_lin_interp_diag(tlp, trp, blp),
                    "1001": calc_lin_interp_vert(),
                    "1010": {**calc_lin_interp_diag(trp, tlp, brp), **calc_lin_interp_diag(blp, brp, tlp)},
                    "1011": calc_lin_interp_diag(trp, tlp, brp),
                    "1100": calc_lin_interp_sides(),
                    "1101": calc_lin_interp_diag(brp, blp, trp),
                    "1110": calc_lin_interp_diag(blp, brp, tlp),
                    "1111": {}
                }
                # Dictionary describing how to form path given the binary signature.
                dic = m_sqrs_dict[vals_str]
                for k, v in dic.items():
                    if k in contours.keys() and v not in contours[k]:
                        contours[k].append(v)
                    elif k not in contours.keys():
                        contours[k] = [v]

        return contours

    def generate_points(self):
        contours = self.get_contours()

        def try_rem(arr, val):
            if val in arr:
                arr.remove(val)
            return arr

        def len_filter(dic):
            return {k: arr for k, arr in dic.items() if len(arr) > 0}
        """
        This generates path basically in a follow-the-points sort of manner.
        It starts at the 'first points' in the dictionary, starts a path at the
        'start' point and iteratively follows the path from the current point 
        to the first point in the current point's list of adjacent points.
        It does this until there is nowhere else to go for that curve and then
        proceeds to the next curve. At every point, current points are removed from
        the contours just to ensure no vertices are visited more than once.
        """
        while len(len_filter(contours).keys()) > 0:
            sptt, eptts = next(iter(len_filter(contours).items()))
            eptt = eptts[0]
            spta = np.array(sptt)
            epta = np.array(eptt)
            contours[sptt] = try_rem(contours[sptt], eptt)
            contours = {k: try_rem(arr, sptt) for k, arr in contours.items()}
            self.start_new_path(spta)
            cur_pt = epta
            pts = []
            while cur_pt is not None:
                pts.append(cur_pt)
                cur_ptt = tuple(cur_pt)
                if len(contours[cur_ptt])>0:
                    next_ptt = contours[cur_ptt][0]
                    next_pt = np.array(next_ptt)
                    cur_pt = next_pt
                    contours[cur_ptt] = try_rem(contours[cur_ptt], next_ptt)
                    contours = {k: try_rem(arr, cur_ptt) for k, arr in contours.items()}
                else:
                    cur_pt = None
            self.add_points_as_corners(pts)
        self.make_smooth()
        return self