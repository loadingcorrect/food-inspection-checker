import paramiko
import sys

def check_status(host, port, username, password, remote_dir):
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
    except Exception as e:
        print(f"Connection failed: {e}")
        # Try without semicolon
        if password.endswith(';'):
             try:
                ssh.connect(host, port, username, password[:-1])
             except:
                return

    commands = [
        f"cat {remote_dir}/app/app.log | tail -n 20",
        "netstat -tulnp | grep python",
        "ps aux | grep src/app.py"
    ]
    
    for cmd in commands:
        print(f"\n--- Executing: {cmd} ---")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        print(out)
        if err: print(f"STDERR: {err}")

    ssh.close()

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    REMOTE_DIR = "/root/extraction_system_deploy"
    
    check_status(HOST, 22, USER, PASS, REMOTE_DIR)
