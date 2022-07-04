import os
import tkinter as tk
from PIL import Image

if __name__ == '__main__':
    f = "lvls/"+input("Lvl file : ")
    lvl_file = ""
    try:
        lvl_file = open(f, 'r')
    except FileNotFoundError:
        print("File not found.")
        input()
        exit()

    lvlf = lvl_file.read().split("\n")

    lib = lvlf[0].replace("lib=", "")

    lvlf.remove(lvlf[0])

    walls = {}
    try:
        for i in os.listdir(lib):
            walls[i.replace(".png", "")] = lib+"/"+i
    except FileNotFoundError:
        print("lib not found or syntax error.")
        input()
        exit()

    size = Image.open(walls['0']).width

    lvl = []
    for l in range(0, len(lvlf)):
        lvl.append(lvlf[l].split(" "))

    root = tk.Tk()
    p_r = int(root.winfo_screenwidth() / 2 - len(lvl[0]) * size / 2)
    p_d = int(root.winfo_screenheight() / 2 - len(lvl) * size / 2 - 50)
    root.geometry("{}x{}+{}+{}".format(len(lvl[0]) * size, len(lvl) * size, p_r, p_d))

    can = tk.Canvas(root, height=len(lvl) * size, width=len(lvl[0]) * size, bg="#555")
    can.pack()

    imgs = {}
    for y in range(0, len(lvl)):
        for x in range(0, len(lvl[0])):
            if lvl[y][x] != ".":
                try:
                    imgs[str(y)+str(x)] = (tk.PhotoImage(file=walls[lvl[y][x]]))
                except KeyError:
                    print("Bloc '"+lvl[y][x]+"' not recognized. Replaced by floor.")
                    imgs[str(y) + str(x)] = tk.PhotoImage(file=walls['floor'])
                    can.create_image(x * size + 2, y * size + 2, anchor=tk.NW, image=imgs[str(y) + str(x)])

                can.create_image(x*size+2, y*size+2, anchor=tk.NW, image=imgs[str(y)+str(x)])
            else:
                imgs[str(y)+str(x)] = tk.PhotoImage(file=walls['floor'])
                can.create_image(x*size+2, y*size+2, anchor=tk.NW, image=imgs[str(y)+str(x)])

    root.mainloop()