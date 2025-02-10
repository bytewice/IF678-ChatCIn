from socket import *
from utils.FileManager import FileManager

serverPort = 1057
buffer_size = 1024
host = 'localhost'
serverAddress = (host, serverPort)
fragment_size = 200

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

print('The server is ready.')

while True:
    
    # Receive message and decode
    file, clientAddress = serverSocket.recvfrom(buffer_size)
    #action, fileName, content = file.decode().split(" ", 2)
    
    #decode pq ele recebe a informação em bytes e tem q transformar em string pra ser usável
    action_cod = serverSocket.recvfrom(buffer_size)
    action = action_cod.decode()

    fileName_cod = serverSocket.recvfrom(buffer_size)
    fileName = fileName_cod.decode()


    print(f'Command received from client: {action} {fileName}.')
    
    if action == 'close':
        break 
    # Act on file
    #returned = FileManager.actFile(fileName, action, content)
    #print(f'Command accomplished, send response to: {clientAddress}.')
    elif action == 'post':
        #recebe o tamanho do arquivo que vai ser enviado
        fileSize = serverSocket.recvfrom(buffer_size)
        #                   ...                 #
        #               PAREI POR AQUI           #
        #                   ...                 #

    elif action == 'get':
        pass

    # If there is a file to send back
    if returned is not None:
        returned = f'{fileName} {returned}'
        serverSocket.sendto(returned.encode(), clientAddress)
    
    else:
        serverSocket.sendto('None'.encode(), clientAddress)
    
    
serverSocket.close()