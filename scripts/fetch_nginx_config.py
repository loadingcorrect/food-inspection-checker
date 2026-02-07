import paramiko
import os

def fetch_config(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    sftp = ssh.open_sftp()
    
    local_path = "nginx_remote_site.conf"
    remote_path = "/etc/nginx/sites-enabled/pdf-extraction"
    
    print(f"Downloading {remote_path} to {local_path}...")
    try:
        sftp.get(remote_path, local_path)
        print("Download successful.")
    except Exception as e:
        print(f"Download failed: {e}")
        
    ssh.close()

if __name__ == "__main__":
    fetch_config("114.55.65.26", 22, "root", "ASDfghjkl;")
