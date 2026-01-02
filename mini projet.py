import string
import random
from collections import Counter

alphabet = string.ascii_uppercase
english_frequency_order = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# --------------------------------------------------
# 1) Monoalphabetic Substitution Cipher
# --------------------------------------------------
def generate_key():
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def encrypt(plaintext, key):
    plaintext = plaintext.upper()
    ciphertext = ""
    for c in plaintext:
        if c in alphabet:
            ciphertext += key[c]
        else:
            ciphertext += c
    return ciphertext

# --------------------------------------------------
# 2) Frequency Analysis
# --------------------------------------------------
def frequency_analysis(ciphertext):
    freq = Counter(c for c in ciphertext if c in alphabet)
    total = sum(freq.values())
    return sorted(
        [(c, freq[c] / total) for c in freq],
        key=lambda x: x[1],
        reverse=True
    )

# --------------------------------------------------
# 3) Frequency Analysis Attack
# --------------------------------------------------
def generate_guess_key(freq_sorted):
    guessed_key = {}
    for i, (cipher_char, _) in enumerate(freq_sorted):
        if i < len(english_frequency_order):
            guessed_key[cipher_char] = english_frequency_order[i]
    return guessed_key

def decrypt(ciphertext, guessed_key):
    result = ""
    for c in ciphertext:
        if c in guessed_key:
            result += guessed_key[c]
        elif c in alphabet:
            result += "_"
        else:
            result += c
    return result

# --------------------------------------------------
# 4) Success Rate Evaluation
# --------------------------------------------------
def success_rate(original, decrypted):
    correct = 0
    total = 0
    for o, d in zip(original, decrypted):
        if o in alphabet:
            total += 1
            if o == d:
                correct += 1
    return (correct / total) * 100 if total > 0 else 0

# --------------------------------------------------
# 5) Experiments with Different Lengths
# --------------------------------------------------
sample_text = (
    "CRYPTOGRAPHY IS THE PRACTICE AND STUDY OF TECHNIQUES "
    "FOR SECURE COMMUNICATION IN THE PRESENCE OF ADVERSARIES "
) * 20  # make it long

lengths = [50, 100, 300, 600, 1000]

key = generate_key()

print("Message Length | Success Rate (%)")
print("----------------------------------")

for L in lengths:
    plaintext = sample_text[:L]
    ciphertext = encrypt(plaintext, key)

    freq_sorted = frequency_analysis(ciphertext)
    guessed_key = generate_guess_key(freq_sorted)
    decrypted = decrypt(ciphertext, guessed_key)

    rate = success_rate(plaintext, decrypted)
    print(f"{L:14} | {rate:.2f}")

