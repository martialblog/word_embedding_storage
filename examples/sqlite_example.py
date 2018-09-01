#!/usr/bin/env python3


import dummy
import sqlite3
import numpy
from io import BytesIO


def adapt_array(array):
    """
    Using the numpy.save function to save a binary version of the array,
    and BytesIO to catch the stream of data and convert it into a sqlite3.Binary.

    :param numpy.array array: NumPy array to turn into sqlite3.Binary
    :return: NumPy array as sqlite3.Binary
    :rtype: sqlite3.Binary
    """
    out = BytesIO()
    numpy.save(out, array)
    out.seek(0)

    return sqlite3.Binary(out.read())


def convert_array(blob):
    """
    Using BytesIO to convert the binary version of the array back into a numpy array.

    :param sqlite3.Binary blob: sqlite3.Binary containing a NumPy array
    :return: One steaming hot NumPy array
    :rtype: numpy.array
    """
    out = BytesIO(blob)
    out.seek(0)

    return numpy.load(out)


# Register the adapters
sqlite3.register_adapter(numpy.ndarray, adapt_array)
sqlite3.register_converter('array', convert_array)

connection = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
cursor = connection.cursor()

cursor.execute('CREATE TABLE embeddings (key text, embedding array)')

#########
# Write #
#########
for key, emb in dummy.embeddings():
    cursor.execute('INSERT INTO embeddings (key, embedding) VALUES (?, ?)', [key, emb])

########
# Read #
########
for key, emb in dummy.embeddings():
    cursor.execute('SELECT * FROM embeddings WHERE key=?', (key,))
    data = cursor.fetchone()

connection.close()
