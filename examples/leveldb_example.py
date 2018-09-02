#!/usr/bin/env python3


import dummy
import numpy
import plyvel
from io import BytesIO


def adapt_array(array):
    """
    Using the numpy.save function to save a binary version of the array,
    and BytesIO to catch the stream of data and convert it into a BLOB.

    :param numpy.array array: NumPy array to turn into sqlite3.Binary
    :return: NumPy array as BLOB
    :rtype: BLOB
    """
    out = BytesIO()
    numpy.save(out, array)
    out.seek(0)

    return out.read()


def convert_array(blob):
    """
    Using BytesIO to convert the binary version of the array back into a numpy array.

    :param BLOG blob: BLOB containing a NumPy array
    :return: One steaming hot NumPy array
    :rtype: numpy.array
    """
    out = BytesIO(blob)
    out.seek(0)

    return numpy.load(out)


connection = plyvel.DB('./leveldb.embedding.db', create_if_missing=True)

#########
# Write #
#########
for key, emb in dummy.embeddings():
    arr = adapt_array(emb)
    connection.put(key.encode(), arr)

########
# Read #
########
for key, _ in dummy.embeddings():
    arr = connection.get(key.encode())
    emb = convert_array(arr)
    assert(type(emb) is numpy.ndarray)

connection.close()
