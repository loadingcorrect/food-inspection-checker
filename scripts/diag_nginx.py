import paramiko
import sys

def diag_nginx(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    # Find configs
    cmd = "find /etc/nginx -name '*.conf' -o -name 'default' 2>/dev/null"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    files = stdout.read().decode().strip().split('\n')
    
    print("Found Nginx configs:", files)
    
    for f in files:
        if not f: continue
        print(f"\n--- CONTENT OF {f} ---")
        stdin, stdout, stderr = ssh.exec_command(f"cat {f}")
        print(stdout.read().decode())
        
    ssh.close()

if __name__ == "__main__":
    diag_nginx("114.55.65.26", 22, "root", "ASDfghjkl;")
