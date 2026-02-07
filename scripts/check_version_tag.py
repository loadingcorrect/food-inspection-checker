import paramiko
import sys

def check_remote_content(host, port, username, password):
    print(f"Connecting to {host}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, password)
        except:
             if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

        files = [
            "/var/www/pdf-extraction/templates/index.html",
            "/var/www/pdf-extraction/templates/result.html"
        ]
        
        for f in files:
            print(f"\nChecking {f} for 'style.css?v=2'...")
            stdin, stdout, stderr = ssh.exec_command(f"grep 'style.css?v=2' {f}")
            result = stdout.read().decode().strip()
            if result:
                print(f"SUCCESS: Found version tag in {f}")
                print(f"Match: {result}")
            else:
                print(f"FAILURE: Version tag NOT found in {f}")

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    check_remote_content(HOST, 22, USER, PASS)
