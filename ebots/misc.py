from __future__ import division
from functools import partial

import matplotlib.pyplot as plt
import numpy


random = partial(numpy.random.uniform, low=-1, high=1)


def generalized_logistic(t, A, B, K, M, Q, nu):
    return A + ((K - A) / ((1 + Q * numpy.exp(-B * (t - M))) ** (1 / nu)))


def _blob(x, y, area, colour):
    '''
    Draws a square-shaped blob with the given area (< 1) at
    the given coordinates. https://gist.github.com/292018
    '''
    hs = numpy.sqrt(area) / 2
    xcorners = numpy.array([x - hs, x + hs, x + hs, x - hs])
    ycorners = numpy.array([y - hs, y - hs, y + hs, y + hs])
    plt.fill(xcorners, ycorners, colour, edgecolor=colour)


def hinton(W, maxweight=None):
    '''
    Draws a Hinton diagram for visualizing a weight matrix.
    Temporarily disables matplotlib interactive mode if it is on,
    otherwise this takes forever. https://gist.github.com/292018
    '''

    plt.figure()
    height, width = W.shape

    if not maxweight:
        maxweight = 2 ** numpy.ceil(numpy.log(numpy.max(numpy.abs(W))) / numpy.log(2))

    plt.fill(numpy.array([0, width, width, 0]),
             numpy.array([0, 0, height, height]),
             'gray')

    plt.axis('off')
    plt.axis('equal')

    for x in range(width):
        for y in range(height):
            _x = x + 1
            _y = y + 1
            w = W[y, x]

            if w > 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1, w / maxweight), 'white')
            elif w < 0:
                _blob(_x - 0.5, height - _y + 0.5, min(1, -w / maxweight), 'black')
