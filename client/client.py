from socket import *
from utils.FileManager import FileManager
import random

serverPort = 1057
clientPort = 1058
buffer_size = 1024
fragment_size = 200
host = 'localhost'

serverAddress = (host, serverPort)
clientAddress = (host, clientPort)

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(clientAddress)

print('The client is ready.')
session_id = 0

while True:
    action = input('Enter action (get/post/close): ').strip().lower()

    if action == 'close':
        clientSocket.sendto('close'.encode(), serverAddress)
        break

    fileName = input('Enter file name (with extension): ').strip()
    #sessões diferentes
    session_id = session_id + 1
    clientSocket.sendto(action.encode(), serverAddress)
    clientSocket.sendto(fileName.encode(), serverAddress)

    # Act depends on the action
    
    # Post file to server
    if action == 'post':
        #em tese esse content vai estar em bytes
        content = FileManager.actFile(fileName, 'get')
        
        #envia o tamanho do arquivo para o servidor
        fileSize = len(content)
        clientSocket.sendto(fileSize, serverAddress)

        #quantidade de fragmentos necessários e id da sessão
        fragments_amount = fileSize / fragment_size + 1
        session_id = session_id + 1

        fragment = [content[i:i+fragment_size] for i in range(0,len(content), fragment_size)]

        #separa os pacotes e marca o último pacote!
        for i in range(fragments_amount):
            flag = False
            if i == fragments_amount: 
                flag = True
            packet = {
                "session_id": session_id,
                "packet_id": i,
                "content": fragment[i],
                "end": flag
            }
        #                   ...                 #
        #               PAREI POR AQUI           #
        #                   ...                 #
        # Sends file to the server
#-------acho que nao precisa enviar action e filename ja q ja mandou antes---------$
#       action = f'{action}'
#       fileName = f'{fileName}'
        #content = f'{content}'
        #clientSocket.sendto(content.encode(), serverAddress)


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