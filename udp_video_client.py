# udp_video_client.py

import socket
import cv2
import numpy as np

# Client configuration
IP = "127.0.0.1"
PORT = 9999

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP, PORT))
sock.settimeout(5)  # Optional: avoid hanging

print(f"[CLIENT] Listening on {IP}:{PORT}")
print("[CLIENT] Press 'q' to quit.")

buffer = b''

while True:
    try:
        data, _ = sock.recvfrom(65536)
        if not data:
            continue

        marker = data[0]
        chunk = data[1:]
        buffer += chunk

        if marker == 1:
            # Reconstruct full frame
            np_data = np.frombuffer(buffer, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            buffer = b''

            if frame is not None:
                cv2.imshow("UDP Video Stream", frame)

            # Quit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except socket.timeout:
        print("[CLIENT] Timeout — No data received.")
        break
    except Exception as e:
        print(f"[CLIENT] Error: {e}")
        break

# Cleanup
sock.close()
cv2.destroyAllWindows()
print("[CLIENT] Closed.")
