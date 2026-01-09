import cv2
import numpy as np

# Create 500x500 pixel square
img = np.zeros((500, 500, 3), dtype=np.uint8)

# Draw a white square border
img[50:450, 50:450] = [255, 255, 255]
img[100:400, 100:400] = [0, 0, 0]

# Add a circle to verify
cv2.circle(img, (250, 250), 150, (255, 0, 0), 5)

# Add horizontal and vertical lines through center
cv2.line(img, (0, 250), (500, 250), (0, 255, 0), 2)
cv2.line(img, (250, 0), (250, 500), (0, 255, 0), 2)

cv2.imwrite('test_square.png', img)
print("Created test_square.png")
