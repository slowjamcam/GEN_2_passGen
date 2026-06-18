"""
Simple plaintext password export helper.

WARNING: This writes secrets in cleartext. Use only for temporary/simple workflows.
"""

from __future__ import annotations

import os
import csv
from datetime import datetime


def append_plaintext_entry(
    title: str,
    username: str,
    password: str,
    notes: str = "",
    path: str = "stored_passwords.csv",
) -> None:
    """
    Append a CSV record to `path`. Creates parent directories if needed.
    CSV columns: timestamp_iso, title, username, password, notes
    """
    # Ensure directory exists if a directory was provided
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    file_exists = os.path.exists(path)
    # Open in append mode and write a header if file did not exist
    with open(path, "a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if not file_exists:
            writer.writerow(["timestamp", "title", "username", "password", "notes"])
        writer.writerow([
            datetime.utcnow().isoformat() + "Z",
            title,
            username,
            password,
            notes,
        ])


def append_plaintext_file(
    title: str,
    username: str,
    password: str,
    notes: str = "",
    path: str = "stored_passwords.txt",
) -> None:
    """
    Append a simple human-readable plaintext entry to `path`.

    Each entry is separated by a line of dashes and includes a UTC timestamp.
    """
    # Ensure directory exists if a directory was provided
    dirpath = os.path.dirname(path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    entry_lines = [
        "-----",
        f"timestamp: {datetime.utcnow().isoformat()}Z",
        f"title: {title}",
        f"username: {username}",
        f"password: {password}",
    ]
    if notes:
        entry_lines.append(f"notes: {notes}")
    entry_lines.append("\n")

    # Append the entry
    with open(path, "a", encoding="utf-8") as fh:
        fh.write("\n".join(entry_lines))


