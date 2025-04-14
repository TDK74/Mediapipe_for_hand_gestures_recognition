import time
import cv2
import numpy as np
import pickle
import mediapipe as mp
import ssh_comm


width = 640
height = 480
tol = 10
keyPoints = [0, 4, 5, 9, 13, 17, 8, 12, 16, 20]


class mpHands:
    """
    Recognition of hands and hand gestures using mediapipe.
    """
    def __init__(self, maxHands = 2, tol1 = 0.5, tol2 = 0.5):
        self.hands = mp.solutions.hands.Hands(
                                                static_image_mode = False,
                                                max_num_hands = maxHands,
                                                min_detection_confidence = tol1,
                                                min_tracking_confidence = tol2
                                            )

    def Marks(self, frame):
        """
        Extract hand landmarks from a given frame.
        """
        myHands = []
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)

        if results.multi_hand_landmarks:
            for handLandMarks in results.multi_hand_landmarks:
                myHand = [(int(landMark.x * width), int(landMark.y * height))
                          for landMark in handLandMarks.landmark]
                myHands.append(myHand)

        return myHands


def findDistances(handData):
    """
    Calculate distance matrix based on hand's landmarks.
    """
    distMatrix = np.zeros([len(handData), len(handData)], dtype = 'float')
    palmSize = ((handData[0][0] - handData[9][0]) ** 2 +
                (handData[0][1] - handData[9][1]) ** 2) ** 0.5

    for row in range(len(handData)):
        for column in range(len(handData)):
            distMatrix[row][column] = (((handData[row][0] - handData[column][0]) ** 2 +
                                        (handData[row][1] - handData[column][1]) ** 2) **
                                          0.5) / palmSize

    return distMatrix


def findError(gestureMatrix, unknownMatrix, keyPoints):
    """
    Calculate error between two matrices based on key points.
    """
    error = 0

    for row in keyPoints:
        for column in keyPoints:
            error += abs(gestureMatrix[row][column] - unknownMatrix[row][column])

    return error


def findGesture(unknownGesture, knownGestures, keyPoints, gestNames, tol):
    """
    Find the closest matching gesture based on error calculation.
    """
    errorArray = [findError(knownGestures[idx], unknownGesture, keyPoints)
                  for idx in range(len(gestNames))]
    errorMin = min(errorArray)
    minIndex = errorArray.index(errorMin)

    return gestNames[minIndex] if errorMin < tol else 'Unknown'


def cam_set_up(cam):
    """
    Set up the camera with specified parameters.
    """
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FPS, 30)   # was 30
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))


def frame_set_up(frame, width, height):
    """
    Resize and flip a frame.
    """
    frame = cv2.resize(frame, (width, height))
    frame = cv2.flip(frame, 1)

    return frame


def train_gestures(gestNames):
    """
    Train gestures by prompting user for names and saving to file.
    """
    numGest = int(input('How Many Gestures Do You Want? : '))

    for idx in range(numGest):
        name = input(f'Name of Gesture #{idx + 1} ')
        gestNames.append(name)

    print(gestNames)
    trainName = input('Filename for training data?\
                       (Press Enter for Default) : ') or 'default'
    trainName += '.pkl'

    return gestNames, numGest, trainName


def recognize_gesture(handData, knownGestures, keyPoints, gestNames, tol):
    """
    Recognize gestures based on the trained data.
    """
    unknownGesture = findDistances(handData[0])
    myGesture = findGesture(unknownGesture, knownGestures, keyPoints,
                            gestNames, tol)
    ssh_comm.gesture_commands(myGesture)

    return myGesture


def palm_circles(frame, handData, keyPoints):
    """
    Draw circles around key points on palms in a frame.
    """
    for hand in handData:
        for idx in keyPoints:
            cv2.circle(frame, hand[idx], 15, (255, 0, 255), 2)

    return frame


def process_frame(frame, train, handData, gestNames, knownGestures,
                  trainCnt, numGest, trainName, key_pressed):
    """
    Process the frame based on training or recognition mode.
    """
    if train == 1 and len(handData) > 0 and trainCnt < numGest:
        print(f'Please, Show Gesture: {gestNames[trainCnt]} : Press t when Ready: ')
        time.sleep(0.5)

        if key_pressed & 0xff == ord('t'):
            knownGesture = findDistances(handData[0])
            knownGestures.append(knownGesture)
            trainCnt += 1

            if trainCnt == numGest:
                train = 0

                with open(trainName, 'wb') as f:
                    pickle.dump(gestNames, f)
                    pickle.dump(knownGestures, f)

    elif train == 0 and len(handData) > 0:
        myGesture = recognize_gesture(handData, knownGestures, keyPoints,
                                      gestNames, tol)
        cv2.putText(frame, myGesture, (100, 175), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 0, 0), 3)

        return frame, myGesture, trainCnt, train

    return frame, None, trainCnt, train


def main():
    """
    Main function to control the program flow.
    """
    ssh_comm.set_ssh_connection()
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam_set_up(cam)

    findHands = mpHands(1)
    time.sleep(5)

    train = int(input('Enter in the terminal 1 to Train. Enter 0 to Recognize: '))
    gestNames, knownGestures = [], []
    trainCnt, numGest, trainName = 0, 0, ""

    if train == 1:
        gestNames, numGest, trainName = train_gestures(gestNames)
    elif train == 0:
        trainName = input('What Training Data Do You Want to Use?\
                           (Press Enter for Default) : ') or 'default'
        trainName += '.pkl'

        with open(trainName, 'rb') as f:
            gestNames = pickle.load(f)
            knownGestures = pickle.load(f)

    try:
        while True:
            ret, frame = cam.read()
            frame = frame_set_up(frame, width, height)
            handData = findHands.Marks(frame)

            key_pressed = cv2.waitKey(10)

            frame, myGesture, trainCnt, train = process_frame(frame, train, handData, gestNames,
                                                        knownGestures, trainCnt, numGest,
                                                        trainName, key_pressed)

            if myGesture == "Quit":
                time.sleep(1)
                break

            frame = palm_circles(frame, handData, keyPoints)

            cv2.imshow('MyCam', frame)
            #cv2.moveWindow('MyCam', 0, 0)

            if key_pressed & 0xff == ord('q'):
                break

    except KeyboardInterrupt:
        print("User's Ctrl+C detected.")
        ssh_comm.gesture_commands("Quit")

    finally:
        cam.release()
        ssh_comm.close_ssh_connection()


if __name__ == "__main__":
    main()
