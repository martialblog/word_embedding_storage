#!/usr/bin/env python3


"""
This command line tool with convert a Gensim KeyedVector file into a LevelDB with lexical items as keys
and embeddings as values.
"""


import plyvel
import numpy
from argparse import ArgumentParser
from gensim.models.keyedvectors import KeyedVectors
from io import BytesIO
from tqdm import tqdm


def create_parser():
    """
    Settings for argparse
    """

    parser = ArgumentParser(description='Loads a gensim KeyedVector file into a LevelDB')

    parser.add_argument(
        '--input',
        help='KeyedVector file to convert',
        dest='input',
        type=str,
        required=True
    )

    parser.add_argument(
        '--output',
        help='LevelDB output path. Default: ./leveldb.embedding.db',
        dest='output',
        type=str,
        required=False
    )

    parser.set_defaults(output='./leveldb.embedding.db')

    return parser


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


def main(argsparser):
    """
    Where the magic happens
    """

    args = argsparser.parse_args()
    vectors_filepath = args.input
    leveldb_filepath = args.output

    try:
        embeddings = KeyedVectors.load(vectors_filepath)
    except FileNotFoundError:
        print('Error. KeyedVector file not found.')
        exit(1)

    connection = plyvel.DB(leveldb_filepath, create_if_missing=True)

    for key in tqdm(embeddings.vocab):
        arr = adapt_array(embeddings[key])
        connection.put(key.encode(), arr)

    connection.close()
    exit(0)


if __name__ == '__main__':

    CMDARGS = create_parser()
    main(CMDARGS)
