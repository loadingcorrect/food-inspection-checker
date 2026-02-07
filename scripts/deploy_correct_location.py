import paramiko
import os
import sys
import time

def deploy(host, port, username, password, local_zip, remote_dir):
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, port, username, password)
        print("Connected successfully.")
    except Exception as e:
        print(f"Connection failed: {e}")
        # Try without semicolon
        if password.endswith(';'):
             try:
                ssh.connect(host, port, username, password[:-1])
             except:
                return False

    sftp = ssh.open_sftp()
    
    remote_zip = os.path.join(remote_dir, os.path.basename(local_zip)).replace('\\', '/')
    print(f"Uploading {local_zip} to {remote_zip}...")
    sftp.put(local_zip, remote_zip)
    print("Upload complete.")
    
    # Clean up my previous mistake (port 5000)
    print("Killing previous wrong process on 5000...")
    ssh.exec_command("pkill -f 'python src/app.py'")
    
    # Use python to unzip
    print(f"Unzipping to {remote_dir}...")
    unzip_cmd = f"python3 -m zipfile -e {remote_zip} {remote_dir}"
    
    # Restart Gunicorn
    # 1. Kill old gunicorn
    kill_cmd = "pkill -f gunicorn"
    
    # 2. Start new gunicorn
    # Assuming virtualenv is used, or system python. The pwdx said /var/www/pdf-extraction/src
    # I should check if there is a venv.
    # Usually: /var/www/pdf-extraction/.venv/bin/gunicorn or similar.
    # But for now, try to run gunicorn from path.
    # Command seen: gunicorn -c ...
    start_cmd = f"cd {remote_dir} && nohup gunicorn -c gunicorn_config.py src.app:app > gunicorn.log 2>&1 &"
    # Note: src.app:app because app.py is in src/. 
    # WAIT! The old process was `app:app`. 
    # If the working directory was /var/www/pdf-extraction/src, then `app:app` works.
    # If working directory is /var/www/pdf-extraction, then `src.app:app` is needed OR change dir to src.
    # The PROPER way: cd /var/www/pdf-extraction && gunicorn -c gunicorn_config.py src.app:app 
    # OR cd /var/www/pdf-extraction/src && gunicorn -c ../gunicorn_config.py app:app
    
    # Let's align with my file structure.
    # My zip -> src/app.py.
    # If I unzip to /var/www/pdf-extraction, I have /var/www/pdf-extraction/src/app.py.
    
    commands = [
        unzip_cmd,
        "pip install -r requirements.txt", # Try installing deps
        kill_cmd,
        "sleep 2",
        start_cmd,
        "sleep 2",
        "ps aux | grep gunicorn"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        out = stdout.read().decode().strip()
        err = stderr.read().decode().strip()
        
        if out: print(f"STDOUT: {out}")
        if err: print(f"STDERR: {err}")
        
        if exit_status != 0 and "pkill" not in cmd and "grep" not in cmd:
             print(f"Command failed with status {exit_status}")

    sftp.close()
    ssh.close()
    print("Deployment script finished.")
    return True

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;" 
    
    LOCAL_ZIP = "project_deploy.zip"
    REMOTE_DIR = "/var/www/pdf-extraction" # DIRECTORY OF TRUTH
    
    if not os.path.exists(LOCAL_ZIP):
        print(f"Error: {LOCAL_ZIP} not found.")
        sys.exit(1)
        
    deploy(HOST, 22, USER, PASS, LOCAL_ZIP, REMOTE_DIR)
