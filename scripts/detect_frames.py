import cv2
import numpy as np

img = cv2.imread('static/img/museum_gallery.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# The canvases inside the frames are very bright/white.
_, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

frames = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    # The frames should be of a certain size
    if 2000 < w*h < 50000 and 0.5 < w/h < 1.5:
        # Also ensure it's not the ceiling light (y > 100)
        if y > 100:
            frames.append((x, y, w, h))

print(f"Found {len(frames)} frames: {frames}")
