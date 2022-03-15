import os
import sys
import subprocess

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if not os.path.exists(f"tools/{sys.argv[1]}.py"):
            filenames = next(os.walk("tools"), (None, None, []))[2]
            commands = " | ".join([os.path.splitext(f)[0] for f in filenames])
            print(f"Error: Command not found ({commands}).")
            sys.exit(1)

        subprocess.run(["python", f"tools/{sys.argv[1]}.py"] + sys.argv[2:])
    else:
        print("Usage: python manage.py <command> [...args]")
