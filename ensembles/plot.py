import math

import numpy as np
import matplotlib as plt
import matplotlib.patches as plt_patch

def text(cx, x : float, y : float, message : str, **kwargs):
    xl = cx.get_xlim()
    yl = cx.get_ylim()
    cx.text(xl[0]*(1-x)+xl[1]*x, yl[0]*(1-y)+yl[1]*y, message, **kwargs)

def show_real_spectrum(cx, z, only_positive=False):
    assert np.all(np.abs(np.imag(z))<1e-10)
    m = 1.1*np.max(np.abs(z))

    cx.hist(np.real(z), density=True, color='C7')
    cx.set_xlabel('$\\mathrm{Re}\\lambda$')
    cx.set_ylabel('Density')
    if only_positive:
        cx.set_xlim([-0.1*m, m])
    else:
        cx.set_xlim([-m, m])
    cx.spines["right"].set_visible(False)
    cx.spines["top"].set_visible(False)

# Show an eigenvalue spectrum
def show_complex_spectrum(cx, z, radius=None, center=[0, 0], rotation=1,
                          show_center=False, outlier=None, equal_aspect=True):
    if np.abs(rotation) == 0:
        angle = 0
    else:
        rotation /= np.abs(rotation)
        angle = np.arctan2(np.imag(rotation), np.real(rotation))*180/math.pi
    mx1 = np.max(np.real(z))
    mx0 = np.min(np.real(z))
    my1 = np.max(np.imag(z))
    my0 = np.min(np.imag(z))
    if radius is not None:
        mx1 = np.maximum(mx1, center[0]+radius[0])
        mx0 = np.minimum(mx0, center[0]-radius[0])
        my1 = np.maximum(my1, center[1]+radius[1])
        my0 = np.minimum(my0, center[1]-radius[1])
    
    if outlier is not None:
        cx.plot(outlier[0], outlier[1], 'x', color='C8', markersize=20)
        mx0 = np.minimum(mx0, outlier[0])
        mx1 = np.maximum(mx1, outlier[0])
        my0 = np.minimum(my0, outlier[1])
        my1 = np.maximum(my1, outlier[1])
    
    cx.scatter(np.real(z), np.imag(z), color='C7', edgecolor='w')

    if radius is not None:
        ellipsis = plt_patch.Ellipse(center, 2*radius[0], 2*radius[1],
                                     color='C1', fill=None, angle=angle, 
                                     linewidth=1.5)
        cx.add_patch(ellipsis)

    if show_center:
        cx.plot(0, 0, '+k', markersize=40)
        mx0 = np.minimum(mx0, 0)
        mx1 = np.maximum(mx1, 0)
        my0 = np.minimum(my0, 0)
        my1 = np.maximum(my1, 0)

    cx.set_xlabel('$\\mathrm{Re}\\lambda$')
    cx.set_ylabel('$\\mathrm{Im}\\lambda$')

    if equal_aspect:
        cx.set_aspect('equal')
        m = np.maximum(np.maximum(-mx0, mx1), np.maximum(-my0, my1))
        cx.set_xlim([-1.1*m, 1.1*m])
        cx.set_ylim([-1.1*m, 1.1*m])
    else:
        cx.set_xlim([1.1*mx0-0.1*mx1, 1.1*mx1-0.1*mx0])
        cx.set_ylim([1.1*my0-0.1*my1, 1.1*my1-0.1*my0])

    cx.spines["right"].set_visible(False)
    cx.spines["top"].set_visible(False)
