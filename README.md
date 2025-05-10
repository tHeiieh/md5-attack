
# 🔓 Hash Length Extension Attack Demonstration

This project demonstrates a **hash length extension attack** using the `hashpumpy` Python library. It contrasts a vulnerable MAC implementation (in `server.py`) with a secure HMAC-based implementation (in `server_hmac.py`) to highlight the risks of insecure message authentication code (MAC) construction.

---

## 🧠 What is a Hash Length Extension Attack?

A **hash length extension attack** exploits the way certain hash functions (like MD5 or SHA1) process input. If a system generates a MAC by simply computing:

```
MAC = Hash(secret || message)
```

then an attacker can:

- Infer how many bytes the secret is.
- Extend the original message (e.g., add `&admin=true`).
- Compute a valid MAC for the extended message **without knowing the secret**.

This is possible because many hash functions allow continuing the hashing process from an intermediate state.

> ✅ HMAC constructions are **not** vulnerable to this attack because the key is mixed into both the inner and outer hashing process.

---

## 📂 Project Structure

```
.
├── client.py              # The main attack script
├── server.py              # Insecure server using MD5-based MAC
├── server_hmac.py         # Secure server using HMAC (MD5)
└── README.md              # This documentation
```

---

## ⚙️ Prerequisites

- Python 3.x
- `hashpumpy` library (for performing the attack)

Install with:

```bash
pip install hashpumpy
```

---

## 🔧 Server Function Requirements

Your `server.py` and `server_hmac.py` modules must define these functions:

```python
# Insecure MAC
def generate_mac(message: bytes) -> str:
    ...

def verify(message: bytes, mac: str) -> bool:
    ...

# Secure MAC (HMAC)
def generate_mac(message: bytes) -> str:
    ...

def verify(message: bytes, mac: str) -> bool:
    ...
```

---

## 🚀 Running the Attack

Use the provided script:

```bash
python client.py
```

The script:

1. Simulates an intercepted message (`amount=100&to=alice`).
2. Attempts to append malicious data (`&admin=true`).
3. Uses `hashpumpy` to forge a valid MAC for the extended message.
4. Verifies the result against both the insecure and secure servers.

---

## 🖥️ Sample Output

```text
=== Attack on Vulnerable Server (server.py) ===
Original message: amount=100&to=alice
Original MAC: 8e78f6c89c21...
Forged message (bytes): b'amount=100&to=alice\x80...&admin=true'
Forged MAC: eaf23d09f3...

--- Verifying forged message (vulnerable server) ---
MAC verified successfully (attack succeeded).

=== Attack on Secure HMAC Server (server_hmac.py) ===
Original message: amount=100&to=alice
Original MAC: 345bd72d1e...
Forged MAC: 78f3a1bc...
--- Verifying forged message (HMAC server) ---
MAC verification failed (attack failed).
```

---

## 🔐 Why HMAC is Secure

HMAC (Hash-based Message Authentication Code) is defined as:

```
HMAC(K, M) = H((K ⊕ opad) || H((K ⊕ ipad) || M))
```

- The key is mixed into both the inner and outer hashes.
- Hash length extension attacks are impossible because the attacker cannot continue hashing without knowing the secret key.

Always use **HMAC** or a proven cryptographic construction for authentication!

---

## 📚 References

- [Hash Length Extension (Wikipedia)](https://en.wikipedia.org/wiki/Length_extension_attack)
- [HMAC (Wikipedia)](https://en.wikipedia.org/wiki/HMAC)
- [hashpumpy GitHub](https://github.com/bwall/HashPump)

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. Do **not** use this code for malicious activities. Always follow responsible disclosure guidelines when testing security systems.

---

## 📄 License

MIT License – feel free to use and adapt.

---

