import asyncio
import json
import sys

import cv2
import mediapipe as mp
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

commands = {
    "click": True,
    "directionX": 0,
    "directionY": 0,
    "averageY": [],
    "mediaMovelIndex": 0,
    "w":-1,
    "jump":False,
    "running":False
}

async def runCommands():
    pyautogui.move(20 * commands["directionX"], 20 * commands["directionY"])

    if commands["w"] == 1 and not commands["running"]:
        pyautogui.keyDown("w")
        commands["running"] = True
        
    elif commands['w']==0 and commands["running"]:
        pyautogui.press("w")
        pyautogui.keyUp("w")
        commands["running"] = False
    
    if commands['jump']:
        pyautogui.press("space")
        commands['jump'] = False
    
    if commands['click']:
        pyautogui.leftClick()
        commands['click'] = False


async def imageProcess(cap, pose):
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

    commands["directionX"] = -10 * marks[0]['x']

    index = commands["mediaMovelIndex"]%20
    if len(commands["averageY"])<index+1:
        commands["averageY"].append(marks[0]["y"]-marks[12]["y"])
    else:
        commands["averageY"][index] = marks[0]["y"]-marks[12]["y"]
    if index == 0: commands["mediaMovelIndex"] = 0
    commands["mediaMovelIndex"]+=1
    commands["directionY"] = ((sum(commands["averageY"]) / len(commands["averageY"]))-(marks[0]["y"]-marks[12]["y"]))*-10

    commands["w"] = 1 if marks[15]['visibility'] > 0.5 else 0

    commands["click"] = marks[16]['visibility'] > 0.5

    print(f'index: 0, x: {marks[0]["x"]}, y: {marks[0]["x"]}, v: {marks[0]["visibility"]}')

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
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5, model_complexity=1, static_image_mode=False, smooth_landmarks=False, ) as pose:
        
        while cap.isOpened():
        
            await asyncio.ensure_future(imageProcess(cap, pose))
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
