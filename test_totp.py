from utils_crypto import generate_totp_code, verify_totp_code

hex_seed = "dc7e6294d256cdd7ecfbc9f9febb2d7c47dc38b391dce1c5e28b44259e9c03f6"

code = generate_totp_code(hex_seed)
print("Generated TOTP:", code)

print("Verify:", verify_totp_code(hex_seed, code))
