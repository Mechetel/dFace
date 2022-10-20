import numpy as np
import cv2

class Image:

    def __init__(self, data):
        self._data = data

    def normalize(self):
        self._data = np.array(self._data, dtype='float32') / 255
        self._data = np.expand_dims(self._data, axis=0)

    def to_rgb(self):
        self._data = cv2.cvtColor(self._data, cv2.COLOR_BGR2RGB)

    def resize(self, shape):
        self._data = cv2.resize(self._data, (shape.get_width(), shape.get_height()), interpolation=cv2.INTER_AREA)

    def getPixels(self):
        return self._data
