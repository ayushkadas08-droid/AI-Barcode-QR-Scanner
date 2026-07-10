import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_local_env():
    env_path = os.path.join(BASE_DIR, ".env")

    if not os.path.exists(env_path):
        return

    with open(env_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()

            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


load_local_env()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Flask Settings
DEBUG = True

# Upload Folder
UPLOAD_FOLDER = "static/uploads"

# Capture Folder
CAPTURE_FOLDER = "static/captures"

# Local scan history database
DATA_FOLDER = "data"
DATABASE_PATH = os.path.join(DATA_FOLDER, "scan_history.db")
