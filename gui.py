from io import BytesIO
from tkinter import *
from tkinter import filedialog
import chess
import chess.svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import tempfile
from PIL import ImageTk, Image
import time
from solver import AStarSolver, heuristic, action
import os

def solve(input):
    # solve here
    intiState = [6, -1, -1, -1, -1, -1, -1, -1]
    return AStarSolver(
        state=intiState, 
        heuristic=heuristic, 
        action=action
    ).solve().getResult(isPrint=False)
    # return ["7 6 5 4 3 2 1 0"]

def encode(pos):
    board = [[0,0,0,0,0,0,0,0] for i in range(0, 8)]
    for i in range(0,8):
        if not pos[i] == "-1":
            board[int(pos[i])][i] = 1
    
    board_encoded = ""

    for i in range(0,8):
        cnt = 0
        if not i == 0:
            board_encoded = board_encoded + "/"
        for j in range(0,8):
            if board[i][j] == 0:
                cnt = cnt + 1
            else:
                if not cnt == 0:
                    board_encoded = board_encoded + str(cnt)
                board_encoded = board_encoded + 'q' 
                cnt = 0
        
        if not cnt == 0:
            board_encoded = board_encoded + str(cnt)
    return board_encoded

class App:
    def __init__(self, window):
        self.window = window
        self.window.geometry("500x500")
        self.frame = Canvas(self.window, width=500, height=500)
        self.frame.pack(expand=YES,fill=BOTH)

        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        fileMenu = Menu(menubar)

        fileMenu.add_command(label="Load", command=self.onLoad)
        fileMenu.add_command(label="Exit", command=self.onExit)

        menubar.add_cascade(label="File", menu=fileMenu)

        self.speed_slider = Scale(self.frame, from_=0, to=1000, orient=HORIZONTAL, showvalue=False)
        self.speed_slider.set(1000)
        self.speed_slider.pack(anchor=CENTER, side=BOTTOM)

        self.label = Label(self.frame, text="0/0")
        self.label.pack(side=BOTTOM, anchor=CENTER)

    def onExit(self):
        quit()
    
    def onLoad(self):
        filename = filedialog.askopenfilename(initialdir=os.getcwd())
        f = open(filename, "r")
        line = f.readline()

        self.display(encode(line.split(" ")))   

        res = solve(line)
        self.total = len(res)
        self.current = 0
        self.show_result(res)
        # for x in res:
        #     time.sleep(self.speed_slider.get()/1000)
        #     # self.display(encode(x.split(" ")))

    def show_result(self, res):
        if len(res) == 0:
            return
        
        self.current = self.current + 1
        self.label["text"] = str(self.current) + "/" +str(self.total)
        # print(res[0])
        self.window.after(self.speed_slider.get(), self.display,encode(res[0]))
        self.window.after(self.speed_slider.get(), self.show_result, res[1:])

    def display(self, board_encoded):
        board = chess.Board(board_encoded)
        svg = chess.svg.board(board=board, size=500)

        # svg_tempfile = tempfile.NamedTemporaryFile(delete=False)
        svg_tempfile = open('temp', 'w')
        svg_tempfile.write(svg)
        svg_tempfile.close()
        
        drawing = svg2rlg(svg_tempfile.name)
        # print(svg_tempfile.name)
        svg_buffer = BytesIO()
        renderPM.drawToFile(drawing, svg_buffer, fmt='PNG')
        img = Image.open(svg_buffer)

        self.frame.render = ImageTk.PhotoImage(img)
        self.frame.create_image(0,0,anchor='nw',image=self.frame.render)

window = Tk(className = "Chessboard")
app = App(window)
window.mainloop()