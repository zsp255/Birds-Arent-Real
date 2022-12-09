import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 3737))

msg_rec = client.recv(1024)
msg_rec = msg_rec.decode()

if(msg_rec == 'go'):

    file = open('106GOPRO-GOPR6423.jpg', 'rb')
    image_data = file.read(2048)

    while image_data:
        client.send(image_data)
        image_data = file.read(2048)

    file.close()
    client.close()
