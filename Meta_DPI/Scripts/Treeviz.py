from dtreeviz.trees import *
import graphviz

def treeviz(treeparams,result_path,code,cols):
    (X, y, tree,depth) = treeparams
    viz = dtreeviz(tree, 
        X, 
        y,
        target_name='Interface',
        feature_names= cols, 
        class_names= ["non_interface", "interface"], 
        show_node_labels= True, 
        fancy=False 
        )  
    
    path = f"{result_path}/META_DPI_RESULTS{code}/tests/Rftree_{depth}.svg" 
    viz.save(path)
    
    