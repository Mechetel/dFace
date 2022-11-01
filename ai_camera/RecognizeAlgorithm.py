from .constants import (
        mtcnn,
        input_shape
    )
from .Image import Image
from .Shape import Shape
from .utils import to_base64
import numpy as np
import cv2
import os


class RecognizeAlgorithm(object):

    @staticmethod
    def __recognize_face(face_data, model):
        face_data = Image(face_data)
        face_data.to_rgb()
        face_data.resize(Shape(96, 96))
        face_data.normalize()
        predicted_face_data = model.encode(face_data)
        return predicted_face_data


    @staticmethod
    def __draw_keypoints(img, keypoints):
        cv2.circle(img, keypoints["left_eye"],    1, (0, 0, 255), 2)
        cv2.circle(img, keypoints["right_eye"],   1, (0, 0, 255), 2)
        cv2.circle(img, keypoints["nose"],        1, (0, 0, 255), 2)
        cv2.circle(img, keypoints["mouth_left"],  1, (0, 0, 255), 2)
        cv2.circle(img, keypoints["mouth_right"], 1, (0, 0, 255), 2)


    @staticmethod
    def __scaling_image(image_height, image_widht):
        (font_scale, thickness, padding) = (0.6, 2, 20)
        if image_height > 1000 or image_widht > 1000:
            font_scale = 1
            padding = 24
            scale = (image_height / 1000, image_widht / 1000)
            scale = max(scale)
            (font_scale, thickness, padding) = [int(s * scale) for s in (font_scale, thickness, padding)]
        return (font_scale, thickness, padding)


    @staticmethod
    def __compare(face_image, comparations, model):
        face_vector = RecognizeAlgorithm.__recognize_face(face_image, model)
        for comparison in comparations:
            distance = np.linalg.norm(face_vector - comparison['person_image_lfw_nd_array'])
            comparison['distance'] = distance

        comparations = sorted(comparations, key=lambda x: x['distance'])
        return comparations


    @staticmethod
    def __get_face_xy_attributes(box):
        x1, y1, face_widht, face_height = box
        (x2, y2) = (x1 + face_widht, y1 + face_height)

        (xx1, yy1, xx2, yy2) = [int(p) for p in (x1, y1, x2, y2)]
        half_width           = int((xx2 - xx1) / 2.8)
        half_height          = int((yy2 - yy1) / 2.8)
        (xx1, yy1)           = [c - half_width  for c in (xx1, yy1)]
        (xx2, yy2)           = [c + half_height for c in (xx2, yy2)]
        return ((x1,y1), (x2,y2), (xx1,yy1), (xx2,yy2))


    @staticmethod
    def recognize(image, persons, model):
        face_list = mtcnn.detect_faces(image)
        persons_to_json = []

        persons_array = []
        for person in persons:
            persons_array.append({
                'person_name': person.name,
                'person_image': person.image.url,
                'person_image_lfw_nd_array': person.image_lfw_nd_array
                })

        (image_height, image_widht, _) = np.shape(image)

        for face in face_list:
            box        = face["box"]
            confidence = face["confidence"]
            keypoints  = face["keypoints"]

            ((x1,y1), (x2,y2), (xx1,yy1), (xx2,yy2)) = RecognizeAlgorithm.__get_face_xy_attributes(box)
            face["xy1"],   face["xy2"]   = (x1,  y1),  (x2,  y2)
            face["xxyy1"], face["xxyy2"] = (xx1, yy1), (xx2, yy2)

            if xx1 < 0 or yy1 < 0 or xx2 > image_widht or yy2 > image_height:
                #can't be recognized
                continue
            else:
                #have enough space to be recognized
                face_data = image[yy1:yy2, xx1:xx2]
                comparison = RecognizeAlgorithm.__compare(face_data, persons_array, model)[0]
                print('min distance: ' + str(comparison['distance']))
                positive = comparison['distance'] < 1

                if positive:
                    person = comparison['person_name']
                else:
                    person = "unknown"

                # person = comparison['person_name']

                face["person"] = person
                json_person = {}
                json_person['name'] = person
                json_person['base64_data'] = to_base64(face_data)
                persons_to_json.append(json_person)

        #scaling for better image experience
        (font_scale, thickness, padding) = RecognizeAlgorithm.__scaling_image(image_height, image_widht)

        for face in face_list:
            ((x1,y1), (x2,y2), (xx1,yy1), (xx2,yy2)) = (face["xy1"], face["xy2"], face["xxyy1"], face["xxyy2"])

            if xx1 < 0 or yy1 < 0 or xx2 > image_widht or yy2 > image_height:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                RecognizeAlgorithm.__draw_keypoints(image, keypoints)
            else:
                person = face["person"]
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                RecognizeAlgorithm.__draw_keypoints(image, keypoints)
                cv2.rectangle(image, (xx1, yy1), (xx2, yy2), (0, 255, 0), thickness)
                cv2.putText(image, str(person), (x1, y2 + padding),
                            cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)

        found_persons_with_image_json = {
                "image": to_base64(image),
                "persons": persons_to_json
            }

        return found_persons_with_image_json


    @staticmethod
    def recognize_video(videos_dir, filename, persons, model):
        cap = cv2.VideoCapture(f'{videos_dir}/{filename}');
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter(f'{videos_dir}/r-{filename}', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))

        persons_array = []
        for person in persons:
            persons_array.append({
                'person_name': person.name,
                'person_image': person.image.url,
                'person_image_lfw_nd_array': person.image_lfw_nd_array
                })

        (font_scale, thickness, padding) = RecognizeAlgorithm.__scaling_image(height, width)

        for frame_idx in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
            ret, image = cap.read()
            recognized_image = image
            print(frame_idx) #===============================

            face_list = mtcnn.detect_faces(image)
            (image_height, image_width, _) = np.shape(image)

            for face in face_list:
                box        = face["box"]
                confidence = face["confidence"]
                keypoints  = face["keypoints"]

                ((x1,y1), (x2,y2), (xx1,yy1), (xx2,yy2)) = RecognizeAlgorithm.__get_face_xy_attributes(box)
                face["xy1"],   face["xy2"]   = (x1,  y1),  (x2,  y2)
                face["xxyy1"], face["xxyy2"] = (xx1, yy1), (xx2, yy2)

                if xx1 < 0 or yy1 < 0 or xx2 > image_width or yy2 > image_height:
                    continue
                else:
                    face_data = image[yy1:yy2, xx1:xx2]
                    comparison = RecognizeAlgorithm.__compare(face_data, persons_array, model)[0]
                    print('min distance: ' + str(comparison['distance']))
                    positive = comparison['distance'] < 1.1

                    if positive:
                        person = comparison['person_name']
                    else:
                        person = "unknown"

                    face["person"] = person

            for face in face_list:
                ((x1,y1), (x2,y2), (xx1,yy1), (xx2,yy2)) = (face["xy1"], face["xy2"], face["xxyy1"], face["xxyy2"])

                if xx1 < 0 or yy1 < 0 or xx2 > image_width or yy2 > image_height:
                    cv2.rectangle(recognized_image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                    RecognizeAlgorithm.__draw_keypoints(recognized_image, keypoints)
                else:
                    person = face["person"]
                    cv2.rectangle(recognized_image, (x1, y1), (x2, y2), (0, 0, 255), thickness)
                    RecognizeAlgorithm.__draw_keypoints(recognized_image, keypoints)
                    cv2.rectangle(recognized_image, (xx1, yy1), (xx2, yy2), (0, 255, 0), thickness)
                    cv2.putText(recognized_image, str(person), (x1, y2 + padding),
                                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 0, 255), thickness)

            out.write(recognized_image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
