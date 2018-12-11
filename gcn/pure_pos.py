import h5py
import numpy as np
import time
import os
import sys
from tqdm import tqdm
import errno


def save_h5(node_feature, edge_feature, label, filename, size):
    (h1, w1, d1) = np.shape(node_feature)
    (h2, w2, d2) = np.shape(edge_feature)
    (h3, w3) = np.shape(label)
    if size == 0:
        h5f = h5py.File(filename, 'w')
        node_set = h5f.create_dataset("node_feature", data=node_feature, maxshape=(None, w1, d1), dtype='float32')
        edge_set = h5f.create_dataset("edge_feature", data=edge_feature, maxshape=(None, w2, d2), dtype='float32')
        label_set = h5f.create_dataset("labels", data=label, maxshape=(None, w3), dtype='float32')
        h5f.close()

    else:
        h5f = h5py.File(filename, 'a')

        node_set = h5f['node_feature']
        node_set.resize([size+h1, w1, d1])
        node_set[size:] = node_feature

        edge_set = h5f['edge_feature']
        edge_set.resize([size+h2, w2, d2])
        edge_set[size:] = edge_feature

        label_set = h5f['labels']
        label_set.resize([size+h3, w3])
        label_set[size:] = label
        h5f.close()
    return size + h1


def generate_gcn_input():
    train_positive_file = '/home/yaoshihu/downloads/data/training_input_positive.h5'
    test_positive_file = '/home/yaoshihu/downloads/data/testing_input_positive.h5'
    
    try:
        os.mkdir('/home/yaoshihu/downloads/data/')
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

    target_file = '/home/yaoshihu/downloads/data/pure_positive.h5'

    def save_to_file(file_dir, ind):
        print("Loading data")
        file = h5py.File(file_dir, 'r')
        node_features = file['node_feature'].value
        edge_features = file['edge_feature'].value
        labels = file['labels'].value
        print("Finish loading data")

        index = 1
        while index*100 <= node_features.shape[0]:
            indexes = np.arange(90, 100)+(index-1)*100
            clip_node = node_features[indexes]
            clip_edge = edge_features[indexes]
            clip_label = labels[indexes]
            ind = save_h5(clip_node, clip_edge, clip_label, target_file, ind)
            index += 1
        return ind

    ind = 0
    print("Purifying Training Positive")
    ind = save_to_file(train_positive_file, ind)
    print("Purifying Testing Positive")
    ind = save_to_file(test_positive_file, ind)

if __name__ == "__main__":
    generate_gcn_input()
