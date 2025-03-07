import socket

HOST="0.0.0.0"
PORT=3000 
QUIT_MESSAGE="quit"
    
class ControllerWifiServer:
    
    def __init__(self, motor_driver):
        self.motor_driver = motor_driver
    
    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        
        server.listen(1)
        print(f"Server listening on {HOST}:{PORT}")
        
        client_socket, client_address = server.accept()
        print(f"Connection from {client_address}")
        
        try:
            while True:
                data_length = client_socket.recv(1)[0]
                if not data_length:
                    continue
                
                data = client_socket.recv(data_length)
                data = list(data)
                #print(f"Received: {data}")
                self.motor_driver.command_parser(data)
         
        except ConnectionResetError:
            print("The connection have been close bruptly")
        except KeyboardInterrupt:
            print("The user close the server")
            client_socket.sendall(QUIT_MESSAGE.encode())
        except IndexError:
            print("The client is disconnected !")
        finally:
            client_socket.close()
            server.close()