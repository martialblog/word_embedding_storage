#!/usr/bin/env python3


import dummy
import numpy
import mysql.connector
from io import BytesIO


# Start an MySQL database
# docker run -ti --rm --name ohmysql -e MYSQL_ROOT_PASSWORD=mikolov -e MYSQL_DATABASE=embeddings -p 3306:3306 mysql:5.7


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


connection = mysql.connector.connect(user='root', password='mikolov',
                              host='127.0.0.1',
                              database='embeddings')

cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS `embeddings` (`key` TEXT, `embedding` BLOB);')

#########
# Write #
#########

for key, emb in dummy.embeddings():
    arr = adapt_array(emb)
    cursor.execute('INSERT INTO `embeddings` (`key`, `embedding`) VALUES (%s, %s);', (key, arr))

########
# Read #
########
for key, emb in dummy.embeddings():
    cursor.execute('SELECT embedding FROM `embeddings` WHERE `key`=%s;', (key,))
    data = cursor.fetchone()
    arr = convert_array(data[0])

cursor.execute('DROP TABLE `embeddings`;')

connection.close()
