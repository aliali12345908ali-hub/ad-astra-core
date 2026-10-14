import base64
import hashlib

def simple_encrypt(data_str, secret_key="ad-astra-core-secret"):
    key_hash = hashlib.sha256(secret_key.encode()).digest()
    data_bytes = data_str.encode('utf-8')
    encrypted_bytes = bytearray(b ^ key_hash[i % len(key_hash)] for i, b in enumerate(data_bytes))
    return base64.b64encode(encrypted_bytes).decode('utf-8')

def simple_decrypt(enc_str, secret_key="ad-astra-core-secret"):
    key_hash = hashlib.sha256(secret_key.encode()).digest()
    dec_bytes = base64.b64decode(enc_str.encode('utf-8'))
    decrypted_bytes = bytearray(b ^ key_hash[i % len(key_hash)] for i, b in enumerate(dec_bytes))
    return decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    payload = "Sensitive Data: Cloud Management Credentials"
    encrypted = simple_encrypt(payload)
    decrypted = simple_decrypt(encrypted)
    print(f"[CRYPTO] Original: {payload}")
    print(f"[CRYPTO] Encrypted: {encrypted}")
    print(f"[CRYPTO] Decrypted: {decrypted}")
