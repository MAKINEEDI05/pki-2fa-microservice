import requests

STUDENT_ID = "23P31A0536"
GITHUB_REPO_URL = "https://github.com/MAKINEEDI05/pki-2fa-microservice"

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def main():
    print("[*] Reading student public key...")
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key
    }

    print("[*] Sending request to instructor API...")
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        encrypted_seed = data.get("encrypted_seed")
        if encrypted_seed:
            with open("encrypted_seed.txt", "w") as f:
                f.write(encrypted_seed)
            print("[+] Encrypted seed saved to encrypted_seed.txt")
        else:
            print("[X] Response missing encrypted_seed field")
    else:
        print("[X] API Error:", response.status_code, response.text)

if __name__ == "__main__":
    main()
