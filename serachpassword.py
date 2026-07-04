import csv
import os


def searchPasswords(path: str = "stored_passwords.csv") -> None:
    """Prompt for a search term and print any CSV entries where the username or notes
    (or title) contain the term (case-insensitive).
    """
    if not os.path.exists(path):
        print(f"No CSV file found at {path}.")
        return

    term = input("Enter search term (searches title, username, notes): ").strip()
    if not term:
        print("Empty search term; aborting.")
        return

    term_low = term.lower()
    matches = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                # Normalize missing keys
                title = (row.get("title") or "").lower()
                username = (row.get("username") or "").lower()
                notes = (row.get("notes") or "").lower()
                if term_low in username or term_low in notes or term_low in title:
                    matches.append(row)
    except Exception as exc:
        print("Failed to read CSV file:", exc)
        return

    if not matches:
        print("No matches found.")
        return

    print(f"Found {len(matches)} match(es):")
    for i, m in enumerate(matches, start=1):
        ts = m.get("timestamp", "(no timestamp)")
        title = m.get("title", "(no title)")
        username = m.get("username", "(no username)")
        password = m.get("password", "(no password)")
        notes = m.get("notes", "")
        print("----")
        print(f"#{i} timestamp: {ts}")
        print(f" title: {title}")
        print(f" username: {username}")
        print(f" password: {password}")
        if notes:
            print(f" notes: {notes}")