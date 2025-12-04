import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend

def load_private_key(key_path: str):
    with open(key_path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

def load_public_key(key_path: str):
    with open(key_path, 'rb') as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

def decrypt_seed(encrypted_seed_b64: str, private_key_path: str = "student_private.pem") -> str:
    try:
        private_key = load_private_key(private_key_path)
        encrypted_bytes = base64.b64decode(encrypted_seed_b64)
        seed_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        seed_hex = seed_bytes.decode('utf-8')
        
        if len(seed_hex) != 64:
            raise ValueError(f"Seed must be 64 chars, got {len(seed_hex)}")
        
        int(seed_hex, 16)
        return seed_hex
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def sign_message(message: str, private_key_path: str = "student_private.pem") -> bytes:
    private_key = load_private_key(private_key_path)
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key_path: str = "instructor_public.pem") -> bytes:
    public_key = load_public_key(public_key_path)
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def generate_commit_proof(commit_hash: str) -> tuple:
    signature = sign_message(commit_hash)
    encrypted_sig = encrypt_with_public_key(signature)
    encrypted_sig_b64 = base64.b64encode(encrypted_sig).decode('utf-8')
    return commit_hash, encrypted_sig_b64
