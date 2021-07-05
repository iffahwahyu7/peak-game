import random
import socket
import sys
import threading


def read_msg(clients, friends, sock_cli, addr_cli, src_username):
    #Menerima pesan
    while True:
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        #parsing pesannya
        dest, msg = data.split(b"|", 1)
        dest = dest.decode("utf-8")

        #Mengulingkan dadu
        if dest == "roll":
            # print("{} ".format(src_username))
            # num = move(clients[src_username][0], clients[src_username][3])
            # clients[src_username][3] = num step[src_username]
            num = move(src_username, addr_cli, clients[src_username][0], step[src_username])
            step[src_username] = num
            for x in clients:
                print(x, ":", step[x])
                curr = str(x) + " : " + str(step[x])
                # print(curr)
                current_step(clients, curr, addr_cli)

    #Mengirim pesan ke client
        #Mengirim pesan ke semua client
        elif dest == "bcast":
            msg = msg.decode("utf-8")
            msg2 = "<{}>: {}".format(src_username, msg)
            send_broadcast(clients, msg2, addr_cli)

        #Menambah teman
        elif dest == "addfriend":
            dest_username = msg.decode("utf-8")
            friends[src_username].append(dest_username)
            friends[dest_username].append(src_username)
            send_msg(clients[dest_username][0], f"{src_username} is now friend")
            send_msg(clients[src_username][0], f"{dest_username} is now friend")

        #Mengirim pesan ke semua teman
        elif dest == "friends":
            msg = msg.decode("utf-8")
            msg2 = "<{}>: {}".format(src_username, msg)
            send_friends(clients, friends, src_username, msg2, addr_cli)
            
        #Mengirim file
        elif dest == "sendfile":
            dest_username, filename, size, filedata = msg.split(b'|', 3)
            dest_username = dest_username.decode("utf-8")
            filename = filename.decode("utf-8")
            size = int(size.decode("utf-8"))

            while len(filedata) < size:
                if size-len(filedata) > 65536:
                    filedata += sock_cli.recv(65536)
                else:
                    filedata += sock_cli.recv(size - len(filedata))
                    break
            dest_sock_cli = clients[dest_username][0]
            if dest_sock_cli is not None:
                send_file(dest_sock_cli, filename, size, filedata, src_username)
        
        #Mengirim pesan privat
        else:
            msg = msg.decode("utf-8")
            msg2 = "<{}>: {}".format(src_username, msg)
            dest_sock_cli = clients[dest][0]
            send_msg(dest_sock_cli, msg2)

    #Disconnect client dan dihapus dari daftar client
    sock_cli.close()
    print("connection closed", addr_cli)
    del clients["{}:{}".format(addr_cli[0], addr_cli[1])]

def move(src_username, addr_cli, sock_cli, step):
    chasm_squares = {16: 4, 22:10, 33: 20, 48: 24, 62: 56, 78: 69, 74: 60, 91: 42, 97: 6}
    rope_squares = {3: 12, 7: 23, 11:25, 21: 56, 47: 53, 60: 72, 80: 96}
    throw = random.randint(1, 6)
    # throw = 3
    step = step + throw
    if step>100:
        step = step - throw
        data_bcast = src_username + " rolled a " + str(throw) + " and cannot move. Still on " + str(step)
        data = "You rolled a " + str(throw) + " YOU CAN'T MOVE, YOU NEED A {} TO WIN.".format(100 - step) + ". Still on " + str(step)
    #     print("Rolled a", Throw, "BAD LUCK, YOU CANT MOVE, YOU NEED A {} TO WIN".format(100 - step))
    #     return value
    elif step == 100:
        data_bcast = src_username + " REACHED THE PEAK! CONGRATULATION " + src_username + "!!!"
        data = "YOU REACHED THE PEAK! CONGRATULATION!!!"
    #     return num

    else: 
        if step in chasm_squares:
            #if landed in a chasm square
            data_bcast = src_username + " rolled a " + str(throw) + ". Fell in a chasm and is now on square " + str(chasm_squares[step])
            data = "You fell in a chasm and is now on square " + str(chasm_squares[step])
            step = chasm_squares[step]
        elif step in rope_squares:
            #if landed in a rope square
            data_bcast = src_username + " rolled a " + str(throw) + ". Climbed a rope and is now on square " + str(rope_squares[step])
            data = "You climbed a rope and is now on square " + str(rope_squares[step])
            step = rope_squares[step]
        else:
            data_bcast = src_username + " rolled a " + str(throw) + " and is now on " + str(step)
            data = "You rolled a " + str(throw) + " And is now on " + str(step)
            # print(data)
    send_broadcast(clients, data_bcast, addr_cli)
    send_msg(sock_cli, data)
 
    return step

#current_step setiap player
def current_step(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        send_msg(sock_cli, data)

#send_broadcast(ke semua client)
def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, _ in clients.values():
        if not (addr_cli[0] == sender_addr_cli[0] and addr_cli[1] == sender_addr_cli[1]):
            send_msg(sock_cli, data)

#send_msg(pesan ke client tertentu)
def send_msg(sock_cli, data):
    message = f'message|{data}'
    sock_cli.send(bytes(message, "utf-8"))

#send_friends(ke semua teman)
def send_friends(clients, friends, src_username, data, sender_addr_cli):
    cur_friends = friends[src_username]
    for cur_friend in cur_friends:
        if cur_friend not in clients:
            continue
        sock_cli, addr_cli, _ = clients[cur_friend]
        if not (sender_addr_cli[0] == addr_cli[0] and sender_addr_cli[1] == addr_cli[1]):
            send_msg(sock_cli, data)

#send_file(kirim file)
def send_file(sock_cli, filename, size, filedata, username):
    file = f'file|{username}|{filename}|{size}|'.encode('utf-8')
    file += filedata
    sock_cli.sendall(file)


#Object socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Bind server ke IP dan port tertentu
server_socket.bind(('0.0.0.0', 6666))

#Server listen
server_socket.listen(5)

#Dictionary untuk client dan friend
clients = {}
friends = {}
step = {}

try:
    while True:
        sock_cli, addr_cli = server_socket.accept()

        #Menerima username dari client
        src_username = sock_cli.recv(65535).decode("utf-8")
        print(" {} successfully joined".format(src_username))

        #Buat Thread
        thread_cli = threading.Thread(target=read_msg, args=(clients, friends, sock_cli, addr_cli, src_username))
        thread_cli.start()

        #Menambah client baru ke dictionary
        clients[src_username] = (sock_cli, addr_cli, thread_cli)
        # tes = len(clients)
        # print(tes)
        step[src_username] = 0
        # for x in clients:
        #     print(x, ":", step[x])
            # curr = x, ":", step[x]
            # print(curr)
            # current_step(clients,  curr)
        # print(" {} successfully joined".format(step[src_username]))
        friends[src_username] = []

except KeyboardInterrupt:
    #Menutup object server
    server_socket.close()
    sys.exit(0)
