import random

import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

playerBat = True
detector = HandDetector(maxHands=1)

# res = False
# aWin = 0
# uWin = 0

timer = 0
stateResult = False
startGame = False
scores = [0,0]
print("Lets play BatBall")
while True:
    imgBG = cv2.imread("Resources/BG.png")
    success, img = cap.read()

    imgScaled =cv2.resize(img, (0,0), None, 0.875,0.875)
    imgScaled = imgScaled[:,80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)


    if(startGame==False):
        cv2.putText(imgBG, str("Press: s"), (540, 640), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    if startGame:
        # if(res ==False):
        if(playerBat):
                cv2.putText(imgBG, str("You'll Bat"), (540, 640), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        else:
                cv2.putText(imgBG, str("You'll Bowl"), (540, 640), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        # else:
        #     if (uWin == 1):
        #         cv2.putText(imgBG, str("You Win"), (540, 640), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        #         time.sleep(3)
        #         break
        #     if (aWin == 1):
        #         cv2.putText(imgBG, str("You Loose"), (540, 640), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        #         time.sleep(3)
        #         break
        #     else:
        #         cv2.putText(imgBG, str("Draw"), (540, 640), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        #         time.sleep(3)
        #         break
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605,435), cv2.FONT_HERSHEY_PLAIN, 6, (0,0,0), 4)

            if timer>3:
                stateResult = True
                timer=0

                if hands:
                    playermove =None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    # print(fingers)
                    if fingers == [0,1,0,0,0]:
                        playermove = 1
                    if fingers == [0,1,1,0,0]:
                        playermove = 2
                    if fingers == [0,1,1,1,0]:
                        playermove = 3
                    if fingers == [0,1,1,1,1]:
                        playermove = 4
                    if fingers == [1,1,1,1,1]:
                        playermove = 5
                    if fingers == [1,0,0,0,0]:
                        playermove = 6

                    randomNumber = random.randint(1,6)
                    imgAI = cv2.imread(f'Resources2/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgAI = cv2.resize(imgAI, (276, 276))
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

                    if(playerBat):
                        # Invalid Input
                        if(playermove != 1 and playermove != 2 and playermove != 3 and playermove != 4 and playermove != 5 and playermove != 6):
                            scores[1] += 0

                        # Player Wins
                        elif(playermove != randomNumber):
                            scores[1] += playermove
                        # AI Wins
                        elif (playermove == randomNumber):
                            # scores[0] += 1

                            print("You are out.", end="")
                            print("Your score = ", end="")
                            print(scores[1])
                            print("Now AI will bat")
                            playerBat = False

                    else:
                        if (playermove != 1 and playermove != 2 and playermove != 3 and playermove != 4 and playermove != 5 and playermove != 6):
                            scores[0] += 0

                        elif (playermove != randomNumber):
                            scores[0] += randomNumber
                            if(scores[0] > scores[1]):
                                print("AI's score = ", end="")
                                print(scores[0])
                                print("AI Won")
                                time.sleep(3)
                                break
                                # aWin = 1
                                # res = True

                            # AI Wins
                        elif (playermove == randomNumber):
                            # scores[0] += 1
                            # res == True
                            print("AI is out.", end="")
                            print("AI's score = ", end="")
                            print(scores[0])

                            if(scores[1] > scores[0]):
                                print("You Won")
                                time.sleep(3)
                                break
                                # uWin = 1

                            elif(scores[1] == scores[0]):
                                print("Match Tied")
                                time.sleep(3)
                                break

                            else:
                                print("AI Won")
                                time.sleep(3)
                                break
                                # aWin = 1


                else:
                    print("Unable to trace your Hands")
                    print("Game Over")
                    print("Your Score: ", end="")
                    print(scores[1])
                    break


    imgBG[234:654,795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149,310))

    cv2.putText(imgBG, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,0), 6)
    cv2.putText(imgBG, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (0,0,0), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    # cv2.imshow("Image", imgScaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult=False