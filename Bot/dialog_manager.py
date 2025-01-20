import json
import os

DIALOGUES_FILE = 'dialogues.json'
MAX_LENGTH = 4096


def read_dialogues():
    if os.path.exists(DIALOGUES_FILE):
        try:
            with open(DIALOGUES_FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}


def write_dialogues(dialogues):
    with open(DIALOGUES_FILE, 'w', encoding='utf-8') as file:
        json.dump(dialogues, file, ensure_ascii=False, indent=4)


def save_dialog(user_id, dialog_id, prompt, response):
    dialogues = read_dialogues()
    user_key = str(user_id)

    if user_key not in dialogues:
        dialogues[user_key] = {}

    if dialog_id not in dialogues[user_key]:
        dialogues[user_key][dialog_id] = []

    dialogues[user_key][dialog_id].append({"prompt": prompt, "response": response})

    while len(json.dumps(dialogues[user_key][dialog_id], ensure_ascii=False)) > MAX_LENGTH:
        dialogues[user_key][dialog_id].pop(0)

    write_dialogues(dialogues)


def load_dialog_context(user_id, dialog_id):
    dialogues = read_dialogues()
    user_key = str(user_id)
    return dialogues.get(user_key, {}).get(dialog_id, [])
