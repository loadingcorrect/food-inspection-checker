import paramiko
import sys

def verify_deployment(host, port, username, password):
    print(f"Connecting to {host}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, password)
        except:
             if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

        # 1. Check Gunicorn
        print("\n--- Checking Gunicorn Process ---")
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep gunicorn | grep -v grep")
        gunicorn_procs = stdout.read().decode().strip()
        if gunicorn_procs:
            print("Gunicorn is running:")
            print(gunicorn_procs)
        else:
            print("WARNING: Gunicorn process NOT found.")

        # 2. Check File Permissions
        print("\n--- Checking File Permissions ---")
        files_to_check = [
            "/var/www/pdf-extraction/templates/index.html",
            "/var/www/pdf-extraction/templates/result.html",
            "/var/www/pdf-extraction/static/style.css"
        ]
        
        for f in files_to_check:
            stdin, stdout, stderr = ssh.exec_command(f"ls -l {f}")
            print(stdout.read().decode().strip())

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    verify_deployment(HOST, 22, USER, PASS)
