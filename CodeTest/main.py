import cv2
import pyautogui
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils
  
# Initialize states
play_pause_triggered = False
volume_up_triggered = False
volume_down_triggered = False
next_track_triggered = False
prev_track_triggered = False
alt_tab_triggered = False
vscode_triggered = False
windows_triggered = False
pip_triggered = False
screenshot_triggered = False
screen_recording = False
tab_right_triggered = False
tab_left_triggered = False
repeat_triggered = False
shuffle_triggered = False
save_playlist_triggered = False
skip_media_start_time = None

# Cooldown for key presses
last_key_time = time.time()
key_cooldown = 0.5  # seconds

# Gesture counters
pinch_counter = 0
shuffle_counter = 0
save_playlist_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror view
    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    gesture_text = "No gesture detected"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Determine finger states
            index_extended = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
            middle_extended = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y
            ring_extended = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y
            pinky_extended = landmarks[mp_hands.HandLandmark.PINKY_TIP].y < landmarks[mp_hands.HandLandmark.PINKY_PIP].y
            thumb_extended = landmarks[mp_hands.HandLandmark.THUMB_TIP].x > landmarks[mp_hands.HandLandmark.THUMB_IP].x

            index_tip_y = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            thumb_tip_y = landmarks[mp_hands.HandLandmark.THUMB_TIP].y

            finger_info = f"I:{int(index_extended)} M:{int(middle_extended)} R:{int(ring_extended)} P:{int(pinky_extended)} T:{int(thumb_extended)}"
            y_diff = index_tip_y - thumb_tip_y
            cv2.putText(frame, finger_info, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(frame, f"Y-diff: {y_diff:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

            current_time = time.time()

            # Volume Up: Only Index Finger up
            if index_extended and not middle_extended and not ring_extended and not pinky_extended:
                if (thumb_tip_y - index_tip_y) > 0.02:
                    if not volume_up_triggered and current_time - last_key_time > key_cooldown:
                        pyautogui.keyDown('volumeup')
                        volume_up_triggered = True
                        last_key_time = current_time
                        gesture_text = "Volume Up"
                else:
                    volume_up_triggered = False
            else:
                volume_up_triggered = False

            # Volume Down: Index below thumb
            if index_extended and not middle_extended and not ring_extended and not pinky_extended:
                if (index_tip_y - thumb_tip_y) > 0.02:
                    if not volume_down_triggered and current_time - last_key_time > key_cooldown:
                        pyautogui.keyDown('volumedown')
                        volume_down_triggered = True
                        last_key_time = current_time
                        gesture_text = "Volume Down"
                else:
                    volume_down_triggered = False
            else:
                volume_down_triggered = False

            # Play/Pause: All fingers down
            all_fingers_down = not index_extended and not middle_extended and not ring_extended and not pinky_extended and not thumb_extended
            if all_fingers_down and not play_pause_triggered and current_time - last_key_time > key_cooldown:
                pyautogui.press('space')
                play_pause_triggered = True
                last_key_time = current_time
                gesture_text = "Play/Pause"
            elif not all_fingers_down:
                play_pause_triggered = False

            # Next Track: Index + Middle extended
            if index_extended and middle_extended and not ring_extended and not pinky_extended and not thumb_extended:
                if not next_track_triggered and current_time - last_key_time > key_cooldown:
                    pyautogui.press('right')
                    next_track_triggered = True
                    last_key_time = current_time
                    gesture_text = "Next Track"
            else:
                next_track_triggered = False

            # Previous Track: Index + Pinky extended
            if index_extended and not middle_extended and not ring_extended and pinky_extended and not thumb_extended:
                if not prev_track_triggered and current_time - last_key_time > key_cooldown:
                    pyautogui.press('left')
                    prev_track_triggered = True
                    last_key_time = current_time
                    gesture_text = "Previous Track"
            else:
                prev_track_triggered = False

            # Alt+Tab Switch: Index + Middle + Ring extended
            three_fingers_extended = index_extended and middle_extended and ring_extended and not pinky_extended
            if three_fingers_extended:
                if not alt_tab_triggered and current_time - last_key_time > key_cooldown:
                    pyautogui.keyDown('alt')
                    if thumb_extended:
                        pyautogui.press('tab')
                        gesture_text = "Alt+Tab Forward"
                    else:
                        pyautogui.keyDown('shift')
                        pyautogui.press('tab')
                        pyautogui.keyUp('shift')
                        gesture_text = "Alt+Tab Backward"
                    time.sleep(0.1)
                    pyautogui.keyUp('alt')
                    alt_tab_triggered = True
                    last_key_time = current_time
            else:
                alt_tab_triggered = False

            # Picture-in-Picture (PIP): Thumb + Pinky (Shaka Sign)
            if not index_extended and not middle_extended and not ring_extended and pinky_extended and thumb_extended:
                if not pip_triggered and current_time - last_key_time > key_cooldown:
                    pyautogui.keyDown('alt')
                    pyautogui.press('p')
                    pyautogui.keyUp('alt')
                    pip_triggered = True
                    last_key_time = current_time
                    gesture_text = "Picture-in-Picture"
            else:
                pip_triggered = False

            # Screenshot: All fingers extended
            if index_extended and middle_extended and ring_extended and pinky_extended and thumb_extended:
                if not screenshot_triggered and current_time - last_key_time > key_cooldown:
                    screenshot = pyautogui.screenshot()
                    screenshot.save(f'screenshot_{int(time.time())}.png')
                    screenshot_triggered = True
                    last_key_time = current_time
                    gesture_text = "Screenshot Taken"
            else:
                screenshot_triggered = False

            # Tab Right: Index + Ring + Thumb extended
            if index_extended and not middle_extended and ring_extended and not pinky_extended and thumb_extended:
                if not tab_right_triggered and current_time - last_key_time > key_cooldown:
                    pyautogui.hotkey('ctrl', 'tab')
                    tab_right_triggered = True
                    last_key_time = current_time
                    gesture_text = "Tab Right"
            else:
                tab_right_triggered = False

            # Tab Left: Middle + Ring extended
            if not index_extended and middle_extended and ring_extended and not pinky_extended and not thumb_extended:
                if not tab_left_triggered and current_time - last_key_time > key_cooldown:
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                    tab_left_triggered = True
                    last_key_time = current_time
                    gesture_text = "Tab Left"
            else:
                tab_left_triggered = False

            # Repeat/Loop: Pinch Gesture x3
            pinch_distance = abs(landmarks[mp_hands.HandLandmark.THUMB_TIP].x - landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)
            if pinch_distance < 0.03:
                pinch_counter += 1
                if pinch_counter >= 3 and not repeat_triggered:
                    pyautogui.hotkey('ctrl', 'r')  # Example key for loop/repeat
                    repeat_triggered = True
                    gesture_text = "Repeat/Loop"
            else:
                pinch_counter = 0
                repeat_triggered = False

            # Shuffle: Index + Middle (peace) x2
            if index_extended and middle_extended and not ring_extended and not pinky_extended:
                shuffle_counter += 1
                if shuffle_counter >= 2 and not shuffle_triggered:
                    pyautogui.hotkey('ctrl', 's')  # Example key for shuffle
                    shuffle_triggered = True
                    gesture_text = "Shuffle"
            else:
                shuffle_counter = 0
                shuffle_triggered = False

            # Save Playlist: Thumb + Middle pinch x2
            pinch_thumb_middle = abs(landmarks[mp_hands.HandLandmark.THUMB_TIP].x - landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)
            if pinch_thumb_middle < 0.03:
                save_playlist_counter += 1
                if save_playlist_counter >= 2 and not save_playlist_triggered:
                    pyautogui.hotkey('ctrl', 'd')  # Example key to save
                    save_playlist_triggered = True
                    gesture_text = "Save Playlist"
            else:
                save_playlist_counter = 0
                save_playlist_triggered = False

            # Skip Media: Open palm held for 3 secs
            if index_extended and middle_extended and ring_extended and pinky_extended and thumb_extended:
                if skip_media_start_time is None:
                    skip_media_start_time = current_time
                elif current_time - skip_media_start_time > 3:
                    pyautogui.press('end')  # Example key for skip
                    gesture_text = "Skip Media"
                    skip_media_start_time = None
            else:
                skip_media_start_time = None

    # Display current gesture
    cv2.putText(frame, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Multimedia Controller using Hand Gesture', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
