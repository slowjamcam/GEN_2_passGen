"""Simple Tkinter GUI for the PasswordGen2 project.

Provides a minimal interface to generate passwords (using GEN_G2.generate_password),
validate a user-supplied password (using GEN_G2.validate_password), copy to clipboard,
and save entries to the plaintext CSV store (plaintext_store.append_plaintext_entry).

Run: python gui.py
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import sys

# Reuse existing generator/validator and storage helpers
from GEN_G2 import generate_password, validate_password
from plaintext_store import append_plaintext_entry


class PasswordGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("PasswordGen2 - Simple GUI")
        self.resizable(False, False)
        self._show_password = False
        self._build()

    def _build(self) -> None:
        # Create notebook (tabs)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        # Tab 1: Password Generator
        gen_frame = ttk.Frame(notebook, padding=8)
        notebook.add(gen_frame, text="Generator")
        self._build_generator_tab(gen_frame)

        # Tab 2: Saved Passwords
        saved_frame = ttk.Frame(notebook, padding=8)
        notebook.add(saved_frame, text="Saved Passwords")
        self._build_saved_tab(saved_frame)

    def _build_generator_tab(self, parent: ttk.Frame) -> None:
        """Build the password generator tab."""
        frm = parent

        # Title
        ttk.Label(frm, text="Title / Site:").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.title_var, width=40).grid(row=0, column=1, columnspan=3, sticky="w")

        # Username
        ttk.Label(frm, text="Username:").grid(row=1, column=0, sticky="w")
        self.user_var = tk.StringVar()
        ttk.Entry(frm, textvariable=self.user_var, width=40).grid(row=1, column=1, columnspan=3, sticky="w")

        # Password field
        ttk.Label(frm, text="Password:").grid(row=2, column=0, sticky="w")
        self.pw_var = tk.StringVar()
        # Keep a direct reference to the Entry so toggling show/hide is simple
        self.pw_entry = ttk.Entry(frm, textvariable=self.pw_var, width=40, show="*")
        self.pw_entry.grid(row=2, column=1, columnspan=2, sticky="w")
        ttk.Button(frm, text="Show", command=self._toggle_show).grid(row=2, column=3)

        # Controls: length and difficulty
        ttk.Label(frm, text="Length:").grid(row=3, column=0, sticky="w")
        self.len_var = tk.IntVar(value=16)
        ttk.Spinbox(frm, from_=6, to=128, textvariable=self.len_var, width=6).grid(row=3, column=1, sticky="w")

        ttk.Label(frm, text="Difficulty:").grid(row=3, column=2, sticky="w")
        self.diff_var = tk.StringVar(value="medium")
        ttk.Combobox(frm, textvariable=self.diff_var, values=["easy", "medium", "hard", "very hard"], width=10, state="readonly").grid(row=3, column=3, sticky="w")

        # Notes
        ttk.Label(frm, text="Notes:").grid(row=4, column=0, sticky="nw")
        self.notes = tk.Text(frm, width=50, height=4)
        self.notes.grid(row=4, column=1, columnspan=3, sticky="w")

        # Action buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=5, column=0, columnspan=4, pady=(6, 0), sticky="w")

        ttk.Button(btn_frame, text="Generate", command=self.on_generate).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Validate", command=self.on_validate).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Copy", command=self.on_copy).grid(row=0, column=2, padx=4)
        ttk.Button(btn_frame, text="Save", command=self.on_save).grid(row=0, column=3, padx=4)
        ttk.Button(btn_frame, text="Quit", command=self.destroy).grid(row=0, column=4, padx=4)

    def _build_saved_tab(self, parent: ttk.Frame) -> None:
        """Build the saved passwords display tab."""
        frm = parent

        # Create Treeview with columns
        columns = ("Title", "Username", "Password", "Notes", "Timestamp")
        self.tree = ttk.Treeview(frm, columns=columns, height=20, show="headings")

        # Define column headings and widths
        self.tree.column("Title", width=100, anchor="w")
        self.tree.column("Username", width=100, anchor="w")
        self.tree.column("Password", width=150, anchor="w")
        self.tree.column("Notes", width=100, anchor="w")
        self.tree.column("Timestamp", width=150, anchor="w")

        for col in columns:
            self.tree.heading(col, text=col)

        # Add scrollbars
        scroll_y = ttk.Scrollbar(frm, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(frm, orient="horizontal", command=self.tree.xview)
        self.tree.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        # Layout
        self.tree.grid(row=0, column=0, columnspan=3, sticky="nsew")
        scroll_y.grid(row=0, column=3, sticky="ns")
        scroll_x.grid(row=1, column=0, columnspan=3, sticky="ew")

        frm.grid_rowconfigure(0, weight=1)
        frm.grid_columnconfigure(0, weight=1)

        # Control buttons
        btn_frame = ttk.Frame(frm)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=(6, 0), sticky="w")

        ttk.Button(btn_frame, text="Refresh", command=self.on_refresh_saved).grid(row=0, column=0, padx=4)
        ttk.Button(btn_frame, text="Delete Selected", command=self.on_delete_selected).grid(row=0, column=1, padx=4)
        ttk.Button(btn_frame, text="Copy Password", command=self.on_copy_from_tree).grid(row=0, column=2, padx=4)

        # Load initial data
        self.on_refresh_saved()

    def _toggle_show(self) -> None:
        # Toggle password entry visibility using the stored entry reference
        if self._show_password:
            self.pw_entry.config(show="*")
            self._show_password = False
        else:
            self.pw_entry.config(show="")
            self._show_password = True

    def on_refresh_saved(self) -> None:
        """Load and display saved passwords from CSV."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        csv_path = "stored_passwords.csv"
        if not os.path.exists(csv_path):
            return

        try:
            with open(csv_path, "r", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    if row:
                        title = row.get("title", "")
                        username = row.get("username", "")
                        password = row.get("password", "")
                        notes = row.get("notes", "")
                        timestamp = row.get("timestamp", "")
                        self.tree.insert("", "end", values=(title, username, password, notes, timestamp))
        except Exception as exc:
            messagebox.showerror("Load failed", f"Failed to load passwords: {exc}")

    def on_delete_selected(self) -> None:
        """Delete the selected row from the Treeview and CSV file."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a row to delete.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        if not values:
            return

        title, username, password, notes, timestamp = values

        # Confirm deletion
        if not messagebox.askyesno("Confirm Delete", f"Delete entry for '{title}' / '{username}'?"):
            return

        # Remove from Treeview
        self.tree.delete(item)

        # Remove from CSV file
        csv_path = "stored_passwords.csv"
        try:
            rows = []
            with open(csv_path, "r", encoding="utf-8") as fh:
                reader = csv.DictReader(fh)
                for row in reader:
                    if not (row.get("title") == title and row.get("username") == username and row.get("password") == password):
                        rows.append(row)

            # Write back (excluding the deleted row)
            with open(csv_path, "w", encoding="utf-8", newline="") as fh:
                if rows:
                    writer = csv.DictWriter(fh, fieldnames=["timestamp", "title", "username", "password", "notes"])
                    writer.writeheader()
                    writer.writerows(rows)
            messagebox.showinfo("Deleted", "Entry deleted successfully.")
        except Exception as exc:
            messagebox.showerror("Delete failed", f"Failed to delete entry: {exc}")

    def on_copy_from_tree(self) -> None:
        """Copy the password of the selected row to clipboard."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a row.")
            return

        item = selected[0]
        values = self.tree.item(item, "values")
        if not values or len(values) < 3:
            messagebox.showwarning("No password", "Could not find password in row.")
            return

        password = values[2]  # Password is the third column
        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def on_generate(self) -> None:
        try:
            length = int(self.len_var.get())
        except Exception:
            messagebox.showerror("Invalid length", "Please enter a valid integer length.")
            return
        diff = self.diff_var.get() or "medium"
        try:
            pw = generate_password(length, diff)
        except Exception as exc:
            messagebox.showerror("Generation error", str(exc))
            return
        self.pw_var.set(pw)

    def on_validate(self) -> None:
        pw = self.pw_var.get() or ""
        valid, missing = validate_password(pw)
        if valid:
            messagebox.showinfo("Valid", "Password meets the basic requirements.")
        else:
            messagebox.showwarning("Invalid", "Missing: " + ", ".join(missing))

    def on_copy(self) -> None:
        pw = self.pw_var.get() or ""
        if not pw:
            messagebox.showwarning("No password", "Nothing to copy.")
            return
        self.clipboard_clear()
        self.clipboard_append(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def on_save(self) -> None:
        title = self.title_var.get() or "(no title)"
        username = self.user_var.get() or ""
        password = self.pw_var.get() or ""
        notes = self.notes.get("1.0", "end").strip()
        if not password:
            messagebox.showwarning("No password", "There is no password to save.")
            return
        try:
            append_plaintext_entry(title=title, username=username, password=password, notes=notes)
            messagebox.showinfo("Saved", "Saved to stored_passwords.csv (plaintext, not secure).")
            # Refresh the saved passwords tab
            self.on_refresh_saved()
        except Exception as exc:
            messagebox.showerror("Save failed", f"Failed to save: {exc}")


def main() -> None:
    app = PasswordGUI()
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Cancelled by user.")
        sys.exit(1)

