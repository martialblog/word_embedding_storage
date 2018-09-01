#!/usr/bin/env python3


import numpy


def embeddings(n=1000, dim=50):
    """
    Yield n tuples of random numpy arrays of *dim* length indexed by *n*
    """

    idx = 0
    while idx < n:
        yield (str(idx), numpy.random.rand(dim))
        idx += 1
