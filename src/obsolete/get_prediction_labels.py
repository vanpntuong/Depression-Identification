import os

import numpy as np
from sklearn.externals import joblib

import src.main.config
import src.obsolete.utils
from src.obsolete import read_labels


def final_classifier(mode,category="PN",problem_type="C",normalize="normalize"):
    if category == "PN":
        cat_1 = "positive"
        cat_2 = "negative"
    if mode == "late_fusion":
        X_test = [    [   map(np.asarray, read_labels.features("acoustic", cat_1, "test", problem_type, normalize)),
                      map(np.asarray, read_labels.features("acoustic", cat_2, "test", problem_type, normalize))
                  ],
                  [   map(np.asarray, read_labels.features("visual", cat_1, "test", problem_type, normalize)),
                      map(np.asarray, read_labels.features("visual", cat_2, "test", problem_type, normalize))
                  ],
                  [   map(np.asarray, read_labels.features("linguistic", cat_1, "test", problem_type, normalize)),
                      map(np.asarray, read_labels.features("linguistic", cat_2, "test", problem_type, normalize))
                  ]
              ]
    else:

        X_test = [map(np.asarray, read_labels.features(mode, cat_1, "test", problem_type, normalize)),
                  map(np.asarray, read_labels.features(mode, cat_2, "test", problem_type, normalize))]

    clf = joblib.load(os.path.join(src.main.config.GRID_SEARCH_CLF_DIR, mode + '_pickle' + category + '.pkl'))
    preds_label = clf.predict(X_test)
    return preds_label

def main():
    print "acoustic"
    print final_classifier("acoustic")
    print "visual"
    print final_classifier("visual")
    print "linguistic"
    print final_classifier("linguistic")
    print "late_fusion"
    print final_classifier("late_fusion")



main()

