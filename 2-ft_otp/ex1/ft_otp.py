#!/usr/bin/env python3
import argparse
import sys
import os
import string
import hmac
import hashlib
import struct
import time
from cryptography.fernet import Fernet

MASTER_KEY = b'7KuVFz0qyyMOIFXd-OzRotwpARn77s5ywOXGxdzwRjI='

def handle_save_key(filepath: str):
    try:
        with open(filepath, "r") as f:
            raw_key = f.read().strip()
    except Exception as e:
        print(f"./ft_otp: error: impossible de lire {filepath} ({e})", file=sys.stderr)
        sys.exit(1)

    is_hex = all(c in string.hexdigits for c in raw_key)
    if len(raw_key) < 64 or not is_hex:
        print("./ft_otp: error: key must be 64 hexadecimal characters.", file=sys.stderr)
        sys.exit(1)

    cipher = Fernet(MASTER_KEY)
    encrypted_data = cipher.encrypt(raw_key.encode())

    try:
        with open("ft_otp.key", "wb") as f:
            f.write(encrypted_data)
        print("Key was successfully saved in ft_otp.key.")
    except Exception as e:
        print(f"./ft_otp: error: impossible d'écrire ft_otp.key ({e})", file=sys.stderr)
        sys.exit(1)

def generate_hotp(key_bytes: bytes, counter: int) -> str:
    """
    Implémentation stricte de la RFC 4226 (HOTP)
    """
    # 1. Encodage du compteur sur 8 octets en Big-Endian (format unsigned long long: >Q)
    counter_bytes = struct.pack(">Q", counter)

    # 2. Calcul du HMAC-SHA1 (donne un condensat de 20 octets)
    hmac_hash = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest()

    # 3. Troncature dynamique (Dynamic Truncation)
    # L'offset est déterminé par les 4 bits de poids faible du dernier octet (0x0F)
    offset = hmac_hash[19] & 0x0F

    # On extrait 4 octets à partir de l'offset en masquant le bit de poids fort (0x7FFFFFFF)
    # pour éviter qu'il soit interprété comme un entier signé négatif
    code_int = struct.unpack(">I", hmac_hash[offset : offset + 4])[0] & 0x7FFFFFFF

    # 4. Réduction à 6 chiffres avec padding de zéros si nécessaire
    otp = code_int % 1_000_000
    return f"{otp:06d}"


def handle_generate_otp(filepath: str):
    """
    Lit le fichier chiffré, déchiffre la clé et affiche le code OTP
    """
    # 1. Lecture du fichier chiffré
    try:
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
    except Exception as e:
        print(f"./ft_otp: error: impossible de lire {filepath} ({e})", file=sys.stderr)
        sys.exit(1)

    # 2. Déchiffrement en mémoire
    try:
        cipher = Fernet(MASTER_KEY)
        decrypted_hex = cipher.decrypt(encrypted_data).decode().strip()
    except Exception:
        print(f"./ft_otp: error: échec du déchiffrement de {filepath}", file=sys.stderr)
        sys.exit(1)

    # 3. Conversion de la chaîne hexadécimale en octets bruts
    try:
        key_bytes = bytes.fromhex(decrypted_hex)
    except ValueError:
        print("./ft_otp: error: la clé déchiffrée n'est pas un hexadécimal valide", file=sys.stderr)
        sys.exit(1)

    # 4. Calcul du compteur temporel (tranches de 30 secondes)
    counter = int(time.time()) // 30

    # 5. Génération et affichage strict (uniquement les 6 chiffres)
    code = generate_hotp(key_bytes, counter)
    print(code)

def main():
    parser = argparse.ArgumentParser(description="ft_otp - One-Time Password generator")

    # On crée un groupe mutuellement exclusif : l'utilisateur choisit -g OU -k
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", metavar="KEY_FILE", help="Enregistre et chiffre une clé de 64 caractères hex")
    group.add_argument("-k", metavar="ENCRYPTED_KEY", help="Génère un code OTP à partir de la clé chiffrée")

    args = parser.parse_args()

    if args.g:
        handle_save_key(args.g)
    elif args.k:
        handle_generate_otp(args.k)

if __name__ == "__main__":
    main()