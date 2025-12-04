import os
import time
from fastapi import FastAPI, HTTPException
from app.crypto_utils import decrypt_seed
from app.totp_utils import generate_totp_code, get_totp_remaining_seconds, verify_totp_code

app = FastAPI(title="PKI 2FA Microservice")

SEED_FILE = "/data/seed.txt"

def load_seed() -> str:
    if not os.path.exists(SEED_FILE):
        return None
    with open(SEED_FILE, 'r') as f:
        return f.read().strip()

@app.post("/decrypt-seed")
def api_decrypt_seed(payload: dict):
    try:
        encrypted_seed = payload.get("encrypted_seed")
        if not encrypted_seed:
            raise HTTPException(status_code=400, detail="Missing encrypted_seed")
        
        seed_hex = decrypt_seed(encrypted_seed)
        
        if len(seed_hex) != 64 or not all(c in '0123456789abcdef' for c in seed_hex):
            raise ValueError("Invalid seed format")
        
        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE, 'w') as f:
            f.write(seed_hex)
        
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
def api_generate_2fa():
    try:
        seed = load_seed()
        if not seed:
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        
        code = generate_totp_code(seed)
        valid_for = get_totp_remaining_seconds()
        
        return {"code": code, "valid_for": valid_for}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error generating 2FA code")

@app.post("/verify-2fa")
def api_verify_2fa(payload: dict):
    try:
        code = payload.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Missing code")
        
        seed = load_seed()
        if not seed:
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        
        is_valid = verify_totp_code(seed, code, valid_window=1)
        return {"valid": is_valid}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error verifying code")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
