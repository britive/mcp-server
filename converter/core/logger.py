import logging, os

LOG_FILE = "logs/app.log"
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    # Clear handlers to prevent duplicates
    if root.hasHandlers():
        root.handlers.clear()

    # File handler (detailed)
    fh = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    root.addHandler(fh)

    # Console handler (simple)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root.addHandler(ch)
