import os
import sys
import sqlite3

# Vercel adapter: app.py itself is kept unchanged.
# Vercel function files are read-only, so runtime SQLite/uploads use /tmp.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNTIME_DIR = "/tmp/luki_data"
RUNTIME_DB = os.path.join(RUNTIME_DIR, "filepoint.db")
RUNTIME_UPLOAD = os.path.join(RUNTIME_DIR, "uploads")
os.makedirs(RUNTIME_UPLOAD, exist_ok=True)

_original_connect = sqlite3.connect
def _connect(database, *args, **kwargs):
    if isinstance(database, str) and database.endswith("filepoint.db"):
        database = RUNTIME_DB
    return _original_connect(database, *args, **kwargs)
sqlite3.connect = _connect

_original_makedirs = os.makedirs
def _makedirs(name, *args, **kwargs):
    if isinstance(name, str) and os.path.normpath(name) == os.path.normpath(os.path.join(BASE_DIR, "uploads")):
        name = RUNTIME_UPLOAD
    return _original_makedirs(name, *args, **kwargs)
os.makedirs = _makedirs

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import app as _app

# Keep all application routes/features intact; only redirect writable storage.
_app.DB = RUNTIME_DB
_app.UPLOAD = RUNTIME_UPLOAD
os.makedirs(RUNTIME_UPLOAD, exist_ok=True)

app = _app.app
