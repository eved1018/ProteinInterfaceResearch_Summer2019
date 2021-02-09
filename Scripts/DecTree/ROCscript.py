import pandas as pd
import matplotlib as plt
import tkinter
import PySimpleGUI as sg

sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()

# def ROC_Plt(Master, code,results_path):
    # predictors = []
    # for key in Master:
    #     predictors.append(key)
    # color_index = 0    
    # colors = ["#0000FF","#ff8333","#008000","#FFFF00","#800080","#00FF00","#808000","#00FFFF","#FF0000","#008080","#000080","#FF00FF"]
    # plt.title('Receiver Operating Characteristic')
    # plt.title('Receiver Operating Characteristic')
    # for key in predictors:
    #     AUC = Master[key]["AUC"][0]
    #     AUC = AUC.round(3)
    #     TPRS = Master[key]['TPRS'][0]
    #     FPRS = Master[key]['FPRS'][0]
    #     plt.plot(FPRS, TPRS, c=colors[color_index], label = '{}: AUC = {}'.format(Master[key]["name"],AUC))
    #     color_index += 1
    # plt.style.use("fivethirtyeight")
    # plt.legend(loc = 'lower right')
    # plt.plot([0, 1], [0, 1],'r--')
    # plt.xlim([0, 1])
    # plt.ylim([0, 1])
    # plt.ylabel('True Positive Rate')
    # plt.xlabel('False Positive Rate')
    # plt.savefig( "{}/Crossvaltest{}/ROC.png" .format(results_path,code))
    # plt.clf()