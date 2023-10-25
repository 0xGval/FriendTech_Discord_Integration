import subprocess

def main():
    # Paths to your scripts - If they're in the same directory as this script, you can just use the file names.
    path_to_autod = "autod.py"
    path_to_listen = "listen.py"

    print("Starting scripts...")

    # Start the processes
    process_autod = subprocess.Popen(["python", path_to_autod], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)
    process_listen = subprocess.Popen(["python", path_to_listen], shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)

    print("Scripts are running in the background...")

if __name__ == "__main__":
    main()
