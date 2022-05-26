import numpy as np
import tensorflow as tf
from math import ceil


def generate_mus(filename, folder="Converted"):
    name = "../Data/"+folder+"/" + filename + "/song.npy"
    furie = np.load(name)
    with open("../Data/"+folder+"/" + filename + "/SongInfo.txt", 'r') as f:
        beat = float(f.read().split(" ")[0])
    return furie, beat


def generate_mus_test():
    name = "../Data/Testing Songs/1/song.npy"
    furie = np.load(name)
    with open("../Data/Testing Songs/1/SongInfo.txt", 'r') as f:
        beat = float(f.read().split(" ")[0])
    return furie, beat



def givePureCouple(song_name):
    song_path = song_name
    furie, beat = generate_mus(song_name)
    with open("../Data/Converted/" + song_name + "/TextLevel.txt",
              'r') as f:
        level = f.read()
        level = level.split(" ")
        level = np.array(level)
        level = level.astype("int")

    return furie, level


def giveSong():
    furie, beat = generate_mus_test()
    return furie, beat


def divide(X, part, seed = -1):
    X1 = []
    X2 = []
    indx = np.random.permutation((len(X)))
    if seed !=-1:
      indx = np.random.RandomState(seed=42).permutation((len(X)))
    for i in range(len(X)):
        if(i<part*len(X)):
            X1.append(X[indx[i]])
        else:
            X2.append(X[indx[i]])
    return X1, X2


def pure_generator(X, tokenizator, batch_size=1, max_len=10000):
    idx = np.random.permutation((len(X)))
    batchX = []
    batchY = []
    while True:
        for i in idx:
            furie, level = givePureCouple(X[i])
            if level.shape[0] < max_len:
                batchX.append(furie)
                batchY.append(np.array(tokenizator.tokenize(level, make_drop=True, prob=0.001)))
            if len(batchX) >= batch_size:
                max_lenX = batchX[0].shape[0]
                max_lenY = batchY[0].shape[0]
                for x in batchX:
                    if x.shape[0] > max_lenX:
                        max_lenX = x.shape[0]
                for y in batchY:
                    if y.shape[0] > max_lenY:
                        max_lenY = y.shape[0]
                for i in range(len(batchX)):
                    add_shape = (batchX[i].shape[1], max_lenX - batchX[i].shape[0])
                    batchX[i] = np.c_[batchX[i].transpose(), np.zeros(add_shape)].transpose()
                    batchY[i] = np.concatenate((batchY[i], np.zeros((max_lenY - batchY[i].shape[0],))))
                batchX = np.array(batchX)
                batchX = batchX.astype("float16")
                batchX = tf.convert_to_tensor(np.array(batchX))
                batchY = (np.array(batchY)).astype("int32")
                batchY = tf.convert_to_tensor(batchY)
                yield batchX, batchY
                batchX = []
                batchY = []
        idx = np.random.permutation(idx)


def create_generators(song_names, tokenizator, batch_size=1, test_size = 0.1):
    max_len = 3000
    X_test, X_train = divide(song_names, test_size)

    g_train = pure_generator(X_train, tokenizator, batch_size=batch_size)
    g_test = pure_generator(X_train, tokenizator, batch_size=batch_size)

    return g_train, g_test


