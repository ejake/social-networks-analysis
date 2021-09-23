import socket

def main():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname) 
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + IPAddr) 

if __name__ == "__main__":
    main()
