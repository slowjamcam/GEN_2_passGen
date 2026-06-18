"""
Password generator script.

Behavior:
 - Ask user if they want to supply their own password. If yes, validate it meets requirements
   (at least one uppercase, one lowercase, at least two digits, and at least one special char).
 - If user chooses not to supply their own password, ask for a minimum character requirement
   and then the requested character amount (requested must be >= minimum and must accommodate
   mandatory character types).
 - Ask desired difficulty: Easy, Medium, Hard, or Very Hard. All passwords always include at least
   1 uppercase, 1 lowercase, 2 digits and special characters. For Hard/Very Hard the generator
   will use a larger set of special characters and require more special characters.

Run: python GEN_G2.py
"""

from __future__ import annotations

from plaintext_store import append_plaintext_entry, append_plaintext_file

import random
import string
import sys



def prompt_yes_no(prompt: str) -> bool:
    while True:
        resp = input(prompt + " [y/n]: ").strip().lower()
        if resp in ("y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


""" NOT USED
def prompt_choice(prompt: str, choices: list[str]) -> str:
    choices_lower = [c.lower() for c in choices]
    while True:
        resp = input(f"{prompt} ({'/'.join(choices)}): ").strip().lower()
        if resp in choices_lower:
            return resp
        print(f"Please choose one of: {', '.join(choices)}")
"""

def prompt_int(prompt: str, min_value: int = 1) -> int:
    while True:
        try:
            val = int(input(prompt + ": ").strip())
            if val < min_value:
                print(f"Please enter an integer >= {min_value}.")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")


def validate_password(pw: str, min_special: int = 1) -> tuple[bool, list[str]]:
    """Return (is_valid, list_of_missing_requirements)"""
    missing = []
    if not any(c.isupper() for c in pw):
        missing.append("at least one uppercase letter")
    if not any(c.islower() for c in pw):
        missing.append("at least one lowercase letter")
    digits = sum(c.isdigit() for c in pw)
    if digits < 2:
        missing.append("at least two digits")
    special_count = sum(not c.isalnum() for c in pw)
    if special_count < min_special:
        missing.append(f"at least {min_special} special character(s)")
    return (len(missing) == 0, missing)


def generate_password(length: int, difficulty: str) -> str:
    """Generate a password of given length and difficulty.

    difficulty: easy, medium, hard, very hard (lowercase accepted)
    Returns generated password (string).
    """
    rnd = random.SystemRandom()

    # character pools
    uppers = string.ascii_uppercase
    lowers = string.ascii_lowercase
    digits = string.digits
    base_special = "!@#$%&*?"
    extra_special = "-_=+[]{};:,.<>/\\|`~"

    # accept numeric or textual difficulty
    d = str(difficulty).strip().lower()
    if d in ("1", "easy", "e"):
        mode = "easy"
    elif d in ("2", "medium", "m"):
        mode = "medium"
    elif d in ("3", "hard", "h"):
        mode = "hard"
    elif d in ("4", "very hard", "veryhard", "very", "v", "very_hard"):
        mode = "very hard"
    else:
        mode = d

    if mode == "easy":
        min_special = 1
        specials = base_special
    elif mode == "medium":
        min_special = 1
        specials = base_special + extra_special[:6]
    elif mode == "hard":
        min_special = 2
        specials = base_special + extra_special
    elif mode == "very hard":
        min_special = 3
        specials = base_special + extra_special
    else:
        min_special = 1
        specials = base_special + extra_special[:6]

    # enforce mandatory counts
    mandatory = []
    mandatory.append(rnd.choice(uppers))
    mandatory.append(rnd.choice(lowers))
    # two digits
    mandatory.extend(rnd.choice(digits) for _ in range(2))
    # required special characters
    mandatory.extend(rnd.choice(specials) for _ in range(min_special))

    remaining_len = length - len(mandatory)
    if remaining_len < 0:
        raise ValueError("Requested length too small for the mandatory character requirements.")

    all_pool = uppers + lowers + digits + specials
    password_chars = mandatory + [rnd.choice(all_pool) for _ in range(remaining_len)]
    rnd.shuffle(password_chars)
    return "".join(password_chars)


def main() -> None:
    print("Password Generator")

    use_own = prompt_yes_no("Do you want to supply your own password?")

    if use_own:
        min_special = 1
        # difficulty still affects validation threshold for special characters
        sel = input("Choose difficulty (1-Easy,2-Medium,3-Hard,4-Very Hard): ").strip().lower()
        map_mode = {"1": "easy", "2": "medium", "3": "hard", "4": "very hard"}
        diff = map_mode.get(sel, sel)
        if diff == "hard":
            min_special = 2
        elif diff.startswith("very"):
            min_special = 3

        while True:
            pw = input("Enter your password: ")
            valid, missing = validate_password(pw, min_special=min_special)
            if valid:
                print("Your password is valid and accepted.")
                print("Generated/Accepted password: ", pw)

                # Collect metadata once
                t_title = input("Title / site name: ").strip() or "(no title)"
                t_user = input("Username: ").strip()
                t_notes = input("Notes (optional): ").strip()

                # Offer to save plaintext CSV copy
                if prompt_yes_no("Save this password to a CSV file? (not secure)"):
                    file_path = input("Enter filename (default: stored_passwords.csv): ").strip() or "stored_passwords.csv"
                    try:
                        append_plaintext_entry(title=t_title, username=t_user, password=pw, notes=t_notes, path=file_path)
                        print(f"Appended CSV entry to {file_path}")
                    except Exception as exc:
                        print("Failed to write CSV file:", exc)

                # Offer to save to a simple plaintext file as well
                if prompt_yes_no("Also save this password to a plain text file? (not secure)"):
                    txt_path = input("Enter filename (default: stored_passwords.txt): ").strip() or "stored_passwords.txt"
                    try:
                        append_plaintext_file(title=t_title, username=t_user, password=pw, notes=t_notes, path=txt_path)
                        print(f"Appended plaintext entry to {txt_path}")
                    except Exception as exc:
                        print("Failed to write plaintext file:", exc)

                return
            print("Password is missing the following requirements:")
            for m in missing:
                print(" - ", m)
            if not prompt_yes_no("Try again with another password?"):
                print("Exiting without accepting a password.")
                return

    # User wants generator
    print("We'll generate a password for you.")
    minimum = prompt_int("Enter the minimum character requirement", min_value=4)
    while True:
        requested = prompt_int("Enter the requested character amount", min_value=minimum)
        # ask difficulty (accept number or word)
        sel = input("Choose difficulty (1-Easy,2-Medium,3-Hard,4-Very Hard): ").strip().lower()
        map_mode = {"1": "easy", "2": "medium", "3": "hard", "4": "very hard"}
        difficulty = map_mode.get(sel, sel)

        # determine min special count for difficulty
        min_special = 1
        if difficulty == "hard":
            min_special = 2
        elif difficulty.startswith("very"):
            min_special = 3

        required_min_len = 1 + 1 + 2 + min_special  # upper + lower + two digits + specials
        if requested < required_min_len:
            print(f"Requested length is too small for the chosen difficulty. Minimum required is {required_min_len}.")
            if not prompt_yes_no("Try entering lengths/difficulty again?"):
                print("Aborting.")
                return
            continue

        # generate
        pw = generate_password(requested, difficulty)
        print("Generated password:", pw)

        # Collect metadata once
        t_title = input("Title / site name: ").strip() or "(no title)"
        t_user = input("Username: ").strip()
        t_notes = input("Notes (optional): ").strip()

        # Offer to save to a CSV file (vault disabled)
        if prompt_yes_no("Save this password to a CSV file? (not secure)"):
            file_path = input("Enter filename (default: stored_passwords.csv): ").strip() or "stored_passwords.csv"
            try:
                append_plaintext_entry(title=t_title, username=t_user, password=pw, notes=t_notes, path=file_path)
                print(f"Appended CSV entry to {file_path}")
            except Exception as exc:
                print("Failed to write CSV file:", exc)

        # Offer to save to a simple plaintext file as well
        if prompt_yes_no("Also save this password to a plain text file? (not secure)"):
            txt_path = input("Enter filename (default: stored_passwords.txt): ").strip() or "stored_passwords.txt"
            try:
                append_plaintext_file(title=t_title, username=t_user, password=pw, notes=t_notes, path=txt_path)
                print(f"Appended plaintext entry to {txt_path}")
            except Exception as exc:
                print("Failed to write plaintext file:", exc)

        return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(1)
