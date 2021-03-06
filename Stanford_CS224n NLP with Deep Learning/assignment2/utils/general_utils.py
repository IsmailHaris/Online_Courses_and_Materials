import sys
import time
import numpy as np


def get_minibatches(data, minibatch_size, shuffle=True):
    """
    Iterates through the provided data one minibatch at at time. You can use this function to
    iterate through data in minibatches as follows:

        for inputs_minibatch in get_minibatches(inputs, minibatch_size):
            ...

    Or with multiple data sources:

        for inputs_minibatch, labels_minibatch in get_minibatches([inputs, labels], minibatch_size):
            ...

    Args:
        data: there are two possible values:
            - a list or numpy array
            - a list where each element is either a list or numpy array
        minibatch_size: the maximum number of items in a minibatch
        shuffle: whether to randomize the order of returned data
    Returns:
        minibatches: the return value depends on data:
            - If data is a list/array it yields the next minibatch of data.
            - If data a list of lists/arrays it returns the next minibatch of each element in the
              list. This can be used to iterate through multiple data sources
              (e.g., features and labels) at the same time.

    """
    list_data = type(data) is list and (type(data[0]) is list or type(data[0]) is np.ndarray)
    #To test whether the input data is a list of lists/arrays or not
    data_size = len(data[0]) if list_data else len(data)
    #To meansure the length of 1st list in the list of lists, or to measure the length of the list of data.
    indices = np.arange(data_size)
    if shuffle:
        np.random.shuffle(indices)
    for minibatch_start in np.arange(0, data_size, minibatch_size):
        minibatch_indices = indices[minibatch_start:minibatch_start + minibatch_size]
        #minibatch_indices is still to calculate the indices for the mini-batch
        yield [_minibatch(d, minibatch_indices) for d in data] if list_data \
            else _minibatch(data, minibatch_indices) 
        # so _minibatch is another funtion defined as below - -
'''
---------Grammar on 'yield' expression----------
yield is a keyword that is used like return, except the function will return a generator.
Generators are iterators, a kind of iterable you can only iterate over once. 
Generators do not store all the values in memory, they generate the values on the fly.
'''

'''
---------Note on the for loop here------------
In [13]: for minibatch_start in np.arange(0, 10, 3):
    ...:         minibatch_indices = indices[minibatch_start: minibatch_start+3]
    ...:         print(minibatch_indices)
    ...:         
[0 1 2]
[3 4 5]
[6 7 8]
[9]

so the last minibatch will have data_size%minibatch_size amount of data
'''


def _minibatch(data, minibatch_idx):
    return data[minibatch_idx] if type(data) is np.ndarray else [data[i] for i in minibatch_idx]


def test_all_close(name, actual, expected):
    if actual.shape != expected.shape:
        raise ValueError("{:} failed, expected output to have shape {:} but has shape {:}"
                         .format(name, expected.shape, actual.shape))
    if np.amax(np.fabs(actual - expected)) > 1e-6:
        raise ValueError("{:} failed, expected {:} but value is {:}".format(name, expected, actual))
    else:
        print (name, "passed!")
