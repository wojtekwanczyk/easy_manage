"Module responsible for running bash commands and scripts on a remote server through ssh"
import socket
import sys
import termios
import tty
import select


class BashShell:
    """Class responsible for running bash commands and
    scripts on a remote server through ssh"""

    def __init__(self, connector):
        self.connector = connector

    # Base commands


    def execute(self, cmd):
        _, stdout, _ = self.connector.exec_command(cmd)
        return list(stdout)

    def interactive_shell(self):
        "Run remote interactive shell on connected client machine"
        channel = self.connector.invoke_shell()
        oldtty = termios.tcgetattr(sys.stdin)
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            channel.settimeout(0.0)

            while True:
                rlist, _, _ = select.select([channel, sys.stdin], [], [])
                if channel in rlist:
                    try:
                        output = channel.recv(1024).decode()
                        if not output:
                            sys.stdout.write("*** exiting interactive shell ***\r\n")
                            break
                        sys.stdout.write(output)
                        sys.stdout.flush()
                    except socket.timeout:
                        pass
                if sys.stdin in rlist:
                    user_input = sys.stdin.read(1)
                    if not user_input:
                        break
                    channel.send(user_input)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
        channel.close()

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

    def get_memory_percentage(self, swap=False, ndigits=2):
        """Return device memory usage in percentage
        or None in case of lack of memory"""
        total = self.get_memory_total(swap)
        if not total:
            return None  # In case no swap is used
        used = self.get_memory_used(swap)
        return round(float(used/total), ndigits)

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


    # Complete batch of bash readings

    def readings(self):
        data = {
            'disk_quota': self.get_disk_percentage(),
            'cpu_quota': self.get_cpu_usage_current(),
            'memory_quota': self.get_memory_percentage(),
            'swap_quota': self.get_memory_percentage(swap=True),
        }
        return data
