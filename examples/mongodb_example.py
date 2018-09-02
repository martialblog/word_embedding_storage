#!/usr/bin/env python3


import dummy
import numpy
import bson
import pymongo
from io import BytesIO


# Start a Mongo database via Docker
# docker run -it --rm --name ohmongo -e MONGO_INITDB_ROOT_USERNAME=mikolov -e MONGO_INITDB_ROOT_PASSWORD=word2vec -p 27017:27017 mongo:4


def adapt_array(array):
    """
    Using the numpy.save function to save a binary version of the array,
    and BytesIO to catch the stream of data and convert it into a bson.binary.Binary

    :param numpy.array array: NumPy array to turn into BLOB
    :return: NumPy array as bson.binary.Binary
    :rtype: bson.binary.Binary
    """
    out = BytesIO()
    numpy.save(out, array)
    out.seek(0)

    return bson.binary.Binary(out.read())


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


uri = 'mongodb://mikolov:word2vec@localhost:27017'
client = pymongo.MongoClient(uri)

database = client['embedding_db']
embeddings_collection = database['embeddings']

#########
# Write #
#########
for key, emb in dummy.embeddings():
    arr = adapt_array(emb)
    obj = {'key': key, 'emb': arr}
    embeddings_collection.insert_one(obj)

########
# Read #
########
for key, _ in dummy.embeddings():
    obj = embeddings_collection.find_one({'key': key})
    emb = convert_array(obj['emb'])
    assert(type(emb) is numpy.ndarray)

embeddings_collection.delete_many({})

client.close()
