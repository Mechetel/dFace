import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from facenet_pytorch import MTCNN
import torch
import numpy as np
import cv2
from .cnn_model import create_models

device = 'cuda' if torch.cuda.is_available() else 'cpu'
mtcnn = MTCNN(keep_all=True, device=device)
input_shape = (96, 96, 3) # height, width, channels
(openface_model, lfw_trained_model, pinface_trained_model) = create_models()


def predict_face(prob, face_data, cnn_model):
    face_data = cv2.cvtColor(face_data, cv2.COLOR_BGR2RGB)
    face_data = cv2.resize(face_data, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
    # cv2.imwrite(prob + "file.jpg", face_data)  # all right
    face_data = np.array(face_data, dtype='float32') / 255


    # print("--------------")
    # print(np.shape(face_data))  # (96, 96, 3)
    # print("--------------")


    # predicted_face_data = cnn_model.predict(face_data) #error
    ## ValueError: Input 0 of layer "model_8" is incompatible with the layer: expected shape=(None, 96, 96, 3), found shape=(32, 96, 3)

    # return predicted_face_data


def predict(image):
    faces, probs = mtcnn.detect(image)
    if faces is not None:
        for face, prob in zip(faces, probs):
            if prob > 0.9:
                x1, y1, x2, y2 = [int(p) for p in face]


                face_data = image[y1:y2, x1:x2]
                predicted_face = predict_face(str(prob), face_data, lfw_trained_model)


                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(image, str(prob), (x1, y2+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return image

