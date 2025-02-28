from scripts.core.camera import Camera
import socket
from scripts.core.udp_packet import UdpPacketsHandler, UdpPacket
import cv2

# Streaning configuration
HOST = "192.168.2.18"  # Connect to server to the address
PORT = 4099       # Choose an available port
PACKET_SIZE=60000 # UDP packet size
MAX_PACKET_ID=256 # packet idx max value


class NetworkService:
    keep_streaming = False
    
    def startSteaming(self, camera: Camera):
        keep_Streaming = True
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create UDP socket
        print(f"[*] Sending video stream to {HOST}:{PORT}")
        msg_id=0
        
        try:
            while keep_Streaming:
                frame = camera.capture_image() 
                _, buffer = cv2.imencode(".jpg", frame)
                packets = UdpPacketsHandler.split_data(msg_idx=msg_id, data=buffer.tobytes(), max_packet_size=PACKET_SIZE)

                # Send packets over UDP socket
                for packet in packets:
                    client_socket.sendto(UdpPacket.encode(packet), (HOST, PORT))
                    
                msg_id = (msg_id + 1) % MAX_PACKET_ID
            

        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client_socket.close()
            camera.stop_camera()
            print("[*] Connection closed")
        