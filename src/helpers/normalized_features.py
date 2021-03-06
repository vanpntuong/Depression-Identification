import pandas as pd
import os
from sklearn import preprocessing
from ..main import config
import numpy as np
import sys

def get_normalized_features(filename):
    filename_train = filename
    data_train = pd.read_csv(filename_train)
    filename_val = filename.replace("train","val")
    filename_test = filename.replace("train", "test")
    data_val = pd.read_csv(filename_val)
    data_test = pd.read_csv(filename_test)
    columns = data_train.columns[1:]
    column = columns[:-2]
    #print column
    #print filename_train
    X_train = data_train.as_matrix(columns=column)
    X_val = data_val.as_matrix(columns = column)
    X_test = data_test.as_matrix(columns = column)

    scalar = preprocessing.StandardScaler().fit(X_train)

    transformed_train = scalar.transform(X_train)
    transformed_val = scalar.transform(X_val)
    #print X_test
    #print np.isfinite(X_test).all()
    # for i in X_test:
    #     for j in i:
    #         if j == True:
    #             print i,j
    X_test[np.isnan(X_test)] = 0
    transformed_test = scalar.transform(X_test)


    data_normalized_train = pd.DataFrame(transformed_train,columns=column)
    data_normalized_val = pd.DataFrame(transformed_val, columns=column)
    data_normalized_test = pd.DataFrame(transformed_test, columns=column)

    data_normalized_train[['video','label','score']] = data_train[['video','label','score']]
    data_normalized_val[['video','label','score']] = data_val[['video','label','score']]
    data_normalized_test[['video','label','score']] = data_test[['video','label','score']]


    write_path_file_train = filename_train.replace("regular","normalize")
    write_path_file_val = filename_val.replace("regular","normalize")
    write_path_file_test = filename_test.replace("regular", "normalize")


    #print write_path_file_train
    #print filename_val
    #print write_path_file_val
    #print filename_test
    #print write_path_file_test

    data_normalized_train.to_csv(write_path_file_train,index=None)
    data_normalized_val.to_csv(write_path_file_val,index=None)
    data_normalized_test.to_csv(write_path_file_test,index=None)

def normalize_features(select = "select"):
    if select == "select":
        path_classify = config.SEL_FEAT_TRAIN_REGULAR_CLASSIFY
        path_estimate = config.SEL_FEAT_TRAIN_REGULAR_ESTIMATE
    else:
        path_classify = config.ALL_FEAT_TRAIN_REGULAR_CLASSIFY
        path_estimate = config.ALL_FEAT_TRAIN_REGULAR_ESTIMATE
    list_train_classify = [os.path.join(path_classify, fn) for fn in next(os.walk(config.SEL_FEAT_TRAIN_REGULAR_CLASSIFY))[2]]
    print list_train_classify
    for i in range(len(list_train_classify)):
        get_normalized_features(list_train_classify[i])

    list_train_estimate = [os.path.join(path_estimate, fn) for fn in next(os.walk(config.SEL_FEAT_TRAIN_REGULAR_ESTIMATE))[2]]
    print list_train_estimate
    for i in range(len(list_train_estimate)):
        get_normalized_features(list_train_estimate[i])


#normalize_features()

if __name__ == '__main__':
    select = "select"
    if len(sys.argv) == 2:
        select = sys.argv[1]
    print select
    normalize_features(select)