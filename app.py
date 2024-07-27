import subprocess
import json
from flask import Flask, render_template, request

app = Flask(__name__)

entries = []


def read_from_subprocess():
    try:
        process = subprocess.Popen(['./vizlink'], stdout=subprocess.PIPE, text=True)
        for line in process.stdout:
            if line.strip():
                try:
                    entry = json.loads(line)
                    print(f"Eintrag: {entry}")
                    entries.append(entry)
                except json.JSONDecodeError as e:
                    print(f"Fehler beim Lesen der JSON-Daten: {e}")
        for line in process.stderr:
            print(f"Fehlerausgabe: {line.strip()}")
        process.stdout.close()
        process.stderr.close()
        process.wait()
    except OSError as e:
        print(f"Fehler beim Ausführen des Subprozesses: {e}")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Lesen der JSON-Daten: {e}")
    except KeyboardInterrupt:
        print("Eingabe gestoppt durch Tastendruck")
    except Exception as e:
        print(f"Unbekannter Fehler: {e}")
    finally:
        print("Prozess beendet")


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
