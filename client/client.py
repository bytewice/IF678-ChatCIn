from socket import *
from utils.FileManager import FileManager
import json
import time

serverPort = 1057
clientPort = 1058
buffer_size = 1024
host = 'localhost'

serverAddress = (host, serverPort)
clientAddress = (host, clientPort)

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(clientAddress)

print('The client is ready.')

# Dicionário para armazenar mensagens fragmentadas
messages = {}

while True:
    action = input('Enter action (get/post/close): ').strip().lower()

    if action == 'close':
        clientSocket.sendto('close'.encode(), serverAddress)
        break
    
    fileName = input('Enter file name (with extension): ').strip()

    # Act depends on the action
    
    # Post file to server
    if action == 'post':
        content = FileManager.actFile(fileName, 'get')
        fragment_size = 200
        fragments = content[i:i+fragment_size] for i in range(0,len(content), fragment_size)

        session_id = "1234" #dps arrumar pra gerar aleatório cada seção

        for i, fragment in enumerate(fragments):
            packet = {
                "session_id": session_id.
                "packet_id": i,
                "content": fragment,
                "end": False 
            }
            client_socket.sendto(json.dumps(packet).encode("utf-8"), (SERVER_HOST, SERVER_PORT))
            print(f"Enviado fragmento {i}")

            time.sleep(0.1)  # Pequeno atraso para evitar congestionamento
        end_packet = {
            "session_id": session_id.
            "packet_id": len(fragments),
            "content": "",
            "end": True 
        }
        client_socket.sendto(json.dumps(end_packet).encode("utf-8"), (SERVER_HOST, SERVER_PORT))
        print("Todos os fragmentos foram enviados!")
        
        # Sends file to the server
        message = f'{action} {fileName} {fileSize}'
        clientSocket.sendto(message.encode(), serverAddress)

    # Get file from server
    elif action == 'get':
        message = f'{action} {fileName} None'
        clientSocket.sendto(message.encode(), serverAddress)

        data, serverAddress = clientSocket.recvfrom(buffer_size)
        response = data.decode()

        if response != 'None':
            fileName, content = response.split(" ", 1)
            
            FileManager.actFile(fileName, 'post', content)
            
            print(f'File "{fileName}" downloaded successfully.')

    else:
        print('Invalid action. Use "get", "post", or "close".')

clientSocket.close()