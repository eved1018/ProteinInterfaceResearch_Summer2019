import pandas as pd
import numpy as np
import graphviz
import pydot 
from sklearn.tree import export_graphviz


# tree viz
def TreeViz(model,feature_cols,trees):
    for i in range(0,trees):
        tree = model.estimators_[i]
        outfilename= "/Users/evanedelstein/Desktop/Rftree{}.dot".format(i)
        export_graphviz(tree, out_file = outfilename, feature_names = feature_cols, rounded = True, precision = 1)
        (graph, ) = pydot.graph_from_dot_file(outfilename)
        graph.write_png('/Users/evanedelstein/Desktop/RFtree{}.png'.format(i))
    