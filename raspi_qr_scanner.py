"""
Simple QR code scanner for Raspberry Pi 5 using OpenCV.

- Shows a live preview window from the default camera.
- Prints decoded QR code text to the console whenever a code is detected.
- Press "q" in the preview window to quit.

Dependencies:
    pip install opencv-python
"""
import sys
from typing import Optional

import cv2


def draw_bounding_box(frame, points):
    """Draw a bounding box around detected QR code points."""
    for i in range(4):
        start_point = tuple(points[i][0].astype(int))
        end_point = tuple(points[(i + 1) % 4][0].astype(int))
        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)


def main() -> int:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open camera 0. Check that the camera is connected and accessible.")
        return 1

    detector = cv2.QRCodeDetector()
    last_text: Optional[str] = None

    print("Press 'q' in the video window to exit.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from camera.")
            break

        data, points, _ = detector.detectAndDecode(frame)
        if points is not None:
            draw_bounding_box(frame, points)
            if data and data != last_text:
                print(f"Detected QR text: {data}")
                last_text = data

        cv2.imshow("QR Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == "__main__":
    sys.exit(main())
