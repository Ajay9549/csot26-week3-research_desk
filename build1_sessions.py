import os
import json
import uuid
from datetime import datetime

SESSIONS_DIR = ".agent/sessions"

def create_session() -> str:
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    session_id = uuid.uuid4().hex[:8]

    data = {
        "id": session_id,
        "title": "Untitled",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "messages": []
    }

    with open(
        os.path.join(SESSIONS_DIR, f"{session_id}.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(data, f, indent=2)

    return session_id


def save_session(
    session_id: str,
    messages: list,
    title: str = "Untitled"
) -> None:

    os.makedirs(SESSIONS_DIR, exist_ok=True)

    file_path = os.path.join(
        SESSIONS_DIR,
        f"{session_id}.json"
    )

    created_at = datetime.now().isoformat()

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            old = json.load(f)
            created_at = old.get(
                "created_at",
                created_at
            )

    data = {
        "id": session_id,
        "title": title,
        "created_at": created_at,
        "updated_at": datetime.now().isoformat(),
        "messages": messages
    }

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(data, f, indent=2)


def load_session(
    session_id: str
) -> dict:

    file_path = os.path.join(
        SESSIONS_DIR,
        f"{session_id}.json"
    )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def list_sessions() -> list:

    os.makedirs(SESSIONS_DIR, exist_ok=True)

    sessions = []

    for file in os.listdir(SESSIONS_DIR):

        if not file.endswith(".json"):
            continue

        with open(
            os.path.join(SESSIONS_DIR, file),
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

            sessions.append({
                "id": data["id"],
                "title": data["title"],
                "updated_at": data["updated_at"]
            })

    sessions.sort(
        key=lambda x: x["updated_at"],
        reverse=True
    )

    return sessions
if __name__ == "__main__":

    sid = create_session()

    messages = [
        {
            "role": "system",
            "content": "Hello"
        },
        {
            "role": "user",
            "content": "Test"
        }
    ]

    save_session(
        sid,
        messages,
        title="Test Session"
    )

    print(load_session(sid))
    print(list_sessions())
if __name__ == "__main__":

    sid = create_session()

    messages = [
        {
            "role": "system",
            "content": "Hello"
        },
        {
            "role": "user",
            "content": "Test"
        }
    ]

    save_session(
        sid,
        messages,
        title="Test Session"
    )

    print(load_session(sid))
    print(list_sessions())