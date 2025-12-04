import os
import time
import sys

# Ensure /app is on sys.path so we can import app.totp_utils
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.totp_utils import generate_totp_code

SEED_FILE_PATH = "/data/seed.txt"
OUTPUT_FILE = "/data/2fa-codes.txt"


def load_seed():
    if not os.path.exists(SEED_FILE_PATH):
        return None
    with open(SEED_FILE_PATH, "r") as f:
        return f.read().strip()


def main():
    seed = load_seed()
    if not seed:
        return  # seed not decrypted yet

    code = generate_totp_code(seed)
    timestamp = int(time.time())

    os.makedirs("/data", exist_ok=True)

    with open(OUTPUT_FILE, "a") as f:
        f.write(f"{timestamp},{code}\n")


if __name__ == "__main__":
    main()
