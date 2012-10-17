from functools import partial
import numpy


random = partial(numpy.random.uniform, low=-1, high=1)


def generalized_logistic(t, A, B, K, M, Q, nu):
    return A + ((K - A) / ((1 + Q * numpy.exp(-B * (t - M))) ** (1 / nu)))
