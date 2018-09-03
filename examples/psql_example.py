#!/usr/bin/env python3

import numpy
import psycopg2
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json

import dummy


# Start a postgres database via Docker
# docker run -ti --rm --name word_psql -e POSTGRES_PASSWORD=mikolov -p 5433:5432 postgres:10.5


def addapt_numpy_ndarray(numpy_ndarray):
    return Json(numpy_ndarray.tolist())


connection = psycopg2.connect("host=localhost user=postgres password=mikolov port=5433")
register_adapter(numpy.ndarray, addapt_numpy_ndarray)
cursor = connection.cursor()

cursor.execute('CREATE TABLE embeddings (key varchar, embedding jsonb);')
connection.commit()

#########
# Write #
#########
for key, emb in dummy.embeddings():
    cursor.execute('INSERT INTO embeddings (key, embedding) VALUES (%s, %s)', [key, emb])
    connection.commit()

########
# Read #
########
for key, _ in dummy.embeddings():
    cursor.execute('SELECT key, embedding FROM embeddings WHERE key=%s', (key,))
    data = cursor.fetchone()
    value = numpy.array(data[1])
    assert type(value) is numpy.ndarray
    assert len(value) is 50


cursor.execute('DROP TABLE embeddings')
connection.commit()

connection.close()
