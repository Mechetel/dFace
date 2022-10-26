import numpy as np
import abc

class FaceRecognitionNet(abc.ABC):

    def __init__(self, input_shape):
        self._input_shape = input_shape
        self._model = self._create_model(input_shape)

    def get_input_shape(self):
        return self._input_shape

    def encode(self, image):
        predictions = self._model.predict(image.getPixels())
        return predictions

    def load_weights(self, file):
        self._model.load_weights(file)

    def save_weights(self, file):
        self._model.save_weights(file)

    @abc.abstractmethod
    def _create_model(self, input_shape):
        pass
