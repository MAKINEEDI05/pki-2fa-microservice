#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app.totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"
LOG_FILE = "/cron/last_code.txt"

def main():
    try:
        if not os.path.exists(SEED_FILE):
            print(f"[ERROR] Seed file not found", file=sys.stderr)
            return
        
        with open(SEED_FILE, 'r') as f:
            seed = f.read().strip()
        
        if not seed:
            print(f"[ERROR] Seed file is empty", file=sys.stderr)
            return
        
        code = generate_totp_code(seed)
        utc_now = datetime.now(timezone.utc)
        timestamp = utc_now.strftime("%Y-%m-%d %H:%M:%S")
        
        os.makedirs("/cron", exist_ok=True)
        log_line = f"{timestamp} - 2FA Code: {code}\n"
        
        with open(LOG_FILE, 'a') as f:
            f.write(log_line)
        
        print(f"[OK] Logged code {code} at {timestamp}")
    except Exception as e:
        print(f"[ERROR] Cron job failed: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
