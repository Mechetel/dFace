from .constants import input_shape, lfw_trained_model, mtcnn
import numpy as np
import cv2
import os


def recognize_face(face_data, model):
    face_data = cv2.cvtColor(face_data, cv2.COLOR_BGR2RGB)
    face_data = cv2.resize(face_data, tuple(reversed(input_shape[:-1])), interpolation=cv2.INTER_AREA)
    face_data = np.array(face_data, dtype='float32') / 255
    face_data = np.expand_dims(face_data, axis=0)
    predicted_face_data = model.predict(face_data)
    return predicted_face_data


def draw_keypoints(img, keypoints):
    cv2.circle(img, keypoints["left_eye"],    1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["right_eye"],   1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["nose"],        1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["mouth_left"],  1, (0, 0, 255), 2)
    cv2.circle(img, keypoints["mouth_right"], 1, (0, 0, 255), 2)


def scaling_image(image_height, image_widht):
    (font_scale, thickness, padding) = (0.6, 2, 20)
    if image_height > 1000 or image_widht > 1000:
        font_scale = 1
        padding = 24
        scale = (image_height / 1000, image_widht / 1000)
        scale = max(scale)
        (font_scale, thickness, padding) = [int(s * scale) for s in (font_scale, thickness, padding)]
    return (font_scale, thickness, padding)


def compare(model, face_image, comparations):
    face_vector = recognize_face(face_image, model)
    for comparison in comparations:
        distance = np.linalg.norm(face_vector - comparison['person_image_nd_array'])
        comparison['distance'] = distance

    comparations = sorted(comparations, key=lambda x: x['distance'])
    return comparations


def recognize(image, persons):
    face_list = mtcnn.detect_faces(image)

    persons_array = []
    for person in persons:
        persons_array.append({
            'person_name': person.name,
            'person_image': person.image.url,
            'person_image_nd_array': person.image_nd_array
            })

    for face in face_list:
        box        = face["box"]
        confidence = face["confidence"]
        keypoints  = face["keypoints"]
        (image_height, image_widht, _) = np.shape(image)

        x1,y1, face_widht, face_height = box
        (x2,y2) = (x1 + face_widht, y1 + face_height)

        (xx1, yy1, xx2, yy2) = [int(p) for p in (x1, y1, x2, y2)]
        half_width           = int((xx2 - xx1) / 2.8)
        half_height          = int((yy2 - yy1) / 2.8)
        (xx1, yy1)           = [c - half_width  for c in (xx1, yy1)]
        (xx2, yy2)           = [c + half_height for c in (xx2, yy2)]

        #scaling for better image experience
        (font_scale, thickness, padding) = scaling_image(image_height, image_widht)

        if xx1 < 0 or yy1 < 0 or xx2 > image_widht or yy2 > image_height:
            #can't be recognized
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
            draw_keypoints(image, keypoints)
        else:
            #have enough space to be recognized
            face_data = image[yy1:yy2, xx1:xx2]
            comparison = compare(lfw_trained_model, face_data, persons_array)[-1]
            print(comparison['distance'])
            positive = comparison['distance'] < 0.4
            if positive:
                person = comparison['person_name']
            else:
                person = "unknown"

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
            draw_keypoints(image, keypoints)

            cv2.rectangle(image, (xx1, yy1), (xx2, yy2), (0, 255, 0), thickness)
            cv2.putText(image, str(person), (x1, y2 + padding),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)


    return image
