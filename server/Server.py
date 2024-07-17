#SERVER
import socket
import threading
import random
import time


HEADER = 2
FORMAT = "utf-8"
DISCONNECT = "DI"

clients = set()
client_lock = threading.Lock()

server = ""

Final_Res = ""
msg = ""
Player_Names = {}
Nums = []
Server_Grid = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
Count = 0

def Var_Setup():
    global clients, client_lock, server, Nums, Server_Grid, Count, Player_Names, Final_Res
    clients = set()
    client_lock = threading.Lock()

    server = ""
    Final_Res = ""

    msg = ""
    Player_Names = {}
    Nums = ["1", "2"]
    Server_Grid = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
    Count = 0

def handle_client(conn, addr, Num):
    global Nums
    with client_lock:
        
        clients.add(conn)
        Player_Names[addr] = "Player " + Num
    conn.send(("Pl" + Num).encode(FORMAT)) 
    
    connected = False
    BREAK = False
    
    #TODO: what is this function
    def TimeOut():
        global BREAK
        time.sleep(10)
        return True

    threading.Thread(target = TimeOut).start()
    
    while not(connected) and not(BREAK):
        if not(Nums):
            conn.send(("S").encode(FORMAT))
            #for c in clients:
            #    c.sendall(("S").encode(FORMAT)) 
            connected = True
        else:
            connected = False

    while connected:
        try:
            msg = conn.recv(HEADER).decode(FORMAT)
        except:
            break
        print("Position recieved", msg)
        if msg == DISCONNECT:
            connected = False

            if not(Final_Res):
                conn.close()
                clients.remove(conn)
                Player_Num = int(Player_Names[addr][-1])
                print(Player_Num)
                if Player_Num == 1:
                    Send_Win(1)
                else:
                    Send_Win(0)
                break
            
        else:
            if not(Final_Res):
                Check(msg[0], msg[1], addr)

    try:
        for c in clients:
            c.send("DIS".encode(FORMAT))
            c.close()
    except:
        pass
    
    global server
    server.close()
    print("Server closed!")
    #TODO Check why server closed don't print
Wins = [["X", "X", "X"], ["O", "O", "O"]]

def Check_Win(Posx, Posy, Sign):
    global Server_Grid
    Posx = int(Posx)
    Posy = int(Posy)
    Server_Grid[Posy][Posx] = Sign
    SG = Server_Grid
    if not(Final_Res):
        for i in range(2):
            for r in range(3):
                if SG[r] == Wins[i]:
                    Send_Win(i)
                    break
                elif [str(SG[0][r]), str(SG[1][r]), str(SG[2][r])] == Wins[i]:
                    Send_Win(i)
                    break
            if [SG[0][0], SG[1][1], SG[2][2]] == Wins[i]:
                Send_Win(i)
                break
            if [SG[0][2], SG[1][1], SG[2][0]] == Wins[i]:
                Send_Win(i)
                break

        Total_Filled = 0
        for row in SG:
            for col in row:
                if col:
                    Total_Filled += 1
        if Total_Filled == 9:
            Send_Win("Both")

Final_Res = False
def Send_Win(Winner):
    global Final_Res
    if not(Final_Res):
        if Winner != "Both":
            Winner += 1
            TEXT = "WI" + str(Winner)
        else:
            TEXT = "Dra"
        for c in clients:
            c.send(TEXT.encode(FORMAT))
        print("WE HAVE WINNER", Winner)
    Final_Res = True


def Check(Posx, Posy, addr):
    Name = Player_Names[addr]

    def Send():
        global Count
        msg = str(Posx) + str(Posy)
        print("sending message:", msg)

        for c in clients:
            c.sendall((msg + Sign).encode(FORMAT))
        Check_Win(Posx, Posy, Sign)
        
        Count += 1
    if Count % 2 == 0 and Name == "Player 1":
        Sign = "X"
        Send()
    elif Count % 2 != 0 and Name == "Player 2":
        Sign = "O"
        Send()
        

def Start(SERVER, PORT):
    global server, Nums
    Var_Setup()
    ADDR = (SERVER, PORT)
    print(f"[{SERVER}] Server started")
    server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    
    server.listen()
    while Nums:
        conn, addr = server.accept()
        print(f"[Listening] Server is waiting for players to join")
        Num = str(random.choice(Nums))
        Nums.remove(Num)
        thread = threading.Thread(target = handle_client, args = (conn, addr, Num))
        thread.start()
        print(f"Player {Num} has joined")
    print("All players have joined")


#Start()
