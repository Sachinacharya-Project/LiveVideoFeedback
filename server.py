import socket, cv2, pickle, struct

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
print("""Conectivity Informations
    Hostname {}
    IP Address {}
""".format(hostname, hostip))

port = 1111
socket_address = (hostip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("""Server Information
    Listenning as {}:{}
""".format(hostip, port))
while True:
    client_socket, addr = server_socket.accept()
    print("""New Client Connected
     at {}
    """.format(addr))
    if client_socket:
        video = cv2.VideoCapture(0)
        while video.isOpened():
            _, frame = video.read()
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)
            cv2.imshow("Server Video", frame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                client_socket.close()
                break