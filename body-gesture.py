import cv2
import mediapipe as mp
import json
import pyautogui
import sys
import asyncio
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

commands = {
    "directionX": 0,
    "directionY": 0,
    "w":0,
    "jump":False
}

async def runCommands():
    pyautogui.move(20 * commands["directionX"], 2 * commands["directionY"]w)

    if commands["w"] == 1:
        pyautogui.keyDown("w")
        commands['w'] = 0
    elif commands['w']==-1:
        pyautogui.keyUp("w")
        commands['w'] = 0
    
    if commands['jump']:
        pyautogui.press("space")
        commands['jump'] = False


async def imageProcess(cap, pose, firstResult, running):
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        return

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    landmarkList = results.pose_world_landmarks
    if (landmarkList is None):
        return
    marksStr = str(landmarkList).replace("landmark ", "").replace(
        "\n", "").replace("  ", ", ").replace("{,", "{").replace("}{", "}, {")
    marks = json.loads("["+marksStr.replace("x", "\"x\"").replace(
        "visibility", "\"visibility\"").replace(" y", " \"y\"").replace("z", "\"z\"")+"]")
    for index, mark in enumerate(marks):
        if (index == 0):
            print(index)
            print(mark['x'])
            loop = asyncio.get_event_loop()
            if mark['x'] > 0.1:
                commands["directionX"] = -1
            elif mark['x'] < -0.1:
                commands["directionX"] = 1
        elif index == 15:
            print(index)
            print(mark['visibility'])
            if (mark['visibility'] > 0.4 and not running):
                commands["w"] = 1
            elif (mark['visibility'] <= 0.3 and running):
                commands["w"] = -1

    if firstResult is None:
        firstResult = results
        print(str(firstResult))

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

async def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.1, model_complexity=0, static_image_mode=False, smooth_landmarks=False) as pose:
        firstResult = None
        running = False
        while cap.isOpened():
            await asyncio.ensure_future(imageProcess(cap, pose, firstResult, running))
            await asyncio.ensure_future(runCommands())
            if cv2.waitKey(1) & 0xFF == 27:
                commands = {
                    "directionX": 0,
                    "directionY": 0,
                    "w":0,
                    "jump":False
                }
                break
    cap.release()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
