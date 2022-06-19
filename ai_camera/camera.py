import cv2
import os
import numpy as np


class VideoCamera(object):
    def __init__(self, url = 0):
        self.video = cv2.VideoCapture(url)

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.video.read()
        frame_flip = cv2.flip(frame, 1)
        ret, frame = cv2.imencode('.jpg', frame_flip)
        return frame.tobytes()
