import paramiko
import os

def read_nginx_config(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    sftp = ssh.open_sftp()
    
    # 1. List sites-enabled
    print("--- Sites Enabled ---")
    try:
        files = sftp.listdir("/etc/nginx/sites-enabled")
        print(files)
        for f in files:
            print(f"\n--- Content of {f} ---")
            try:
                # remote_file = sftp.open(f"/etc/nginx/sites-enabled/{f}")
                # print(remote_file.read().decode())
                # sftp open sometimes fails with links, use cat
                stdin, stdout, stderr = ssh.exec_command(f"cat /etc/nginx/sites-enabled/{f}")
                print(stdout.read().decode())
            except Exception as e:
                print(f"Error reading {f}: {e}")
    except Exception as e:
        print(f"Error listing sites-enabled: {e}")

    # 2. Check /var/www
    print("\n--- /var/www Listing ---")
    stdin, stdout, stderr = ssh.exec_command("ls -F /var/www/")
    print(stdout.read().decode())
    
    # 3. Check /var/www/html if exists
    print("\n--- /var/www/html Listing ---")
    stdin, stdout, stderr = ssh.exec_command("ls -F /var/www/html/")
    print(stdout.read().decode())

    ssh.close()

if __name__ == "__main__":
    read_nginx_config("114.55.65.26", 22, "root", "ASDfghjkl;")
