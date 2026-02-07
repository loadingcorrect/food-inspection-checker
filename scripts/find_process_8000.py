import paramiko
import sys

def find_old_process(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    print("--- Process on Port 8000 ---")
    stdin, stdout, stderr = ssh.exec_command("netstat -tulnp | grep 8000")
    out = stdout.read().decode()
    print(out)
    
    if out:
        pid = out.split()[6].split('/')[0]
        print(f"PID: {pid}")
        stdin, stdout, stderr = ssh.exec_command(f"ps -p {pid} -f")
        print(stdout.read().decode())
        
        stdin, stdout, stderr = ssh.exec_command(f"pwdx {pid}")
        print(stdout.read().decode())

    ssh.close()

if __name__ == "__main__":
    find_old_process("114.55.65.26", 22, "root", "ASDfghjkl;")
