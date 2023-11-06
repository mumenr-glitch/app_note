from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Get the desktop path for the current user on macOS
DESKTOP_PATH = os.path.expanduser('~/Desktop')
BACKUP_FILE = os.path.join(DESKTOP_PATH, "notes_backup.json")

@app.route('/backup', methods=['POST'])
def backup_notes():
    notes = request.json
    try:
        with open(BACKUP_FILE, 'w') as file:
            json.dump(notes, file)
        return jsonify({"status": "success", "message": "Notes backed up successfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/restore', methods=['GET'])
def restore_notes():
    try:
        if os.path.exists(BACKUP_FILE):
            with open(BACKUP_FILE, 'r') as file:
                notes = json.load(file)
            return jsonify(notes)
        else:
            return jsonify({"status": "error", "message": "Backup file does not exist."}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=False)
