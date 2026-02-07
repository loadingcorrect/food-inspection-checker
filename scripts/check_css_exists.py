import paramiko

def check_file(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
    except:
        if password.endswith(';'): ssh.connect(host, port, username, password[:-1])

    print("--- Local static/css check (local simulation) ---")
    # I can't check local here easily via script running on local, well I can but I listed dir above.
    
    print("--- Remote static recursive list ---")
    stdin, stdout, stderr = ssh.exec_command("find /var/www/pdf-extraction/static -maxdepth 3")
    print(stdout.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    check_file("114.55.65.26", 22, "root", "ASDfghjkl;")
