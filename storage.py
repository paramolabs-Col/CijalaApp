import json
import os
import threading


def get_or_create_file_key(path, generator):
    """Lee una clave binaria persistida en disco, o la genera la primera vez."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read().strip()
    key = generator()
    key_bytes = key if isinstance(key, bytes) else key.encode()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(key_bytes)
    os.chmod(path, 0o600)
    return key_bytes


class JSONStore:
    """Almacén simple de JSON en disco con lock para escritura concurrente."""

    def __init__(self, path, default_factory=list):
        self.path = path
        self.default_factory = default_factory
        self.lock = threading.Lock()
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def load(self):
        if not os.path.exists(self.path):
            return self.default_factory()
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return self.default_factory()

    def save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
