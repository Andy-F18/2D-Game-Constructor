import os
import pprint
import tkinter as tk
from PIL import Image
import time


class Game:
    def __init__(self, f):
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

        self.walls = {}
        try:
            for i in os.listdir(lib + "/walls"):
                self.walls[i.replace(".png", "")] = lib + "/walls/" + i
        except FileNotFoundError:
            print("lib not found or syntax error.")
            input()
            exit()

        self.items = {}
        try:
            for i in os.listdir(lib + "/items"):
                self.items[i.replace(".png", "")] = lib + "/items/" + i
        except FileNotFoundError:
            print("lib not found or syntax error.")
            input()
            exit()

        self.size = Image.open(self.walls['0']).width

        self.lvl = []
        for l in range(0, len(lvlf)):
            self.lvl.append(lvlf[l].split(" "))

        self.root = tk.Tk()
        p_r = int(self.root.winfo_screenwidth() / 2 - len(self.lvl[0]) * self.size / 2)
        p_d = int(self.root.winfo_screenheight() / 2 - len(self.lvl) * self.size / 2 - 50)
        self.root.geometry("{}x{}+{}+{}".format(len(self.lvl[0]) * self.size, len(self.lvl) * self.size, p_r, p_d))

        self.can = tk.Canvas(self.root, height=len(self.lvl) * self.size, width=len(self.lvl[0]) * self.size, bg="#555")
        self.can.pack()

        self.imgs = {}
        self.ids = {}
        self.__loadMap()
        self.inventory = {}

        self.imgs["player"] = tk.PhotoImage(file=lib + "/player.png")

        self.player = {"x": 1, "y": 1}
        self.player["id"] = self.can.create_image(self.player['x'] * self.size, self.player['y'] * self.size,
                                                  anchor=tk.NW,
                                                  image=self.imgs["player"])

        self.root.bind("<Left>", self.__playerMove)
        self.root.bind("<Right>", self.__playerMove)
        self.root.bind("<Up>", self.__playerMove)
        self.root.bind("<Down>", self.__playerMove)

        self.root.bind("<space>", self.__pickUp)

        self.root.mainloop()

    def __loadMap(self):
        for y in range(0, len(self.lvl)):
            for x in range(0, len(self.lvl[0])):
                self.imgs["y" + str(y) + "x" + str(x) + "f"] = tk.PhotoImage(file=self.walls['floor'])
                self.ids["y" + str(y) + "x" + str(x) + "f"] = \
                    self.can.create_image(x * self.size + 2, y * self.size + 2,
                                          anchor=tk.NW, image=self.imgs["y" + str(y) + "x" + str(x) + "f"])
                if self.lvl[y][x] != ".":
                    try:
                        self.imgs["y" + str(y) + "x" + str(x) + "b"] = tk.PhotoImage(file=self.walls[self.lvl[y][x]])
                        self.ids["y" + str(y) + "x" + str(x) + "b"] = \
                            self.can.create_image(x * self.size + 2, y * self.size + 2,
                                                  anchor=tk.NW, image=self.imgs["y" + str(y) + "x" + str(x) + "b"])
                    except KeyError:
                        try:
                            self.imgs["y" + str(y) + "x" + str(x) + "i"] = (
                                tk.PhotoImage(file=self.items[self.lvl[y][x]]))
                            self.ids["y" + str(y) + "x" + str(x) + "i"] = \
                                self.can.create_image(x * self.size + 2, y * self.size + 2,
                                                      anchor=tk.NW, image=self.imgs["y" + str(y) + "x" + str(x) + "i"])
                        except KeyError:
                            print("Item '" + self.lvl[y][x] + "' not recognized. Replaced by floor.")
                            self.lvl[y][x] = "."

    def __playerMove(self, event):
        if event.keysym == "Left":
            x = -1
            y = 0
        elif event.keysym == "Right":
            x = 1
            y = 0
        elif event.keysym == "Up":
            x = 0
            y = -1
        elif event.keysym == "Down":
            x = 0
            y = 1
        else:
            x = 0
            y = 0

        item = False
        if self.walls.get(self.lvl[self.player['y'] + y][self.player['x'] + x]) is None:
            if self.items.get(self.lvl[self.player['y'] + y][self.player['x'] + x]) is None:
                item = False
            else:
                item = True

        if item or self.lvl[self.player['y'] + y][self.player['x'] + x] == '.':
            self.player['x'] += x
            self.player['y'] += y
            for n in range(0, int(self.size*4)):
                self.can.move(self.player['id'], x/4, y/4)
                self.can.update()

    def __pickUp(self, event):
        x = self.player['x']
        y = self.player['y']
        if self.items.get(self.lvl[y][x]) is not None:
            for ny in range(0, self.size*4):
                self.can.update()
                for nx in range(0, self.size):
                    self.imgs["y" + str(y) + "x" + str(x) + "i"].transparency_set(nx, int(ny/4), True)
                    self.can.delete(self.ids["y" + str(y) + "x" + str(x) + "i"])

            if self.inventory.get(self.lvl[y][x]) is not None:
                self.inventory[self.lvl[y][x]] += 1
            else:
                self.inventory[self.lvl[y][x]] = 1


if __name__ == '__main__':
    Game("lvls/"+input("level file : "))
