import time
import cv2
import numpy as np
import pickle
import mediapipe as mp
import ssh_comm


class mpHands:
    """
    Recognition of hands and hand's gestures using mediapipe
    """

    def __init__(self, maxHands = 2, tol1 = 0.5, tol2 = 0.5):
        self.hands = mp.solutions.hands.Hands(static_image_mode = False, max_num_hands = maxHands,
                                              min_detection_confidence = tol1, min_tracking_confidence = tol2)

    def Marks(self, frame):
        """
        Extract hand's landmarks from a given frame.
        """

        myHands = []
        frameRGB  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frameRGB)

        if results.multi_hand_landmarks != None:

            for handLandMarks in results.multi_hand_landmarks:
                myHand = []

                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x * width), int(landMark.y * height)))

                myHands.append(myHand)

        return myHands


def findDistances(handData):
    """
    Calculate distance matrix based on hand's landmarks.
    """

    distMatrix = np.zeros([len(handData), len(handData)], dtype = 'float')
    palmSize = ((handData[0][0] - handData[9][0]) ** 2 + (handData[0][1] - handData[9][1]) ** 2) ** (1.0 / 2.0)

    for row in range(0, len(handData)):

        for column in range(0, len(handData)):
            distMatrix[row][column] = (((handData[row][0] - handData[column][0]) ** 2 + (handData[row][1] - handData[column][1]) ** 2)
                                        ** (1. / 2.)) / palmSize

    return distMatrix


def findError(gestureMatrix, unknownMatrix, keyPoints):
    """
    Calculate error between two matrices based on key points.
    """

    error = 0

    for row in keyPoints:

        for column in keyPoints:
            error = error + abs(gestureMatrix[row][column] - unknownMatrix[row][column])

    print(error)
    return error


def findGesture(unknownGesture, knownGestures, keyPoints, gestNames, tol):
    """
    Find the closest matching gesture based on error calculation.
    """

    errorArray = []

    for idx in range(0, len(gestNames), 1):
        error = findError(knownGestures[idx], unknownGesture, keyPoints)
        errorArray.append(error)

    errorMin = errorArray[0]
    minIndex = 0

    for idx in range(0, len(errorArray), 1):

        if errorArray[idx] < errorMin:
            errorMin = errorArray[idx]
            minIndex = idx

    if errorMin < tol:
        gesture = gestNames[minIndex]

    if errorMin >= tol:
        gesture = 'Unknown'

    return gesture


def cam_set_up() -> None:
    """
    Set up the camera with specified parameters.
    """

    cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cam.set(cv2.CAP_PROP_FPS, 30)
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    pass  # Implicitly returns None


def frame_set_up(frame, width, height) -> np.ndarray:
    """
    Resize and flip a frame.
    """

    frame = cv2.resize(frame, (width, height))
    frame = cv2.flip(frame, 1)

    return frame


def gestures_train(gestNames) -> tuple[list[str], int, str]:
    """
    Train gestures by prompting user for names and saving to file.
    """

    numGest = int(input('How Many Gestures Do You Want? : '))

    for idx in range(0, numGest, 1):
        prompt = 'Name of Gesture #' + str(idx + 1) + ' '
        name = input(prompt)
        gestNames.append(name)

    print(gestNames)
    trainName = input('Filename for training data? (Press Enter for Default) : ')

    if trainName == '':
        trainName = 'default'

    trainName = trainName + '.pkl'

    return gestNames, numGest, trainName


def gestures_read(gestNames, knownGestures) -> tuple[str, list[str], list[np.ndarray]]:
    """
    Read trained gestures from a file.
    """

    trainName = input('What Training Data Do You Want to Use? (Press Enter for Default) : ')

    if trainName == '':
        trainName = 'default'

    trainName = trainName + '.pkl'

    with open(trainName,'rb') as f:
        gestNames = pickle.load(f)
        knownGestures = pickle.load(f)

    return trainName, gestNames, knownGestures


def palm_circles(frame, handData, keyPoints) -> np.ndarray:
    """
    Draw circles around key points on palms in a frame.
    """

    for hand in handData:

        for idx in keyPoints:
            cv2.circle(frame, hand[idx], 15, (255, 0, 255), 2)

    return frame


width = 640
height = 480
tol = 10
keyPoints = [0, 4, 5, 9, 13, 17, 8, 12, 16, 20]

ssh_comm.set_ssh_connection()

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam_set_up()

findHands = mpHands(1)
time.sleep(5)

train = int(input('Enter 1 to Train, Enter 0 to Recognize: '))

if train == 1:
    trainCnt = 0
    gestNames = []
    knownGestures = []
    gestNames, numGest, trainName = gestures_train(gestNames=[])

if train == 0:
    trainName, gestNames, knownGestures = gestures_read(gestNames=[], knownGestures=[])

try:
    while True:
        ignore,  frame = cam.read()
        frame = frame_set_up(frame, width, height)
        handData = findHands.Marks(frame)

        if train == 1:

            if handData != []:
                print('Please, Show Gesture: ', gestNames[trainCnt], ': Press t when Ready: ')

                if cv2.waitKey(1) & 0xff == ord('t'):
                    knownGesture = findDistances(handData[0])
                    knownGestures.append(knownGesture)
                    trainCnt = trainCnt + 1

                    if trainCnt == numGest:
                        train = 0

                        with open(trainName, 'wb') as f:
                            pickle.dump(gestNames, f)
                            pickle.dump(knownGestures, f)

        if train == 0:

            if handData != []:
                unknownGesture = findDistances(handData[0])
                myGesture = findGesture(unknownGesture, knownGestures, keyPoints, gestNames, tol)
                # error = findError(knownGesture, unknownGesture, keyPoints)
                cv2.putText(frame, myGesture, (100, 175), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
                ssh_comm.gesture_commands(myGesture)

                if myGesture == "Quit":
                    time.sleep(5)
                    break

        frame = palm_circles(frame, handData, keyPoints)

        cv2.imshow('MyCam', frame)
        cv2.moveWindow('MyCam', 0, 0)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break

except KeyboardInterrupt:
    print("User's Ctrl+C detected.")
    ssh_comm.gesture_commands("Quit")

finally:
    cam.release()
    ssh_comm.close_ssh_connection()
