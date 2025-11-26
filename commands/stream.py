from flask import Flask, Response
import cv2
import time
import subprocess

app = Flask(__name__)

def find_usb_camera():
    """Returns the /dev/videoX of the USB camera."""
    devices = subprocess.getoutput("v4l2-ctl --list-devices").split("\n")

    cam_index = None
    current_name = ""

    for line in devices:
        if line.endswith(":"):
            current_name = line.strip(":")
        elif "/dev/video" in line:
            dev = line.strip()
            # Avoid CSI cameras; only detect USB cams
            if "usb" in current_name.lower() or "camera" in current_name.lower():
                return dev

    return "/dev/video0"  # fallback


# Auto-detect camera
CAMERA_DEVICE = find_usb_camera()
print(f"? USB Camera detected at: {CAMERA_DEVICE}")

# OpenCV capture
cap = cv2.VideoCapture(CAMERA_DEVICE)

# Optional: set resolution & FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)


def generate_frames():
    """Real-time streaming generator."""
    while True:
        success, frame = cap.read()
        if not success:
            print("?? Frame read failed! Retrying...")
            time.sleep(0.1)
            continue

        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Stream frame
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
        )


@app.route('/video')
def video_feed():
    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/')
def index():
    return "<h2>USB Camera Streaming<br>Go to: <a href='/video'>/video</a></h2>"


if __name__ == '__main__':
    print("? Starting server at http://0.0.0.0:5000/video")
    app.run(host='0.0.0.0', port=5000)
