import struct
import numpy as np
from file_class import algorithms_cycle

DATA_FORMAT = 'IH'
DATA_SIZE = 6
first_data = [[385719, 48], [290284, 65], [12841, 12], [56895, 57], [59203, 58], [92517, 76], [48898, 41]]


def first_record():
    data_file = open('data.bin', 'ab')
    data_file.seek(0)
    for i in range(len(algorithms_cycle)):
        data_file.write(struct.pack(DATA_FORMAT, first_data[i][0], first_data[i][1]))
    data_file.close()


def read_database():
    data_file = open('data.bin', 'rb')
    data = []
    for i in range(len(algorithms_cycle)):
        data.append(np.asarray(struct.unpack(DATA_FORMAT, data_file.read(DATA_SIZE))))
    data_file.close()
    return data


def update_database(data):
    data_file = open('data.bin', 'wb')
    data_file.truncate()
    data_file.close()
    data_file = open('data.bin', 'ab')
    data_file.seek(0)
    for i in range(len(algorithms_cycle)):
        data_file.write(struct.pack(DATA_FORMAT, data[i][0], data[i][1]))
    data_file.close()


if __name__ == '__main__':
    print(read_database())
