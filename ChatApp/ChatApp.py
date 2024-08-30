import subprocess
import time

def run_chat_app_instance():
    # Start the chat application script
    return subprocess.Popen(['python', 'ChatApp_Lib.py'])

def main():
    # Start two instances of the chat application
    instance = run_chat_app_instance()

    # Optionally, wait for the processes to complete
    instance.wait()

if __name__ == "__main__":
    main()
