import pickle, cv2, socket, struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostip = input("Enter IP Adress\n")
port = input("Enter Port (1111)\n")
if port == '':
    port = 1111
client_socket.connect((hostip, port))
data = b""
payloadsize = struct.calcsize("Q")
while True:
    while len(data) < payloadsize:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
        packed_msg_size = data[:payloadsize]
        data = data[payloadsize:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        cv2.imshow("Client Video", frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
        client_socket.close()