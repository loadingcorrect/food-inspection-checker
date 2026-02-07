import paramiko
import sys

def verify_http_response(host, port, username, password):
    print(f"Connecting to {host}...")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, password)
        except:
             if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

        print("\n--- Curling Localhost:8000 ---")
        # curl the index page and check for v=2
        cmd = "curl -s http://127.0.0.1:8000/"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        response = stdout.read().decode()
        
        # We look for the substring "?v=2" which should be present in the rendered HTML
        if "?v=2" in response:
            print("SUCCESS: Response contains '?v=2'")
            # Print the line containing it for confirmation
            for line in response.splitlines():
                if "?v=2" in line:
                    print(f"Match: {line.strip()}")
        else:
            print("FAILURE: Response DOES NOT contain '?v=2'")
            print("Response head:")
            print(response[:200])

        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    HOST = "114.55.65.26"
    USER = "root"
    PASS = "ASDfghjkl;"
    
    verify_http_response(HOST, 22, USER, PASS)
