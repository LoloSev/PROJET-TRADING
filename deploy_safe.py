#!/usr/bin/env python3
import pyautogui
import time
import subprocess
import sys

# Get the script name from command line argument
script_name = sys.argv[1] if len(sys.argv) > 1 else "LOLO_SWING_M15.pine"
script_path = rf'C:\Users\Laurent\Desktop\PROJET TRADING\{script_name}'

# Read the Pine Script code
with open(script_path, 'r', encoding='utf-8') as f:
    pine_code = f.read()

print(f"[OK] Code read from {script_name}")

# Copy to clipboard using pyperclip
try:
    import pyperclip
    pyperclip.copy(pine_code)
    print("[OK] Code copied to clipboard")
except ImportError:
    process = subprocess.Popen('clip', stdin=subprocess.PIPE)
    process.communicate(pine_code.encode('utf-8'))
    print("[OK] Code copied via clip")

time.sleep(1)

# CRITICAL: Click deep inside the Pine Editor text area (not near edges)
# Pine Editor is usually on the RIGHT side, centered vertically
print("[ACTION] Clicking INSIDE Pine Editor text area...")
pyautogui.click(1100, 400)  # Click in the middle of the editor area (right side)
time.sleep(0.5)

# Click again to ensure focus
pyautogui.click(1100, 400)
time.sleep(0.3)

# Select all
print("[ACTION] Selecting all text...")
pyautogui.hotkey('ctrl', 'a')
time.sleep(0.3)

# Paste
print("[ACTION] Pasting code...")
pyautogui.hotkey('ctrl', 'v')
time.sleep(1.5)

# Save
print("[ACTION] Saving...")
pyautogui.hotkey('ctrl', 's')
time.sleep(2)

print(f"[OK] {script_name} deployed to Pine Editor")
