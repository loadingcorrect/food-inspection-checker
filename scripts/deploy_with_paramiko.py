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
            print("Retrying without semicolon...")
            try:
                ssh.connect(host, port, username, password[:-1])
                print("Connected successfully (without semicolon).")
            except Exception as e2:
                print(f"Retry failed: {e2}")
                return False
        else:
            return False

    # Create remote directory first
    print(f"Creating remote directory {remote_dir}...")
    ssh.exec_command(f"mkdir -p {remote_dir}")
    
    sftp = ssh.open_sftp()
    
    remote_zip = os.path.join(remote_dir, os.path.basename(local_zip)).replace('\\', '/')
    print(f"Uploading {local_zip} to {remote_zip}...")
    sftp.put(local_zip, remote_zip)
    print("Upload complete.")
    
    # Commands to run
    # Use python to unzip
    unzip_cmd = f"python -m zipfile -e {remote_zip} {remote_dir}/app"
    
    commands = [
        f"mkdir -p {remote_dir}/app",
        unzip_cmd,
        f"cd {remote_dir}/app && pip install -r requirements.txt",
        "pkill -f 'python src/app.py' || true",
        f"cd {remote_dir}/app && nohup python src/app.py > app.log 2>&1 &",
        "sleep 2",
        "ps aux | grep src/app.py"
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
    REMOTE_DIR = "/root/extraction_system_deploy"
    
    if not os.path.exists(LOCAL_ZIP):
        print(f"Error: {LOCAL_ZIP} not found.")
        sys.exit(1)
        
    deploy(HOST, 22, USER, PASS, LOCAL_ZIP, REMOTE_DIR)
