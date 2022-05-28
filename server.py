import socket
import threading
import os


PORT = 8080
SIZE_RECEIVE = 4096
FORMAT = 'utf-8'

def HandlerDownload(con):
    
    message = con.recv(SIZE_RECEIVE).decode(FORMAT)      
    if message != 'favicon.ico': 
        if not message:
            con.close()
            return       
            
        filename = message.split()[1]
        if  not os.path.isfile(filename[1:]):
            con.sendall(bytes("\nHTTP/1.1 404 Not Found\n\n", FORMAT))
            con.close()
            
        else:   
            con.sendall(bytes(f"\nHTTP/1.1 200 OK\nContent-Disposition: attachment; filename={filename[1:]}\n\n", FORMAT))
            with open(filename[1:], "rb") as output:
                con.sendfile(output)
            con.close()


def main():
    ms=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ms.bind(('',PORT))
    ms.listen(4096)
    print(f"Listening on port {PORT}")
    while True:
        con, addr=ms.accept()
        clients = threading.Thread(target=HandlerDownload, args=(con,))
        clients.start()


if __name__ == '__main__':
    main()