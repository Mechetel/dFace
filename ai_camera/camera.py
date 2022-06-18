import cv2
import os
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.video.read()
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)
        return frame.tobytes()


class IPWebCamera(object):
    def __init__(self, url):
        self.url = url
        self.video = cv2.VideoCapture(url)

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.video.read()
        resize = cv2.resize(frame, (640, 480), interpolation = cv2.INTER_LINEAR)
        ret, frame = cv2.imencode('.jpg', resize)
        return frame.tobytes()

