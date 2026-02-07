import paramiko
import os
import sys

def upload_ui_fixes(host, port, username, password):
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    sftp = ssh.open_sftp()
    
    # Upload Templates
    local_dir = "templates"
    remote_dir = "/var/www/pdf-extraction/templates"
    files = ['result.html'] # Only result.html changed
    
    for f in files:
        local_path = os.path.join(local_dir, f)
        remote_path = f"{remote_dir}/{f}"
        print(f"Uploading {local_path} to {remote_path}...")
        sftp.put(local_path, remote_path)

    # Upload CSS
    local_css = "static/style.css"
    remote_css = "/var/www/pdf-extraction/static/style.css"
    print(f"Uploading {local_css} to {remote_css}...")
    sftp.put(local_css, remote_css)
    
    print("Upload complete.")
    sftp.close()
    
    # Reload Gunicorn
    print("Reloading Gunicorn...")
    ssh.exec_command("pkill -HUP -f gunicorn")
    
    ssh.close()

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    if not os.path.exists("templates/result.html") or not os.path.exists("static/style.css"):
        print("Error: Local files not found.")
        sys.exit(1)
        
    upload_ui_fixes(HOST, 22, USER, PASS)
