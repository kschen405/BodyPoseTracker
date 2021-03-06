import cv2
import time
import mediapipe as mp


class PoseTracking:
    def __init__(
        self,
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):

        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(
            self.static_image_mode,
            self.model_complexity,
            self.smooth_landmarks,
            self.enable_segmentation,
            self.smooth_segmentation,
            self.min_detection_confidence,
            self.min_tracking_confidence,
        )

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS
                )
        return img

    def findPosition(self, img, draw=True):
        self.lmList = []
        self.dict = {}
        if self.results.pose_landmarks != None:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                self.dict[id] = (cx, cy)
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    def markAngle(self, img):
        cv2.line(img, self.dict[14], self.dict[12], (0, 0, 255), 5)
        cv2.line(img, self.dict[14], self.dict[16], (0, 0, 255), 5)


def main():
    cap = cv2.VideoCapture("testVideos\/flat\/20220112_130536L.mp4")
    pTime = 0
    Tracker = PoseTracking()
    while True:
        success, img = cap.read()
        img = Tracker.findPose(img, draw=True)
        lmList = Tracker.findPosition(img, draw=True)
        Tracker.markAngle(img)
        if len(lmList) != 0:
            print(lmList[14])
            cv2.circle(
                img, (lmList[14][1], lmList[14][2]
                      ), 5, (0, 0, 255), 5  # , cv2.FILLED
            )
        cTime = time.time()
        if cTime != pTime:
            fps = 1 / (cTime - pTime)
        else:
            fps = 0
        pTime = cTime

        cv2.putText(
            img, f"FPS: {int(fps)}", (70,
                                      100), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4
        )

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
