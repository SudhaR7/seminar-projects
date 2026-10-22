"""
PROJECT 4 — Password Guardian 🔐  (Simple Python, no external libraries)
- Checks how strong your password is
- Estimates how long a hacker needs to crack it
- Generates super-strong passwords & easy-to-remember passphrases
Run:  python password_guardian.py
"""
import math
import os
import secrets
import string

GREEN, YELLOW, RED, CYAN, BOLD, END = "\033[92m", "\033[93m", "\033[91m", "\033[96m", "\033[1m", "\033[0m"
os.system("")  # enables colours on Windows terminals
COMMON = {"123456", "password", "qwerty", "12345678", "111111", "iloveyou", "admin", "welcome", "abc123", "password123"}
WORDS = ["tiger", "mango", "rocket", "chennai", "laptop", "coffee", "planet", "dosa", "galaxy", "river",
         "python", "thunder", "silver", "jungle", "pixel", "cricket", "monsoon", "dragon", "ocean", "lotus"]


def crack_time(seconds):
    units = [("years", 31536000), ("days", 86400), ("hours", 3600), ("minutes", 60), ("seconds", 1)]
    if seconds > 31536000 * 1e6:
        return "millions of years 🦕"
    for name, sec in units:
        if seconds >= sec:
            return f"{seconds / sec:,.0f} {name}"
    return "instantly ⚡"


def check(pw):
    pool = 0
    tips = []
    if any(c.islower() for c in pw): pool += 26
    else: tips.append("add lowercase letters")
    if any(c.isupper() for c in pw): pool += 26
    else: tips.append("add UPPERCASE letters")
    if any(c.isdigit() for c in pw): pool += 10
    else: tips.append("add numbers")
    if any(c in string.punctuation for c in pw): pool += 32
    else: tips.append("add symbols like @ # $ !")
    if len(pw) < 12: tips.append("make it at least 12 characters")

    entropy = len(pw) * math.log2(pool) if pool else 0
    if pw.lower() in COMMON:
        entropy = 5
        tips.insert(0, "this is one of the MOST hacked passwords!")
    guesses_per_sec = 1e10  # a modern GPU cracking rig
    seconds = (2 ** entropy) / guesses_per_sec

    score = min(100, int(entropy * 1.25))
    color = RED if score < 40 else YELLOW if score < 70 else GREEN
    label = "WEAK 😱" if score < 40 else "MEDIUM 😐" if score < 70 else "STRONG 💪"
    bar = "█" * (score // 5) + "░" * (20 - score // 5)

    print(f"\n  Strength : {color}{bar} {score}/100  {label}{END}")
    print(f"  Entropy  : {entropy:.1f} bits")
    print(f"  Hacker needs about: {BOLD}{crack_time(seconds)}{END} to crack it")
    if tips:
        print(f"  {YELLOW}Tips:{END} " + ", ".join(tips))


def generate(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*?"
    while True:
        pw = "".join(secrets.choice(chars) for _ in range(length))
        if (any(c.islower() for c in pw) and any(c.isupper() for c in pw)
                and any(c.isdigit() for c in pw) and any(c in "!@#$%^&*?" for c in pw)):
            return pw


def passphrase(n=4):
    words = [secrets.choice(WORDS).capitalize() for _ in range(n)]
    return "-".join(words) + str(secrets.randbelow(90) + 10) + secrets.choice("!@#$")


def main():
    print(f"{CYAN}{BOLD}\n  ╔══════════════════════════════════╗\n  ║     🔐  PASSWORD  GUARDIAN  🔐    ║\n  ╚══════════════════════════════════╝{END}")
    while True:
        print("\n  1) Check my password\n  2) Generate a strong password\n  3) Generate an easy-to-remember passphrase\n  4) Exit")
        choice = input("  Choose: ").strip()
        if choice == "1":
            check(input("  Enter a password to test: "))
        elif choice == "2":
            n = input("  Length (default 16): ").strip()
            pw = generate(int(n) if n.isdigit() and int(n) >= 8 else 16)
            print(f"\n  {GREEN}{BOLD}{pw}{END}")
            check(pw)
        elif choice == "3":
            pw = passphrase()
            print(f"\n  {GREEN}{BOLD}{pw}{END}")
            check(pw)
        elif choice == "4":
            print("  Stay safe online! 👋")
            break
        else:
            print(f"  {RED}Invalid choice{END}")


if __name__ == "__main__":
    main()
