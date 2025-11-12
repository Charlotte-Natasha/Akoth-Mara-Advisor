# chat_history module to manage Q&A history
import json
import os

HISTORY_FILE = "chat_history.json"
MAX_HISTORY = 10  # Keep last 10 Q&A

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-MAX_HISTORY:], f, indent=2)

def add_to_history(question, answer):
    history = load_history()
    history.append({"question": question, "answer": answer})
    save_history(history)
