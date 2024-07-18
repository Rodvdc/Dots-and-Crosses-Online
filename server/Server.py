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

final_res = ""
msg = ""
player_names = {}
nums = []
server_grid = [[0, 0, 0],
               [0, 0, 0],
               [0, 0, 0]]
count = 0

def var_setup():
    global clients, client_lock, server, nums, server_grid, count, player_names, final_res
    clients = set()
    client_lock = threading.Lock()

    server = ""
    final_res = ""

    msg = ""
    player_names = {}
    nums = ["1", "2"]
    server_grid = [[0, 0, 0],
                   [0, 0, 0],
                   [0, 0, 0]]
    count = 0

def handle_client(conn, addr, Num):
    global nums
    with client_lock:
        
        clients.add(conn)
        player_names[addr] = "Player " + Num
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
        if not(nums):
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

            if not(final_res):
                conn.close()
                clients.remove(conn)
                player_num = int(player_names[addr][-1])
                print(player_num)
                if player_num == 1:
                    send_win(1)
                else:
                    send_win(0)
                break
            
        else:
            if not(final_res):
                check(msg[0], msg[1], addr)

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

def check_win(pos_x, pos_y, sign):
    global server_grid
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    server_grid[pos_y][pos_x] = sign
    if not(final_res):
        for i in range(2):
            for r in range(3):
                if server_grid[r] == Wins[i]:
                    send_win(i)
                    break
                elif [str(server_grid[0][r]), str(server_grid[1][r]), str(server_grid[2][r])] == Wins[i]:
                    send_win(i)
                    break
            if [server_grid[0][0], server_grid[1][1], server_grid[2][2]] == Wins[i]:
                send_win(i)
                break
            if [server_grid[0][2], server_grid[1][1], server_grid[2][0]] == Wins[i]:
                send_win(i)
                break

        total_filled = 0
        for row in server_grid:
            for col in row:
                if col:
                    total_filled += 1
        if total_filled == 9:
            send_win("Both")

final_res = False
def send_win(winner):
    global final_res
    if not(final_res):
        if winner != "Both":
            winner += 1
            TEXT = "WI" + str(winner)
        else:
            TEXT = "Dra"
        for c in clients:
            c.send(TEXT.encode(FORMAT))
        print("WE HAVE WINNER", winner)
    final_res = True


def check(Posx, Posy, addr):
    name = player_names[addr]

    def Send():
        global count
        msg = str(Posx) + str(Posy)
        print("sending message:", msg)

        for c in clients:
            c.sendall((msg + Sign).encode(FORMAT))
        check_win(Posx, Posy, Sign)
        
        count += 1
    if count % 2 == 0 and name == "Player 1":
        Sign = "X"
        Send()
    elif count % 2 != 0 and name == "Player 2":
        Sign = "O"
        Send()
        

def start(SERVER, PORT):
    global server, nums
    var_setup()
    ADDR = (SERVER, PORT)
    print(f"[{SERVER}] Server started")
    server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    
    server.listen()
    while nums:
        conn, addr = server.accept()
        print(f"[Listening] Server is waiting for players to join")
        num = str(random.choice(nums))
        nums.remove(num)
        thread = threading.Thread(target = handle_client, args = (conn, addr, num))
        thread.start()
        print(f"Player {num} has joined")
    print("All players have joined")


#Start()
