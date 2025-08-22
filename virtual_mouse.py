import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

# -----------------------------
# Initialize MediaPipe Hands for hand tracking
# -----------------------------
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)  # Track only one hand at a time
mpDraw = mp.solutions.drawing_utils  # Utility to draw hand landmarks

# -----------------------------
# Get screen resolution for cursor mapping
# -----------------------------
screen_w, screen_h = pyautogui.size()

# -----------------------------
# Webcam setup
# -----------------------------
cap = cv2.VideoCapture(0)  # Use default webcam
cap.set(3, 640)  # Set frame width
cap.set(4, 480)  # Set frame height

# -----------------------------
# Variables for smooth cursor movement
# -----------------------------
plocX, plocY = 0, 0  # Previous cursor coordinates
clocX, clocY = 0, 0  # Current cursor coordinates
smoothening = 15      # Higher value slows cursor movement for stability

# -----------------------------
# Active area margin to prevent cursor going outside frame
# -----------------------------
frame_margin = 100

# -----------------------------
# Gesture cooldown timers
# -----------------------------
click_cooldown = 0
scroll_cooldown = 0

# -----------------------------
# Fingertip landmark IDs for thumb, index, middle, ring, pinky
# -----------------------------
tip_ids = [4, 8, 12, 16, 20]

# -----------------------------
# Function to detect which fingers are up
# Returns list: [thumb, index, middle, ring, pinky]
# -----------------------------
def get_finger_status(lmList):
    fingers = []
    # Thumb: check horizontal position relative to previous joint
    fingers.append(lmList[tip_ids[0]][0] < lmList[tip_ids[0] - 1][0])
    # Other fingers: check vertical position relative to previous joint
    for i in range(1, 5):
        fingers.append(lmList[tip_ids[i]][1] < lmList[tip_ids[i] - 2][1])
    return fingers

# -----------------------------
# Main loop: capture frames and process gestures
# -----------------------------
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Mirror image for natural movement
    h, w, _ = img.shape

    # Default values for gesture display
    color_box = (255, 0, 255)
    gesture_text = ""

    # Draw boundary rectangle to define active area
    cv2.rectangle(img, (frame_margin, frame_margin), (w - frame_margin, h - frame_margin), color_box, 3)

    # Convert frame to RGB for MediaPipe processing
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    # -----------------------------
    # If hand landmarks are detected
    # -----------------------------
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lmList = []
            # Extract pixel coordinates of landmarks
            for id, lm in enumerate(handLms.landmark):
                px, py = int(lm.x * w), int(lm.y * h)
                lmList.append((px, py))

            # Draw landmarks and connections on the frame
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

            if lmList:
                fingers = get_finger_status(lmList)
                fingers_up = fingers.count(True)  # Number of fingers extended

                # Draw circles on tips of fingers that are up
                for i, tip_id in enumerate(tip_ids):
                    if fingers[i]:
                        x, y = lmList[tip_id]
                        cv2.circle(img, (x, y), 10, (0, 255, 255), cv2.FILLED)

                # -----------------------------
                # Move cursor if only index finger is up
                # -----------------------------
                if fingers_up == 1 and fingers[1]:
                    x1, y1 = lmList[8]  # Index fingertip coordinates
                    # Map coordinates from camera frame to screen size
                    x3 = np.interp(x1, (frame_margin, w - frame_margin), (0, screen_w))
                    y3 = np.interp(y1, (frame_margin, h - frame_margin), (0, screen_h))

                    # Smooth cursor movement
                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening
                    pyautogui.moveTo(clocX, clocY)
                    plocX, plocY = clocX, clocY

                    gesture_text = "Moving Mouse"
                    color_box = (0, 255, 0)
                    click_cooldown = 0
                    scroll_cooldown = 0

                # -----------------------------
                # Left click gesture: index + middle fingers
                # -----------------------------
                elif fingers_up == 2 and fingers[1] and fingers[2]:
                    if click_cooldown == 0:
                        pyautogui.click()
                        gesture_text = "Left Click"
                        color_box = (255, 0, 0)
                        click_cooldown = 20  # Set cooldown to avoid multiple clicks

                # -----------------------------
                # Right click gesture: index + middle + ring fingers
                # -----------------------------
                elif fingers_up == 3 and fingers[1] and fingers[2] and fingers[3]:
                    if click_cooldown == 0:
                        pyautogui.rightClick()
                        gesture_text = "Right Click"
                        color_box = (0, 165, 255)
                        click_cooldown = 20

                # -----------------------------
                # Scroll up gesture: four fingers up
                # -----------------------------
                elif fingers_up == 4:
                    if scroll_cooldown == 0:
                        for i in range(4):
                            pyautogui.scroll(30)
                            time.sleep(0.01)
                        gesture_text = "Scroll Up"
                        color_box = (0, 255, 255)
                        scroll_cooldown = 10

                # -----------------------------
                # Scroll down gesture: all five fingers up
                # -----------------------------
                elif fingers_up == 5:
                    if scroll_cooldown == 0:
                        for i in range(4):
                            pyautogui.scroll(-30)
                            time.sleep(0.01)
                        gesture_text = "Scroll Down"
                        color_box = (0, 255, 255)
                        scroll_cooldown = 10

    # -----------------------------
    # Reduce cooldowns per frame
    # -----------------------------
    if click_cooldown > 0:
        click_cooldown -= 1
    if scroll_cooldown > 0:
        scroll_cooldown -= 1

    # -----------------------------
    # Display current gesture text on frame
    # -----------------------------
    if gesture_text:
        cv2.putText(img, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color_box, 3)

    # Show webcam feed
    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

