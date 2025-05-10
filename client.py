import hashpumpy
from server import generate_mac as generate_mac_vulnerable, verify as verify_vulnerable
from server_hmac import generate_mac as generate_mac_hmac, verify as verify_hmac

def perform_attack():
    # Intercepted message
    intercepted_message = b"amount=100&to=alice"
    # Data to append
    data_to_append = b"&admin=true"
    # Secret key length
    key_length = len(b"supersecretkey")  # 13 bytes

    # --- Attack on Vulnerable Server ---
    print("=== Attack on Vulnerable Server (server.py) ===")
    intercepted_mac = generate_mac_vulnerable(intercepted_message)
    print(f"Original message: {intercepted_message.decode()}")
    print(f"Original MAC: {intercepted_mac}")

    # Perform length extension attack
    new_mac, new_message = hashpumpy.hashpump(
        intercepted_mac,
        intercepted_message,
        data_to_append,
        key_length
    )

    forged_message = new_message
    forged_mac = new_mac

    print(f"Forged message (bytes): {forged_message}")
    print(f"Forged message (hex): {forged_message.hex()}")
    print(f"Forged MAC: {forged_mac}")

    # Verify with vulnerable server
    print("\n--- Verifying forged message (vulnerable server) ---")
    if verify_vulnerable(forged_message, forged_mac):
        print("MAC verified successfully (attack succeeded).")
    else:
        print("MAC verification failed (attack failed).")

    # --- Attack on HMAC Server ---
    print("\n=== Attack on Secure HMAC Server (server_hmac.py) ===")
    intercepted_mac = generate_mac_hmac(intercepted_message)
    print(f"Original message: {intercepted_message.decode()}")
    print(f"Original MAC: {intercepted_mac}")

    # Perform length extension attack
    new_mac, new_message = hashpumpy.hashpump(
        intercepted_mac,
        intercepted_message,
        data_to_append,
        key_length
    )

    forged_message = new_message
    forged_mac = new_mac

    print(f"Forged message (bytes): {forged_message}")
    print(f"Forged message (hex): {forged_message.hex()}")
    print(f"Forged MAC: {forged_mac}")

    # Verify with HMAC server
    print("\n--- Verifying forged message (HMAC server) ---")
    if verify_hmac(forged_message, forged_mac):
        print("MAC verified successfully (attack succeeded).")
    else:
        print("MAC verification failed (attack failed).")

if __name__ == "__main__":
    perform_attack()
