from .constants import input_shape, lfw_trained_model
import numpy as np
from mtcnn import MTCNN
import cv2
import os

def detect(image):
    detector = MTCNN()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(image)
    for result in results:
        bounding_box = result['box']
        keypoints = result['keypoints']
        cv2.rectangle(image,
                (bounding_box[0], bounding_box[1]),
               (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                (0,155,255), 2)
        cv2.circle(image,(keypoints['left_eye']), 2, (0,155,255), 2)
        cv2.circle(image,(keypoints['right_eye']), 2, (0,155,255), 2)
        cv2.circle(image,(keypoints['nose']), 2, (0,155,255), 2)
        cv2.circle(image,(keypoints['mouth_left']), 2, (0,155,255), 2)
        cv2.circle(image,(keypoints['mouth_right']), 2, (0,155,255), 2)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def recognize_face(prob, face_data, cnn_model):
    face_data = cv2.cvtColor(face_data, cv2.COLOR_BGR2RGB)
    face_data = cv2.resize(face_data, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
    face_data = np.array(face_data, dtype='float32') / 255
    face_data = np.expand_dims(face_data, axis=0)
    predicted_face_data = cnn_model.predict(face_data)

    return predicted_face_data


def recognize(image):
    faces, probs = mtcnn.detect_faces(image)
    if faces is not None:
        for face, prob in zip(faces, probs):
            if prob > 0.1:
                x1, y1, x2, y2 = [int(p) for p in face]
                (image_height, image_widht, _) = np.shape(image)

                #scaling for better image experience
                (font_scale, thickness, padding) = (0.6, 2, 20)
                if image_height > 1000 or image_widht > 1000:
                    font_scale = 1
                    padding = 24
                    scale = (image_height / 1000, image_widht / 1000)
                    scale = max(scale)
                    (font_scale, thickness, padding) = [int(s * scale) for s in (font_scale, thickness, padding)]


                xx1, yy1, xx2, yy2 = [int(p) for p in face]
                half_width         = int((xx2 - xx1) / 2.8)
                half_height        = int((yy2 - yy1) / 2.8)
                (xx1, yy1)         = [c - half_width  for c in (xx1, yy1)]
                (xx2, yy2)         = [c + half_height for c in (xx2, yy2)]
                if xx1 < 0 or yy1 < 0 or xx2 > image_widht or yy2 > image_height:
                    #can't be recognized
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                else:
                    #have enough space to be recognized
                    face_data = image[yy1:yy2, xx1:xx2]
                    predicted_face = recognize_face(str(prob), face_data, lfw_trained_model)

                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                    cv2.rectangle(image, (xx1, yy1), (xx2, yy2), (0, 255, 0), thickness)
                    cv2.putText(image, str(prob), (x1, y2 + padding),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)

    return image

