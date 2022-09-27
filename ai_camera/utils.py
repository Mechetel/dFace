from .constants import input_shape, lfw_trained_model, mtcnn
import numpy as np
import cv2
import os


def recognize_face(confidence, face_data, cnn_model):
    face_data = cv2.cvtColor(face_data, cv2.COLOR_BGR2RGB)
    face_data = cv2.resize(face_data, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
    face_data = np.array(face_data, dtype='float32') / 255
    face_data = np.expand_dims(face_data, axis=0)
    predicted_face_data = cnn_model.predict(face_data)

    return predicted_face_data

def draw_keypoints(img, keypoints):
    cv2.circle(img, keypoints["left_eye"],    1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["right_eye"],   1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["nose"],        1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["mouth_left"],  1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["mouth_right"], 1, (0, 0, 255), 2)


def recognize(image):
    face_list = mtcnn.detect_faces(image)
    for face in face_list:
        box = face["box"]
        confidence = face["confidence"]
        keypoints = face["keypoints"]
        if confidence > 0.9:
            x1,y1, image_widht, image_height = box
            (x2,y2) = (x1 + image_widht, y1 + image_height)

            #scaling for better image experience
            (font_scale, thickness, padding) = (0.6, 2, 20)
            if image_height > 1000 or image_widht > 1000:
                font_scale = 1
                padding = 24
                scale = (image_height / 1000, image_widht / 1000)
                scale = max(scale)
                (font_scale, thickness, padding) = [int(s * scale) for s in (font_scale, thickness, padding)]


            xx1, yy1, xx2, yy2 = [int(p) for p in face]
            half_width         = int(image_widht / 2.8)
            half_height        = int(image_height / 2.8)
            (xx1, yy1)         = [c - half_width  for c in (xx1, yy1)]
            (xx2, yy2)         = [c + half_height for c in (xx2, yy2)]
            if xx1 < 0 or yy1 < 0 or xx2 > image_widht or yy2 > image_height:
                #can't be recognized
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                draw_keypoints(image, keypoints)
            else:
                #have enough space to be recognized
                face_data = image[yy1:yy2, xx1:xx2]
                predicted_face = recognize_face(str(confidence), face_data, lfw_trained_model)

                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                draw_keypoints(image, keypoints)

                cv2.rectangle(image, (xx1, yy1), (xx2, yy2), (0, 255, 0), thickness)
                cv2.putText(image, str(round(confidence,4)), (x1, y2 + padding),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)

    return image
