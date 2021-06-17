import tkinter as tk 
from tkinter import filedialog, Text,Button
import os


def main():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
    
    frame = tk.Frame(root, bg= "white")
    text = tk.Text(root)
    button = tk.Button(root, text="hello")
    frame.pack()
    text.pack()
    button.pack()
    canvas.pack()
    print(text)
    # frame.place()
    root.mainloop()

main()