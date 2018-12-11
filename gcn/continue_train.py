import h5py
import numpy as np
from keras.models import Input, Model, Sequential
from keras.layers import Dense, Activation, Dropout, Lambda
import keras.backend as K
from sklearn.utils import shuffle
import os
from utils import *
import h5py
from keras_dgl.layers import MultiGraphCNN
from datetime import datetime
import errno
from keras import optimizers

nb_epochs = 50
batch_size = 169

X_shape = (None, 21, 1024)
graph_shape = (None, 1029, 21)
Y_shape = (None, 2)
SYM_NORM = True
num_filters = 49

file_dir = '/home/yaoshihu/downloads/data'
data_name = 'gcn_input_features.h5'
folders = ["00" + str(i) for i in range(10, 20)]

log_dir = "./logs/gcn_logs.txt"
loss_dir = "./logs/loss_history.txt"

def load_from_dir(file_dir):
    file = h5py.File(file_dir, 'r')
    node_features = file['node_feature'].value
    edge_features = file['edge_feature'].value
    labels = file['labels'].value
    return node_features, edge_features, labels

def build_model(X_shape, graph_shape, Y_shape, num_filters):
    # build model
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
    return model

def os_mkdir(dir_to_create):
    try:
        os.mkdir(dir_to_create)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass

def save_numpy_array(file_name, call_back, folder="First"):
    loss = call_back.history["loss"]
    acc = call_back.history["acc"]
    val_acc = call_back.history["val_acc"]
    val_loss =call_back.history["val_loss"]
    with open(file_name, "a+") as model_file:
        model_file.write("History of folder {} at time {}\n".format(folder, datetime.now()))
        for i in range(len(loss)):
            model_file.write("loss: {}, acc: {}, val_acc: {}, val_loss: {}\n".
                format(loss[i], acc[i], val_acc[i], val_loss[i]))

if __name__ == '__main__':
    print("Data Folders: {}".format(folders))

    print("Building Model")
    model = build_model(X_shape, graph_shape, Y_shape, num_filters)
    model.load_weights('./models/model_weights.h5')

    for folder in folders:
        with open(log_dir, "a") as log_file:
            log_file.write("{} Start Training {}\n".format(datetime.now(), folder))
        print("Start loading folder number {}".format(folder))
        X, A, Y = load_from_dir(os.path.join(file_dir, folder, data_name))
        print("Finish loading folder number {}".format(folder))
        A, X, Y = shuffle(A, X, Y)
        # build graph_conv_filters
        graph_conv_filters = preprocess_edge_adj_tensor(A, SYM_NORM)

        print("Training Start")
        call_back = model.fit([X, graph_conv_filters], Y, batch_size=batch_size, 
            validation_split=0.1, epochs=nb_epochs, shuffle=True, verbose=1)
        # logging the data
        save_numpy_array(loss_dir, call_back, folder)
        loss, accuracy = model.evaluate([X, graph_conv_filters], Y)
        with open(log_dir, "a") as log_file:
            log_file.write("Finish training {} at {}\n".format(folder, datetime.now()))
            log_file.write("Accuracy: {}\nLoss: {}\n".format(accuracy, loss))
        print("For the data used in training: \nLoss: {}\nAccuracy: {}".format(loss, accuracy))

    model.save_weights("./models/model_weights.h5")
    print('saved_weights')
    