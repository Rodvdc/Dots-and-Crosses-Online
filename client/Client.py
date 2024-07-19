from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread

HEADER = 3
#PORT = 5050
FORMAT = "utf-8"
#SERVER = "192.168.1.46"


DISCONNECT = "DIS"
FONT = ("Helvetica", 20)
INPROGRESS = "inprogress"
DONE = "done"


class Client():
    def __init__(self, root):
        self.start = ""
        self.root = root
        self.progress = ""
        self.result = ""
        

    def disconnect(self):
        self.start = ""
        try:
            self.client.send(DISCONNECT.encode(FORMAT))
            self.client.close()
        except:
            pass
        self.progress = DONE
        #self.root.destroy()
        #TODO: send result to main
        #TODO later set to main menu

    def receive_pos(self, turn):
        self.start = self.client.recv(1).decode(FORMAT)

        turn.configure(text = "Waiting for opponent to choose")
        turn.grid(row = 0, column = 0, columnspan = 3)
        player = "Player 1"
        while self.start:
            if player == self.user_player:
                TEXT = "Your turn"
                COLOUR = "black"
            elif len(player) == 1:
                if player == self.user_player[-1]:
                    TEXT = "YOU WON"
                else:
                    TEXT = "YOU LOST"
                self.result = TEXT
            elif player == "Draw":
                TEXT = "YOU DRAW"
                self.result = TEXT
            else:
                TEXT = "Waiting for opponent to choose"
                COLOUR = "grey"

        
            turn.configure(text = TEXT)

            msg = self.client.recv(HEADER).decode(FORMAT)

            if msg[2] == "O" or msg[2] == "X":
                Button(self.root, text = str(msg[2]), bg = "white", font = FONT, width = 10, height = 4,
                    state = "disabled", disabledforeground = COLOUR).grid(row = int(msg[1]) + 1, column = msg[0])
            if msg[2] == "X":
                player = "Player 2"
            elif msg[2] == "O":
                player = "Player 1"
            elif msg[0] + msg[1] == "WI":
                player = msg[2]
            elif msg == "Dra":
                player = "Draw"
            elif msg == DISCONNECT:
                break

        
    def send_pos(self, pos_x, pos_y):
        if self.start:
            Message = str(pos_x) + str(pos_y)
            print(Message)
            Message = Message.encode(FORMAT)
            self.client.send(Message)

    def generate_game(self, SERVER, PORT):    
        #Create connection with server
        try:
            self.progress = INPROGRESS
            ADDR = (SERVER, PORT)
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(ADDR)
        
            #Configure the window
            self.root.title("Dots and Crosses")
            turn = Label(self.root, text = "Waiting for opponent...", font = FONT, bg = "white")
            turn.grid(row = 0, column = 0, columnspan = 3)
            for Row in range(3):
                for Col in range(3):
                    action = lambda x = Col, y = Row: self.send_pos(x, y)
                    Button(self.root, bg = "white", font = FONT, width = 10, height = 4, command = action).grid(row = Row + 1, column = Col)
            Button(self.root, text = "Quit", bg = "white", font = FONT, fg = "red", command = self.disconnect).grid(row = 4, column = 0, columnspan = 3)

            self.user_player = self.client.recv(HEADER).decode(FORMAT)
            self.user_player = "Player " + self.user_player[2]

            receive_thread = Thread(target = lambda: self.receive_pos(turn))
            receive_thread.start() 

        except Exception as e:
            tryAgain = False
            if isinstance(e, ConnectionRefusedError):
                print("Connection refused")
                tryAgain = messagebox.askretrycancel("Connection Refused", "Game not available")
            
            if (not tryAgain):
                print("Disconnecting...")
                self.disconnect()
            else:
                self.generate_game(SERVER, PORT)
        