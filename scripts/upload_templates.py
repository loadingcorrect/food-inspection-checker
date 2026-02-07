import paramiko
import os
import sys

def upload_templates(host, port, username, password, local_dir, remote_dir):
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    sftp = ssh.open_sftp()
    
    files = ['index.html', 'result.html']
    
    for f in files:
        local_path = os.path.join(local_dir, f)
        remote_path = f"{remote_dir}/{f}"
        print(f"Uploading {local_path} to {remote_path}...")
        sftp.put(local_path, remote_path)
    
    print("Upload complete.")
    sftp.close()
    
    # Reload Gunicorn (just in case)
    print("Reloading Gunicorn...")
    ssh.exec_command("pkill -HUP -f gunicorn")
    
    ssh.close()

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    LOCAL_TEMPLATES = "templates"
    REMOTE_TEMPLATES = "/var/www/pdf-extraction/templates"
    
    if not os.path.exists(LOCAL_TEMPLATES):
        print(f"Error: {LOCAL_TEMPLATES} not found locally.")
        sys.exit(1)
        
    upload_templates(HOST, 22, USER, PASS, LOCAL_TEMPLATES, REMOTE_TEMPLATES)
