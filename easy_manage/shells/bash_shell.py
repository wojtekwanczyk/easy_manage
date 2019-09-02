"Module responsible for running bash commands and scripts on a remote server through ssh"
from paramiko import SSHClient, AutoAddPolicy


class BashShell:
    """Class responsible for running bash commands and 
    scripts on a remote server through ssh"""

    def __init__(self, host, credentials):
        self.host = host
        self.credentials = credentials
        self.client = None

    def connect(self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(
            hostname=self.host,
            username=self.credentials.username,
            password=self.credentials.password)

    def disconnect(self):
        self.client.close()

    def cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        for line in stdout:
            print('... ' + line.strip('\n'))
