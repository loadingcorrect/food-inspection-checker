import paramiko
import sys

def check_style_issue(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    print("--- Permissions of static dir ---")
    stdin, stdout, stderr = ssh.exec_command("ls -la /var/www/pdf-extraction/static")
    print(stdout.read().decode())
    
    print("--- Permissions of static/css ---")
    stdin, stdout, stderr = ssh.exec_command("ls -la /var/www/pdf-extraction/static/css")
    print(stdout.read().decode())

    print("\n--- Nginx Error Log (Last 20 lines) ---")
    # Usually /var/log/nginx/error.log
    stdin, stdout, stderr = ssh.exec_command("tail -n 20 /var/log/nginx/error.log")
    print(stdout.read().decode())

    print("\n--- Nginx Access Log (Last 20 CSS requests) ---")
    stdin, stdout, stderr = ssh.exec_command("grep '\.css' /var/log/nginx/access.log | tail -n 20")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    check_style_issue(HOST, 22, USER, PASS)
