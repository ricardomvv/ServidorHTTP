#by ricardomvv 
# importacao das bibliotecas
import socket
import re

# definicao do host e da porta do servidor
HOST = '127.0.0.1' # ip do servidor (em branco)
PORT = 8080 # porta do servidor

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)

client_connection, client_address = listen_socket.accept()

while True:
    # aguarda por novas conexoes
    
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    # imprime na tela o que o cliente enviou ao servidor
    mensagem = request.rstrip()
    
    print(mensagem)
    if re.search('\\bGET /index.html HTTP/1.1\\b', str(mensagem), re.IGNORECASE):
        requisicao = True
    elif re.search('\\bGET / HTTP/1.1\\b', str(mensagem), re.IGNORECASE):
        requisicao = True
    else:
        requisicao = False
    
    if requisicao :
        if(open('index.html','r')):
            arquivo = open('index.html','r')
            mensagem = arquivo.read()
            http_response = """\
HTTP/1.1 200 OK

Hello, World!
"""
            client_connection.send(mensagem.encode('utf-8'))
        else: http_response = """\
HTTP/1.1 404 Not Found

Hello, World!
"""
    else: http_response = """\
HTTP/1.1 400

Bad Request

"""
        
    
    # declaracao da resposta do servidor
    
    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response.encode('utf-8'))
    # encerra a conexao
client_connection.close()

# encerra o socket do servidor
listen_socket.close()
