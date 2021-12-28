from io import BytesIO
from tkinter import *
from tkinter import filedialog
import chess
import chess.svg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import tempfile
from PIL import ImageTk, Image

def solve(input):
    # solve here

    return ["7 6 5 4 3 2 1 0"]

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

        speed_slider = Scale(self.window, from_=200, to=1000, tickinterval=100, orient=HORIZONTAL)
        speed_slider.set(1000)
        speed_slider.pack()

    def onExit(self):
        quit()
    
    def onLoad(self):
        filename = filedialog.askopenfilename()
        f = open(filename, "r")
        line = f.readline()

        self.display(encode(line.split(" ")))   

        res = solve(line)
        for x in res:
            self.display(encode(x.split(" ")))

    def display(self, board_encoded):
        board = chess.Board(board_encoded)
        svg = chess.svg.board(board=board, size=500)

        svg_tempfile = tempfile.NamedTemporaryFile(delete=False)
        svg_tempfile.write(svg.encode('utf-8'))
        svg_tempfile.close()
        
        drawing = svg2rlg(svg_tempfile.name)
        print(svg_tempfile.name)
        svg_buffer = BytesIO()
        renderPM.drawToFile(drawing, svg_buffer, fmt='PNG')
        img = Image.open(svg_buffer)

        self.frame.render = ImageTk.PhotoImage(img)
        self.frame.create_image(0,0,anchor='nw',image=self.frame.render)

window = Tk(className = "Chessboard")
app = App(window)
window.mainloop()