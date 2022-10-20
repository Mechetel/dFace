from .FaceRecognitionNet import FaceRecognitionNet


class ModifiedOpenFace(FaceRecognitionNet):

    def __init__(self, input_shape, model):
        self._model = model
        super().__init__(input_shape)

    def _create_model(self, input_shape):
        return self._model
