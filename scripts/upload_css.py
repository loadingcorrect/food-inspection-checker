import paramiko
import os
import sys

def upload_css(host, port, username, password, local_file, remote_path):
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    sftp = ssh.open_sftp()
    
    print(f"Uploading {local_file} to {remote_path}...")
    sftp.put(local_file, remote_path)
    print("Upload complete.")
    sftp.close()
    
    # Fix permissions
    print("Fixing permissions...")
    ssh.exec_command(f"chown www-data:www-data {remote_path}")
    ssh.exec_command(f"chmod 644 {remote_path}")
    
    ssh.close()

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    LOCAL_CSS = "static/style.css"
    REMOTE_CSS = "/var/www/pdf-extraction/static/style.css"
    
    if not os.path.exists(LOCAL_CSS):
        print(f"Error: {LOCAL_CSS} not found locally.")
        sys.exit(1)
        
    upload_css(HOST, 22, USER, PASS, LOCAL_CSS, REMOTE_CSS)
