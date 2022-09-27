#from facenet_pytorch import MTCNN
#from mtcnn import MTCNN
from .cnn_model import create_models
#import torch

#device = 'cuda' if torch.cuda.is_available() else 'cpu'
#mtcnn = MTCNN()
# mtcnn = MTCNN(keep_all=True, device=device)
input_shape = (96, 96, 3) # height, width, channels
(openface_model, lfw_trained_model, pinface_trained_model) = create_models()
