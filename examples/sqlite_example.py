#!/usr/bin/env python3


import dummy
import sqlite3
import numpy
import io


def adapt_array(array):
    """
    Using the numpy.save function to save a binary version of the array,
    and BytesIO to catch the stream of data and convert it into a sqlite3.Binary.
    """
    out = io.BytesIO()
    numpy.save(out, array)
    out.seek(0)

    return sqlite3.Binary(out.read())

def convert_array(text):
    """
    Using BytesIO to convert the binary version of the array back into a numpy array.
    """
    out = io.BytesIO(text)
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
