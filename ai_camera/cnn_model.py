from .OriginalOpenFace import OriginalOpenFace
from .TrainableOpenFace import TrainableOpenFace
from os.path import join, dirname

def create_models():
    input_shape           = (96, 96, 3)
    openface_model        = OriginalOpenFace(input_shape)
    lfw_trained_model     = TrainableOpenFace(input_shape, 5749)
    pinface_trained_model = TrainableOpenFace(input_shape, 105)

    # Loading weights
    # openface_model.load_weights(join(dirname(__file__), "weights/openface_weights.h5"))
    lfw_trained_model.load_weights(join(dirname(__file__), "weights/weights-lfw.h5"))
    pinface_trained_model.load_weights(join(dirname(__file__), "weights/weights-pin-faces.h5"))

    # Removing last layer in trained models
    lfw_trained_model.to_useable_net()
    pinface_trained_model.to_useable_net()
    return (openface_model, lfw_trained_model, pinface_trained_model)

