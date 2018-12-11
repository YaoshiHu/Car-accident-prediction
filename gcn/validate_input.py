import h5py

target_file = '/home/yaoshihu/downloads/data/gcn_input_features.h5'

file = h5py.File(target_file, 'r')
node_features = file['node_feature'].value
edge_features = file['edge_feature'].value
labels = file['labels'].value

print(node_features.shape)
print(edge_features.shape)
print(labels.shape)
