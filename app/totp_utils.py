import pyotp
import base64
import time

def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    return base32_seed

def generate_totp_code(hex_seed: str) -> str:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.now()

def get_totp_remaining_seconds(hex_seed: str = None) -> int:
    current_time = time.time()
    period_start = (int(current_time) // 30) * 30
    period_end = period_start + 30
    remaining = int(period_end - current_time)
    return remaining

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30)
    return totp.verify(code, valid_window=valid_window)
