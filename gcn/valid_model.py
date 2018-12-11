# model reconstruction from JSON:
from keras_dgl.layers import MultiGraphCNN
from keras.models import model_from_json
import json
from keras.models import Input, Model, Sequential
from keras.layers import Dense, Activation, Dropout, Lambda
import keras.backend as K
import h5py
from keras import optimizers
from utils import *
import sys, os

def load_from_dir(file_dir):
    file = h5py.File(file_dir, 'r')
    node_features = file['node_feature'].value
    edge_features = file['edge_feature'].value
    labels = file['labels'].value
    return node_features, edge_features, labels

X_shape = (None, 21, 1024)
graph_shape = (None, 1029, 21)
Y_shape = (None, 2)
SYM_NORM = True
num_filters = 49

# build model
def build_model(X_shape, graph_shape, Y_shape, num_filters):
    X_input = Input(shape=(X_shape[1], X_shape[2]))
    graph_conv_filters_input = Input(shape=(graph_shape[1], graph_shape[2]))

    output = MultiGraphCNN(100, num_filters, activation='elu')([X_input, graph_conv_filters_input])
    output = Dropout(0.2)(output)
    output = MultiGraphCNN(100, num_filters, activation='elu')([output, graph_conv_filters_input])
    output = Dropout(0.2)(output)
    output = Lambda(lambda x: K.mean(x, axis=1))(output)  # adding a node invariant layer to make sure output does not depends upon the node order in a graph.
    output = Dense(Y_shape[1])(output)
    output = Activation('softmax')(output)

    model = Model(inputs=[X_input, graph_conv_filters_input], outputs=output)
    model.compile(loss='categorical_crossentropy', 
        optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), 
        metrics=['acc'])

    model.load_weights('models/model_weights.h5')
    return model

def main(args):
    if len(args) <= 1 and args[1] != 'origin' and args[1] != 'train' and args[1] != 'dir':
        raise ValueError("Input can only be 'origin', 'train' or 'dir <custom_dir>'")

    else:
        model = build_model(X_shape, graph_shape, Y_shape, num_filters)
        if args[1] == 'origin':
            train_positive_file = '/home/yaoshihu/downloads/data/training_input_positive.h5'
            train_negative_file = '/home/yaoshihu/downloads/data/training_input_negative.h5'
            test_positive_file = '/home/yaoshihu/downloads/data/testing_input_positive.h5'
            test_negative_file = '/home/yaoshihu/downloads/data/testing_input_negative.h5'

            dirs = [train_positive_file, train_negative_file, test_positive_file, test_negative_file]

            for file_dir in dirs:
                print("For {}".format(file_dir[30:-3]))
                print("Start loading data")
                X, A, Y = load_from_dir(file_dir)
                print("Finish loading data")
                graph_conv_filters = preprocess_edge_adj_tensor(A, SYM_NORM)
                loss, accuracy = model.evaluate([X, graph_conv_filters], Y)
                print("Loss: {}\nAccuracy: {}".format(loss, accuracy))

        elif args[1] == 'train':
            file_dir = '/home/yaoshihu/downloads/data'
            data_name = 'gcn_input_features.h5'
            paths = [os.path.join(file_dir, "00"+str(i), data_name) for i in range(20)]
            for path in paths:
                print("Start loading data")
                X, A, Y = load_from_dir(path)
                print("Finish loading data")
                graph_conv_filters = preprocess_edge_adj_tensor(A, SYM_NORM)
                loss, accuracy = model.evaluate([X, graph_conv_filters], Y)
                print("Loss: {}\nAccuracy: {}".format(loss, accuracy))

        elif args[1] == 'dir':
            print("Start loading data")
            X, A, Y = load_from_dir(args[2])
            print("Finish loading data")
            graph_conv_filters = preprocess_edge_adj_tensor(A, SYM_NORM)
            loss, accuracy = model.evaluate([X, graph_conv_filters], Y)
            print("Loss: {}\nAccuracy: {}".format(loss, accuracy))

if __name__ == "__main__":
    main(sys.argv)
