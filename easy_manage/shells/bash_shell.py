"Module responsible for running bash commands and scripts on a remote server through ssh"
from paramiko import SSHClient, AutoAddPolicy


class BashShell:
    """Class responsible for running bash commands and
    scripts on a remote server through ssh"""

    def __init__(self, host, credentials):
        self.host = host
        self.credentials = credentials
        self.client = None

    # Base commands

    def connect(self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(
            hostname=self.host,
            username=self.credentials.username,
            password=self.credentials.password)

    def disconnect(self):
        self.client.close()

    def execute(self, cmd):
        _, stdout, _ = self.client.exec_command(cmd)
        return list(stdout)

    # Memory commands

    def get_memory_total(self, swap=False):
        "Return total device memory in kibibytes"
        row = '2'
        if swap:
            row = '3'
        cmd = f"free -m | awk 'NR=={row}{{printf $2}}'"
        output = self.execute(cmd)
        return int(output[0])

    def get_memory_used(self, swap=False):
        "Return device memory in use in kibibytes"
        row = '2'
        if swap:
            row = '3'
        cmd = f"free -m | awk 'NR=={row}{{printf $3}}'"
        output = self.execute(cmd)
        return int(output[0])

    def get_memory_percentage(self, swap=False):
        "Return device memory usage in percentage"
        total = self.get_memory_total(swap)
        used = self.get_memory_used(swap)
        return float(used/total)

    # CPU commands

    def get_cpu_usage_current(self):
        cmd = "top -b -n1 | grep 'Cpu(s)' | awk '{printf $2 + $4}'"
        output = self.execute(cmd)
        return float(output[0])

    # Disk commands

    def get_disk_percentage(self):
        cmd = "df -h | awk '$NF==\"/\"{print $5}' | cut -d% -f1"
        output = self.execute(cmd)
        return int(output[0])