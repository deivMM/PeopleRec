import subprocess

main_proc = subprocess.Popen(['python3', 'main.py'])
app_proc = subprocess.Popen(['python3', 'app.py'])

try:
    main_proc.wait()
    app_proc.wait()
except KeyboardInterrupt:
    main_proc.terminate()
    app_proc.terminate()

