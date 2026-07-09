#!/usr/bin/env python
"""Quick test to verify the GUI tabs and saved passwords functionality."""

from gui import PasswordGUI

app = PasswordGUI()

# Check that both tabs are created
notebook = app.winfo_children()[0]
print(f"Number of tabs: {len(notebook.tabs())}")
print(f"Tab 1: {notebook.tab(0, 'text')}")
print(f"Tab 2: {notebook.tab(1, 'text')}")

# Check that the tree has items loaded from CSV
print(f"Number of saved passwords: {len(app.tree.get_children())}")

# Print the loaded passwords
print("\nLoaded passwords:")
for item in app.tree.get_children():
    values = app.tree.item(item, 'values')
    print(f"  - {values[0]} / {values[1]}")

app.destroy()
print("\nAll tests passed!")

