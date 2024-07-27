import subprocess
import json
from flask import Flask, render_template, request

app = Flask(__name__)

entries = []

def read_from_subprocess():
    global entries
    try:
        process = subprocess.Popen(['./vizlink/vizlink.exe'], stdout=subprocess.PIPE, text=True)
        for line in process.stdout:
            if line.strip():
                try:
                    entry = json.loads(line)
                    entries.append(entry)
                except json.JSONDecodeError as e:
                    print(f"Fehler beim Lesen der JSON-Daten: {e}")
        process.stdout.close()
        process.wait()
    except Exception as e:
        print(f"Fehler beim Ausführen des Subprozesses: {e}")
    except KeyboardInterrupt:
        print("Eingabe gestoppt durch Tastendruck")

@app.route('/')
def index():
    return render_template('index.html', entries=entries)

@app.route('/stop')
def stop():
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown:
        shutdown()
    return "Server wird gestoppt..."

if __name__ == '__main__':
    from threading import Thread

    subprocess_thread = Thread(target=read_from_subprocess)
    subprocess_thread.daemon = True
    subprocess_thread.start()

    app.run(debug=True, use_reloader=False)