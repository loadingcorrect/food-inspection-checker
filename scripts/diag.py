import sys
import os
print(f"Python executable: {sys.executable}")
print(f"CWD: {os.getcwd()}")
print(f"Sys Path: {sys.path}")
try:
    import paramiko
    print(f"Paramiko version: {paramiko.__version__}")
    print(f"Paramiko file: {paramiko.__file__}")
except ImportError as e:
    print(f"Paramiko import failed: {e}")
