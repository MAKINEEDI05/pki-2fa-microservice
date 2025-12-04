#!/usr/bin/env python3
import os
import sys
import subprocess
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from app.crypto_utils import generate_commit_proof

def get_commit_hash():
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H"],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] Failed to get commit hash: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    print("[*] Generating commit proof...")
    commit_hash = get_commit_hash()
    print(f"[+] Commit Hash: {commit_hash}")
    
    hash_out, sig_b64 = generate_commit_proof(commit_hash)
    
    print(f"\n[+] Successfully generated proof!")
    print(f"\n{'='*60}")
    print(f"COMMIT HASH:")
    print(f"{hash_out}")
    print(f"\n{'='*60}")
    print(f"ENCRYPTED SIGNATURE (base64, single line):")
    print(f"{sig_b64}")
    print(f"{'='*60}\n")
    
    with open(os.path.join(BASE_DIR, "commit_proof.txt"), "w") as f:
        f.write(f"Commit Hash: {hash_out}\n")
        f.write(f"Encrypted Signature: {sig_b64}\n")
    
    print("[+] Proof also saved to commit_proof.txt")

if __name__ == "__main__":
    main()
