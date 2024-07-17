#MAIN
from tkinter import *
import threading
import socket
import time
import os

#import Server and Client
import client.Client as Client
import server.Server as Server
from server.Server import handle_client


FONT = ("Helvetica", 20)

INPROGRESS = "inprogress"
DONE = "done"

#TODO when pressing quit and hosting - should close the server
#TODO make sure you don't get stuck when joining a server that does not exist

class Main():
    def __init__(self):
        self.WIN = "WIN"
        self.LOSE = "LOSE"

        self.wins = 0
        self.root = Tk()
        self.reset()

        self.Client = Client.Client(self.root)

        self.start()

        self.root.mainloop()

    def get_result(self, result):
        result = self.Client.result
        print(result)
        if result == self.WIN:
            self.wins += 1

    def reset(self):
        #self.root = Tk()
        self.clear()
        self.root.resizable(width = False, height = False)
        self.root.title("Main Menu")
        self.PORT = ""
        self.SERVER = ""

    def clear(self):
        try:
            list = self.root.grid_slaves()
            for i in list:
                i.destroy()
        except:
            print("Exiting")
            os._exit(1)

    def start(self):
        self.clear()
        Label(self.root, bg = "red", text = "Xs and Os", font = FONT, width = 20, height = 2).grid(row = 0, column = 0)
        Button(self.root, bg = "white", text = "Host and Play",font = FONT, width = 20, command = self.server_setup).grid(row = 1, column = 0)
        Button(self.root, bg = "white", text = "Join game",font = FONT, width = 20, command = self.game_setup).grid(row = 2, column = 0)
        Label(self.root, bg = "white", text = "Wins: " + str(self.wins), font = FONT, width = 20).grid(row = 3, column = 0)

    def server_setup(self):
        self.clear()
        SERVER = socket.gethostbyname(socket.gethostname())
        def next():
            PORT = int(port_input.get())
            server_thread = threading.Thread(target = Server.Start, args = (SERVER, PORT))
            server_thread.start()
            time.sleep(0.1)
            self.start_game(SERVER, PORT)
            
        Button(self.root, text = "< Back", font = ("Helvatica", 13), anchor = W, bg = "white", width = 35, padx = 3, fg = "red",  command = self.start).grid(row = 0, column = 0)

        Label(self.root, bg = "white", width = 20, font = FONT, text = "Server IP: " + SERVER).grid(row = 1, column = 0)      
        port_label = Label(self.root, bg = "white", width = 20, font = FONT, text = "Enter Server Port:").grid(row = 2, column = 0)
        port_input = Entry(self.root, font = FONT, width = 21, justify = CENTER)
        port_input.grid(row = 3, column = 0)

        next_button = Button(self.root, bg = "white", text = "Next", font = FONT, width = 20, command = next).grid(row = 4, column = 0)

    def game_setup(self):
        self.clear() 
        def next():
            SERVER = server_input.get()
            PORT = int(port_input.get())
            self.start_game(SERVER, PORT)
        
        Button(self.root, text = "< Back", font = ("Helvatica", 13), anchor = W, bg = "white", width = 35, padx = 3, fg = "red",  command = self.start).grid(row = 0, column = 0)
            
        server_label = Label(self.root, bg = "white", width = 20, font = FONT, text = "Input IP of game:").grid(row = 1, column = 0)
        server_input = Entry(self.root, width = 21, font = FONT, justify = CENTER)
        server_input.grid(row = 2, column = 0)

        port_label = Label(self.root, bg = "white", width = 20, font = FONT, text = "Input port of game:").grid(row = 3, column = 0)
        port_input = Entry(self.root, width = 21, font = FONT, justify = CENTER)
        port_input.grid(row = 4, column = 0)

        next_button = Button(self.root, text = "Next", font = FONT, bg = "white", width = 20, command = next).grid(row = 5, column = 0)

    def start_game(self, SERVER, PORT):
        self.clear()
        self.Client.generate_game(SERVER, PORT)

        threading.Thread(target=self.wait_for_finish).start()
        
    def wait_for_finish(self):
        while (self.Client.progress == INPROGRESS):
            continue
        if (self.Client.result == "YOU WON"):
            self.wins += 1
        Server.server.close()
        self.reset()
        self.start()

if __name__ == "__main__":
    Main().start()
