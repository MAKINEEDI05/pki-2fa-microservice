from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def main():
    print("[*] Generating 4096-bit RSA key pair...")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    # Save private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open("student_private.pem", "wb") as f:
        f.write(private_pem)
    print("[+] Saved private key to student_private.pem")

    # Save public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open("student_public.pem", "wb") as f:
        f.write(public_pem)
    print("[+] Saved public key to student_public.pem")

if __name__ == "__main__":
    main()
