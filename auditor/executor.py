import subprocess
import paramiko
import shlex
class LocalExecutor:
    #this executor is used for localhost audit
    def run(self, command, check=True, shell=False):
        res=subprocess.run(command,
            check=check,
            capture_output=True,
            text=True,
            shell=shell,
        )
        return res

class SSHExecutor:
    #this executor is used for remote hosts audit
    def __init__(self, host, user, key_file=None):
        self.host = host
        self.user = user
        self.key_file = key_file
        self.client = None

    def check_connection(self):
        # 1. Check if host is reachable
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", "2", self.host],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3,
            )

            if result.returncode != 0:
                return {
                    "reachable": False,
                    "connectable": False,
                    "message": "Host is unreachable",
                }

        except subprocess.TimeoutExpired:
            return {
                "reachable": False,
                "connectable": False,
                "message": "Ping timed out",
            }

        # 2. Try SSH
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(
            paramiko.AutoAddPolicy()
        )

        try:
            self.client.connect(
                hostname=self.host,
                username=self.user,
                key_filename=self.key_file,
                timeout=5,
                auth_timeout=5,
            )

            return {
                "reachable": True,
                "connectable": True,
                "message": "SSH connection successful",
            }

        except paramiko.AuthenticationException:
            return {
                "reachable": True,
                "connectable": False,
                "message": f"SSH authentication failed for user '{self.user}'",
            }

        except paramiko.SSHException as e:
            return {
                "reachable": True,
                "connectable": False,
                "message": f"SSH error: {e}",
            }

        except Exception as e:
            return {
                "reachable": True,
                "connectable": False,
                "message": f"Connection failed: {e}",
            }
        


    def run(self, command, check=True):
        ssh_command = [
            "ssh",
            f"{self.user}@{self.host}",
            shlex.join(command),
        ]

        result = subprocess.run(
            ssh_command,
            check=check,
            capture_output=True,
            text=True,
        )

        return result