import cv2
import time
import requests
import subprocess

# ======================
# TELEGRAM BOT CONFIG
# ======================

BOT_TOKEN = "8587098263:AAEguz32JT32W7SdjzFWWOGnaGdZiRt5sV4"
CHAT_ID = "5322613212"   # <-- Replace with your number


# ======================
# AUTO-DETECT USB CAMERA
# ======================
def find_usb_camera():
    devices = subprocess.getoutput("v4l2-ctl --list-devices").split("\n")
    current_name = ""

    for line in devices:
        if line.endswith(":"):
            current_name = line.strip(":")
        elif "/dev/video" in line:
            dev = line.strip()
            # detect only USB cams
            if ("usb" in current_name.lower()) or ("camera" in current_name.lower()):
                return dev

    return "/dev/video0"   # fallback


# ======================
# CAPTURE IMAGE FUNCTION
# ======================
def capture_image():
    cam_device = find_usb_camera()
    print("📷 USB Camera detected at:", cam_device)

    cap = cv2.VideoCapture(cam_device, cv2.CAP_V4L2)
    time.sleep(1)

    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture image")
        return None

    filename = "capture.jpg"
    cv2.imwrite(filename, frame)
    cap.release()
    print("✅ Image captured:", filename)
    return filename


# ======================
# SEND PHOTO TO TELEGRAM
# ======================
def send_to_telegram(photo_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    with open(photo_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID}

        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("✅ Photo successfully sent to Telegram!")
        else:
            print("❌ Telegram Error:", response.text)


# ======================
# MAIN EXECUTION
# ======================
print("📸 Capturing image...")
photo = capture_image()

if photo:
    print("📩 Sending to Telegram...")
    send_to_telegram(photo)

