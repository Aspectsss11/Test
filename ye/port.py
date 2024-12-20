import socket
import keyboard
import time

# Signature code for the script
SIGNATURE = "2365498307059828"  # Your specified unique signature

def verify_signature():
    # Dummy verification for the signature
    if SIGNATURE != "2365498307059828":  # Modify as needed for actual validation
        print("Invalid signature!")
        exit(1)

def main():
    verify_signature()  # Check signature at the start of the script

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 65432))
    sock.listen(1)
  
    time.sleep(0.1)
    
    conn, addr = sock.accept()
    print(f"Connected to {addr}")  # Print when connected
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            key = data.decode()
            if len(key) == 1 and key.isalnum():  # Check if the key is a single letter or number
                keyboard.send(key)
            time.sleep(0.01)

if __name__ == "__main__":
    main()
