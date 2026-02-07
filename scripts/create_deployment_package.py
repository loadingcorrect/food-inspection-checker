import os
import zipfile

def zip_project(output_filename, source_dir):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Exclude directories
            dirs[:] = [d for d in dirs if d not in ['.venv', '.git', '__pycache__', 'project.zip']]
            
            for file in files:
                if file.endswith('.zip') or file.endswith('.log') or file.endswith('.pyc'):
                    continue
                
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=source_dir)
                zipf.write(file_path, arcname)
                print(f"Added {arcname}")

if __name__ == "__main__":
    source = os.getcwd()
    output = os.path.join(source, 'project_deploy.zip')
    print(f"Zipping {source} to {output}...")
    zip_project(output, source)
    print("Done.")
