from socket import *
from utils.FileManager import FileManager
import json
import time

serverPort = 1057
buffer_size = 1024
host = 'localhost'
serverAddress = (host, serverPort)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddress)

print('The server is ready.')

# Dicionário para armazenar mensagens fragmentadas
messages = {}

while True:
    
    # Receive message and decode
    file, clientAddress = serverSocket.recvfrom(buffer_size)
    action, fileName, fileSize = file.decode().split(" ", 2)
    #colocar pra passar o action, fileName e o fileSize

    print(f'Command received from client: {action} {fileName}.')
    
    if action == 'close':
        break
    elif action == 'post':
        is_last = False
        while is_last == False:
            try:
                received_data = json.loads(file.decode())  # Decodifica JSON
                session_id = received_data["session_id"]  # ID da sessão do cliente
                packet_id = received_data["packet_id"]  # Número do fragmento
                content = received_data["content"]  # Conteúdo do fragmento
                is_last = received_data.get("end", False)  # Flag indicando último fragmento

                # Inicializa a sessão caso seja a primeira mensagem recebida
                if session_id not in messages:
                    messages[session_id] = []

                 # Armazena o fragmento recebido
                messages[session_id].append((packet_id, content))
                print(f"Recebido fragmento {packet_id} de {client_address}")

                # Se for o último pacote, reconstruir a mensagem
                if is_last:
                    # Ordena os fragmentos para garantir a sequência correta
                    messages[session_id].sort()

                    # Junta os fragmentos para reconstruir a mensagem original
                    full_message = "".join(fragment[1] for fragment in messages[session_id])
                    #acho q é isso que cria o arquivo no /files, to so testando
                    returned = FileManager.actFile(fileName, action, full_message)
                    print(f"\n--- Mensagem completa de {client_address} ---\n{full_message}\n")
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON de {client_address}: {data.decode('utf-8')}")
    elif action == 'get':
        break
    # Act on file
    print(f'Command accomplished, send response to: {clientAddress}.')
    
    # If there is a file to send back
    if returned is not None:
        returned = f'{fileName} {returned}'
        serverSocket.sendto(returned.encode(), clientAddress)
    
    else:
        serverSocket.sendto('None'.encode(), clientAddress)
    
    
serverSocket.close()