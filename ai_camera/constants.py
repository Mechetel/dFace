from mtcnn import MTCNN
from .cnn_model import create_models

mtcnn = MTCNN()
input_shape = (96, 96, 3) # height, width, channels
(openface_model, lfw_trained_model, pinface_trained_model) = create_models()
