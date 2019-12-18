import numpy as np
import pandas as pd


def convert(data, to):
    converted = None
    if to == 'array':
        if isinstance(data, np.ndarray):
            converted = data
        elif isinstance(data, pd.Series):
            converted = data.values
        elif isinstance(data, list):
            converted = np.array(data)
        elif isinstance(data, pd.DataFrame):
            converted = data.as_matrix()
    elif to == 'list':
        if isinstance(data, list):
            converted = data
        elif isinstance(data, pd.Series):
            converted = data.values.tolist()
        elif isinstance(data, np.ndarray):
            converted = data.tolist()
    elif to == 'dataframe':
        if isinstance(data, pd.DataFrame):
            converted = data
        elif isinstance(data, np.ndarray):
            converted = pd.DataFrame(data)
    else:
        raise ValueError("Unknown data conversion: {}".format(to))
    if converted is None:
        raise TypeError('cannot handle data conversion of type: {} to {}'.format(type(data),to))
    else:
        return converted


def remove_incomplete_samples(x, y=None):
    #print 'before removing'
    #print x
    #print y
    if y is not None:
        #x = [v if v is not None else np.nan for v in x]
        #y = [v if v is not None else np.nan for v in y]
        arr = np.array([x, y], dtype=object).transpose()
        #print "remiving incomplete"
        #print arr
        #for e in arr:
        #    print(e, pd.isnull(e))
        arr = arr[~pd.isnull(arr).any(axis=1)].transpose()

        #if isinstance(x, list):
        #    return arr[0].tolist(), arr[1].tolist()
        #else:
        return arr[0], arr[1]
    else:
        return x[~pd.isnull(x)]



'''
turns values with occurrence below a threshold to nan
'''
def remove_small_bins(x, y, min_bin_size):

    values, count = np.unique(x, return_counts=True)
    xval_drop = []
    for i,c in enumerate(count):
        if c < min_bin_size:
            x[x==values[i]]=np.nan

    values, count = np.unique(y, return_counts=True)
    yval_drop = []
    for i,c in enumerate(count):
        if c < min_bin_size:
            y[y==values[i]]=np.nan

    return x, y


def replace_nan_with_value(x, y, value):
    x = [v if v == v and v is not None else value for v in x]  # NaN != NaN
    y = [v if v == v and v is not None else value for v in y]
    return x, y
