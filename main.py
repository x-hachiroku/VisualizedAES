from aes import AES

import cv2
import numpy as np
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import ttk

def cv2tk(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    img = cv2.resize(img, (350, 350))
    img = Image.fromarray(img, 'RGBA')
    return ImageTk.PhotoImage(img)

def encrypt():
    global ciphertext, ciphertext_bytes, ciphertext_tk
    key_length = int(key_length_val.get())
    keystr = key_val.get()
    if keystr == "00...00":
        key = b'\x00' * (key_length // 8)
    elif keystr == "ff...ff":
        key = b'\xff' * (key_length // 8)
    elif keystr == "aa...aa":
        key = b'\xaa' * (key_length // 8)
    else:
        with open('/dev/urandom', 'rb') as f:
            key = f.read(key_length // 8)

    ivstr = iv_val.get()
    if ivstr == "00...00":
        iv = b'\x00' * 16
    elif ivstr == "ff...ff":
        iv = b'\xff' * 16
    elif ivstr == "aa...aa":
        iv = b'\xaa' * 16
    else:
        with open('/dev/urandom', 'rb') as f:
            iv = f.read(16)

    rounds = int(rounds_val.get())
    no_sub_bytes = no_sub_bytes_val.get()
    no_shift_rows = no_shift_rows_val.get()
    no_mix_columns = no_mix_columns_val.get()

    aes = AES(key, iv, rounds, no_sub_bytes, no_shift_rows, no_mix_columns)

    if op_mode_val.get() == "ECB":
        encrypt = aes.encrypt_ecb
        decrypt = aes.decrypt_ecb
    elif op_mode_val.get() == "CBC":
        encrypt = aes.encrypt_cbc
        decrypt = aes.decrypt_cbc
    elif op_mode_val.get() == "CTR":
        encrypt = aes.encrypt_ctr
        decrypt = aes.decrypt_ctr

    if direction_val.get() == "Decrypt":
        encrypt = decrypt

    ciphertext_bytes = encrypt(plaintext.tobytes())
    ciphertext = np.frombuffer(ciphertext_bytes, dtype=np.uint8).reshape(plaintext.shape)
    ciphertext_tk = cv2tk(ciphertext)

    cipher_label.configure(image=ciphertext_tk)
    cipher_label.image = ciphertext_tk

def send_to_input():
    global plaintext
    plaintext = ciphertext
    plaintext_label.configure(image=ciphertext_tk)
    plaintext_label.image = ciphertext_tk


def source_cb(*args):
    global plaintext
    if source_val.get() == "Tippy":
        plaintext = np.copy(tippy)
    elif source_val.get() == "Mari":
        plaintext = np.copy(mari)
    elif source_val.get() == "White":
        plaintext = np.ones((128, 128, 4), dtype=np.uint8) * 255
    elif source_val.get() == "Black":
        plaintext = np.zeros((128, 128, 4), dtype=np.uint8)
        plaintext[:, :, 3] = 255

    plaintext_tk = cv2tk(plaintext)
    plaintext_label.configure(image=plaintext_tk)
    plaintext_label.image = plaintext_tk



tippy = cv2.imread('./tippy.png', cv2.IMREAD_UNCHANGED)
mari = cv2.imread('./mari.png', cv2.IMREAD_UNCHANGED)

root = tk.Tk()
root.title("Visualized AES")
root.geometry("1080x350")
main_frame = tk.Frame(root)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)
main_frame.pack()

plaintext_frame = tk.Frame(main_frame)
plaintext_frame.grid(row=0, column=0, sticky=tk.E)

menu_frame = tk.Frame(main_frame)
menu_frame.grid(row=0, column=1)

cipher_frame = tk.Frame(main_frame)
cipher_frame.grid(row=0, column=2, sticky=tk.W)

plaintext = np.copy(tippy)
plaintext_tk = cv2tk(plaintext)
plaintext_label = tk.Label(plaintext_frame, image=plaintext_tk)
plaintext_label.pack()

ciphertext = np.copy(tippy)
ciphertext_tk = cv2tk(plaintext)
cipher_label = tk.Label(cipher_frame, image=ciphertext_tk)
cipher_label.pack()


menu_frame.columnconfigure(0, weight=2)
menu_frame.columnconfigure(1, weight=3)
menu_frame.rowconfigure(0, weight=1)
menu_frame.rowconfigure(1, weight=1)
menu_frame.rowconfigure(2, weight=1)
menu_frame.rowconfigure(3, weight=1)
menu_frame.rowconfigure(4, weight=1)
menu_frame.rowconfigure(5, weight=1)
menu_frame.rowconfigure(6, weight=1)
menu_frame.rowconfigure(7, weight=1)
menu_frame.rowconfigure(8, weight=1)
menu_frame.rowconfigure(9, weight=1)
menu_frame.rowconfigure(10, weight=1)

source_label = tk.Label(menu_frame, text="Input:").grid(row=0, column=0)
source_val = tk.StringVar(value="Tippy")
source_val.trace_add('write', source_cb)
source_entry = ttk.OptionMenu(menu_frame, source_val, "Tippy", "Tippy", "Mari", "White", "Black").grid(row=0, column=1)

direction_label = tk.Label(menu_frame, text="Direction:").grid(row=1, column=0)
direction_val = tk.StringVar(value="Encrypt")
direction_entry = ttk.OptionMenu(menu_frame, direction_val, "Encrypt", "Encrypt", "Decrypt").grid(row=1, column=1)

op_mode_label = tk.Label(menu_frame, text="Operation Mode:").grid(row=3, column=0)
op_mode_val = tk.StringVar(value="ECB")
op_mode_entry = ttk.OptionMenu(menu_frame, op_mode_val, "ECB", "ECB", "CBC", "CTR").grid(row=3, column=1)

key_length_label = tk.Label(menu_frame, text="Key Length:").grid(row=4, column=0)
key_length_val = tk.StringVar(value="128")
key_length_entry = ttk.OptionMenu(menu_frame, key_length_val, "128", "128", "192", "256").grid(row=4, column=1)

rounds_label = tk.Label(menu_frame, text="rounds:").grid(row=5, column=0)
rounds_val = tk.StringVar(value="10")
rounds_entry = ttk.Entry(menu_frame, textvariable=rounds_val).grid(row=5, column=1)

key_label = tk.Label(menu_frame, text="Key:").grid(row=6, column=0)
key_val = tk.StringVar(value="00...00")
key_entry = ttk.OptionMenu(menu_frame, key_val, "00...00", "ff...ff", "aa...aa", "Random").grid(row=6, column=1)

iv_label = tk.Label(menu_frame, text="IV:").grid(row=7, column=0)
iv_val = tk.StringVar(value="00...00")
iv_entry = ttk.OptionMenu(menu_frame, iv_val, "00...00", "ff...ff", "aa...aa", "Random").grid(row=7, column=1)

no_sub_bytes_label = tk.Label(menu_frame, text="Disable S-Box:").grid(row=8, column=0)
no_sub_bytes_val = tk.BooleanVar(value=False)
no_sub_bytes_entry = ttk.Checkbutton(menu_frame, variable=no_sub_bytes_val).grid(row=8, column=1)

no_shift_rows_label = tk.Label(menu_frame, text="Disable Shift Rows:").grid(row=9, column=0)
no_shift_rows_val = tk.BooleanVar(value=False)
no_shift_rows_entry = ttk.Checkbutton(menu_frame, variable=no_shift_rows_val).grid(row=9, column=1)

no_mix_columns_label = tk.Label(menu_frame, text="Disable Mix Columns:").grid(row=10, column=0)
no_mix_columns_val = tk.BooleanVar(value=False)
no_mix_columns_entry = ttk.Checkbutton(menu_frame, variable=no_mix_columns_val).grid(row=10, column=1)

encrypt_button = tk.Button(menu_frame, text="Run", command=encrypt).grid(row=11, column=0)

send_button = tk.Button(menu_frame, text="Send to Input", command=send_to_input).grid(row=11, column=1)

main_frame.mainloop()
