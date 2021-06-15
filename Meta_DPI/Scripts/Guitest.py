import PySimpleGUI as sg
import sys
import Meta_DPI
import subprocess

def main():
    loop = True
    while loop == True:
        window = Main_window()
        if window is None:
            window = Main_window()
        event, values = window.read()
        print("event",event)
        print("values",values)
        if event == "Submit":
            args = (values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[0])
            Meta_DPI.Main(*args)
        if event == "test":
            args = (int(values[1]),int(values[2]),int(values[3]),values[4],values[5],values[6],values[7],"test")
            runCommand(args)
            break
            print(finish)
            
            event, values = create_output_window(finish).read(close=True)
        if event == sg.WIN_CLOSED or event=="Exit" or event=="Cancel":
            break
    window.close()

def Main_window():
    layout = [[sg.Text('Document to open')],
            [sg.In(), sg.FileBrowse()],
            [sg.Text('Please enter random forest parameters')],
            [sg.Text('trees', size =(15, 1)), sg.InputText()],
            [sg.Text('depth', size =(15, 1)), sg.InputText()],
            [sg.Text('ccp', size =(15, 1)), sg.InputText()],
            [sg.Text('Output options:')],
            [sg.Checkbox('printout', default=False)],
            [sg.Checkbox('param test', default=False)],
            [sg.Checkbox('tree viz', default=True)],
            [sg.Checkbox('protein viz', default=True)],
            [sg.Button('test')],
            [sg.Submit(), sg.Cancel()]]
    window = sg.Window("Meta_DPI",layout,size = (1920, 1080))
    return window 

def create_output_window(param):
    layout = [[sg.Text(f'{param}')]]
    window = sg.Window('output', layout, keep_on_top=True, finalize=True,size = (1920, 1080) )
    return window

    

def runCommand(args, timeout=None, window=None):
    # finish = Meta_DPI.Main(*args)
    print("hello")
    # return finish

main()