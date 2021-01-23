import bluetooth

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
bd_addr = "E8:6F:38:47:A0:EC"
port = 2

try:
    server_sock.bind((bd_addr, port))
    server_sock.listen(5)
    print("Waiting for connection...")
    print("listening on {}, port {}".format(bd_addr, port))
    conn, addr = server_sock.accept()
    print("Accepted connection from: {}".format(addr))

    data = conn.recv(1024)
    print("received [{}]".format(data))

    conn.close()
    server_sock.close()
except KeyboardInterrupt:
    print("\nExiting...")
    exit()


