import bluetooth

bd_addr = "E8:6F:38:47:A0:EC"
port = 2

s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print("Connecting to {} on port {}".format(bd_addr,port))
s.connect((bd_addr, port))

sock.send("client_109611087 & server_<ID>")
sock.close()


