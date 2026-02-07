import paramiko
import sys

def check_ports(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    stdin, stdout, stderr = ssh.exec_command("netstat -tulnp")
    print(stdout.read().decode())
    ssh.close()

if __name__ == "__main__":
    check_ports("114.55.65.26", 22, "root", "ASDfghjkl;")
